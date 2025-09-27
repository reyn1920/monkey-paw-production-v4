"""
Metrics Collection System for monitoring application performance and business metrics.
Provides comprehensive metric tracking, aggregation, and reporting capabilities.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, deque
import threading
from abc import ABC, abstractmethod
import statistics
from typing import Union
from typing import Optional
from typing import Any
from typing import Callable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics that can be collected."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"
    RATE = "rate"
    PERCENTAGE = "percentage"


class MetricUnit(Enum):
    """Units for metric values."""

    COUNT = "count"
    BYTES = "bytes"
    SECONDS = "seconds"
    MILLISECONDS = "milliseconds"
    PERCENTAGE = "percentage"
    REQUESTS_PER_SECOND = "requests_per_second"
    ERRORS_PER_MINUTE = "errors_per_minute"


class AlertLevel(Enum):
    """Alert levels for metric thresholds."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class MetricValue:
    """Individual metric value with timestamp."""

    value: Union[int, float]
    timestamp: datetime
    tags: Optional[dict[str, str]] = None
    metadata: Optional[dict[str, Any]] = None


@dataclass
class MetricThreshold:
    """Threshold configuration for metric alerts."""

    name: str
    condition: str  # "gt", "lt", "eq", "gte", "lte"
    value: Union[int, float]
    alert_level: AlertLevel
    duration_seconds: int = 60  # How long condition must persist


@dataclass
class MetricConfig:
    """Configuration for a metric."""

    name: str
    metric_type: MetricType
    unit: MetricUnit
    description: str
    tags: Optional[dict[str, str]] = None
    thresholds: Optional[list[MetricThreshold]] = None
    retention_days: int = 30
    aggregation_window: int = 300  # seconds


class MetricStorage(ABC):
    """Abstract base class for metric storage backends."""

    @abstractmethod
    async def store_metric(self, metric_name: str, value: MetricValue) -> bool:
        """Store a metric value."""

    @abstractmethod
    async def get_metrics(
        self, metric_name: str, start_time: datetime, end_time: datetime
    ) -> list[MetricValue]:
        """Retrieve metric values for a time range."""

    @abstractmethod
    async def get_metric_names(self) -> list[str]:
        """Get all available metric names."""


class InMemoryMetricStorage(MetricStorage):
    """In-memory storage for metrics (for development/testing)."""

    def __init__(self, max_values_per_metric: int = 10000):
        self.metrics: dict[str, deque[MetricValue]] = defaultdict(
            lambda: deque(maxlen=max_values_per_metric)
        )
        self.lock = threading.RLock()

    async def store_metric(self, metric_name: str, value: MetricValue) -> bool:
        """Store a metric value in memory."""
        try:
            with self.lock:
                self.metrics[metric_name].append(value)
            return True
        except Exception as e:
            logger.error(f"Failed to store metric {metric_name}: {e}")
            return False

    async def get_metrics(
        self, metric_name: str, start_time: datetime, end_time: datetime
    ) -> list[MetricValue]:
        """Retrieve metric values for a time range."""
        try:
            with self.lock:
                if metric_name not in self.metrics:
                    return []

                values = []
                for value in self.metrics[metric_name]:
                    if start_time <= value.timestamp <= end_time:
                        values.append(value)

                return sorted(values, key=lambda x: x.timestamp)
        except Exception as e:
            logger.error(f"Failed to get metrics for {metric_name}: {e}")
            return []

    async def get_metric_names(self) -> list[str]:
        """Get all available metric names."""
        with self.lock:
            return list(self.metrics.keys())


