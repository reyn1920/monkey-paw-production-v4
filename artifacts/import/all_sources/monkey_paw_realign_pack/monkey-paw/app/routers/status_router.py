"""
Status endpoints (can be expanded later, add-only).
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/api/status")
def status():
    return {"status": "ok", "message": "runtime stable"}
