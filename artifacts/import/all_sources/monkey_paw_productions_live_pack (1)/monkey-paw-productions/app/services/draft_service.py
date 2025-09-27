from sqlmodel import Session
from ..store.db import Draft, engine
import datetime

def save_draft(research_id: int, content: str) -> int:
    with Session(engine) as s:
        d = Draft(research_id=research_id, content=content, created_at=datetime.datetime.utcnow())
        s.add(d); s.commit(); s.refresh(d)
        return d.id
