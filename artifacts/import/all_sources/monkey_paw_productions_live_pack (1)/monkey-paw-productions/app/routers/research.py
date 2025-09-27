from fastapi import APIRouter
from pydantic import BaseModel
from ..services.research_service import save_research

router = APIRouter()

class Req(BaseModel):
    topic: str
    source: str = "manual"
    content: str

@router.post("/api/research")
def add_research(req: Req):
    rid = save_research(req.topic, req.source, req.content)
    return {"research_id": rid}
