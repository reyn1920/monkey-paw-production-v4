"""
Analytics Module - Comprehensive analytics and data processing system
"""

import asyncio

# json import removed as it was unused
import logging
from datetime import datetime, timedelta
from typing import Optional, Any, Union
from enum import Enum
import statistics
from collections import defaultdict, deque
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics that can be tracked"""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"
    RATE = "rate"


class AggregationType(Enum):
    """Types of data aggregation"""

    SUM = "sum"
    AVERAGE = "average"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    PERCENTILE = "percentile"


class TimeWindow(Enum):
    """Time windows for analytics"""

    MINUTE = "1m"
    FIVE_MINUTES = "5m"
    HOUR = "1h"
    DAY = "1d"
    WEEK = "1w"
    MONTH = "1M"


@dataclass
class DataPoint:
    """Individual data point"""

    timestamp: datetime
    value: Union[int, float]
    tags: dict[str, str]
    metric_name: str


@dataclass
class MetricSummary:
    """Summary statistics for a metric"""

    name: str
    count: int
    sum: float
    min: float
    max: float
    average: float
    median: float
    std_dev: float
    percentiles: dict[str, float]
    time_range: tuple[datetime, datetime]


@dataclass
class AnalyticsReport:
    """Analytics report structure"""

    id: str
    title: str
    description: str
    generated_at: datetime
    time_range: tuple[datetime, datetime]
    metrics: list[MetricSummary]
    insights: list[str]
    recommendations: list[str]
    data: dict[str, Any]


class MetricStore:
    """In-memory metric storage with time-based retention"""

    def __init__(self, retention_hours: int = 24):
        self.data: dict[str, deque[DataPoint]] = defaultdict(
            lambda: deque(maxlen=10000)
        )
        self.retention_hours = retention_hours
        self.last_cleanup = datetime.now()

    def add_point(
        self,
        metric_name: str,
        value: Union[int, float],
        tags: Optional[dict[str, str]] = None,
        timestamp: Optional[datetime] = None,
    ):
        """Add a data point to the store"""
        if timestamp is None:
            timestamp = datetime.now()

        if tags is None:
            tags = {}

        point = DataPoint(
            timestamp=timestamp, value=value, tags=tags, metric_name=metric_name
        )

        self.data[metric_name].append(point)

        # Periodic cleanup
        if (datetime.now() - self.last_cleanup).total_seconds() > 3600:  # Every hour
            self._cleanup_old_data()

    def get_points(
        self,
        metric_name: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        tags: Optional[dict[str, str]] = None,
    ) -> list[DataPoint]:
        """Retrieve data points with optional filtering"""
        if metric_name not in self.data:
            return []

        points = list(self.data[metric_name])

        # Time filtering
        if start_time:
            points = [p for p in points if p.timestamp >= start_time]
        if end_time:
            points = [p for p in points if p.timestamp <= end_time]

        # Tag filtering
        if tags:
            points = [
                p for p in points if all(p.tags.get(k) == v for k, v in tags.items())
            ]

        return points

    def get_metric_names(self) -> list[str]:
        """Get all metric names"""
        return list(self.data.keys())

    def _cleanup_old_data(self):
        """Remove old data points beyond retention period"""
        cutoff_time = datetime.now() - timedelta(hours=self.retention_hours)

        for metric_name in self.data:
            # Remove old points
            while (
                self.data[metric_name]
                and self.data[metric_name][0].timestamp < cutoff_time
            ):
                self.data[metric_name].popleft()

        self.last_cleanup = datetime.now()
        logger.info("Completed data cleanup")


class AnalyticsProcessor:
    """Processes analytics data and generates insights"""

    def __init__(self, metric_store: MetricStore):
        self.metric_store = metric_store

    def calculate_summary(
        self,
        metric_name: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        tags: Optional[dict[str, str]] = None,
    ) -> Optional[MetricSummary]:
        """Calculate summary statistics for a metric"""
        points = self.metric_store.get_points(metric_name, start_time, end_time, tags)

        if not points:
            return None

        values = [p.value for p in points]

        try:
            summary = MetricSummary(
                name=metric_name,
                count=len(values),
                sum=sum(values),
                min=min(values),
                max=max(values),
                average=statistics.mean(values),
                median=statistics.median(values),
                std_dev=statistics.stdev(values) if len(values) > 1 else 0.0,
                percentiles={
                    "p50": statistics.median(values),
                    "p90": self._percentile(values, 0.9),
                    "p95": self._percentile(values, 0.95),
                    "p99": self._percentile(values, 0.99),
                },
                time_range=(
                    (points[0].timestamp, points[-1].timestamp)
                    if points
                    else (datetime.now(), datetime.now())
                ),
            )

            return summary

        except Exception as e:
            logger.error(f"Failed to calculate summary for {metric_name}: {e}")
            return None

    def _percentile(self, values: list[float], percentile: float) -> float:
        """Calculate percentile value"""
        if not values:
            return 0.0

        sorted_values = sorted(values)
        index = int(percentile * (len(sorted_values) - 1))
        return sorted_values[index]

    def detect_anomalies(
        self, metric_name: str, window_minutes: int = 60, threshold_std: float = 2.0
    ) -> list[DataPoint]:
        """Detect anomalies in metric data"""
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=window_minutes)

        points = self.metric_store.get_points(metric_name, start_time, end_time)

        if len(points) < 10:  # Need minimum data points
            return []

        values = [p.value for p in points]
        mean_val = statistics.mean(values)
        std_val = statistics.stdev(values) if len(values) > 1 else 0

        anomalies = []
        for point in points:
            if abs(point.value - mean_val) > threshold_std * std_val:
                anomalies.append(point)

        return anomalies

    def calculate_trend(
        self, metric_name: str, window_minutes: int = 60
    ) -> Optional[dict[str, Any]]:
        """Calculate trend information for a metric"""
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=window_minutes)

        points = self.metric_store.get_points(metric_name, start_time, end_time)

        if len(points) < 2:
            return None

        # Simple linear trend calculation
        values = [p.value for p in points]
        n = len(values)

        # Calculate slope using least squares
        x_values = list(range(n))
        x_mean = sum(x_values) / n
        y_mean = sum(values) / n

        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)

        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator

        # Determine trend direction
        if slope > 0.1:
            direction = "increasing"
        elif slope < -0.1:
            direction = "decreasing"
        else:
            direction = "stable"

        return {
            "slope": slope,
            "direction": direction,
            # Simple confidence metric
            "confidence": min(abs(slope) * 10, 1.0),
            "data_points": n,
            "time_window": window_minutes,
        }


class ReportGenerator:
    """Generates analytics reports"""

    def __init__(self, processor: AnalyticsProcessor):
        self.processor = processor

    async def generate_report(
        self,
        metric_names: list[str],
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        title: str = "Analytics Report",
    ) -> AnalyticsReport:
        """Generate comprehensive analytics report"""
        if end_time is None:
            end_time = datetime.now()
        if start_time is None:
            start_time = end_time - timedelta(hours=1)

        report_id = hashlib.md5(
            f"{title}_{start_time}_{end_time}".encode()
        ).hexdigest()[:8]

        # Calculate summaries for all metrics
        summaries = []
        insights = []
        recommendations = []

        for metric_name in metric_names:
            summary = self.processor.calculate_summary(
                metric_name, start_time, end_time
            )
            if summary:
                summaries.append(summary)

                # Generate insights
                metric_insights = await self._generate_metric_insights(summary)
                insights.extend(metric_insights)

                # Generate recommendations
                metric_recommendations = await self._generate_recommendations(summary)
                recommendations.extend(metric_recommendations)

        # Generate overall insights
        overall_insights = await self._generate_overall_insights(summaries)
        insights.extend(overall_insights)

        report = AnalyticsReport(
            id=report_id,
            title=title,
            description=f"Analytics report for {
                len(metric_names)} metrics from {start_time} to {end_time}",
            generated_at=datetime.now(),
            time_range=(start_time, end_time),
            metrics=summaries,
            insights=insights,
            recommendations=recommendations,
            data={
                "total_metrics": len(summaries),
                "total_data_points": sum(s.count for s in summaries),
                "report_generation_time": datetime.now(),
            },
        )

        return report

    async def _generate_metric_insights(self, summary: MetricSummary) -> list[str]:
        """Generate insights for a specific metric"""
        insights = []

        # High variability insight
        if summary.std_dev > summary.average * 0.5:
            insights.append(
                f"{summary.name} shows high variability (std dev: {summary.std_dev:.2f})"
            )

        # Extreme values insight
        if summary.max > summary.average * 3:
            insights.append(
                f"{summary.name} has extreme high values (max: {summary.max:.2f})"
            )

        # Data volume insight
        if summary.count < 10:
            insights.append(f"{summary.name} has limited data points ({summary.count})")

        return insights

    async def _generate_recommendations(self, summary: MetricSummary) -> list[str]:
        """Generate recommendations for a specific metric"""
        recommendations = []

        # High variability recommendation
        if summary.std_dev > summary.average * 0.5:
            recommendations.append(
                f"Investigate causes of high variability in {summary.name}"
            )

        # Data collection recommendation
        if summary.count < 50:
            recommendations.append(
                f"Increase data collection frequency for {summary.name}"
            )

        return recommendations

    async def _generate_overall_insights(
        self, summaries: list[MetricSummary]
    ) -> list[str]:
        """Generate overall insights across all metrics"""
        insights = []

        if not summaries:
            return ["No metric data available for analysis"]

        # Overall data quality
        total_points = sum(s.count for s in summaries)
        avg_points_per_metric = total_points / len(summaries)

        if avg_points_per_metric < 20:
            insights.append(
                "Overall data collection appears sparse - consider increasing frequency"
            )

        # Metric correlation (simplified)
        high_var_metrics = [s.name for s in summaries if s.std_dev > s.average * 0.3]
        if len(high_var_metrics) > len(summaries) * 0.5:
            insights.append(
                "Multiple metrics show high variability - system may be unstable"
            )

        return insights


class AnalyticsEngine:
    """Main analytics engine that coordinates all components"""

    def __init__(self, retention_hours: int = 24):
        self.metric_store = MetricStore(retention_hours)
        self.processor = AnalyticsProcessor(self.metric_store)
        self.report_generator = ReportGenerator(self.processor)
        self.is_running = False

    async def start(self):
        """Start the analytics engine"""
        self.is_running = True
        logger.info("Analytics engine started")

        # Start background tasks
        asyncio.create_task(self._periodic_cleanup())

    async def stop(self):
        """Stop the analytics engine"""
        self.is_running = False
        logger.info("Analytics engine stopped")

    def record_metric(
        self, name: str, value: Union[int, float], tags: Optional[dict[str, str]] = None
    ):
        """Record a metric value"""
        self.metric_store.add_point(name, value, tags)

    def increment_counter(self, name: str, tags: Optional[dict[str, str]] = None):
        """Increment a counter metric"""
        self.record_metric(f"{name}_count", 1, tags)

    def record_timer(
        self, name: str, duration_ms: float, tags: Optional[dict[str, str]] = None
    ):
        """Record a timer metric"""
        self.record_metric(f"{name}_duration", duration_ms, tags)

    async def get_metric_summary(
        self, name: str, hours_back: int = 1
    ) -> Optional[MetricSummary]:
        """Get summary for a specific metric"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours_back)
        return self.processor.calculate_summary(name, start_time, end_time)

    async def detect_anomalies(
        self, name: str, window_minutes: int = 60
    ) -> list[DataPoint]:
        """Detect anomalies in a metric"""
        return self.processor.detect_anomalies(name, window_minutes)

    async def generate_report(
        self, metric_names: Optional[list[str]] = None, hours_back: int = 1
    ) -> AnalyticsReport:
        """Generate analytics report"""
        if metric_names is None:
            metric_names = self.metric_store.get_metric_names()

        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours_back)

        return await self.report_generator.generate_report(
            metric_names, start_time, end_time
        )

    async def _periodic_cleanup(self):
        """Periodic cleanup task"""
        while self.is_running:
            try:
                await asyncio.sleep(3600)  # Run every hour
                self.metric_store._cleanup_old_data()
            except Exception as e:
                logger.error(f"Error in periodic cleanup: {e}")


# Global analytics engine instance
analytics_engine = AnalyticsEngine()


async def main():
    """Main function for testing"""
    engine = AnalyticsEngine()
    await engine.start()

    # Simulate some metrics
    for i in range(100):
        engine.record_metric("cpu_usage", 50 + (i % 30))
        engine.record_metric("memory_usage", 60 + (i % 20))
        engine.increment_counter("requests")
        engine.record_timer("response_time", 100 + (i % 50))

        await asyncio.sleep(0.1)

    # Generate report
    report = await engine.generate_report()

    print(f"Generated report: {report.title}")
    print(f"Metrics analyzed: {len(report.metrics)}")
    print(f"Insights: {len(report.insights)}")
    print(f"Recommendations: {len(report.recommendations)}")

    # Check for anomalies
    anomalies = await engine.detect_anomalies("cpu_usage")
    print(f"Detected {len(anomalies)} anomalies in CPU usage")

    await engine.stop()


if __name__ == "__main__":
    asyncio.run(main())
