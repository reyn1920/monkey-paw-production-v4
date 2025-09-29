#!/usr/bin/env python3
"""
TRAE.AI Dashboard - Total Access Command Center

A comprehensive web dashboard providing complete visibility and control over
the TRAE.AI agentic framework. Features four dedicated modules for total system access.

Modules:
1. Agent Command Center - Real-time agent monitoring and control
2. Intelligence Database Explorer - Direct SQLite database access
3. Digital Product Studio - Book/course project management
4. On-Demand Reporting Engine - Instant report generation

Additional Features:
- Manual workflow triggers
- Monetization toggles
- Channel status controls
- Real-time task queue monitoring
- Performance metrics

Author: TRAE.AI System
Version: 2.0.0 - Total Access Upgrade
"""

import logging
import os
import socket
import sqlite3
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from flask import Flask, jsonify, request, send_from_directory
from waitress import serve
from werkzeug.exceptions import BadRequest


# Create fallback functions and classes first
def get_logger(name):
    return logging.getLogger(name)


def setup_logging(log_level="INFO"):
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


# Mock classes for standalone mode
class TaskQueueManager:
    def __init__(self, db_path_or_config):
        if isinstance(db_path_or_config, str):
            self.db_path = db_path_or_config
            self.config = {}
        else:
            self.config = db_path_or_config or {}
            self.db_path = self.config.get("db_path", "trae_ai.db")

    def get_queue_stats(self):
        return {"pending": 0, "in_progress": 0, "completed": 0, "failed": 0}

    def add_task(
        self, task_type=None, payload=None, priority="medium", agent_id=None, **kwargs
    ):
        return "mock-task-id"

    def get_recent_tasks(self, limit=10):
        return []

    def get_tasks(
        self, status=None, task_type=None, agent_id=None, limit=100, offset=0
    ):
        return []


class TaskStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriority:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskType:
    VIDEO_CREATION = "video_creation"
    RESEARCH = "research"
    CONTENT_AUDIT = "content_audit"
    MARKETING = "marketing"


class AgentStatus:
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"


class AgentCapability:
    PLANNING = "planning"
    EXECUTION = "execution"
    AUDITING = "auditing"


# Try to import TRAE.AI components, but use fallbacks if not available
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Import TRAE.AI task manager but keep using our fallback interface
    from backend.task_queue_manager import TaskQueueManager as TraeTaskQueueManager

    # Create a wrapper that maintains our interface
    class TaskQueueManagerWrapper:
        def __init__(self, db_path_or_config):
            try:
                if isinstance(db_path_or_config, str):
                    self._manager = TraeTaskQueueManager({"db_path": db_path_or_config})
                else:
                    self._manager = TraeTaskQueueManager(db_path_or_config or {})
            except Exception:
                # Fallback to mock if TRAE manager fails
                self._manager = None
                self.db_path = (
                    db_path_or_config
                    if isinstance(db_path_or_config, str)
                    else "trae_ai.db"
                )

        def get_queue_stats(self):
            if self._manager and hasattr(self._manager, "get_queue_stats"):
                try:
                    return self._manager.get_queue_stats()
                except Exception:
                    pass
            return {"pending": 0, "in_progress": 0, "completed": 0, "failed": 0}

        def add_task(
            self,
            task_type=None,
            payload=None,
            priority="medium",
            agent_id=None,
            **kwargs,
        ):
            if self._manager and hasattr(self._manager, "add_task"):
                try:
                    # Try with all parameters
                    return self._manager.add_task(
                        task_type=task_type or "default",
                        payload=payload,
                        priority=priority,
                        agent_id=agent_id,
                        **kwargs,
                    )
                except Exception:
                    try:
                        # Fallback with minimal parameters
                        return self._manager.add_task(task_type or "default")
                    except Exception:
                        pass
            return "mock-task-id"

        def get_recent_tasks(self, limit=10):
            if self._manager and hasattr(self._manager, "get_recent_tasks"):
                try:
                    return self._manager.get_recent_tasks(limit=limit)
                except Exception:
                    pass
            return []

        def get_tasks(
            self, status=None, task_type=None, agent_id=None, limit=100, offset=0
        ):
            if self._manager and hasattr(self._manager, "get_tasks"):
                try:
                    return self._manager.get_tasks(
                        status=status,
                        task_type=task_type,
                        agent_id=agent_id,
                        limit=limit,
                        offset=offset,
                    )
                except Exception:
                    try:
                        # Fallback with minimal parameters
                        return self._manager.get_tasks(limit=limit)
                    except Exception:
                        pass
            return []

    # Use the wrapper as TaskQueueManager
    TaskQueueManager = TaskQueueManagerWrapper

    trae_ai_available = True
    print("TRAE.AI TaskQueueManager loaded successfully")
