
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import math
router = APIRouter()
EXPS = {}  # name -> {variant -> {"shows":int, "rewards":float}}
@router.post("/ab/choose")
def choose(body: dict):
    name = body.get("name",""); variants = body.get("variants") or []
    if not name or not variants: return JSONResponse({"ok":False,"error":"name+variants required"}, status_code=400)
    EXPS.setdefault(name, {})
    total = sum(max(v.get("shows",0),1) for v in EXPS[name].values()) or 1
    best_v = variants[0]; best_score = -1e9
    for v in variants:
        st = EXPS[name].setdefault(v, {"shows":0,"rewards":0.0})
        avg = (st["rewards"]/st["shows"]) if st["shows"]>0 else 0.0
        score = avg + math.sqrt(2*math.log(total)/max(st["shows"],1))
        if score > best_score: best_score, best_v = score, v
    return {"ok": True, "variant": best_v}
@router.post("/ab/report")
def report(body: dict):
    name = body.get("name",""); variant = body.get("variant",""); reward = float(body.get("reward",0.0))
    if not name or not variant: return JSONResponse({"ok":False,"error":"name+variant required"}, status_code=400)
    st = EXPS.setdefault(name, {}).setdefault(variant, {"shows":0,"rewards":0.0})
    st["shows"] += 1; st["rewards"] += reward
    return {"ok": True}
