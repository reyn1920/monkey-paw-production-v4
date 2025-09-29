
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pathlib import Path
import aiosqlite, os, json, subprocess, shutil

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")
DB_PATH = os.environ.get("RUNTIME_DB", "backend/runtime.db")

async def ensure_schema():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT)")
        await db.execute("""CREATE TABLE IF NOT EXISTS avatar_profiles (
            id INTEGER PRIMARY KEY,
            name TEXT,
            engine TEXT,      -- linly_talker | talking_head
            shot  TEXT,       -- full | mid | head
            aspect TEXT,      -- 16:9 | 9:16 | 1:1
            scale REAL,       -- 0.1..3.0
            offset_x REAL,    -- -1..1 (relative)
            offset_y REAL,    -- -1..1
            key_color TEXT,   -- #00FF00
            notes TEXT
        )""")
        await db.commit()

async def kv_set(k,v):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR REPLACE INTO kv (key,value) VALUES (?,?)", (k, str(v))); await db.commit()

async def kv_get(k):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT value FROM kv WHERE key=?", (k,)); row = await cur.fetchone(); return row[0] if row else ""

@router.get("/avatars")
async def page(request: Request):
    await ensure_schema()
    # Seed defaults if empty
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM avatar_profiles"); n = (await cur.fetchone())[0]
        if n == 0:
            await db.execute("INSERT INTO avatar_profiles (name,engine,shot,aspect,scale,offset_x,offset_y,key_color,notes) VALUES (?,?,?,?,?,?,?,?,?)",
                             ("Linly — Full", "linly_talker","full","16:9",1.0,0.0,-0.1,"#00FF00","Default full body"))
            await db.execute("INSERT INTO avatar_profiles (name,engine,shot,aspect,scale,offset_x,offset_y,key_color,notes) VALUES (?,?,?,?,?,?,?,?,?)",
                             ("Linly — Mid", "linly_talker","mid","16:9",1.2,0.0,-0.05,"#00FF00","Waist-up"))
            await db.execute("INSERT INTO avatar_profiles (name,engine,shot,aspect,scale,offset_x,offset_y,key_color,notes) VALUES (?,?,?,?,?,?,?,?,?)",
                             ("Talking Head — Head", "talking_head","head","16:9",1.35,0.0,0.0,"#00FF00","Standby head-and-shoulders"))
            await db.commit()
    return templates.TemplateResponse("avatars.html", {"request": request})

@router.get("/api/avatars/defaults")
async def defaults_get():
    primary = await kv_get("AVATAR_PRIMARY") or "linly_talker"
    standby = await kv_get("AVATAR_STANDBY") or "talking_head"
    return {"ok": True, "primary": primary, "standby": standby}

@router.post("/api/avatars/defaults")
async def defaults_set(body: dict):
    p = (body or {}).get("primary","linly_talker")
    s = (body or {}).get("standby","talking_head")
    await kv_set("AVATAR_PRIMARY", p); await kv_set("AVATAR_STANDBY", s)
    return {"ok": True, "primary": p, "standby": s}

@router.get("/api/avatars/profiles")
async def profiles_list():
    await ensure_schema()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT * FROM avatar_profiles ORDER BY id")
        rows = await cur.fetchall(); cols = [d[0] for d in cur.description]
        return {"ok": True, "profiles": [dict(zip(cols, r)) for r in rows]}

@router.post("/api/avatars/profiles/save")
async def profiles_save(body: dict):
    await ensure_schema()
    d = body or {}
    async with aiosqlite.connect(DB_PATH) as db:
        if d.get("id"):
            await db.execute("UPDATE avatar_profiles SET name=?,engine=?,shot=?,aspect=?,scale=?,offset_x=?,offset_y=?,key_color=?,notes=? WHERE id=?",
                             (d.get("name"),d.get("engine"),d.get("shot"),d.get("aspect"),float(d.get("scale",1)),float(d.get("offset_x",0)),float(d.get("offset_y",0)),d.get("key_color","#00FF00"),d.get("notes",""),int(d.get("id"))))
        else:
            await db.execute("INSERT INTO avatar_profiles (name,engine,shot,aspect,scale,offset_x,offset_y,key_color,notes) VALUES (?,?,?,?,?,?,?,?,?)",
                             (d.get("name"),d.get("engine"),d.get("shot"),d.get("aspect"),float(d.get("scale",1)),float(d.get("offset_x",0)),float(d.get("offset_y",0)),d.get("key_color","#00FF00"),d.get("notes","")))
        await db.commit()
    return {"ok": True}

@router.post("/api/compose/preview")
async def compose_preview(body: dict):
    # Requires ffmpeg, and avatar asset should include alpha (ProRes 4444) OR a PNG sequence folder
    bg_folder = body.get("bg_folder","")
    avatar = body.get("avatar","")
    shot = (body.get("shot") or "mid").lower()
    aspect = (body.get("aspect") or "16:9")
    out = body.get("out") or "assets/previews/preview.mp4"
    Path("assets/previews").mkdir(parents=True, exist_ok=True)

    if not shutil.which("ffmpeg"):
        return JSONResponse({"ok": False, "error": "ffmpeg not found"}, status_code=500)
    if not Path(bg_folder).exists():
        return JSONResponse({"ok": False, "error": "bg_folder missing"}, status_code=400)
    # derive width/height from first PNG
    import glob
    pngs = sorted(glob.glob(str(Path(bg_folder)/"*.png")))
    if not pngs:
        return JSONResponse({"ok": False, "error": "no PNG frames in bg_folder"}, status_code=400)

    # Set target geometry by aspect
    wh = {"16:9": (1920,1080), "9:16": (1080,1920), "1:1": (1080,1080)}.get(aspect,(1920,1080))
    W,H = wh
    # Shot → scale/pos preset
    if shot=="full": scale=0.9; x=0.5; y=1.0
    elif shot=="head": scale=1.6; x=0.5; y=0.72
    else: scale=1.2; x=0.5; y=0.86

    # Build ffmpeg command
    # Background images -> looped video
    bg = f"-framerate 30 -pattern_type glob -i '{bg_folder}/*.png' -filter_complex 'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}' -r 30 -f matroska -"
    # Avatar input
    if Path(avatar).is_dir():
        av = f"-framerate 30 -pattern_type glob -i '{avatar}/*.png'"
        av_stream = "[1:v]"
    else:
        av = f"-i '{avatar}'"
        av_stream = "[1:v]"

    # Compose
    # Position via overlay with x,y as relative center, scaling via scale2ref
    filtergraph = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}[bg]; {av_stream}scale=iw*{scale}:ih*{scale}[fg]; [bg][fg]overlay=(W-w)*{x}:(H-h)*{y}:format=auto"
    cmd = f"bash -lc "ffmpeg -y -framerate 30 -pattern_type glob -i '{bg_folder}/*.png' {av} -filter_complex '{filtergraph}' -c:v libx264 -pix_fmt yuv420p '{out}'""
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {"ok": p.returncode==0, "out": out, "stderr": p.stderr[-500:], "stdout": p.stdout[-500:]}
