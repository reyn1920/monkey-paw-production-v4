
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import shutil, os, platform, time, aiosqlite

router = APIRouter()
DB_PATH = os.environ.get("RUNTIME_DB", "backend/runtime.db")

async def kv_get(k):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cur = await db.execute("SELECT value FROM kv WHERE key=?", (k,))
            row = await cur.fetchone(); return row[0] if row else ""
    except Exception:
        return ""

@router.get("/system/status")
async def system_status():
    tools = {
        "ffmpeg": bool(shutil.which("ffmpeg")),
        "blender": os.path.exists(os.environ.get("BLENDER_BIN","/Applications/Blender.app/Contents/MacOS/Blender")),
        "rclone": bool(shutil.which("rclone")),
        "python": True
    }
    mem = shutil.disk_usage(".")
    return {"ok": True, "time": time.time(), "platform": platform.platform(), "tools": tools, "disk": {"free": mem.free, "total": mem.total}}

@router.get("/system/pauses")
async def system_pauses():
    keys = ["PAUSE_ALL","PAUSE_WRITING","PAUSE_THUMBS","PAUSE_CAPTIONS","PAUSE_BUNDLER","PAUSE_PUBLISH","PAUSE_UPLOADS","PAUSE_SCHEDULER","PAUSE_INGEST","PAUSE_BGRENDER","PAUSE_AVATAR"]
    vals = {}
    for k in keys:
        vals[k] = await kv_get(k) or "off"
    return {"ok": True, "pauses": vals}
