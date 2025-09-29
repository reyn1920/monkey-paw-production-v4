"""Simplified Runtime API module."""

from fastapi import APIRouter
import time
import psutil

router = APIRouter(prefix="/api/runtime", tags=["runtime"])

# Global runtime start time
START_TIME = time.time()


@router.get("/status")
def get_runtime_status():
    """Get runtime status."""
    uptime = time.time() - START_TIME
    return {
        "uptime": f"{uptime:.2f} seconds",
        "status": "running",
        "timestamp": time.time(),
    }


@router.get("/metrics")
def get_system_metrics():
    """Get system metrics."""
    try:
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_used": memory.used,
            "memory_total": memory.total,
            "disk_percent": disk.percent,
            "disk_used": disk.used,
            "disk_total": disk.total,
        }
    except Exception:
        return {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "memory_used": 0,
            "memory_total": 0,
            "disk_percent": 0.0,
            "disk_used": 0,
            "disk_total": 0,
        }


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "runtime"}