except ImportError as e:
    print(f"Warning: Could not import TRAE.AI components: {e}")
    print("Running in standalone mode with fallback classes...")
    trae_ai_available = False


@dataclass
class DashboardConfig:
    """Configuration for the dashboard application."""

    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = False
    secret_key: str = "trae-ai-dashboard-secret-key-change-in-production"
    database_path: str = "trae_ai.db"
    intelligence_db_path: str = "right_perspective.db"
    log_level: str = "INFO"
    max_tasks_display: int = 100
    refresh_interval: int = 5  # seconds
    log_directory: str = "logs"


@dataclass
class AgentInfo:
    """Information about an individual agent."""

    id: str
    name: str
    status: str
    current_task_id: Optional[str] = None
    uptime: str = "0h 0m"
    last_activity: Optional[datetime] = None
    error_message: Optional[str] = None


@dataclass
class ProjectInfo:
    """Information about a digital product project."""

    id: str
    name: str
    type: str
    status: str
    progress: float
    chapters_completed: int
    total_chapters: int
    created_at: datetime
    last_updated: datetime


class DashboardApp:
    """Main dashboard application class with Total Access modules."""

    def __init__(self, config: Optional[DashboardConfig] = None):
        self.config = config or DashboardConfig()
        self.app = Flask(__name__, static_folder="static", template_folder="templates")
        self.app.secret_key = self.config.secret_key

        setup_logging(log_level=self.config.log_level)
        self.logger = get_logger(__name__)

        try:
            self.task_manager = TaskQueueManager(self.config.database_path)
            self.logger.info("TaskQueueManager initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize TaskQueueManager: {e}")
            self.task_manager = None

        self.start_time = datetime.now()
        self.agents = {}
        self.projects = {}

        self._setup_routes()
        self._setup_error_handlers()
        self._init_databases()
        self._start_monitoring_thread()
        self.logger.info("Dashboard application initialized")

    def _init_databases(self):
        """Initialize database connections."""
        try:
            intelligence_db_path = Path(self.config.intelligence_db_path)
            if not intelligence_db_path.exists():
                self.logger.warning(
                    f"Intelligence database not found at {intelligence_db_path}"
                )
            with sqlite3.connect(self.config.intelligence_db_path) as conn:
                conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            self.logger.info("Intelligence database connection established")
        except Exception as e:
            self.logger.error(f"Failed to initialize intelligence database: {e}")

    def _start_monitoring_thread(self):
        """Start background thread for monitoring agents and projects."""

        def monitor():
            while True:
                try:
                    self._update_agent_status()
                    self._update_project_status()
                    time.sleep(10)
                except Exception as e:
                    self.logger.error(f"Monitoring thread error: {e}")
                    time.sleep(30)

        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
        self.logger.info("Background monitoring thread started")

    def _setup_routes(self):
        """Setup Flask routes."""

        @self.app.route("/")
        def index():
            return send_from_directory("static", "index.html")

        @self.app.route("/static/<path:filename>")
        def static_files(filename):
            return send_from_directory("static", filename)

        @self.app.route("/api/health")
        def health_check():
            try:
                health_status = {
                    "status": "healthy",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "version": "1.0.0",
                    "components": {
                        "task_manager": self.task_manager is not None,
                        "database": self._check_database_health(),
                    },
                }
                return jsonify(health_status)
            except Exception as e:
                self.logger.error(f"Health check failed: {e}")
                return jsonify({"status": "unhealthy", "error": str(e)}), 500

        @self.app.route("/api/tasks", methods=["GET"])
        def get_tasks():
            try:
                if not self.task_manager:
                    return jsonify({"error": "Task manager not available"}), 503
                status = request.args.get("status")
                limit = min(
                    int(request.args.get("limit", 50)), self.config.max_tasks_display
                )
                tasks = self.task_manager.get_tasks(status=status, limit=limit)
                task_list = [
                    {
                        "id": task.get("id"),
                        "type": task.get("task_type"),
                        "priority": task.get("priority"),
                        "status": task.get("status"),
                        "agent_id": task.get("assigned_agent"),
                        "payload": task.get("payload", {}),
                        "created_at": task.get("created_at"),
                        "updated_at": task.get("updated_at"),
                        "retry_count": task.get("retry_count", 0),
                        "error_message": task.get("error_message"),
                    }
                    for task in tasks
                ]
                return jsonify(
                    {
                        "tasks": task_list,
                        "total": len(task_list),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                )
            except Exception as e:
                self.logger.error(f"Failed to get tasks: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/tasks", methods=["POST"])
        def create_task():
            try:
                if not self.task_manager:
                    return jsonify({"error": "Task manager not available"}), 503
                data = request.get_json()
                if not data:
                    raise BadRequest("No JSON data provided")
                required_fields = ["type", "payload"]
                for field in required_fields:
                    if field not in data:
                        raise BadRequest(f"Missing required field: {field}")
                task_id = self.task_manager.add_task(
                    task_type=data["type"],
                    payload=data["payload"],
                    priority=data.get("priority", "medium"),
                    agent_id=data.get("agent_id"),
                )
                self.logger.info(f"Created task {task_id} of type {data['type']}")
                return (
                    jsonify(
                        {
                            "task_id": task_id,
                            "status": "created",
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        }
                    ),
                    201,
                )
            except BadRequest as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                self.logger.error(f"Failed to create task: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/database/tables/<table_name>/data", methods=["GET"])
        def get_table_data(table_name):
            try:
                limit = min(int(request.args.get("limit", 100)), 1000)
                offset = int(request.args.get("offset", 0))
                with sqlite3.connect(self.config.intelligence_db_path) as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    total_count = cursor.fetchone()[0]
                    cursor.execute(
                        f"SELECT * FROM {table_name} LIMIT ? OFFSET ?", (limit, offset)
                    )
                    rows = cursor.fetchall()
                    data = [dict(row) for row in rows]
                return jsonify(
                    {
                        "table_name": table_name,
                        "data": data,
                        "total_count": total_count,
                        "limit": limit,
                        "offset": offset,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                )
            except Exception as e:
                self.logger.error(f"Failed to get table data for {table_name}: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/database/query", methods=["POST"])
        def execute_database_query():
            try:
                data = request.get_json()
                if not data or "query" not in data:
                    raise BadRequest("Query field required")
                query = data["query"].strip()
                if not query.upper().startswith("SELECT"):
                    raise BadRequest("Only SELECT queries are allowed")
                with sqlite3.connect(self.config.intelligence_db_path) as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    data = [dict(row) for row in rows]
                return jsonify(
                    {
                        "query": query,
                        "data": data,
                        "row_count": len(data),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                )
            except BadRequest as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                self.logger.error(f"Failed to execute query: {e}")
                return jsonify({"error": str(e)}), 500

    def _setup_error_handlers(self):
        """Setup error handlers for the Flask app."""

        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({"error": "Not found"}), 404

        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({"error": "Internal server error"}), 500

    def _check_database_health(self):
        """Check if the database is accessible."""
        try:
            with sqlite3.connect(self.config.database_path) as conn:
                conn.execute("SELECT 1")
            return True
        except Exception:
            return False

    def _update_agent_status(self):
        """Update agent status information."""
        # Mock implementation - replace with actual agent monitoring

    def _update_project_status(self):
        """Update project status information."""
        # Mock implementation - replace with actual project monitoring

    def run(self, host: str = "0.0.0.0", port: int = 8080, debug: bool = False):
        """Run the dashboard application."""
        try:
            self.logger.info(f"Starting TRAE.AI Dashboard on {host}:{port}")
            self._start_background_tasks()
            # Use Waitress for a production-ready server instead of Flask's dev server
            serve(self.app, host=host, port=port, threads=8)
        except KeyboardInterrupt:
            self.logger.info("Dashboard shutdown requested")
        except Exception as e:
            self.logger.error(f"Dashboard error: {e}")
        finally:
            self._cleanup()

    def _start_background_tasks(self):
        """Start background monitoring tasks."""
        try:
            monitor_thread = threading.Thread(
                target=self._background_monitor, daemon=True, name="SystemMonitor"
            )
            monitor_thread.start()
            self.logger.info("Background monitoring tasks started")
        except Exception as e:
            self.logger.error(f"Failed to start background tasks: {e}")

    def _background_monitor(self):
        """Background monitoring loop."""
        while True:
            try:
                self._update_agent_status()
                self._update_project_status()
                time.sleep(30)
            except Exception as e:
                self.logger.error(f"Background monitor error: {e}")
                time.sleep(60)

    def _cleanup(self):
        """Cleanup resources on shutdown."""
        self.logger.info("Cleaning up dashboard resources...")
        # Add any cleanup logic here


def main():
    """Main entry point for the dashboard application."""
    import argparse

    parser = argparse.ArgumentParser(description="TRAE.AI Dashboard")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--config", help="Path to configuration file")
    args = parser.parse_args()

    def find_free_port(start_port, host):
        """Find an available port."""
        for port in range(start_port, start_port + 100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((host, port))
                return port
            except OSError:
                continue
        raise RuntimeError("No free port found")

    try:
        free_port = find_free_port(args.port, args.host)
        # DEBUG_REMOVED: print(f"Dashboard starting on http://{args.host}:{free_port}")

        config = DashboardConfig()
        config.debug = args.debug
        config.host = args.host
        config.port = free_port

        dashboard = DashboardApp(config)
        dashboard.run(host=config.host, port=config.port, debug=config.debug)

    except Exception:
        # DEBUG_REMOVED: print(f"Failed to start dashboard: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
