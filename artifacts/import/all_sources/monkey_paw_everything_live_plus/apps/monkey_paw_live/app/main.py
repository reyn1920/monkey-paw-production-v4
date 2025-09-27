from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import time

app = FastAPI(title="Monkey Paw — Live")

# in-memory store (simple and local-first)
DB: Dict[str, Any] = {"seq": {"research": 1, "draft": 1}, "research": {}, "draft": {}, "approve": False}

def now() -> str:
    return time.strftime("%Y%m%d_%H%M%S", time.gmtime())

@app.get("/api/health")
def health():
    return {"ok": True, "service": "monkey-paw-live", "nocode_stack_enabled": False}

@app.get("/api/status")
def status():
    return {
        "counts": {"research": len(DB["research"]), "draft": len(DB["draft"])},
        "approve_publish": DB["approve"]
    }

class ResearchIn(BaseModel):
    topic: str
    source: str = "manual"
    content: str

@app.post("/api/research")
def add_research(body: ResearchIn):
    rid = DB["seq"]["research"]
    DB["seq"]["research"] += 1
    DB["research"][rid] = {"topic": body.topic, "source": body.source, "content": body.content, "created_at": now()}
    return {"ok": True, "research_id": rid}

class DraftIn(BaseModel):
    research_id: int
    content: str

@app.post("/api/draft")
def add_draft(body: DraftIn):
    if body.research_id not in DB["research"]:
        raise HTTPException(status_code=404, detail="research not found")
    did = DB["seq"]["draft"]
    DB["seq"]["draft"] += 1
    DB["draft"][did] = {"research_id": body.research_id, "content": body.content, "created_at": now()}
    return {"ok": True, "draft_id": did}

class RepurposeIn(BaseModel):
    draft_id: int
    variants: List[str] = ["youtube_script", "blog_post", "social_post"]

@app.post("/api/repurpose")
def repurpose(body: RepurposeIn):
    if body.draft_id not in DB["draft"]:
        raise HTTPException(status_code=404, detail="draft not found")
    # For simplicity, just show which files would be created
    staged = [f"artifacts/staging/draft{body.draft_id}_{v}_{now()}.txt" for v in body.variants]
    return {"ok": True, "staged": staged}

@app.post("/api/admin/approve_publish/{value}")
def approve(value: bool):
    DB["approve"] = bool(value)
    return {"ok": True, "approve_publish": DB["approve"]}

@app.post("/api/publish")
def publish():
    if not DB["approve"]:
        raise HTTPException(status_code=403, detail="publishing not approved")
    # minimal stand-in
    return {"ok": True, "moved": ["artifacts/published/..."]}
