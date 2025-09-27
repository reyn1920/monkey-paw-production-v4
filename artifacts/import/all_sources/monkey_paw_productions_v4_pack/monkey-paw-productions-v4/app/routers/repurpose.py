from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import Session
from ..store.db import engine, Draft
from ..services.repurpose_service import save_asset, render_template, render_markdown_to_site
from pathlib import Path

router = APIRouter()

class Req(BaseModel):
    draft_id: int
    variants: list[str]

@router.post("/api/repurpose")
def repurpose(req: Req):
    paths = []
    for kind in req.variants:
        p = save_asset(req.draft_id, kind, f"{kind.upper()} for draft {req.draft_id}")
        paths.append(p)
    return {"paths": paths}

class RenderReq(BaseModel):
    draft_id: int
    template: str  # e.g., youtube_script.j2 / blog_post.j2 / social_post.j2

@router.post("/api/repurpose/render")
def render(req: RenderReq):
    with Session(engine) as s:
        d = s.get(Draft, req.draft_id)
        if not d:
            return {"ok": False, "reason": "no such draft"}
        out = render_template(d, req.template)
        path = save_asset(d.id, f"render_{req.template.replace('.','_')}", out)
        return {"ok": True, "path": path}

class SiteReq(BaseModel):
    markdown: str

@router.post("/api/repurpose/site")
def site(req: SiteReq):
    out_dir = Path(__file__).resolve().parents[2] / "artifacts" / "published" / "site"
    path = render_markdown_to_site(req.markdown, out_dir)
    return {"ok": True, "path": path}
