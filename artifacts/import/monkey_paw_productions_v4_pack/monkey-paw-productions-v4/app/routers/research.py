from fastapi import APIRouter
from pydantic import BaseModel
from ..services.research_service import save_research, fetch_rss

router = APIRouter()

class Req(BaseModel):
    topic: str
    source: str = "manual"
    content: str

@router.post("/api/research")
def add_research(req: Req):
    rid = save_research(req.topic, req.source, req.content)
    return {"research_id": rid}

class RSSReq(BaseModel):
    url: str
    limit: int = 5

@router.post("/api/research/rss")
def rss(req: RSSReq):
    return {"items": fetch_rss(req.url, req.limit)}
