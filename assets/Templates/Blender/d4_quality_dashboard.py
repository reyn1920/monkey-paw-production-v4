"""
Quality Dashboard for monitoring application health, performance metrics, and quality indicators.
Provides comprehensive visualization and reporting of system quality metrics.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import statistics
from typing import Union
from typing import Optional
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QualityMetricType(Enum):
    """Types of quality metrics."""

    PERFORMANCE = "performance"
    RELIABILITY = "reliability"
    SECURITY = "security"
    USABILITY = "usability"
    MAINTAINABILITY = "maintainability"
    AVAILABILITY = "availability"


class HealthStatus(Enum):
    """Health status levels."""

    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class AlertSeverity(Enum):
    """Alert severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class QualityMetric:
    """Individual quality metric data point."""

    name: str
    value: Union[int, float]
    unit: str
    timestamp: datetime
    metric_type: QualityMetricType
    tags: Optional[dict[str, str]] = None
    threshold_min: Optional[float] = None
    threshold_max: Optional[float] = None


@dataclass
class HealthCheck:
    """Health check result."""

    name: str
    status: HealthStatus
    message: str
    timestamp: datetime
    response_time_ms: Optional[float] = None
    details: Optional[dict[str, Any]] = None


@dataclass
class Alert:
    """Quality alert."""

    id: str
    title: str
    description: str
    severity: AlertSeverity
    metric_name: str
    current_value: Union[int, float]
    threshold_value: Union[int, float]
    timestamp: datetime
    resolved: bool = False
    resolved_at: Optional[datetime] = None


@dataclass
class DashboardWidget:
    """Dashboard widget configuration."""

    id: str
    title: str
    widget_type: str  # "chart", "gauge", "table", "alert_list", "health_status"
    data_source: str
    config: dict[str, Any]
    position: dict[str, int]  # x, y, width, height
    refresh_interval: int = 30  # seconds


@dataclass
class DashboardConfig:
    """Dashboard configuration."""

    id: str
    name: str
    description: str
    widgets: list[DashboardWidget]
    layout: dict[str, Any]
    auto_refresh: bool = True
    refresh_interval: int = 30


