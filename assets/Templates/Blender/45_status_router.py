
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import shutil, os, time, platform

router = APIRouter()
@router.get("/system/status")
def status():
    tools = {"ffmpeg": bool(shutil.which("ffmpeg")), "python": True}
    mem = shutil.disk_usage(".")
    return {"ok": True, "time": time.time(), "platform": platform.platform(), "tools": tools, "disk":{"free":mem.free,"total":mem.total}}
@router.get("/system/pauses")
def pauses(): return {"ok": True, "pauses": {}}
