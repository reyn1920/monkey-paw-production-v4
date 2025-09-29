
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/seo/youtube_meta")
def meta(body: dict):
    topic = (body.get("topic") or "").strip()
    channel = (body.get("channel") or "").strip()
    brand_tags = body.get("brand_tags") or []
    # safe templates, no targeted political persuasion; generic SEO only
    title = f"{topic} — {channel} explained in minutes"
    desc = f"In this episode: {topic}. Chapters, sources (with on-screen attribution), and our analysis. Subscribe for daily Shorts and weekly deep dives."
    tags = brand_tags + [topic, channel, "shorts", "explained"]
    return {"ok": True, "title": title[:100], "description": desc[:4900], "tags": tags[:20]}
