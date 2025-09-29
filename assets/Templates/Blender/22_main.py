from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
import sqlite3
import subprocess
import time

app = FastAPI(title="Base44 Runtime API", version="1.6.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DB = os.getenv("DB_PATH", "data/base44.sqlite")
MEDIA = "data/media"
os.makedirs("data", exist_ok=True)
os.makedirs(MEDIA, exist_ok=True)
con = sqlite3.connect(DB)
con.executescript(
    "CREATE TABLE IF NOT EXISTS channels(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,notes TEXT);CREATE TABLE IF NOT EXISTS episodes(id INTEGER PRIMARY KEY AUTOINCREMENT,channel_id INTEGER,title TEXT,status TEXT,media_path TEXT,created_ts INTEGER,updated_ts INTEGER);CREATE TABLE IF NOT EXISTS voices(id INTEGER PRIMARY KEY AUTOINCREMENT,source TEXT,voice_id TEXT,name TEXT,gender TEXT,lang TEXT,meta TEXT);CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY AUTOINCREMENT,category TEXT,title TEXT,content TEXT,path TEXT,meta TEXT);"
)
con.commit()
con.close()


@app.get("/health")
def h():
    return {"ok": True}


@app.get("/library/voices")
def lv():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return [
        dict(r)
        for r in con.execute(
            "SELECT id,source,voice_id,name,gender,lang,meta FROM voices ORDER BY id DESC"
        )
    ]


@app.get("/library/items")
def li():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return [
        dict(r)
        for r in con.execute(
            "SELECT id,category,title,content,path,meta FROM items ORDER BY id DESC"
        )
    ]


class ChIn(BaseModel):
    name: str
    notes: str | None = None


@app.post("/channels")
def add_ch(b: ChIn):
    con = sqlite3.connect(DB)
    con.execute("INSERT INTO channels(name,notes) VALUES(?,?)", (b.name, b.notes or ""))
    con.commit()
    return {"ok": True}


@app.get("/channels")
def ls_ch():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return [
        dict(r)
        for r in con.execute("SELECT id,name,notes FROM channels ORDER BY id DESC")
    ]


class EpIn(BaseModel):
    title: str


@app.post("/channels/{cid}/episodes")
def add_ep(cid: int, b: EpIn):
    now = int(time.time())
    mp = os.path.join(MEDIA, f"ch_{cid}", f"{now}_draft.mp4")
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO episodes(channel_id,title,status,media_path,created_ts,updated_ts) VALUES(?,?,?,?,?,?)",
        (cid, b.title, "draft", mp, now, now),
    )
    con.commit()
    eid = con.execute("SELECT last_insert_rowid()").fetchone()[0]
    return {"ok": True, "episode_id": eid, "media_path": mp}


class RIn(BaseModel):
    voice_primary: str = "en-US-GuyNeural"
    voice_secondary: str = "en-US-JennyNeural"
    use_library_voice: bool = False
    library_voice_id: str | None = None
    avatar_engine: str | None = None
    pro_thumbnails: bool = True
    captions_on: bool = True


@app.post("/episodes/{eid}/render")
def rnd(eid: int, b: RIn):
    try:
        out = subprocess.check_output(
            [
                "python",
                "utils/render_episode.py",
                str(eid),
                b.voice_primary,
                b.voice_secondary,
                b.avatar_engine or "",
                "1" if b.pro_thumbnails else "0",
                "1" if b.captions_on else "0",
                b.library_voice_id or "",
                "1" if b.use_library_voice else "0",
            ],
            stderr=subprocess.STDOUT,
            text=True,
        )
        return {"ok": True, "log": out}
    except subprocess.CalledProcessError as e:
        raise HTTPException(500, e.output)


@app.post("/episodes/{eid}/approve")
def ap(eid: int):
    con = sqlite3.connect(DB)
    con.execute(
        'UPDATE episodes SET status="approved", updated_ts=? WHERE id=?',
        (int(time.time()), eid),
    )
    con.commit()
    return {"ok": True}


@app.post("/episodes/{eid}/publish")
def pb(eid: int):
    con = sqlite3.connect(DB)
    con.execute(
        'UPDATE episodes SET status="published", updated_ts=? WHERE id=?',
        (int(time.time()), eid),
    )
    con.commit()
    return {"ok": True}


if os.path.isdir("frontend/dist"):
    app.mount(
        "/dashboard_assets",
        StaticFiles(directory="frontend/dist", html=False),
        name="dashboard_assets",
    )
app.mount("/media", StaticFiles(directory=MEDIA, html=False), name="media")


@app.get("/dashboard")
def dash():
    p = "frontend/dist/index.html"
    return (
        FileResponse(p)
        if os.path.isfile(p)
        else JSONResponse({"ok": False, "hint": "build frontend"}, status_code=404)
    )
