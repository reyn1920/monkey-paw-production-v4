from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import json

router = APIRouter(prefix="/pack", tags=["pack"])

BASE = Path(__file__).resolve().parents[2]  # project root
PACK_DIR = BASE / "_mp_integration"
PUBLIC_STATE_PATH = PACK_DIR / "merge" / "public_state.json"
DASHBOARD_HTML = PACK_DIR / "dashboard" / "index.html"


def _read_public_state() -> dict:
    try:
        return json.loads(PUBLIC_STATE_PATH.read_text())
    except Exception:
        return {"public": False}


def _write_public_state(public: bool) -> None:
    PUBLIC_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_STATE_PATH.write_text(json.dumps({"public": bool(public)}))


@router.post("/toggle_public")
async def toggle_public(body: dict):
    public = bool(body.get("public", False))
    _write_public_state(public)
    return {"public": public}


@router.get("/public_state")
async def public_state():
    return _read_public_state()


@router.post("/prompt_broker")
async def prompt_broker(body: dict):
    goal = body.get("goal", "")
    constraints = body.get("constraints", [])
    context = body.get("context", {})
    prompt_text = (
        f"Goal: {goal}\n"
        f"Constraints: {constraints}\n"
        f"Context: {context}"
    )
    return {"prompt": prompt_text}


@router.get("/dashboard", response_class=HTMLResponse)
async def pack_dashboard():
    try:
        html = DASHBOARD_HTML.read_text(encoding="utf-8")
        return HTMLResponse(content=html)
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)
