from fastapi import APIRouter
from pydantic import BaseModel
from ..services.draft_service import save_draft

router = APIRouter()

class DraftIn(BaseModel):
    research_id: int
    content: str

@router.post("/draft")
def add_draft(body: DraftIn):
    did = save_draft(body.research_id, body.content)
    return {"ok": True, "draft_id": did}
