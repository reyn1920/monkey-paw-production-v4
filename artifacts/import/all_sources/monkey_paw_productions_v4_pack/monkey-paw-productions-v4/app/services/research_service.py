from sqlmodel import Session
from ..store.db import ResearchItem, engine
import datetime, feedparser
from typing import List

def save_research(topic: str, source: str, content: str) -> int:
    with Session(engine) as s:
        item = ResearchItem(topic=topic, source=source, content=content, created_at=datetime.datetime.utcnow())
        s.add(item); s.commit(); s.refresh(item)
        return item.id

def fetch_rss(url: str, limit: int = 5) -> List[dict]:
    feed = feedparser.parse(url)
    out = []
    for e in (feed.entries or [])[:limit]:
        out.append({"title": e.get("title",""), "link": e.get("link",""), "summary": e.get("summary","")})
    return out
