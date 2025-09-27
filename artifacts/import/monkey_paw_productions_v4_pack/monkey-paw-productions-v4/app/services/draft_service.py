from sqlmodel import Session, select
from ..store.db import Draft, ResearchItem, engine
import datetime, json
from typing import Optional

def save_draft(research_id: int, content: str, avatar: str = "default") -> int:
    with Session(engine) as s:
        d = Draft(research_id=research_id, content=content, avatar=avatar, created_at=datetime.datetime.utcnow())
        s.add(d); s.commit(); s.refresh(d)
        return d.id

def get_research(research_id: int) -> Optional[ResearchItem]:
    with Session(engine) as s:
        return s.get(ResearchItem, research_id)