class Metric:
    """Individual metric implementation."""

    def __init__(self, config: MetricConfig, storage: MetricStorage):
        self.config = config
        self.storage = storage
        self.current_value: Optional[Union[int, float]] = None
        self.last_updated = datetime.now()
        self.alert_states: dict[str, bool] = {}

    async def record(
        self,
        value: Union[int, float],
        tags: Optional[dict[str, str]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """Record a new metric value."""
        try:
            # Merge tags
            combined_tags = {}
            if self.config.tags:
                combined_tags.update(self.config.tags)
            if tags:
                combined_tags.update(tags)

            metric_value = MetricValue(
                value=value,
                timestamp=datetime.now(),
                tags=combined_tags if combined_tags else None,
                metadata=metadata,
            )

            # Store the metric
            success = await self.storage.store_metric(self.config.name, metric_value)
            if success:
                self.current_value = value
                self.last_updated = metric_value.timestamp

                # Check thresholds
                await self._check_thresholds(value)

                logger.debug(f"Recorded metric {self.config.name}: {value}")
            else:
                logger.error(f"Failed to store metric {self.config.name}")
        except Exception as e:
            logger.error(f"Error recording metric {self.config.name}: {e}")

    async def increment(
        self, amount: Union[int, float] = 1, tags: Optional[dict[str, str]] = None
    ):
        """Increment a counter metric."""
        if self.config.metric_type != MetricType.COUNTER:
            logger.warning(
                f"Increment called on non-counter metric: {self.config.name}"
            )
            return

        current = self.current_value or 0
        await self.record(current + amount, tags)

    async def set_gauge(
        self, value: Union[int, float], tags: Optional[dict[str, str]] = None
    ):
        """Set a gauge metric value."""
        if self.config.metric_type != MetricType.GAUGE:
            logger.warning(f"Set gauge called on non-gauge metric: {self.config.name}")
            return

        await self.record(value, tags)

    async def time_operation(
        self, operation: Callable[[], Any], tags: Optional[dict[str, str]] = None
    ) -> Any:
        """Time an operation and record the duration."""
        if self.config.metric_type != MetricType.TIMER:
            logger.warning(
                f"Time operation called on non-timer metric: {self.config.name}"
            )
            return await operation()

        start_time = time.time()
        try:
            result = (
                await operation()
                if asyncio.iscoroutinefunction(operation)
                else operation()
            )
            duration = (time.time() - start_time) * 1000  # Convert to milliseconds
            await self.record(duration, tags)
            return result
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            error_tags = tags.copy() if tags else {}
            error_tags["error"] = str(type(e).__name__)
            await self.record(duration, error_tags)
            raise

    async def _check_thresholds(self, value: Union[int, float]):
        """Check if value exceeds any configured thresholds."""
        if not self.config.thresholds:
            return

        for threshold in self.config.thresholds:
            condition_met = False

            if threshold.condition == "gt" and value > threshold.value:
                condition_met = True
            elif threshold.condition == "lt" and value < threshold.value:
                condition_met = True
            elif threshold.condition == "eq" and value == threshold.value:
                condition_met = True
            elif threshold.condition == "gte" and value >= threshold.value:
                condition_met = True
            elif threshold.condition == "lte" and value <= threshold.value:
                condition_met = True

            if condition_met and not self.alert_states.get(threshold.name, False):
                self.alert_states[threshold.name] = True
                logger.warning(
                    f"Threshold alert: {
                        self.config.name} {
                        threshold.condition} {
                        threshold.value} "
                    f"(current: {value}, level: {
                        threshold.alert_level.value})"
                )
            elif not condition_met and self.alert_states.get(threshold.name, False):
                self.alert_states[threshold.name] = False
                logger.info(
                    f"Threshold alert resolved: {
                        self.config.name} {
                        threshold.name}"
                )

    async def get_statistics(
        self, start_time: datetime, end_time: datetime
    ) -> dict[str, Any]:
        """Get statistical summary for the metric over a time range."""
        values = await self.storage.get_metrics(self.config.name, start_time, end_time)

        if not values:
            return {"count": 0, "min": None, "max": None, "avg": None, "sum": None}

        numeric_values = [v.value for v in values]

        stats = {
            "count": len(numeric_values),
            "min": min(numeric_values),
            "max": max(numeric_values),
            "avg": statistics.mean(numeric_values),
            "sum": sum(numeric_values),
            "latest": values[-1].value if values else None,
            "latest_timestamp": values[-1].timestamp.isoformat() if values else None,
        }

        if len(numeric_values) > 1:
            stats["median"] = statistics.median(numeric_values)
            stats["stdev"] = statistics.stdev(numeric_values)

        return stats


