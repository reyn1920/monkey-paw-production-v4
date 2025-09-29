
from fastapi import APIRouter
router = APIRouter()
@router.post("/seo/youtube_meta")
def meta(body: dict):
    topic = (body.get("topic") or "").strip()
    channel = (body.get("channel") or "").strip()
    title = f"{topic} — {channel} explained in minutes"[:100]
    desc = f"In this episode: {topic}. Chapters, sources (with on-screen attribution), and our analysis."
    tags = [topic, channel, "explained","shorts"]
    return {"ok": True, "title": title, "description": desc, "tags": tags}
