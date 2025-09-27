# Fixed incomplete statement  # Fixed incomplete statement  # Fixed
# incomplete statement  # Fixed incomplete statement
from fastapi import (APIRouter, )
# Fixed incomplete statement  # Fixed incomplete statement  # Fixed
# incomplete statement  # Fixed incomplete statement
from backend.policy.do_not_delete import (
    DO_NOT_DELETE, REVENUE_SOURCES, decoded_paths, )

router = APIRouter()


@router.get("/api/policy/do-not-delete")
async def get_do_not_delete():
    reg = {**DO_NOT_DELETE, "paths": decoded_paths()}
    return {"ok": True, "registry": reg}


@router.get("/api/policy/revenue-sources")
async def get_revenue_sources():
    return {"ok": True, "sources": REVENUE_SOURCES}
