from fastapi import APIRouter
from ..store.db import get_state_snapshot

router = APIRouter()

@router.get("/health")
def health():
    snap = get_state_snapshot()
    return {"ok": True, "service": snap["service_name"], "nocode_stack_enabled": snap["flags"]["nocode_stack_enabled"]}

@router.get("/status")
def status():
    return get_state_snapshot()
