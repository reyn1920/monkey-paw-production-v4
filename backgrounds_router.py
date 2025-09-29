
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pathlib import Path
import os, subprocess, json, time, shutil

router = APIRouter()
BLENDER_BIN = os.environ.get("BLENDER_BIN","/Applications/Blender.app/Contents/MacOS/Blender")
SCRIPT_REL = "blender/make_backgrounds.py"

def ensure_dirs():
    Path("assets/backgrounds").mkdir(parents=True, exist_ok=True)
    Path("assets/previews").mkdir(parents=True, exist_ok=True)

@router.get("/api/backgrounds/list")
def bg_list():
    ensure_dirs()
    items = []
    for p in sorted(Path("assets/backgrounds").glob("*")):
        if not p.is_dir(): continue
        pngs = sorted(p.glob("*.png"))
        mp4 = p.with_suffix(".mp4")
        # Allow preview.mp4 inside the folder
        prev = p / "preview.mp4"
        if prev.exists(): mp4 = prev
        items.append({"name": p.name, "count": len(pngs), "preview": str(prev) if prev.exists() else str(mp4) if mp4.exists() else ""})
    return {"ok": True, "items": items}

@router.post("/api/backgrounds/render")
def bg_render(req: dict):
    ensure_dirs()
    name = (req.get("name") or f"bg_{int(time.time())}").strip().replace(" ","_")
    preset = (req.get("preset") or "gradient").lower()
    w = int(req.get("width", 1920)); h = int(req.get("height", 1080))
    sec = int(req.get("seconds", 8)); fps = int(req.get("fps", 30))

    # Validate blender
    if not Path(BLENDER_BIN).exists():
        return JSONResponse({"ok": False, "error": f"Blender not found: {BLENDER_BIN}. Set BLENDER_BIN env."}, status_code=500)
    if not Path(SCRIPT_REL).exists():
        return JSONResponse({"ok": False, "error": f"Script missing: {SCRIPT_REL}"}, status_code=500)

    # Create a temp override file
    tmp = Path("blender/tmp_bg_override.py")
    tmp.write_text(f"""PRESET='{preset}'
RES_X={w}
RES_Y={h}
FPS={fps}
DURATION_SEC={sec}
MAKE_ALPHA=True
# Output into a staging folder, then we move it to assets/backgrounds/{name}
OUTPUT_DIR='//renders'
""", encoding="utf-8")

    # Run Blender headless
    cmd = [BLENDER_BIN, "-b", "-P", SCRIPT_REL, "--python-expr", f"exec(open('{tmp}').read())"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    # Move renders to assets/backgrounds/<name>
    staging = Path("renders")/preset
    out_dir = Path("assets/backgrounds")/name
    out_dir.mkdir(parents=True, exist_ok=True)
    moved = 0
    if staging.exists():
        for f in staging.glob("*.png"):
            shutil.move(str(f), str(out_dir/f.name)); moved+=1
    # build preview mp4 (no alpha) with ffmpeg if present
    if shutil.which("ffmpeg") and moved>0:
        prev = out_dir/"preview.mp4"
        # create list.txt for ffmpeg
        # use glob pattern
        cmd2 = f"ffmpeg -y -framerate {fps} -pattern_type glob -i '{out_dir}/*.png' -c:v libx264 -pix_fmt yuv420p {prev}"
        subprocess.run(cmd2, shell=True)
    return {"ok": p.returncode==0 and moved>0, "stdout": p.stdout[-500:], "stderr": p.stderr[-500:], "out_folder": str(out_dir), "frames": moved}
