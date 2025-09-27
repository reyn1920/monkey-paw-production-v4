#!/usr/bin/env python3
"""
API Master Dashboard
Comprehensive dashboard for monitoring and managing API operations
"""

import asyncio
import logging
import json
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from collections import defaultdict, deque
from typing import Optional
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    ERROR = "error"
    OFFLINE = "offline"


class MetricType(Enum):
    RESPONSE_TIME = "response_time"
    REQUEST_COUNT = "request_count"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    UPTIME = "uptime"


@dataclass
class APIEndpoint:
    """Represents an API endpoint being monitored"""

    id: str
    name: str
    url: str
    method: str
    status: APIStatus
    last_check: Optional[datetime] = None
    response_time: float = 0.0
    success_rate: float = 100.0
    total_requests: int = 0
    failed_requests: int = 0
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_check is None:
            self.last_check = datetime.now()


@dataclass
class APIMetric:
    """Represents a metric data point"""

    endpoint_id: str
    metric_type: MetricType
    value: float
    timestamp: datetime
    metadata: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AlertRule:
    """Represents an alert rule for monitoring"""

    id: str
    name: str
    endpoint_id: str
    metric_type: MetricType
    threshold: float
    condition: str  # 'greater_than', 'less_than', 'equals'
    is_active: bool = True
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Alert:
    """Represents an active alert"""

    id: str
    rule_id: str
    endpoint_id: str
    message: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    triggered_at: datetime
    resolved_at: Optional[datetime] = None
    is_resolved: bool = False


