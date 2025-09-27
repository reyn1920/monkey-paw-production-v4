from fastapi import APIRouter
from ..store.db import set_flag, get_flag

router = APIRouter()

@router.post("/api/admin/approve_publish/{value}")
def approve(value: bool):
    set_flag("approve_publish", "true" if value else "false")
    return {"approve_publish": get_flag("approve_publish","false")}

@router.post("/api/admin/scheduler/{value}")
def toggle_scheduler(value: bool):
    set_flag("scheduler_enabled", "true" if value else "false")
    return {"scheduler_enabled": get_flag("scheduler_enabled","false")}