class QualityDataCollector:
    """Collects quality metrics from various sources."""

    def __init__(self):
        self.metrics: list[QualityMetric] = []
        self.health_checks: list[HealthCheck] = []
        self.alerts: list[Alert] = []
        self.running = False
        self.collection_task: Optional[asyncio.Task[None]] = None

    async def collect_performance_metrics(self) -> list[QualityMetric]:
        """Collect performance-related quality metrics."""
        metrics = []
        timestamp = datetime.now()

        try:
            # Simulate collecting various performance metrics
            metrics.extend(
                [
                    QualityMetric(
                        name="response_time_avg",
                        value=125.5,
                        unit="ms",
                        timestamp=timestamp,
                        metric_type=QualityMetricType.PERFORMANCE,
                        threshold_max=200.0,
                    ),
                    QualityMetric(
                        name="throughput",
                        value=1250,
                        unit="requests/min",
                        timestamp=timestamp,
                        metric_type=QualityMetricType.PERFORMANCE,
                        threshold_min=1000.0,
                    ),
                    QualityMetric(
                        name="error_rate",
                        value=0.5,
                        unit="percentage",
                        timestamp=timestamp,
                        metric_type=QualityMetricType.RELIABILITY,
                        threshold_max=1.0,
                    ),
                    QualityMetric(
                        name="cpu_usage",
                        value=65.2,
                        unit="percentage",
                        timestamp=timestamp,
                        metric_type=QualityMetricType.PERFORMANCE,
                        threshold_max=80.0,
                    ),
                    QualityMetric(
                        name="memory_usage",
                        value=78.9,
                        unit="percentage",
                        timestamp=timestamp,
                        metric_type=QualityMetricType.PERFORMANCE,
                        threshold_max=85.0,
                    ),
                ]
            )

        except Exception as e:
            logger.error(f"Error collecting performance metrics: {e}")

        return metrics

    async def collect_security_metrics(self) -> list[QualityMetric]:
        """Collect security-related quality metrics."""
        metrics = []
        timestamp = datetime.now()

        try:
            metrics.extend(
                [
                    QualityMetric(
                        name="failed_login_attempts",
                        value=12,
                        unit="count",
                        timestamp=timestamp,
                        metric_type=QualityMetricType.SECURITY,
                        threshold_max=50.0,
                    ),
                    QualityMetric(
                        name="ssl_certificate_days_remaining",
                        value=45,
                        unit="days",
                        timestamp=timestamp,
                        metric_type=QualityMetricType.SECURITY,
                        threshold_min=30.0,
                    ),
                    QualityMetric(
                        name="vulnerability_score",
                        value=2.1,
                        unit="score",
                        timestamp=timestamp,
                        metric_type=QualityMetricType.SECURITY,
                        threshold_max=5.0,
                    ),
                ]
            )

        except Exception as e:
            logger.error(f"Error collecting security metrics: {e}")

        return metrics

    async def perform_health_checks(self) -> list[HealthCheck]:
        """Perform system health checks."""
        health_checks = []
        timestamp = datetime.now()

        try:
            # Database health check
            db_start = datetime.now()
            # Simulate database check
            await asyncio.sleep(0.01)
            db_response_time = (datetime.now() - db_start).total_seconds() * 1000

            health_checks.append(
                HealthCheck(
                    name="database",
                    status=(
                        HealthStatus.HEALTHY
                        if db_response_time < 100
                        else HealthStatus.WARNING
                    ),
                    message=f"Database responding in {db_response_time:.1f}ms",
                    timestamp=timestamp,
                    response_time_ms=db_response_time,
                )
            )

            # API health check
            api_start = datetime.now()
            await asyncio.sleep(0.005)
            api_response_time = (datetime.now() - api_start).total_seconds() * 1000

            health_checks.append(
                HealthCheck(
                    name="api",
                    status=HealthStatus.HEALTHY,
                    message="API endpoints responding normally",
                    timestamp=timestamp,
                    response_time_ms=api_response_time,
                )
            )

            # Cache health check
            health_checks.append(
                HealthCheck(
                    name="cache",
                    status=HealthStatus.HEALTHY,
                    message="Cache hit ratio: 85%",
                    timestamp=timestamp,
                    details={"hit_ratio": 0.85, "connections": 12},
                )
            )

            # External services check
            health_checks.append(
                HealthCheck(
                    name="external_services",
                    status=HealthStatus.WARNING,
                    message="Payment gateway experiencing delays",
                    timestamp=timestamp,
                    details={"payment_gateway": "degraded", "email_service": "healthy"},
                )
            )

        except Exception as e:
            logger.error(f"Error performing health checks: {e}")
            health_checks.append(
                HealthCheck(
                    name="health_check_system",
                    status=HealthStatus.CRITICAL,
                    message=f"Health check system error: {str(e)}",
                    timestamp=timestamp,
                )
            )

        return health_checks

    async def check_alerts(self, metrics: list[QualityMetric]) -> list[Alert]:
        """Check metrics against thresholds and generate alerts."""
        new_alerts = []

        for metric in metrics:
            alert_id = f"{metric.name}_{int(metric.timestamp.timestamp())}"

            # Check if metric exceeds thresholds
            if metric.threshold_max and metric.value > metric.threshold_max:
                alert = Alert(
                    id=alert_id,
                    title=f"High {
                        metric.name}",
                    description=f"{
                        metric.name} is {
                        metric.value} {
                        metric.unit}, exceeding threshold of {
                        metric.threshold_max}",
                    severity=(
                        AlertSeverity.HIGH
                        if metric.value > metric.threshold_max * 1.2
                        else AlertSeverity.MEDIUM
                    ),
                    metric_name=metric.name,
                    current_value=metric.value,
                    threshold_value=metric.threshold_max,
                    timestamp=metric.timestamp,
                )
                new_alerts.append(alert)

            elif metric.threshold_min and metric.value < metric.threshold_min:
                alert = Alert(
                    id=alert_id,
                    title=f"Low {
                        metric.name}",
                    description=f"{
                        metric.name} is {
                        metric.value} {
                        metric.unit}, below threshold of {
                        metric.threshold_min}",
                    severity=(
                        AlertSeverity.HIGH
                        if metric.value < metric.threshold_min * 0.8
                        else AlertSeverity.MEDIUM
                    ),
                    metric_name=metric.name,
                    current_value=metric.value,
                    threshold_value=metric.threshold_min,
                    timestamp=metric.timestamp,
                )
                new_alerts.append(alert)

        return new_alerts

    async def collect_all_metrics(self):
        """Collect all quality metrics."""
        try:
            # Collect different types of metrics
            performance_metrics = await self.collect_performance_metrics()
            security_metrics = await self.collect_security_metrics()

            # Combine all metrics
            all_metrics = performance_metrics + security_metrics

            # Store metrics (keep last 1000 entries)
            self.metrics.extend(all_metrics)
            if len(self.metrics) > 1000:
                self.metrics = self.metrics[-1000:]

            # Perform health checks
            health_results = await self.perform_health_checks()
            self.health_checks.extend(health_results)
            if len(self.health_checks) > 100:
                self.health_checks = self.health_checks[-100:]

            # Check for alerts
            new_alerts = await self.check_alerts(all_metrics)
            self.alerts.extend(new_alerts)
            if len(self.alerts) > 200:
                self.alerts = self.alerts[-200:]

            logger.debug(
                f"Collected {
                    len(all_metrics)} metrics, {
                    len(health_results)} health checks, {
                    len(new_alerts)} new alerts"
            )

        except Exception as e:
            logger.error(f"Error in metric collection: {e}")

    async def start_collection(self):
        """Start the metric collection process."""
        self.running = True
        self.collection_task = asyncio.create_task(self._collection_loop())
        logger.info("Started quality data collection")

    async def stop_collection(self):
        """Stop the metric collection process."""
        self.running = False
        if self.collection_task:
            self.collection_task.cancel()
            try:
                await self.collection_task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped quality data collection")

    async def _collection_loop(self):
        """Main collection loop."""
        while self.running:
            try:
                await self.collect_all_metrics()
                await asyncio.sleep(30)  # Collect every 30 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in collection loop: {e}")
                await asyncio.sleep(10)  # Wait before retrying


