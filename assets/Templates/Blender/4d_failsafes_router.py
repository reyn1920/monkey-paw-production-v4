
from fastapi import APIRouter
from fastapi.responses import JSONResponse
router = APIRouter()
FLAGS = {}
@router.post("/failsafes/set")
def set_flag(body: dict):
    k = (body.get("key") or "").strip(); v = (body.get("value") or "").strip()
    if not k: return JSONResponse({"ok":False,"error":"key required"}, status_code=400)
    FLAGS[k]=v; return {"ok": True, "key": k, "value": v}