class MetricsCollector:
    """Main metrics collection system."""

    def __init__(self, storage: Optional[MetricStorage] = None):
        self.storage = storage or InMemoryMetricStorage()
        self.metrics: dict[str, Metric] = {}
        self.running = False
        self.aggregation_task: Optional[asyncio.Task[None]] = None

    def register_metric(self, config: MetricConfig) -> Metric:
        """Register a new metric."""
        if config.name in self.metrics:
            logger.warning(
                f"Metric {
                    config.name} already registered, replacing"
            )

        metric = Metric(config, self.storage)
        self.metrics[config.name] = metric
        logger.info(
            f"Registered metric: {
                config.name} ({
                config.metric_type.value})"
        )
        return metric

    def get_metric(self, name: str) -> Optional[Metric]:
        """Get a registered metric by name."""
        return self.metrics.get(name)

    async def record_metric(
        self, name: str, value: Union[int, float], tags: Optional[dict[str, str]] = None
    ):
        """Record a value for a metric by name."""
        metric = self.get_metric(name)
        if metric:
            await metric.record(value, tags)
        else:
            logger.warning(f"Metric not found: {name}")

    async def increment_counter(
        self,
        name: str,
        amount: Union[int, float] = 1,
        tags: Optional[dict[str, str]] = None,
    ):
        """Increment a counter metric by name."""
        metric = self.get_metric(name)
        if metric:
            await metric.increment(amount, tags)
        else:
            logger.warning(f"Counter metric not found: {name}")

    async def set_gauge(
        self, name: str, value: Union[int, float], tags: Optional[dict[str, str]] = None
    ):
        """Set a gauge metric value by name."""
        metric = self.get_metric(name)
        if metric:
            await metric.set_gauge(value, tags)
        else:
            logger.warning(f"Gauge metric not found: {name}")

    async def time_operation(
        self,
        name: str,
        operation: Callable[[], Any],
        tags: Optional[dict[str, str]] = None,
    ) -> Any:
        """Time an operation using a timer metric."""
        metric = self.get_metric(name)
        if metric:
            return await metric.time_operation(operation, tags)
        else:
            logger.warning(f"Timer metric not found: {name}")
            return (
                await operation()
                if asyncio.iscoroutinefunction(operation)
                else operation()
            )

    def create_counter(
        self, name: str, description: str, tags: Optional[dict[str, str]] = None
    ) -> Metric:
        """Create and register a counter metric."""
        config = MetricConfig(
            name=name,
            metric_type=MetricType.COUNTER,
            unit=MetricUnit.COUNT,
            description=description,
            tags=tags,
        )
        return self.register_metric(config)

    def create_gauge(
        self,
        name: str,
        description: str,
        unit: MetricUnit = MetricUnit.COUNT,
        tags: Optional[dict[str, str]] = None,
    ) -> Metric:
        """Create and register a gauge metric."""
        config = MetricConfig(
            name=name,
            metric_type=MetricType.GAUGE,
            unit=unit,
            description=description,
            tags=tags,
        )
        return self.register_metric(config)

    def create_timer(
        self, name: str, description: str, tags: Optional[dict[str, str]] = None
    ) -> Metric:
        """Create and register a timer metric."""
        config = MetricConfig(
            name=name,
            metric_type=MetricType.TIMER,
            unit=MetricUnit.MILLISECONDS,
            description=description,
            tags=tags,
        )
        return self.register_metric(config)

    async def get_all_metrics_summary(self) -> dict[str, Any]:
        """Get summary of all registered metrics."""
        summary = {"total_metrics": len(self.metrics), "metrics": {}}

        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)  # Last hour

        for name, metric in self.metrics.items():
            stats = await metric.get_statistics(start_time, end_time)
            summary["metrics"][name] = {
                "type": metric.config.metric_type.value,
                "unit": metric.config.unit.value,
                "description": metric.config.description,
                "current_value": metric.current_value,
                "last_updated": (
                    metric.last_updated.isoformat() if metric.last_updated else None
                ),
                "stats_last_hour": stats,
            }

        return summary

    async def export_metrics(self, format_type: str = "json") -> str:
        """Export metrics in various formats."""
        summary = await self.get_all_metrics_summary()

        if format_type.lower() == "json":
            return json.dumps(summary, indent=2, default=str)
        else:
            # Simple text format
            lines = [f"Metrics Summary ({summary['total_metrics']} metrics)"]
            lines.append("=" * 50)

            for name, data in summary["metrics"].items():
                lines.append(f"\n{name} ({data['type']})")
                lines.append(f"  Description: {data['description']}")
                lines.append(
                    f"  Current: {
                        data['current_value']} {
                        data['unit']}"
                )
                lines.append(f"  Last Updated: {data['last_updated']}")

                stats = data["stats_last_hour"]
                if stats["count"] > 0:
                    lines.append(
                        f"  Last Hour: {
                            stats['count']} values, avg={
                            stats['avg']:.2f}"
                    )

            return "\n".join(lines)

    async def start_background_tasks(self):
        """Start background tasks for metric aggregation."""
        self.running = True
        self.aggregation_task = asyncio.create_task(self._aggregation_loop())
        logger.info("Started metrics background tasks")

    async def stop_background_tasks(self):
        """Stop background tasks."""
        self.running = False
        if self.aggregation_task:
            self.aggregation_task.cancel()
            try:
                await self.aggregation_task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped metrics background tasks")

    async def _aggregation_loop(self):
        """Background task for metric aggregation and cleanup."""
        while self.running:
            try:
                # Perform periodic aggregation and cleanup
                await self._cleanup_old_metrics()
                await asyncio.sleep(300)  # Run every 5 minutes
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in aggregation loop: {e}")
                await asyncio.sleep(60)  # Wait before retrying

    async def _cleanup_old_metrics(self):
        """Clean up old metric data based on retention policies."""
        # This would implement cleanup logic based on retention_days
        # For now, just log that cleanup would happen
        logger.debug("Performing metric cleanup (placeholder)")


