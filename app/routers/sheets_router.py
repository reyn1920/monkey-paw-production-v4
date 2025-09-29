from __future__ import annotations
from fastapi import APIRouter, HTTPException
from typing import Any, Dict
from ..sheets_fetcher import fetch_tab, list_sources

router = APIRouter(prefix="/api/sheets", tags=["sheets"])

@router.get("/config")
def sheets_config() -> Dict[str, Any]:
    return {"sources": list_sources()}

@router.get("/{source}/{key}")
def get_tab_from_source(source: str, key: str) -> Dict[str, Any]:
    try:
        rows, ttl = fetch_tab(source, key)
        return {"source": source, "key": key, "count": len(rows), "ttl_seconds": ttl, "rows": rows}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Upstream fetch error: {e}")


# Legacy route: /api/sheets/{key} -> default source
@router.get("/{key}")
def get_tab_legacy(key: str) -> Dict[str, Any]:
    try:
        rows, ttl = fetch_tab("default", key)
        return {"source": "default", "key": key, "count": len(rows), "ttl_seconds": ttl, "rows": rows}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Upstream fetch error: {e}")
