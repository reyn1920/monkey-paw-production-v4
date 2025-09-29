from fastapi import APIRouter
from datetime import datetime
import psutil
import os

router = APIRouter()


@router.get("/health")
async def health_check():
    """System health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent,
        },
        "environment": "production",
    }


@router.get("/status")
async def system_status():
    """Detailed system status"""
    return {
        "trae_ai": "active",
        "data_path": os.path.expanduser("~/ONLINE_PRODUCTION_DATA"),
        "production_ready": True,
        "rule1_enforced": True,
    }
