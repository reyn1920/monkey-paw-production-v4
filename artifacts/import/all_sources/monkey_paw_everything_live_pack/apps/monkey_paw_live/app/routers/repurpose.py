from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from ..services.repurpose_service import stage_variants

router = APIRouter()

class RepurposeIn(BaseModel):
    draft_id: int
    variants: List[str] = ["youtube_script", "blog_post", "social_post"]

@router.post("/repurpose")
def add_variants(body: RepurposeIn):
    out = stage_variants(body.draft_id, body.variants)
    return {"ok": True, "staged": out}