class APIMasterDashboard:
    """Main dashboard for API monitoring and management"""

    def __init__(self):
        self.endpoints: dict[str, APIEndpoint] = {}
        self.metrics: dict[str, Deque[APIMetric]] = defaultdict(
            lambda: deque(maxlen=1000)
        )
        self.alert_rules: dict[str, AlertRule] = {}
        self.active_alerts: dict[str, Alert] = {}
        self.is_monitoring = False
        self.monitoring_interval = 30  # seconds
        self.dashboard_stats = {
            "total_requests": 0,
            "total_errors": 0,
            "average_response_time": 0.0,
            "uptime_percentage": 100.0,
            "last_updated": datetime.now(),
        }

        logger.info("API Master Dashboard initialized")

    async def start_monitoring(self):
        """Start the monitoring system"""
        if self.is_monitoring:
            logger.warning("Monitoring is already running")
            return

        self.is_monitoring = True
        logger.info("Starting API monitoring...")

        # Start monitoring loop
        asyncio.create_task(self._monitoring_loop())

        logger.info("API monitoring started successfully")

    async def stop_monitoring(self):
        """Stop the monitoring system"""
        self.is_monitoring = False
        logger.info("API monitoring stopped")

    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Check all endpoints
                await self._check_all_endpoints()

                # Update dashboard statistics
                await self._update_dashboard_stats()

                # Check alert rules
                await self._check_alert_rules()

                # Clean up old metrics
                await self._cleanup_old_metrics()

                # Sleep until next check
                await asyncio.sleep(self.monitoring_interval)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(10)  # Short sleep on error

    async def _check_all_endpoints(self):
        """Check health of all registered endpoints"""
        for endpoint in self.endpoints.values():
            try:
                await self._check_endpoint_health(endpoint)
            except Exception as e:
                logger.error(f"Error checking endpoint {endpoint.name}: {e}")
                endpoint.status = APIStatus.ERROR

    async def _check_endpoint_health(self, endpoint: APIEndpoint):
        """Check health of a specific endpoint"""
        start_time = time.time()

        try:
            # Simulate API health check (in real implementation, use aiohttp)
            await asyncio.sleep(0.1)  # Simulate network delay

            # Calculate response time
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

            # Update endpoint metrics
            endpoint.last_check = datetime.now()
            endpoint.response_time = response_time
            endpoint.total_requests += 1

            # Determine status based on response time
            if response_time < 200:
                endpoint.status = APIStatus.HEALTHY
            elif response_time < 500:
                endpoint.status = APIStatus.WARNING
            else:
                endpoint.status = APIStatus.ERROR
                endpoint.failed_requests += 1

            # Calculate success rate
            if endpoint.total_requests > 0:
                endpoint.success_rate = (
                    (endpoint.total_requests - endpoint.failed_requests)
                    / endpoint.total_requests
                ) * 100

            # Record metrics
            await self._record_metric(
                endpoint.id, MetricType.RESPONSE_TIME, response_time
            )
            await self._record_metric(endpoint.id, MetricType.REQUEST_COUNT, 1)

            logger.debug(
                f"Endpoint {endpoint.name} checked - Status: {endpoint.status.value}, Response Time: {response_time:.2f}ms"
            )

        except Exception as e:
            logger.error(f"Failed to check endpoint {endpoint.name}: {e}")
            endpoint.status = APIStatus.OFFLINE
            endpoint.failed_requests += 1

    async def _record_metric(
        self, endpoint_id: str, metric_type: MetricType, value: float
    ):
        """Record a metric data point"""
        metric = APIMetric(
            endpoint_id=endpoint_id,
            metric_type=metric_type,
            value=value,
            timestamp=datetime.now(),
        )

        metric_key = f"{endpoint_id}_{metric_type.value}"
        self.metrics[metric_key].append(metric)

    async def _update_dashboard_stats(self):
        """Update overall dashboard statistics"""
        total_requests = sum(
            endpoint.total_requests for endpoint in self.endpoints.values()
        )
        total_errors = sum(
            endpoint.failed_requests for endpoint in self.endpoints.values()
        )

        # Calculate average response time
        response_times = [
            endpoint.response_time
            for endpoint in self.endpoints.values()
            if endpoint.response_time > 0
        ]
        avg_response_time = (
            sum(response_times) / len(response_times) if response_times else 0.0
        )

        # Calculate uptime percentage
        healthy_endpoints = len(
            [
                e
                for e in self.endpoints.values()
                if e.status in [APIStatus.HEALTHY, APIStatus.WARNING]
            ]
        )
        total_endpoints = len(self.endpoints)
        uptime_percentage = (
            (healthy_endpoints / total_endpoints * 100)
            if total_endpoints > 0
            else 100.0
        )

        self.dashboard_stats.update(
            {
                "total_requests": total_requests,
                "total_errors": total_errors,
                "average_response_time": avg_response_time,
                "uptime_percentage": uptime_percentage,
                "last_updated": datetime.now(),
            }
        )

    async def _check_alert_rules(self):
        """Check all alert rules and trigger alerts if necessary"""
        for rule in self.alert_rules.values():
            if not rule.is_active:
                continue

            try:
                await self._evaluate_alert_rule(rule)
            except Exception as e:
                logger.error(f"Error evaluating alert rule {rule.name}: {e}")

    async def _evaluate_alert_rule(self, rule: AlertRule):
        """Evaluate a specific alert rule"""
        endpoint = self.endpoints.get(rule.endpoint_id)
        if not endpoint:
            return

        # Get current metric value
        current_value = self._get_current_metric_value(
            rule.endpoint_id, rule.metric_type
        )
        if current_value is None:
            return

        # Check if alert condition is met
        should_alert = False
        if rule.condition == "greater_than" and current_value > rule.threshold:
            should_alert = True
        elif rule.condition == "less_than" and current_value < rule.threshold:
            should_alert = True
        elif rule.condition == "equals" and current_value == rule.threshold:
            should_alert = True

        if should_alert:
            await self._trigger_alert(rule, current_value)

    def _get_current_metric_value(
        self, endpoint_id: str, metric_type: MetricType
    ) -> Optional[float]:
        """Get the current value for a specific metric"""
        if metric_type == MetricType.RESPONSE_TIME:
            endpoint = self.endpoints.get(endpoint_id)
            return endpoint.response_time if endpoint else None
        elif metric_type == MetricType.ERROR_RATE:
            endpoint = self.endpoints.get(endpoint_id)
            if endpoint and endpoint.total_requests > 0:
                return (endpoint.failed_requests / endpoint.total_requests) * 100
            return 0.0
        # Add more metric types as needed
        return None

    async def _trigger_alert(self, rule: AlertRule, current_value: float):
        """Trigger an alert based on a rule"""
        # Check if alert already exists for this rule
        existing_alert = next(
            (
                alert
                for alert in self.active_alerts.values()
                if alert.rule_id == rule.id and not alert.is_resolved
            ),
            None,
        )

        if existing_alert:
            return  # Alert already active

        # Create new alert
        alert = Alert(
            id=str(uuid.uuid4()),
            rule_id=rule.id,
            endpoint_id=rule.endpoint_id,
            message=f"Alert: {rule.name} - {rule.metric_type.value} is {current_value} (threshold: {rule.threshold})",
            severity="high" if current_value > rule.threshold * 2 else "medium",
            triggered_at=datetime.now(),
        )

        self.active_alerts[alert.id] = alert
        logger.warning(f"Alert triggered: {alert.message}")

    async def _cleanup_old_metrics(self):
        """Clean up metrics older than 24 hours"""
        cutoff_time = datetime.now() - timedelta(hours=24)

        for metric_key, metric_deque in self.metrics.items():
            # Remove old metrics
            while metric_deque and metric_deque[0].timestamp < cutoff_time:
                metric_deque.popleft()

    def add_endpoint(self, name: str, url: str, method: str = "GET") -> str:
        """Add a new API endpoint to monitor"""
        endpoint_id = str(uuid.uuid4())
        endpoint = APIEndpoint(
            id=endpoint_id,
            name=name,
            url=url,
            method=method.upper(),
            status=APIStatus.HEALTHY,
        )

        self.endpoints[endpoint_id] = endpoint
        logger.info(f"Added endpoint: {name} ({url})")
        return endpoint_id

    def remove_endpoint(self, endpoint_id: str) -> bool:
        """Remove an API endpoint from monitoring"""
        if endpoint_id in self.endpoints:
            endpoint = self.endpoints[endpoint_id]
            del self.endpoints[endpoint_id]

            # Clean up related metrics and alerts
            self._cleanup_endpoint_data(endpoint_id)

            logger.info(f"Removed endpoint: {endpoint.name}")
            return True
        return False

    def _cleanup_endpoint_data(self, endpoint_id: str):
        """Clean up all data related to an endpoint"""
        # Remove metrics
        keys_to_remove = [
            key for key in self.metrics.keys() if key.startswith(endpoint_id)
        ]
        for key in keys_to_remove:
            del self.metrics[key]

        # Remove alert rules
        rules_to_remove = [
            rule_id
            for rule_id, rule in self.alert_rules.items()
            if rule.endpoint_id == endpoint_id
        ]
        for rule_id in rules_to_remove:
            del self.alert_rules[rule_id]

        # Remove active alerts
        alerts_to_remove = [
            alert_id
            for alert_id, alert in self.active_alerts.items()
            if alert.endpoint_id == endpoint_id
        ]
        for alert_id in alerts_to_remove:
            del self.active_alerts[alert_id]

    def add_alert_rule(
        self,
        name: str,
        endpoint_id: str,
        metric_type: MetricType,
        threshold: float,
        condition: str = "greater_than",
    ) -> str:
        """Add a new alert rule"""
        rule_id = str(uuid.uuid4())
        rule = AlertRule(
            id=rule_id,
            name=name,
            endpoint_id=endpoint_id,
            metric_type=metric_type,
            threshold=threshold,
            condition=condition,
        )

        self.alert_rules[rule_id] = rule
        logger.info(f"Added alert rule: {name}")
        return rule_id

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an active alert"""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.is_resolved = True
            alert.resolved_at = datetime.now()
            logger.info(f"Alert resolved: {alert.message}")
            return True
        return False

    def get_endpoint(self, endpoint_id: str) -> Optional[APIEndpoint]:
        """Get an endpoint by ID"""
        return self.endpoints.get(endpoint_id)

    def get_all_endpoints(self) -> list[APIEndpoint]:
        """Get all monitored endpoints"""
        return list(self.endpoints.values())

    def get_endpoints_by_status(self, status: APIStatus) -> list[APIEndpoint]:
        """Get endpoints by status"""
        return [
            endpoint
            for endpoint in self.endpoints.values()
            if endpoint.status == status
        ]

    def get_dashboard_stats(self) -> dict[str, Any]:
        """Get overall dashboard statistics"""
        return self.dashboard_stats.copy()

    def get_active_alerts(self) -> list[Alert]:
        """Get all active alerts"""
        return [alert for alert in self.active_alerts.values() if not alert.is_resolved]

    def get_endpoint_metrics(
        self, endpoint_id: str, metric_type: MetricType, hours: int = 1
    ) -> list[APIMetric]:
        """Get metrics for an endpoint within a time range"""
        metric_key = f"{endpoint_id}_{metric_type.value}"
        if metric_key not in self.metrics:
            return []

        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [
            metric
            for metric in self.metrics[metric_key]
            if metric.timestamp >= cutoff_time
        ]

    def get_system_health(self) -> dict[str, Any]:
        """Get overall system health summary"""
        total_endpoints = len(self.endpoints)
        healthy_count = len(self.get_endpoints_by_status(APIStatus.HEALTHY))
        warning_count = len(self.get_endpoints_by_status(APIStatus.WARNING))
        error_count = len(self.get_endpoints_by_status(APIStatus.ERROR))
        offline_count = len(self.get_endpoints_by_status(APIStatus.OFFLINE))
        active_alerts_count = len(self.get_active_alerts())

        return {
            "total_endpoints": total_endpoints,
            "healthy_endpoints": healthy_count,
            "warning_endpoints": warning_count,
            "error_endpoints": error_count,
            "offline_endpoints": offline_count,
            "active_alerts": active_alerts_count,
            "overall_health": (
                "healthy" if error_count == 0 and offline_count == 0 else "degraded"
            ),
            "monitoring_active": self.is_monitoring,
            "last_check": (
                max(
                    [
                        e.last_check
                        for e in self.endpoints.values()
                        if e.last_check is not None
                    ],
                    default=None,
                )
                if self.endpoints
                else None
            ),
            "dashboard_stats": self.dashboard_stats,
        }


# Global instance
api_dashboard = APIMasterDashboard()


# Convenience functions
async def start_api_monitoring():
    """Start API monitoring"""
    await api_dashboard.start_monitoring()


async def stop_api_monitoring():
    """Stop API monitoring"""
    await api_dashboard.stop_monitoring()


def add_api_endpoint(name: str, url: str, method: str = "GET") -> str:
    """Add an API endpoint to monitor"""
    return api_dashboard.add_endpoint(name, url, method)


def get_system_health() -> dict[str, Any]:
    """Get system health summary"""
    return api_dashboard.get_system_health()


def get_dashboard_data() -> dict[str, Any]:
    """Get comprehensive dashboard data"""
    return {
        "endpoints": [
            asdict(endpoint) for endpoint in api_dashboard.get_all_endpoints()
        ],
        "stats": api_dashboard.get_dashboard_stats(),
        "alerts": [asdict(alert) for alert in api_dashboard.get_active_alerts()],
        "health": api_dashboard.get_system_health(),
    }


if __name__ == "__main__":
    # Example usage
    async def main():
        # Start monitoring
        await start_api_monitoring()

        # Add some example endpoints
        endpoint1 = add_api_endpoint("Main API", "https://api.example.com/health")
        endpoint2 = add_api_endpoint("User Service", "https://users.example.com/status")
        endpoint3 = add_api_endpoint("Payment API", "https://payments.example.com/ping")

        # Add alert rules
        api_dashboard.add_alert_rule(
            "High Response Time",
            endpoint1,
            MetricType.RESPONSE_TIME,
            500.0,
            "greater_than",
        )

        # Let it run for a bit
        await asyncio.sleep(10)

        # Check system health
        health = get_system_health()
        print(f"System Health: {json.dumps(health, indent=2, default=str)}")

        # Get dashboard data
        dashboard_data = get_dashboard_data()
        print(f"Dashboard Data: {json.dumps(dashboard_data, indent=2, default=str)}")

        await stop_api_monitoring()

    asyncio.run(main())
