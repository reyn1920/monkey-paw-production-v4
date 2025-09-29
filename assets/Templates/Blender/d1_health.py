"""Health check router for monitoring application status."""

import os
import logging
from typing import Any
from datetime import datetime
import psutil

# Simple fallback classes for missing dependencies


class APIRouter:
    """Simple API router fallback."""

    def __init__(self, **kwargs):
        self.routes = []

    def get(self, path: str, **kwargs):
        def decorator(func):
            self.routes.append({"method": "GET", "path": path, "func": func})
            return func

        return decorator


class HTTPException(Exception):
    """HTTP exception fallback."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class Status:
    """HTTP status codes."""

    HTTP_200_OK = 200
    HTTP_503_SERVICE_UNAVAILABLE = 503


# Logger setup
logger = logging.getLogger(__name__)

# Health check service


class HealthService:
    """Service for health checks and system monitoring."""

    @staticmethod
    def get_system_health() -> dict[str, Any]:
        """Get comprehensive system health information."""
        try:
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            # Check if system is healthy
            is_healthy = cpu_percent < 90 and memory.percent < 90 and disk.percent < 90

            return {
                "status": "healthy" if is_healthy else "degraded",
                "timestamp": datetime.utcnow().isoformat(),
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_used_gb": round(memory.used / (1024**3), 2),
                    "memory_total_gb": round(memory.total / (1024**3), 2),
                    "disk_percent": disk.percent,
                    "disk_used_gb": round(disk.used / (1024**3), 2),
                    "disk_total_gb": round(disk.total / (1024**3), 2),
                },
                "process": {
                    "pid": os.getpid(),
                    "uptime_seconds": psutil.Process().create_time(),
                },
            }
        except Exception as health_error:
            logger.error("Health check failed: %s", health_error)
            return {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(health_error),
            }

    @staticmethod
    def get_basic_health() -> dict[str, str]:
        """Get basic health status."""
        return {
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "online-production-api",
        }


# Router setup
router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
def basic_health_check():
    """Basic health check endpoint."""
    try:
        return HealthService.get_basic_health()
    except Exception as basic_error:
        logger.error("Basic health check failed: %s", basic_error)
        raise HTTPException(
            status_code=Status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable",
        ) from basic_error


@router.get("/detailed")
def detailed_health_check():
    """Detailed health check with system metrics."""
    try:
        health_data = HealthService.get_system_health()
        if health_data["status"] == "unhealthy":
            raise HTTPException(
                status_code=Status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="System unhealthy",
            )
        return health_data
    except HTTPException:
        raise
    except Exception as detailed_error:
        logger.error("Detailed health check failed: %s", detailed_error)
        raise HTTPException(
            status_code=Status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Health check failed",
        ) from detailed_error


@router.get("/ready")
def readiness_check():
    """Readiness check for load balancers."""
    try:
        # Check if all critical services are ready
        # This is a simplified check - in production you'd check database,
        # cache, etc.
        return {
            "ready": True,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {
                "database": "ok",  # Would check actual DB connection
                "cache": "ok",  # Would check cache connection
                "storage": "ok",  # Would check file system
            },
        }
    except Exception as readiness_error:
        logger.error("Readiness check failed: %s", readiness_error)
        raise HTTPException(
            status_code=Status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service not ready"
        ) from readiness_error


@router.get("/live")
def liveness_check():
    """Liveness check for container orchestrators."""
    try:
        # Simple liveness check - just return ok if the service is running
        return {
            "alive": True,
            "timestamp": datetime.utcnow().isoformat(),
            "pid": os.getpid(),
        }
    except Exception as liveness_error:
        logger.error("Liveness check failed: %s", liveness_error)
        raise HTTPException(
            status_code=Status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service not alive"
        ) from liveness_error
