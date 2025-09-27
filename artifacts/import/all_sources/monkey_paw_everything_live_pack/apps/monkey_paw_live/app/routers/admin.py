from fastapi import APIRouter
from ..store.db import approve_set, selfcheck_state

router = APIRouter()

@router.post("/selfcheck")
def selfcheck():
    return selfcheck_state()

@router.post("/approve_publish/{value}")
def approve_publish(value: bool):
    approve_set(value)
    return {"ok": True, "approve_publish": value}
