from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import Session
from ..store.db import engine, Draft
from ..services.qa_service import readability_fkgl, seo_score

router = APIRouter()

class ScoreReq(BaseModel):
    draft_id: int

@router.post("/api/qa/score")
def score(req: ScoreReq):
    with Session(engine) as s:
        d = s.get(Draft, req.draft_id)
        if not d: return {"ok": False, "reason": "no such draft"}
        fk = readability_fkgl(d.content)
        seo = seo_score(d.content)
        return {"ok": True, "readability_fkgl": fk, "seo": seo}
