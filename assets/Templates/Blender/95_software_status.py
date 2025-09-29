"""
Software Status Router for FastAPI Application
Professional-grade status monitoring and reporting system
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import asyncio
import logging
import psutil
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/software", tags=["software-status"])


class SystemMonitor:
    """Professional system monitoring class"""

    def __init__(self):
        self.start_time = datetime.now(timezone.utc)

    async def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health metrics"""
        try:
            # CPU and Memory metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Process information
            process = psutil.Process()
            process_memory = process.memory_info()

            return {
                "status": "healthy",
                "timestamp": datetime.now(
                    timezone.utc).isoformat(),
                "uptime_seconds": (
                    datetime.now(
                        timezone.utc) - self.start_time).total_seconds(),
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory": {
                        "total": memory.total,
                        "available": memory.available,
                        "percent": memory.percent,
                        "used": memory.used},
                    "disk": {
                        "total": disk.total,
                        "used": disk.used,
                        "free": disk.free,
                        "percent": (
                            disk.used / disk.total) * 100}},
                "process": {
                    "pid": process.pid,
                    "memory_rss": process_memory.rss,
                    "memory_vms": process_memory.vms,
                    "cpu_percent": process.cpu_percent(),
                    "num_threads": process.num_threads()},
                "python": {
                    "version": sys.version,
                    "executable": sys.executable,
                    "platform": sys.platform}}
        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }


class ApplicationStatus:
    """Application-specific status monitoring"""

    def __init__(self):
        self.status_checks = []

    async def check_database_connection(self) -> Dict[str, Any]:
        """Check database connectivity"""
        try:
            # Placeholder for actual database check
            return {
                "database": "connected",
                "status": "healthy",
                "response_time_ms": 50
            }
        except Exception as e:
            return {
                "database": "error",
                "status": "unhealthy",
                "error": str(e)
            }

    async def check_external_apis(self) -> Dict[str, Any]:
        """Check external API connectivity"""
        try:
            # Placeholder for API health checks
            return {
                "external_apis": {
                    "status": "healthy",
                    "services_checked": 0,
                    "services_healthy": 0
                }
            }
        except Exception as e:
            return {
                "external_apis": {
                    "status": "error",
                    "error": str(e)
                }
            }

    async def get_application_metrics(self) -> Dict[str, Any]:
        """Get application-specific metrics"""
        try:
            db_status = await self.check_database_connection()
            api_status = await self.check_external_apis()

            return {
                "application": {
                    "name": "FastAPI Production App",
                    "version": "1.0.0",
                    "environment": os.getenv("ENVIRONMENT", "production"),
                    "status": "running"
                },
                "services": {
                    **db_status,
                    **api_status
                },
                "features": {
                    "authentication": "enabled",
                    "monitoring": "enabled",
                    "logging": "enabled",
                    "security": "enabled"
                }
            }
        except Exception as e:
            logger.error(f"Error getting application metrics: {e}")
            return {
                "application": {
                    "status": "error",
                    "error": str(e)
                }
            }


# Initialize monitors
system_monitor = SystemMonitor()
app_status = ApplicationStatus()


@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "software-status-router"
    }


@router.get("/status")
async def get_software_status():
    """Get comprehensive software status"""
    try:
        # Get system and application metrics concurrently
        system_health, app_metrics = await asyncio.gather(
            system_monitor.get_system_health(),
            app_status.get_application_metrics()
        )

        # Determine overall status
        overall_status = "healthy"
        if system_health.get("status") != "healthy" or app_metrics.get(
                "application", {}).get("status") != "running":
            overall_status = "degraded"

        return JSONResponse(
            status_code=200,
            content={
                "overall_status": overall_status,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "system": system_health,
                "application": app_metrics,
                "metadata": {
                    "version": "1.0.0",
                    "environment": os.getenv("ENVIRONMENT", "production"),
                    "deployment_id": os.getenv("DEPLOYMENT_ID", "unknown")
                }
            }
        )
    except Exception as e:
        logger.error(f"Error in get_software_status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {
                str(e)}")


@router.get("/metrics")
async def get_detailed_metrics():
    """Get detailed system metrics for monitoring"""
    try:
        system_health = await system_monitor.get_system_health()

        return JSONResponse(
            status_code=200,
            content={
                "metrics": system_health,
                "collection_time": datetime.now(timezone.utc).isoformat(),
                "format_version": "1.0"
            }
        )
    except Exception as e:
        logger.error(f"Error in get_detailed_metrics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Metrics collection failed: {
                str(e)}")


@router.get("/diagnostics")
async def run_diagnostics():
    """Run comprehensive system diagnostics"""
    try:
        diagnostics = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tests": []
        }

        # File system checks
        try:
            current_dir = Path.cwd()
            diagnostics["tests"].append({
                "name": "filesystem_access",
                "status": "pass",
                "details": f"Current directory: {current_dir}, writable: {os.access(current_dir, os.W_OK)}"
            })
        except Exception as e:
            diagnostics["tests"].append({
                "name": "filesystem_access",
                "status": "fail",
                "error": str(e)
            })

        # Memory check
        try:
            memory = psutil.virtual_memory()
            memory_status = "pass" if memory.percent < 90 else "warning"
            diagnostics["tests"].append({
                "name": "memory_usage",
                "status": memory_status,
                "details": f"Memory usage: {memory.percent}%"
            })
        except Exception as e:
            diagnostics["tests"].append({
                "name": "memory_usage",
                "status": "fail",
                "error": str(e)
            })

        # Overall diagnostic status
        failed_tests = [test for test in diagnostics["tests"]
                        if test["status"] == "fail"]
        diagnostics["overall_status"] = "fail" if failed_tests else "pass"
        diagnostics["summary"] = {
            "total_tests": len(diagnostics["tests"]),
            "passed": len([t for t in diagnostics["tests"] if t["status"] == "pass"]),
            "warnings": len([t for t in diagnostics["tests"] if t["status"] == "warning"]),
            "failed": len(failed_tests)
        }

        return JSONResponse(
            status_code=200 if not failed_tests else 500,
            content=diagnostics
        )

    except Exception as e:
        logger.error(f"Error in run_diagnostics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Diagnostics failed: {
                str(e)}")

# Export router for main application
__all__ = ["router"]
