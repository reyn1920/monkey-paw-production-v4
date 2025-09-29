
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import random, urllib.parse
router = APIRouter()
GROUPS = {}  # group -> [(url, weight)]
@router.post("/links/add")
def add(body: dict):
    g=body.get("group"); url=body.get("url"); w=float(body.get("weight",1.0))
    GROUPS.setdefault(g, []).append((url,w)); return {"ok": True}
@router.get("/links/resolve")
def resolve(group: str, source: str="youtube", campaign: str="default"):
    rows = GROUPS.get(group, [])
    if not rows: return JSONResponse({"ok":False,"error":"no links"}, status_code=404)
    total = sum(w for _,w in rows); r=random.uniform(0,total); upto=0.0
    pick = rows[0][0]
    for url,w in rows:
        if upto+w>=r: pick=url; break
        upto+=w
    u=list(urllib.parse.urlparse(pick)); q=dict(urllib.parse.parse_qsl(u[4])); q.update({"utm_source":source,"utm_campaign":campaign}); u[4]=urllib.parse.urlencode(q)
    return {"ok": True, "url": urllib.parse.urlunparse(u)}
