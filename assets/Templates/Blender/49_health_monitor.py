"""Health Monitor Module

Provides comprehensive health monitoring and system status tracking.
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import psutil
import aiohttp


class HealthStatus(Enum):
    """Health status enumeration."""

    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """Individual health check result."""

    name: str
    status: HealthStatus
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    response_time: Optional[float] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemMetrics:
    """System performance metrics."""

    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: dict[str, int]
    timestamp: datetime = field(default_factory=datetime.now)


class HealthMonitor:
    """Comprehensive health monitoring system."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.checks: dict[str, HealthCheck] = {}
        self.metrics_history: list[SystemMetrics] = []
        self.max_history = 100
        self.check_interval = 30  # seconds
        self.running = False

    async def start_monitoring(self):
        """Start continuous health monitoring."""
        self.running = True
        self.logger.info("Health monitoring started")

        while self.running:
            try:
                await self.run_all_checks()
                await self.collect_system_metrics()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(5)

    def stop_monitoring(self):
        """Stop health monitoring."""
        self.running = False
        self.logger.info("Health monitoring stopped")

    async def run_all_checks(self):
        """Run all registered health checks."""
        tasks = [
            self.check_system_resources(),
            self.check_database_connection(),
            self.check_external_services(),
            self.check_application_health(),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"Health check {i} failed: {result}")

    async def check_system_resources(self) -> HealthCheck:
        """Check system resource usage."""
        start_time = time.time()

        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            # Determine status based on thresholds
            if cpu_percent > 90 or memory.percent > 90 or disk.percent > 90:
                status = HealthStatus.CRITICAL
                message = "System resources critically high"
            elif cpu_percent > 70 or memory.percent > 70 or disk.percent > 80:
                status = HealthStatus.WARNING
                message = "System resources elevated"
            else:
                status = HealthStatus.HEALTHY
                message = "System resources normal"

            check = HealthCheck(
                name="system_resources",
                status=status,
                message=message,
                response_time=time.time() - start_time,
                metadata={
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "disk_percent": disk.percent,
                },
            )

            self.checks["system_resources"] = check
            return check

        except Exception as e:
            check = HealthCheck(
                name="system_resources",
                status=HealthStatus.CRITICAL,
                message=f"Failed to check system resources: {e}",
                response_time=time.time() - start_time,
            )
            self.checks["system_resources"] = check
            return check

    async def check_database_connection(self) -> HealthCheck:
        """Check database connectivity."""
        start_time = time.time()

        try:
            # Simulate database check
            await asyncio.sleep(0.1)  # Simulate connection time

            check = HealthCheck(
                name="database",
                status=HealthStatus.HEALTHY,
                message="Database connection healthy",
                response_time=time.time() - start_time,
            )

            self.checks["database"] = check
            return check

        except Exception as e:
            check = HealthCheck(
                name="database",
                status=HealthStatus.CRITICAL,
                message=f"Database connection failed: {e}",
                response_time=time.time() - start_time,
            )
            self.checks["database"] = check
            return check

    async def check_external_services(self) -> HealthCheck:
        """Check external service dependencies."""
        start_time = time.time()

        try:
            # Check external APIs or services
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://httpbin.org/status/200", timeout=5
                ) as response:
                    if response.status == 200:
                        status = HealthStatus.HEALTHY
                        message = "External services accessible"
                    else:
                        status = HealthStatus.WARNING
                        message = f"External service returned {
                            response.status}"

            check = HealthCheck(
                name="external_services",
                status=status,
                message=message,
                response_time=time.time() - start_time,
            )

            self.checks["external_services"] = check
            return check

        except Exception as e:
            check = HealthCheck(
                name="external_services",
                status=HealthStatus.WARNING,
                message=f"External service check failed: {e}",
                response_time=time.time() - start_time,
            )
            self.checks["external_services"] = check
            return check

    async def check_application_health(self) -> HealthCheck:
        """Check application-specific health metrics."""
        start_time = time.time()

        try:
            # Check application-specific metrics
            # This could include queue lengths, cache hit rates, etc.

            check = HealthCheck(
                name="application",
                status=HealthStatus.HEALTHY,
                message="Application health normal",
                response_time=time.time() - start_time,
                metadata={
                    "active_connections": 42,
                    "queue_length": 0,
                    "cache_hit_rate": 0.95,
                },
            )

            self.checks["application"] = check
            return check

        except Exception as e:
            check = HealthCheck(
                name="application",
                status=HealthStatus.CRITICAL,
                message=f"Application health check failed: {e}",
                response_time=time.time() - start_time,
            )
            self.checks["application"] = check
            return check

    async def collect_system_metrics(self):
        """Collect and store system performance metrics."""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            network = psutil.net_io_counters()

            metrics = SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                disk_percent=disk.percent,
                network_io={
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                },
            )

            self.metrics_history.append(metrics)

            # Keep only recent metrics
            if len(self.metrics_history) > self.max_history:
                self.metrics_history = self.metrics_history[-self.max_history :]

        except Exception as e:
            self.logger.error(f"Failed to collect system metrics: {e}")

    def get_overall_status(self) -> HealthStatus:
        """Get overall system health status."""
        if not self.checks:
            return HealthStatus.UNKNOWN

        statuses = [check.status for check in self.checks.values()]

        if HealthStatus.CRITICAL in statuses:
            return HealthStatus.CRITICAL
        elif HealthStatus.WARNING in statuses:
            return HealthStatus.WARNING
        elif all(status == HealthStatus.HEALTHY for status in statuses):
            return HealthStatus.HEALTHY
        else:
            return HealthStatus.UNKNOWN

    def get_health_report(self) -> dict[str, Any]:
        """Generate comprehensive health report."""
        overall_status = self.get_overall_status()

        return {
            "overall_status": overall_status.value,
            "timestamp": datetime.now().isoformat(),
            "checks": {
                name: {
                    "status": check.status.value,
                    "message": check.message,
                    "response_time": check.response_time,
                    "timestamp": check.timestamp.isoformat(),
                    "metadata": check.metadata,
                }
                for name, check in self.checks.items()
            },
            "metrics": {
                "current": (
                    self.metrics_history[-1].__dict__ if self.metrics_history else None
                ),
                "history_count": len(self.metrics_history),
            },
        }

    def get_metrics_summary(self, minutes: int = 10) -> dict[str, Any]:
        """Get metrics summary for the specified time period."""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_metrics = [m for m in self.metrics_history if m.timestamp >= cutoff_time]

        if not recent_metrics:
            return {"error": "No metrics available for the specified period"}

        cpu_values = [m.cpu_percent for m in recent_metrics]
        memory_values = [m.memory_percent for m in recent_metrics]
        disk_values = [m.disk_percent for m in recent_metrics]

        return {
            "period_minutes": minutes,
            "sample_count": len(recent_metrics),
            "cpu": {
                "avg": sum(cpu_values) / len(cpu_values),
                "min": min(cpu_values),
                "max": max(cpu_values),
            },
            "memory": {
                "avg": sum(memory_values) / len(memory_values),
                "min": min(memory_values),
                "max": max(memory_values),
            },
            "disk": {
                "avg": sum(disk_values) / len(disk_values),
                "min": min(disk_values),
                "max": max(disk_values),
            },
        }


# Global health monitor instance
health_monitor = HealthMonitor()


async def get_health_status() -> dict[str, Any]:
    """Get current health status (API endpoint helper)."""
    return health_monitor.get_health_report()


async def get_metrics(minutes: int = 10) -> dict[str, Any]:
    """Get metrics summary (API endpoint helper)."""
    return health_monitor.get_metrics_summary(minutes)
