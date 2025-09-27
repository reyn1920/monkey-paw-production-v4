from pathlib import Path
from sqlmodel import Session
from ..store.db import engine, Draft, ResearchItem, set_flag
from .repurpose_service import save_asset, render_template
from .publish_service import publish_all, can_publish

def pipeline_heartbeat():
    # placeholder heartbeat; extend with timed tasks as needed
    pass

def run_pipeline_dry(research_id: int) -> dict:
    # Take a research item → draft → repurpose variants (dry to staging)
    with Session(engine) as s:
        r = s.get(ResearchItem, research_id)
        if not r:
            return {"ok": False, "reason": "no such research"}
        d = Draft(research_id=r.id, content=f"Draft based on: {r.content[:280]}...", avatar="default")
        s.add(d); s.commit(); s.refresh(d)
        for kind in ("blog","yt_script","social"):
            save_asset(d.id, kind, f"{kind.upper()} for {d.id}\n\n{d.content}")
        return {"ok": True, "draft_id": d.id}

def try_publish() -> dict:
    if not can_publish():
        return {"ok": False, "reason": "approval gate is off"}
    n = publish_all()
    return {"ok": True, "published_count": n}
