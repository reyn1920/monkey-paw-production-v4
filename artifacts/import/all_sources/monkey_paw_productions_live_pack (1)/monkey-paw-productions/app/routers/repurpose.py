from fastapi import APIRouter
from pydantic import BaseModel
from ..services.repurpose_service import save_asset

router = APIRouter()

class Req(BaseModel):
    draft_id: int
    variants: list[str]  # e.g., ["blog","yt_script","social"]

@router.post("/api/repurpose")
def repurpose(req: Req):
    paths = []
    for kind in req.variants:
        p = save_asset(req.draft_id, kind, f"{kind.upper()} for draft {req.draft_id}")
        paths.append(p)
    return {"paths": paths}
