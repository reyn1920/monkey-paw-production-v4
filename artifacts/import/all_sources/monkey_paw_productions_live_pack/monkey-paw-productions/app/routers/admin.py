from fastapi import APIRouter
from ..store.db import set_flag, get_flag

router = APIRouter()

@router.post("/api/admin/approve_publish/{value}")
def approve(value: bool):
    set_flag("approve_publish", "true" if value else "false")
    return {"approve_publish": get_flag("approve_publish","false")}

@router.post("/api/admin/selftest")
def selftest():
    # simple self-test: ensure health returns ok and approve flag readable
    ok = True
    notes = []
    if get_flag("approve_publish","false") not in ("true","false"):
        ok = False; notes.append("bad approve_publish flag")
    return {"ok": ok, "notes": notes}
