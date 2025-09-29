
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")

@router.get("/bundles", response_class=HTMLResponse)
async def bundles_page(request: Request):
    out = Path("assets/out")
    entries = []
    if out.exists():
        for p in out.iterdir():
            if p.is_dir() and (p / "landing.html").exists():
                entries.append({"slug": p.name, "landing": f"/assets/out/{p.name}/landing.html"})
    return templates.TemplateResponse("bundles.html", {"request": request, "entries": entries})
