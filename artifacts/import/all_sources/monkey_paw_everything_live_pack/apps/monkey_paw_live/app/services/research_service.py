from ..store.db import DB, now_ts

def save_research(topic: str, source: str, content: str) -> int:
    rid = DB["seq"]["research"]
    DB["seq"]["research"] += 1
    DB["research"][rid] = {"topic": topic, "source": source, "content": content, "created_at": now_ts()}
    return rid
