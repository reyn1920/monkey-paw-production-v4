from fastapi import APIRouter
from pathlib import Path
from ..store.db import get_flag

router = APIRouter()

@router.get("/api/health")
def health():
    return {"ok": True, "service": "Monkey Paw Productions V4", "approve_publish": get_flag("approve_publish","false")}

@router.get("/api/status")
def status():
    base = Path(__file__).resolve().parents[2]
    staging = len(list((base / "artifacts" / "staging").glob("*")))
    published = len(list((base / "artifacts" / "published").glob("*")))
    return {"staging_count": staging, "published_count": published}
