from ..store.db import DB, now_ts

def save_draft(research_id: int, content: str) -> int:
    did = DB["seq"]["draft"]
    DB["seq"]["draft"] += 1
    DB["draft"][did] = {"research_id": research_id, "content": content, "created_at": now_ts()}
    return did