class QualityDashboard:
    """Main quality dashboard class."""

    def __init__(self):
        self.data_collector = QualityDataCollector()
        self.dashboards: dict[str, DashboardConfig] = {}
        self.running = False
        self._setup_default_dashboards()

    def _setup_default_dashboards(self):
        """Setup default dashboard configurations."""
        # Main overview dashboard
        overview_widgets = [
            DashboardWidget(
                id="system_health",
                title="System Health",
                widget_type="health_status",
                data_source="health_checks",
                config={"show_details": True},
                position={"x": 0, "y": 0, "width": 6, "height": 4},
            ),
            DashboardWidget(
                id="performance_chart",
                title="Performance Metrics",
                widget_type="chart",
                data_source="performance_metrics",
                config={"chart_type": "line", "time_range": "1h"},
                position={"x": 6, "y": 0, "width": 6, "height": 4},
            ),
            DashboardWidget(
                id="alerts_list",
                title="Active Alerts",
                widget_type="alert_list",
                data_source="alerts",
                config={"show_resolved": False, "max_items": 10},
                position={"x": 0, "y": 4, "width": 12, "height": 4},
            ),
            DashboardWidget(
                id="metrics_table",
                title="Key Metrics",
                widget_type="table",
                data_source="latest_metrics",
                config={"columns": ["name", "value", "unit", "status"]},
                position={"x": 0, "y": 8, "width": 12, "height": 4},
            ),
        ]

        overview_dashboard = DashboardConfig(
            id="overview",
            name="Quality Overview",
            description="Main dashboard showing overall system quality",
            widgets=overview_widgets,
            layout={"grid_size": 12, "row_height": 60},
        )

        self.dashboards["overview"] = overview_dashboard

        # Performance-focused dashboard
        performance_widgets = [
            DashboardWidget(
                id="response_time_gauge",
                title="Response Time",
                widget_type="gauge",
                data_source="response_time",
                config={"min": 0, "max": 500, "thresholds": [200, 350]},
                position={"x": 0, "y": 0, "width": 3, "height": 3},
            ),
            DashboardWidget(
                id="throughput_gauge",
                title="Throughput",
                widget_type="gauge",
                data_source="throughput",
                config={"min": 0, "max": 2000, "thresholds": [1000, 1500]},
                position={"x": 3, "y": 0, "width": 3, "height": 3},
            ),
            DashboardWidget(
                id="error_rate_gauge",
                title="Error Rate",
                widget_type="gauge",
                data_source="error_rate",
                config={"min": 0, "max": 5, "thresholds": [1, 3]},
                position={"x": 6, "y": 0, "width": 3, "height": 3},
            ),
            DashboardWidget(
                id="resource_usage_chart",
                title="Resource Usage",
                widget_type="chart",
                data_source="resource_metrics",
                config={"chart_type": "area", "metrics": ["cpu_usage", "memory_usage"]},
                position={"x": 0, "y": 3, "width": 12, "height": 5},
            ),
        ]

        performance_dashboard = DashboardConfig(
            id="performance",
            name="Performance Dashboard",
            description="Detailed performance metrics and monitoring",
            widgets=performance_widgets,
            layout={"grid_size": 12, "row_height": 60},
        )

        self.dashboards["performance"] = performance_dashboard

    async def get_dashboard_data(self, dashboard_id: str) -> dict[str, Any]:
        """Get data for a specific dashboard."""
        if dashboard_id not in self.dashboards:
            raise ValueError(f"Dashboard {dashboard_id} not found")

        dashboard = self.dashboards[dashboard_id]
        data: dict[str, Any] = {
            "dashboard": asdict(dashboard),
            "data": {},
            "last_updated": datetime.now().isoformat(),
        }

        # Collect data for each widget
        for widget in dashboard.widgets:
            widget_data = await self._get_widget_data(widget)
            data["data"][widget.id] = widget_data

        return data

    async def _get_widget_data(self, widget: DashboardWidget) -> dict[str, Any]:
        """Get data for a specific widget."""
        data_source = widget.data_source

        if data_source == "health_checks":
            return await self._get_health_check_data(widget)
        elif data_source == "performance_metrics":
            return await self._get_performance_metrics_data(widget)
        elif data_source == "alerts":
            return await self._get_alerts_data(widget)
        elif data_source == "latest_metrics":
            return await self._get_latest_metrics_data(widget)
        elif data_source in ["response_time", "throughput", "error_rate"]:
            return await self._get_gauge_data(widget, data_source)
        elif data_source == "resource_metrics":
            return await self._get_resource_metrics_data(widget)
        else:
            return {"error": f"Unknown data source: {data_source}"}

    async def _get_health_check_data(self, widget: DashboardWidget) -> dict[str, Any]:
        """Get health check data for widget."""
        recent_checks = [
            hc
            for hc in self.data_collector.health_checks
            if hc.timestamp > datetime.now() - timedelta(minutes=5)
        ]

        # Group by service name, get latest for each
        latest_checks = {}
        for check in recent_checks:
            if (
                check.name not in latest_checks
                or check.timestamp > latest_checks[check.name].timestamp
            ):
                latest_checks[check.name] = check

        return {
            "checks": [asdict(check) for check in latest_checks.values()],
            "overall_status": self._calculate_overall_health(
                list(latest_checks.values())
            ),
            "total_services": len(latest_checks),
        }

    async def _get_performance_metrics_data(
        self, widget: DashboardWidget
    ) -> dict[str, Any]:
        """Get performance metrics data for chart widget."""
        time_range = widget.config.get("time_range", "1h")

        # Calculate time range
        if time_range == "1h":
            start_time = datetime.now() - timedelta(hours=1)
        elif time_range == "24h":
            start_time = datetime.now() - timedelta(hours=24)
        else:
            start_time = datetime.now() - timedelta(hours=1)

        # Filter metrics by time and type
        performance_metrics = [
            m
            for m in self.data_collector.metrics
            if m.timestamp > start_time
            and m.metric_type == QualityMetricType.PERFORMANCE
        ]

        # Group by metric name
        grouped_metrics = defaultdict(list)
        for metric in performance_metrics:
            grouped_metrics[metric.name].append(
                {"timestamp": metric.timestamp.isoformat(), "value": metric.value}
            )

        return {
            "series": dict(grouped_metrics),
            "time_range": time_range,
            "data_points": len(performance_metrics),
        }

    async def _get_alerts_data(self, widget: DashboardWidget) -> dict[str, Any]:
        """Get alerts data for widget."""
        show_resolved = widget.config.get("show_resolved", False)
        max_items = widget.config.get("max_items", 10)

        # Filter alerts
        filtered_alerts = self.data_collector.alerts
        if not show_resolved:
            filtered_alerts = [a for a in filtered_alerts if not a.resolved]

        # Sort by timestamp (newest first) and limit
        sorted_alerts = sorted(
            filtered_alerts, key=lambda x: x.timestamp, reverse=True
        )[:max_items]

        return {
            "alerts": [asdict(alert) for alert in sorted_alerts],
            "total_active": len(
                [a for a in self.data_collector.alerts if not a.resolved]
            ),
            "total_resolved": len(
                [a for a in self.data_collector.alerts if a.resolved]
            ),
        }

    async def _get_latest_metrics_data(self, widget: DashboardWidget) -> dict[str, Any]:
        """Get latest metrics data for table widget."""
        # Get the latest value for each metric
        latest_metrics = {}
        for metric in reversed(self.data_collector.metrics):
            if metric.name not in latest_metrics:
                latest_metrics[metric.name] = metric

        # Convert to table format
        table_data = []
        for metric in latest_metrics.values():
            status = "normal"
            if metric.threshold_max and metric.value > metric.threshold_max:
                status = "critical"
            elif metric.threshold_min and metric.value < metric.threshold_min:
                status = "warning"

            table_data.append(
                {
                    "name": metric.name,
                    "value": metric.value,
                    "unit": metric.unit,
                    "status": status,
                    "timestamp": metric.timestamp.isoformat(),
                }
            )

        return {
            "rows": table_data,
            "columns": widget.config.get(
                "columns", ["name", "value", "unit", "status"]
            ),
        }

    async def _get_gauge_data(
        self, widget: DashboardWidget, metric_name: str
    ) -> dict[str, Any]:
        """Get gauge data for a specific metric."""
        # Find the latest value for this metric
        latest_metric = None
        for metric in reversed(self.data_collector.metrics):
            if metric.name == metric_name:
                latest_metric = metric
                break

        if not latest_metric:
            return {"value": 0, "status": "no_data"}

        config = widget.config
        min_val = config.get("min", 0)
        max_val = config.get("max", 100)
        thresholds = config.get("thresholds", [])

        # Determine status based on thresholds
        status = "normal"
        if thresholds:
            if len(thresholds) >= 2 and latest_metric.value > thresholds[1]:
                status = "critical"
            elif len(thresholds) >= 1 and latest_metric.value > thresholds[0]:
                status = "warning"

        return {
            "value": latest_metric.value,
            "min": min_val,
            "max": max_val,
            "status": status,
            "thresholds": thresholds,
            "unit": latest_metric.unit,
            "timestamp": latest_metric.timestamp.isoformat(),
        }

    async def _get_resource_metrics_data(
        self, widget: DashboardWidget
    ) -> dict[str, Any]:
        """Get resource metrics data for chart."""
        metrics_to_include = widget.config.get("metrics", ["cpu_usage", "memory_usage"])

        # Filter and group metrics
        resource_data: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for metric in self.data_collector.metrics:
            if metric.name in metrics_to_include:
                resource_data[metric.name].append(
                    {"timestamp": metric.timestamp.isoformat(), "value": metric.value}
                )

        return {
            "series": dict(resource_data),
            "chart_type": widget.config.get("chart_type", "line"),
        }

    def _calculate_overall_health(self, health_checks: list[HealthCheck]) -> str:
        """Calculate overall system health from individual checks."""
        if not health_checks:
            return HealthStatus.UNKNOWN.value

        statuses = [check.status for check in health_checks]

        if any(status == HealthStatus.CRITICAL for status in statuses):
            return HealthStatus.CRITICAL.value
        elif any(status == HealthStatus.WARNING for status in statuses):
            return HealthStatus.WARNING.value
        else:
            return HealthStatus.HEALTHY.value

    async def get_quality_summary(self) -> dict[str, Any]:
        """Get overall quality summary."""
        # Calculate summary statistics
        recent_metrics = [
            m
            for m in self.data_collector.metrics
            if m.timestamp > datetime.now() - timedelta(hours=1)
        ]
        recent_alerts = [
            a
            for a in self.data_collector.alerts
            if not a.resolved and a.timestamp > datetime.now() - timedelta(hours=24)
        ]
        recent_health = [
            h
            for h in self.data_collector.health_checks
            if h.timestamp > datetime.now() - timedelta(minutes=5)
        ]

        # Group metrics by type
        metrics_by_type = defaultdict(list)
        for metric in recent_metrics:
            metrics_by_type[metric.metric_type.value].append(metric)

        # Calculate scores (0-100)
        performance_score = self._calculate_performance_score(
            metrics_by_type.get("performance", [])
        )
        reliability_score = self._calculate_reliability_score(
            metrics_by_type.get("reliability", [])
        )
        security_score = self._calculate_security_score(
            metrics_by_type.get("security", [])
        )

        overall_score = (performance_score + reliability_score + security_score) / 3

        return {
            "overall_score": round(overall_score, 1),
            "performance_score": round(performance_score, 1),
            "reliability_score": round(reliability_score, 1),
            "security_score": round(security_score, 1),
            "active_alerts": len(recent_alerts),
            "critical_alerts": len(
                [a for a in recent_alerts if a.severity == AlertSeverity.CRITICAL]
            ),
            "system_health": self._calculate_overall_health(recent_health),
            "total_metrics": len(recent_metrics),
            "last_updated": datetime.now().isoformat(),
        }

    def _calculate_performance_score(self, metrics: list[QualityMetric]) -> float:
        """Calculate performance score from metrics."""
        if not metrics:
            return 50.0  # Default neutral score

        score = 100.0
        for metric in metrics:
            if metric.threshold_max and metric.value > metric.threshold_max:
                penalty = min(
                    30,
                    (metric.value - metric.threshold_max) / metric.threshold_max * 100,
                )
                score -= penalty

        return max(0, score)

    def _calculate_reliability_score(self, metrics: list[QualityMetric]) -> float:
        """Calculate reliability score from metrics."""
        if not metrics:
            return 50.0

        # Focus on error rates and uptime
        error_metrics = [m for m in metrics if "error" in m.name.lower()]
        if error_metrics:
            avg_error_rate = statistics.mean([m.value for m in error_metrics])
            # Scale error rate to score
            return max(0, 100 - (avg_error_rate * 20))

        return 85.0  # Default good score if no error metrics

    def _calculate_security_score(self, metrics: list[QualityMetric]) -> float:
        """Calculate security score from metrics."""
        if not metrics:
            return 50.0

        score = 100.0
        for metric in metrics:
            if "vulnerability" in metric.name.lower() and metric.value > 0:
                score -= metric.value * 10  # Deduct points for vulnerabilities
            elif "failed_login" in metric.name.lower() and metric.threshold_max:
                if metric.value > metric.threshold_max:
                    score -= 20

        return max(0, score)

    async def start(self):
        """Start the quality dashboard."""
        self.running = True
        await self.data_collector.start_collection()
        logger.info("Quality dashboard started")

    async def stop(self):
        """Stop the quality dashboard."""
        self.running = False
        await self.data_collector.stop_collection()
        logger.info("Quality dashboard stopped")

    def get_available_dashboards(self) -> list[dict[str, str]]:
        """Get list of available dashboards."""
        return [
            {
                "id": dashboard_id,
                "name": dashboard.name,
                "description": dashboard.description,
            }
            for dashboard_id, dashboard in self.dashboards.items()
        ]


# Global dashboard instance
quality_dashboard = QualityDashboard()


async def main():
    """Example usage of the quality dashboard."""
    try:
        # Start the dashboard
        await quality_dashboard.start()

        # Wait a bit for data collection
        await asyncio.sleep(5)

        # Get quality summary
        summary = await quality_dashboard.get_quality_summary()
        print(f"Quality Summary: {json.dumps(summary, indent=2)}")

        # Get dashboard data
        overview_data = await quality_dashboard.get_dashboard_data("overview")
        print(
            f"\nOverview Dashboard: {
                json.dumps(
                    overview_data,
                    indent=2,
                    default=str)}"
        )

        # List available dashboards
        dashboards = quality_dashboard.get_available_dashboards()
        print(f"\nAvailable Dashboards: {json.dumps(dashboards, indent=2)}")

    finally:
        # Stop the dashboard
        await quality_dashboard.stop()


if __name__ == "__main__":
    asyncio.run(main())
