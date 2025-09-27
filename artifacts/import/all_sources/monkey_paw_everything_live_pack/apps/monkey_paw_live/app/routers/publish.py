from fastapi import APIRouter, HTTPException
from ..services.publish_service import publish_staged, is_approved

router = APIRouter()

@router.post("/publish")
def do_publish():
    if not is_approved():
        raise HTTPException(status_code=403, detail="Publishing not approved yet.")
    moved = publish_staged()
    return {"ok": True, "moved": moved}
