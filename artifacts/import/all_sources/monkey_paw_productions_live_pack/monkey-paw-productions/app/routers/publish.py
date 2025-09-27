from fastapi import APIRouter
from ..services.publish_service import publish_all, can_publish

router = APIRouter()

@router.post("/api/publish")
def publish():
    if not can_publish():
        return {"ok": False, "reason": "approve_publish=false; run /api/admin/selftest then approve."}
    n = publish_all()
    return {"ok": True, "published_count": n}
