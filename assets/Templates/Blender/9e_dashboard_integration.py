"""
Dashboard Integration system for connecting multiple dashboard components.
Provides unified interface for dashboard data aggregation and visualization.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from enum import Enum
from abc import ABC, abstractmethod
from typing import Any
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DashboardType(Enum):
    """Types of dashboards that can be integrated."""

    ANALYTICS = "analytics"
    MONITORING = "monitoring"
    QUALITY = "quality"
    AI_INSIGHTS = "ai_insights"
    METRICS = "metrics"
    SECURITY = "security"
    PERFORMANCE = "performance"


class WidgetType(Enum):
    """Types of dashboard widgets."""

    CHART = "chart"
    TABLE = "table"
    METRIC = "metric"
    GAUGE = "gauge"
    MAP = "map"
    TEXT = "text"
    ALERT = "alert"
    TIMELINE = "timeline"


class DataSourceType(Enum):
    """Types of data sources."""

    DATABASE = "database"
    API = "api"
    FILE = "file"
    STREAM = "stream"
    CACHE = "cache"
    EXTERNAL = "external"


class RefreshMode(Enum):
    """Data refresh modes."""

    REAL_TIME = "real_time"
    SCHEDULED = "scheduled"
    ON_DEMAND = "on_demand"
    EVENT_DRIVEN = "event_driven"


@dataclass
class DataPoint:
    """Individual data point for dashboard widgets."""

    timestamp: datetime
    value: Any
    label: str
    metadata: Optional[dict[str, Any]] = None


@dataclass
class WidgetConfig:
    """Configuration for dashboard widgets."""

    widget_id: str
    widget_type: WidgetType
    title: str
    data_source: str
    refresh_mode: RefreshMode
    refresh_interval: int = 60  # seconds
    position: tuple[int, int] = (0, 0)
    size: tuple[int, int] = (1, 1)
    config: Optional[dict[str, Any]] = None


@dataclass
class DashboardConfig:
    """Configuration for a dashboard."""

    dashboard_id: str
    dashboard_type: DashboardType
    title: str
    description: str
    widgets: list[WidgetConfig]
    layout: Optional[dict[str, Any]] = None
    permissions: Optional[list[str]] = None


@dataclass
class DataSourceConfig:
    """Configuration for data sources."""

    source_id: str
    source_type: DataSourceType
    connection_string: str
    credentials: Optional[dict[str, str]] = None
    query_config: Optional[dict[str, Any]] = None
    cache_ttl: int = 300  # seconds


class DataSource(ABC):
    """Abstract base class for data sources."""

    def __init__(self, config: DataSourceConfig):
        self.config = config
        self.last_update = datetime.now()
        self.cache: dict[str, Any] = {}

    @abstractmethod
    async def fetch_data(
        self, query: str, params: dict[str, Any] = None
    ) -> list[DataPoint]:
        """Fetch data from the source."""

    @abstractmethod
    async def test_connection(self) -> bool:
        """Test if the data source is accessible."""


class APIDataSource(DataSource):
    """Data source for REST APIs."""

    async def fetch_data(
        self, query: str, params: dict[str, Any] = None
    ) -> list[DataPoint]:
        """Fetch data from API endpoint."""
        try:
            # Simulate API call
            data_points = []
            for i in range(10):
                data_points.append(
                    DataPoint(
                        timestamp=datetime.now() - timedelta(minutes=i),
                        value=100 - i * 5,
                        label=f"API Data {i}",
                        metadata={"source": "api", "query": query},
                    )
                )
            return data_points
        except Exception as e:
            logger.error(f"API data fetch failed: {e}")
            return []

    async def test_connection(self) -> bool:
        """Test API connection."""
        try:
            # Simulate connection test
            return True
        except Exception:
            return False


class DatabaseDataSource(DataSource):
    """Data source for databases."""

    async def fetch_data(
        self, query: str, params: dict[str, Any] = None
    ) -> list[DataPoint]:
        """Fetch data from database."""
        try:
            # Simulate database query
            data_points = []
            for i in range(20):
                data_points.append(
                    DataPoint(
                        timestamp=datetime.now() - timedelta(hours=i),
                        value=50 + i * 2,
                        label=f"DB Record {i}",
                        metadata={"source": "database", "table": "metrics"},
                    )
                )
            return data_points
        except Exception as e:
            logger.error(f"Database data fetch failed: {e}")
            return []

    async def test_connection(self) -> bool:
        """Test database connection."""
        try:
            # Simulate connection test
            return True
        except Exception:
            return False


class Widget:
    """Dashboard widget implementation."""

    def __init__(self, config: WidgetConfig, data_source: DataSource):
        self.config = config
        self.data_source = data_source
        self.data: list[DataPoint] = []
        self.last_refresh = datetime.now()
        self.refresh_task: Optional[asyncio.Task[None]] = None

    async def refresh_data(self):
        """Refresh widget data from data source."""
        try:
            query = self.config.config.get("query", "") if self.config.config else ""
            params = self.config.config.get("params", {}) if self.config.config else {}

            self.data = await self.data_source.fetch_data(query, params)
            self.last_refresh = datetime.now()

            logger.info(
                f"Widget {self.config.widget_id} refreshed with {len(self.data)} data points"
            )
        except Exception as e:
            logger.error(f"Widget refresh failed for {self.config.widget_id}: {e}")

    async def start_auto_refresh(self):
        """Start automatic data refresh."""
        if self.config.refresh_mode == RefreshMode.SCHEDULED:

            async def refresh_loop():
                while True:
                    await self.refresh_data()
                    await asyncio.sleep(self.config.refresh_interval)

            self.refresh_task = asyncio.create_task(refresh_loop())

    async def stop_auto_refresh(self):
        """Stop automatic data refresh."""
        if self.refresh_task:
            self.refresh_task.cancel()
            try:
                await self.refresh_task
            except asyncio.CancelledError:
                pass

    def get_data(self) -> list[DataPoint]:
        """Get current widget data."""
        return self.data

    def get_summary(self) -> dict[str, Any]:
        """Get widget data summary."""
        if not self.data:
            return {"count": 0, "latest": None, "average": 0}

        numeric_values = [
            dp.value for dp in self.data if isinstance(dp.value, (int, float))
        ]

        return {
            "count": len(self.data),
            "latest": self.data[0].value if self.data else None,
            "average": (
                sum(numeric_values) / len(numeric_values) if numeric_values else 0
            ),
            "last_refresh": self.last_refresh.isoformat(),
        }


class Dashboard:
    """Dashboard implementation."""

    def __init__(self, config: DashboardConfig):
        self.config = config
        self.widgets: dict[str, Widget] = {}
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()

    def add_widget(self, widget: Widget):
        """Add a widget to the dashboard."""
        self.widgets[widget.config.widget_id] = widget
        logger.info(
            f"Added widget {widget.config.widget_id} to dashboard {self.config.dashboard_id}"
        )

    def remove_widget(self, widget_id: str) -> bool:
        """Remove a widget from the dashboard."""
        if widget_id in self.widgets:
            del self.widgets[widget_id]
            logger.info(
                f"Removed widget {widget_id} from dashboard {self.config.dashboard_id}"
            )
            return True
        return False

    async def refresh_all_widgets(self):
        """Refresh all widgets in the dashboard."""
        tasks = []
        for widget in self.widgets.values():
            tasks.append(widget.refresh_data())

        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info(f"Refreshed all widgets in dashboard {self.config.dashboard_id}")

    async def start_auto_refresh(self):
        """Start auto-refresh for all widgets."""
        for widget in self.widgets.values():
            await widget.start_auto_refresh()

    async def stop_auto_refresh(self):
        """Stop auto-refresh for all widgets."""
        for widget in self.widgets.values():
            await widget.stop_auto_refresh()

    def get_layout(self) -> dict[str, Any]:
        """Get dashboard layout information."""
        layout = {
            "dashboard_id": self.config.dashboard_id,
            "title": self.config.title,
            "type": self.config.dashboard_type.value,
            "widgets": [],
        }

        for widget in self.widgets.values():
            widget_info = {
                "widget_id": widget.config.widget_id,
                "type": widget.config.widget_type.value,
                "title": widget.config.title,
                "position": widget.config.position,
                "size": widget.config.size,
                "summary": widget.get_summary(),
            }
            layout["widgets"].append(widget_info)

        return layout


class DashboardIntegration:
    """Main dashboard integration system."""

    def __init__(self):
        self.dashboards: dict[str, Dashboard] = {}
        self.data_sources: dict[str, DataSource] = {}
        self.widget_templates: dict[str, WidgetConfig] = {}
        self.running = False

    def register_data_source(self, config: DataSourceConfig) -> bool:
        """Register a new data source."""
        try:
            if config.source_type == DataSourceType.API:
                data_source = APIDataSource(config)
            elif config.source_type == DataSourceType.DATABASE:
                data_source = DatabaseDataSource(config)
            else:
                # Default to API source
                data_source = APIDataSource(config)

            self.data_sources[config.source_id] = data_source
            logger.info(f"Registered data source: {config.source_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to register data source {config.source_id}: {e}")
            return False

    async def create_dashboard(self, config: DashboardConfig) -> Optional[Dashboard]:
        """Create a new dashboard."""
        try:
            dashboard = Dashboard(config)

            # Create widgets for the dashboard
            for widget_config in config.widgets:
                data_source = self.data_sources.get(widget_config.data_source)
                if data_source:
                    widget = Widget(widget_config, data_source)
                    dashboard.add_widget(widget)
                else:
                    logger.warning(
                        f"Data source not found for widget: {widget_config.widget_id}"
                    )

            self.dashboards[config.dashboard_id] = dashboard
            logger.info(f"Created dashboard: {config.dashboard_id}")
            return dashboard
        except Exception as e:
            logger.error(f"Failed to create dashboard {config.dashboard_id}: {e}")
            return None

    def get_dashboard(self, dashboard_id: str) -> Optional[Dashboard]:
        """Get a dashboard by ID."""
        dashboard = self.dashboards.get(dashboard_id)
        if dashboard:
            dashboard.last_accessed = datetime.now()
        return dashboard

    async def refresh_dashboard(self, dashboard_id: str) -> bool:
        """Refresh all widgets in a dashboard."""
        dashboard = self.get_dashboard(dashboard_id)
        if dashboard:
            await dashboard.refresh_all_widgets()
            return True
        return False

    async def start_all_dashboards(self):
        """Start auto-refresh for all dashboards."""
        self.running = True
        for dashboard in self.dashboards.values():
            await dashboard.start_auto_refresh()
        logger.info("Started all dashboard auto-refresh")

    async def stop_all_dashboards(self):
        """Stop auto-refresh for all dashboards."""
        self.running = False
        for dashboard in self.dashboards.values():
            await dashboard.stop_auto_refresh()
        logger.info("Stopped all dashboard auto-refresh")

    def get_dashboard_list(self) -> list[dict[str, Any]]:
        """Get list of all dashboards."""
        dashboard_list = []
        for dashboard in self.dashboards.values():
            dashboard_info = {
                "dashboard_id": dashboard.config.dashboard_id,
                "title": dashboard.config.title,
                "type": dashboard.config.dashboard_type.value,
                "widget_count": len(dashboard.widgets),
                "created_at": dashboard.created_at.isoformat(),
                "last_accessed": dashboard.last_accessed.isoformat(),
            }
            dashboard_list.append(dashboard_info)
        return dashboard_list

    async def test_all_data_sources(self) -> dict[str, bool]:
        """Test connectivity to all data sources."""
        results = {}
        for source_id, data_source in self.data_sources.items():
            results[source_id] = await data_source.test_connection()
        return results

    def create_widget_template(self, template_id: str, config: WidgetConfig):
        """Create a reusable widget template."""
        self.widget_templates[template_id] = config
        logger.info(f"Created widget template: {template_id}")

    def get_widget_template(self, template_id: str) -> Optional[WidgetConfig]:
        """Get a widget template by ID."""
        return self.widget_templates.get(template_id)


# Global dashboard integration instance
dashboard_integration = DashboardIntegration()


async def main():
    """Example usage of the dashboard integration system."""
    # Register data sources
    api_source = DataSourceConfig(
        source_id="metrics_api",
        source_type=DataSourceType.API,
        connection_string="http://localhost:8001/api/metrics",
    )

    db_source = DataSourceConfig(
        source_id="analytics_db",
        source_type=DataSourceType.DATABASE,
        connection_string="postgresql://localhost:5432/analytics",
    )

    dashboard_integration.register_data_source(api_source)
    dashboard_integration.register_data_source(db_source)

    # Create widget configurations
    cpu_widget = WidgetConfig(
        widget_id="cpu_usage",
        widget_type=WidgetType.GAUGE,
        title="CPU Usage",
        data_source="metrics_api",
        refresh_mode=RefreshMode.SCHEDULED,
        refresh_interval=30,
        position=(0, 0),
        size=(2, 1),
        config={"query": "cpu_usage", "max_value": 100},
    )

    memory_widget = WidgetConfig(
        widget_id="memory_usage",
        widget_type=WidgetType.CHART,
        title="Memory Usage",
        data_source="analytics_db",
        refresh_mode=RefreshMode.SCHEDULED,
        refresh_interval=60,
        position=(2, 0),
        size=(2, 2),
        config={"query": "SELECT * FROM memory_metrics", "chart_type": "line"},
    )

    # Create dashboard
    dashboard_config = DashboardConfig(
        dashboard_id="system_monitoring",
        dashboard_type=DashboardType.MONITORING,
        title="System Monitoring Dashboard",
        description="Real-time system performance monitoring",
        widgets=[cpu_widget, memory_widget],
    )

    dashboard = await dashboard_integration.create_dashboard(dashboard_config)
    if dashboard:
        print(f"Created dashboard: {dashboard.config.title}")

        # Refresh dashboard data
        await dashboard_integration.refresh_dashboard("system_monitoring")

        # Get dashboard layout
        layout = dashboard.get_layout()
        print(f"Dashboard layout: {json.dumps(layout, indent=2)}")

        # Test data sources
        test_results = await dashboard_integration.test_all_data_sources()
        print(f"Data source tests: {test_results}")

        # Start auto-refresh
        await dashboard_integration.start_all_dashboards()

        # Simulate running for a short time
        await asyncio.sleep(5)

        # Stop auto-refresh
        await dashboard_integration.stop_all_dashboards()


if __name__ == "__main__":
    asyncio.run(main())
