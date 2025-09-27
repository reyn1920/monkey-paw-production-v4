from fastapi import APIRouter
from pydantic import BaseModel
from ..services.draft_service import save_draft

router = APIRouter()

class Req(BaseModel):
    research_id: int
    content: str

@router.post("/api/draft")
def add_draft(req: Req):
    did = save_draft(req.research_id, req.content)
    return {"draft_id": did}
