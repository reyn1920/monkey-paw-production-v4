from sqlmodel import Session
from ..store.db import ResearchItem, engine
import datetime

def save_research(topic: str, source: str, content: str) -> int:
    with Session(engine) as s:
        item = ResearchItem(topic=topic, source=source, content=content, created_at=datetime.datetime.utcnow())
        s.add(item); s.commit(); s.refresh(item)
        return item.id
