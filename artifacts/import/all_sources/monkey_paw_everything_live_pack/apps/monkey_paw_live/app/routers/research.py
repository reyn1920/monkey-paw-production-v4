from fastapi import APIRouter
from pydantic import BaseModel
from ..services.research_service import save_research

router = APIRouter()

class ResearchIn(BaseModel):
    topic: str
    source: str = "manual"
    content: str

@router.post("/research")
def add_research(body: ResearchIn):
    rid = save_research(body.topic, body.source, body.content)
    return {"ok": True, "research_id": rid}
