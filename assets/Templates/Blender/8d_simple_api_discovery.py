"""Simplified API Discovery routes for exposing available endpoints."""

from fastapi import APIRouter
from typing import Any

router = APIRouter(prefix="/api", tags=["discovery"])


@router.get("/discovery")
def get_api_discovery() -> dict[str, Any]:
    """Get API discovery information."""
    return {
        "service_name": "TRAE.AI Base44 API",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/api/health", "method": "GET", "description": "Health check"},
            {"path": "/api/channels", "method": "GET", "description": "Get channels"},
            {"path": "/api/pets", "method": "GET", "description": "Get pets"},
            {"path": "/api/discovery", "method": "GET", "description": "API discovery"},
        ],
        "health_check": "/api/health",
    }


@router.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "api-discovery"}
