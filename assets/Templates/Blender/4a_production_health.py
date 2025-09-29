"""Production health monitoring router."""

from typing import Any
from datetime import datetime
import logging
import os
import sys
import time
from fastapi import APIRouter, HTTPException, status

# Logger setup
logger = logging.getLogger(__name__)

# Health check service


class ProductionHealthService:
    """Service for production health monitoring."""

    # Class variable to track start time
    _start_time: float = time.time()

    @staticmethod
    def get_system_health() -> dict[str, Any]:
        """Get comprehensive system health information."""
        try:
            checks = {
                "application": ProductionHealthService._check_application(),
                "system": ProductionHealthService._check_system(),
                "dependencies": ProductionHealthService._check_dependencies(),
            }

            health_data = {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "environment": "production",
                "checks": checks,
            }

            # Determine overall health status
            all_checks_healthy = all(
                check.get("status") == "healthy" for check in checks.values()
            )

            if not all_checks_healthy:
                health_data["status"] = "degraded"

            return health_data

        except Exception as health_error:
            logger.error("Health check failed: %s", health_error)
            return {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(health_error),
            }

    @staticmethod
    def _check_application() -> dict[str, Any]:
        """Check application-specific health."""
        try:
            return {
                "status": "healthy",
                "python_version": sys.version,
                "process_id": os.getpid(),
                "working_directory": os.getcwd(),
                "uptime_seconds": ProductionHealthService._get_uptime(),
            }
        except Exception as app_error:
            return {"status": "unhealthy", "error": str(app_error)}

    @staticmethod
    def _check_system() -> dict[str, Any]:
        """Check system resources."""
        try:
            # Basic system checks without external dependencies
            system_info = {
                "status": "healthy",
                "platform": sys.platform,
                "python_executable": sys.executable,
                "environment_variables": {
                    "PATH": os.environ.get("PATH", "not_set"),
                    "HOME": os.environ.get("HOME", "not_set"),
                    "USER": os.environ.get("USER", "not_set"),
                },
            }

            # Check disk space if possible
            try:
                import shutil

                total, used, free = shutil.disk_usage("/")
                system_info["disk"] = {
                    "total_gb": round(total / (1024**3), 2),
                    "used_gb": round(used / (1024**3), 2),
                    "free_gb": round(free / (1024**3), 2),
                }
            except (ImportError, OSError):
                system_info["disk"] = "unavailable"

            return system_info

        except Exception as system_error:
            return {"status": "unhealthy", "error": str(system_error)}

    @staticmethod
    def _check_dependencies() -> dict[str, Any]:
        """Check critical dependencies."""
        try:
            dependencies = {"status": "healthy", "python_modules": {}}

            # Check for common modules
            modules_to_check = ["json", "datetime", "logging", "os", "sys"]
            for module_name in modules_to_check:
                try:
                    __import__(module_name)
                    dependencies["python_modules"][module_name] = "available"
                except ImportError:
                    dependencies["python_modules"][module_name] = "missing"
                    dependencies["status"] = "degraded"

            # Check for optional modules
            optional_modules = ["fastapi", "uvicorn", "requests"]
            for module_name in optional_modules:
                try:
                    __import__(module_name)
                    dependencies["python_modules"][module_name] = "available"
                except ImportError:
                    dependencies["python_modules"][module_name] = "optional_missing"

            return dependencies

        except Exception as deps_error:
            return {"status": "unhealthy", "error": str(deps_error)}

    @staticmethod
    def _get_uptime() -> float:
        """Get application uptime in seconds."""
        return time.time() - ProductionHealthService._start_time


# Router setup
router = APIRouter(prefix="/api/health", tags=["production-health"])


@router.get("/")
def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "production-health",
    }


@router.get("/detailed")
def detailed_health_check():
    """Detailed health check with system information."""
    health_data = ProductionHealthService.get_system_health()

    # Return appropriate HTTP status based on health
    if health_data["status"] == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(health_data)
        )

    return health_data


@router.get("/readiness")
def readiness_check():
    """Kubernetes-style readiness probe."""
    try:
        # Check if application is ready to serve traffic
        health_data = ProductionHealthService.get_system_health()

        if health_data["status"] in ["healthy", "degraded"]:
            return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service not ready"
        )

    except Exception as readiness_error:
        logger.error("Readiness check failed: %s", readiness_error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service not ready"
        ) from readiness_error


@router.get("/liveness")
def liveness_check():
    """Kubernetes-style liveness probe."""
    try:
        # Basic liveness check - if we can respond, we're alive
        return {
            "status": "alive",
            "timestamp": datetime.utcnow().isoformat(),
            "process_id": os.getpid(),
        }

    except Exception as liveness_error:
        logger.error("Liveness check failed: %s", liveness_error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service not responding",
        ) from liveness_error


@router.get("/metrics")
def get_metrics():
    """Get basic application metrics."""
    try:
        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": ProductionHealthService._get_uptime(),
            "process_id": os.getpid(),
            "python_version": list(sys.version_info[:3]),
        }

        # Add memory usage if available
        try:
            import resource

            usage = resource.getrusage(resource.RUSAGE_SELF)
            metrics["max_rss_kb"] = usage.ru_maxrss
            metrics["user_time"] = usage.ru_utime
            metrics["system_time"] = usage.ru_stime
        except ImportError:
            metrics["memory_status"] = "unavailable"

        return metrics

    except Exception as metrics_error:
        logger.error("Metrics collection failed: %s", metrics_error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to collect metrics",
        ) from metrics_error
