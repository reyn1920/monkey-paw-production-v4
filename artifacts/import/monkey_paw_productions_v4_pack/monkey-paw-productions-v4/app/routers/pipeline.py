from fastapi import APIRouter
from pydantic import BaseModel
from ..services.pipeline_service import run_pipeline_dry, try_publish

router = APIRouter()

class RunReq(BaseModel):
    research_id: int

@router.post("/api/pipeline/run")
def run(req: RunReq):
    return run_pipeline_dry(req.research_id)

@router.post("/api/pipeline/publish")
def publish():
    return try_publish()
