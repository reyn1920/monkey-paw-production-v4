
from fastapi import APIRouter
import shutil, os
router = APIRouter()
TOOLS = ["ffmpeg","git","node","rclone","whisper"]
ENV_KEYS = ["BLENDER_BIN","GOOGLE_DRIVE_MOUNT","ELEVENLABS_API_KEY","SPEECHELO_KEY","OPENAI_API_KEY","YOUTUBE_API_KEY"]
@router.get("/integrations")
def integrations():
  tools = {t: bool(shutil.which(t)) for t in TOOLS}
  tools["blender"] = os.path.exists(os.environ.get("BLENDER_BIN","/Applications/Blender.app/Contents/MacOS/Blender"))
  env = {k: ("set" if os.environ.get(k) else "missing") for k in ENV_KEYS}
  return {"ok": True, "tools": tools, "env": env}