# Global metrics collector instance
metrics_collector = MetricsCollector()


# Convenience functions for common operations
async def increment(
    name: str, amount: Union[int, float] = 1, tags: Optional[dict[str, str]] = None
):
    """Increment a counter metric."""
    await metrics_collector.increment_counter(name, amount, tags)


async def gauge(
    name: str, value: Union[int, float], tags: Optional[dict[str, str]] = None
):
    """Set a gauge metric value."""
    await metrics_collector.set_gauge(name, value, tags)


async def timer(
    name: str, operation: Callable[[], Any], tags: Optional[dict[str, str]] = None
) -> Any:
    """Time an operation."""
    return await metrics_collector.time_operation(name, operation, tags)


def create_standard_metrics():
    """Create a set of standard application metrics."""
    # Request metrics
    metrics_collector.create_counter("http_requests_total", "Total HTTP requests")
    metrics_collector.create_counter("http_errors_total", "Total HTTP errors")
    metrics_collector.create_timer("http_request_duration", "HTTP request duration")

    # System metrics
    metrics_collector.create_gauge(
        "memory_usage_bytes", "Memory usage in bytes", MetricUnit.BYTES
    )
    metrics_collector.create_gauge(
        "cpu_usage_percent", "CPU usage percentage", MetricUnit.PERCENTAGE
    )

    # Application metrics
    metrics_collector.create_counter("user_registrations", "User registrations")
    metrics_collector.create_counter("user_logins", "User logins")
    metrics_collector.create_gauge("active_users", "Currently active users")

    logger.info("Created standard metrics")


async def main():
    """Example usage of the metrics system."""
    # Create standard metrics
    create_standard_metrics()

    # Start background tasks
    await metrics_collector.start_background_tasks()

    try:
        # Simulate some metric recording
        await increment(
            "http_requests_total", tags={"method": "GET", "endpoint": "/api/users"}
        )
        await increment(
            "http_requests_total", tags={"method": "POST", "endpoint": "/api/users"}
        )
        await gauge("active_users", 150)
        await gauge("memory_usage_bytes", 1024 * 1024 * 512)  # 512MB

        # Time an operation
        async def sample_operation():
            await asyncio.sleep(0.1)  # Simulate work
            return "completed"

        result = await timer(
            "http_request_duration", sample_operation, tags={"endpoint": "/api/data"}
        )
        print(f"Operation result: {result}")

        # Get metrics summary
        summary = await metrics_collector.get_all_metrics_summary()
        print(f"Metrics summary: {json.dumps(summary, indent=2, default=str)}")

        # Export metrics
        exported = await metrics_collector.export_metrics("text")
        print(f"\nExported metrics:\n{exported}")

    finally:
        # Stop background tasks
        await metrics_collector.stop_background_tasks()


if __name__ == "__main__":
    asyncio.run(main())
