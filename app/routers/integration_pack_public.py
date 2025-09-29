from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(tags=["pack_public"])  # no prefix; mounts at root

BASE = Path(__file__).resolve().parents[2]
PACK_DIR = BASE / "_mp_integration"
PUBLIC_STATE_PATH = PACK_DIR / "merge" / "public_state.json"


def _read_public_state() -> dict:
    try:
        return json.loads(PUBLIC_STATE_PATH.read_text())
    except Exception:
        return {"public": False}


def _write_public_state(public: bool) -> None:
    PUBLIC_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_STATE_PATH.write_text(json.dumps({"public": bool(public)}))


@router.post("/api/toggle_public")
async def toggle_public(body: dict):
    public = bool(body.get("public", False))
    _write_public_state(public)
    return {"public": public}


@router.post("/api/prompt_broker")
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
