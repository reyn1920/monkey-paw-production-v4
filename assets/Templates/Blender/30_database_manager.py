#!/usr/bin/env python3
"""
Database Manager - Handles all database operations and connections
"""

import sqlite3
from pathlib import Path
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Use sqlite3 for synchronous operations if aiosqlite is not available
try:
    import aiosqlite

    async_db_available = True
except ImportError:
    aiosqlite = None  # type: ignore
    async_db_available = False

logger = logging.getLogger(__name__)

# Database Storage Strategy Configuration
DATABASE_STORAGE_CONFIG = {
    "local_databases": {
        # Performance-critical databases that MUST remain local for
        # video/avatar creation
        "performance_critical": [
            "content_automation.db",
            "quality_metrics.db",
            "performance_metrics.db",
            "automation_performance.db",
            "runtime.db",
            "model_generator.db",
            "ollama_cache.db",
        ],
        "description": "Databases required for high-speed video creation and avatar generation",
    },
    "cloud_databases": {
        # Databases that can be moved to cloud storage
        "analytics": [
            "analytics_dashboard.db",
            "analytics.db",
            "performance_analytics.db",
            "engagement_tracking.sqlite",
            "youtube_engagement.sqlite",
        ],
        "business": [
            "marketing_monetization.sqlite",
            "marketing.db",
            "monetization.db",
            "revenue_streams.db",
            "cost_tracking.db",
            "promotion_campaigns.sqlite",
        ],
        "content_management": [
            "rss_watcher.db",
            "youtube_automation.sqlite",
            "channels.db",
            "collaboration_outreach.db",
        ],
        "system_admin": [
            "error_tracking.db",
            "example_error_tracking.db",
            "scan_results.sqlite",
            "api_integration.db",
            "routellm_usage.db",
        ],
        "development": [
            "test_comprehensive.db",
            "test_fraud.db",
            "test_fraud2.db",
            "test_fraud3.db",
            "test_results.db",
            "test.db",
        ],
        "backups": [
            "right_perspective_backup_20250902_012246.db",
            "base44.sqlite",
            "trae_production.db",
        ],
        "description": "Databases suitable for cloud storage - non-performance critical",
    },
    "hybrid_databases": {
        # Databases that may need evaluation based on usage patterns
        "evaluate_case_by_case": [
            "intelligence.db",
            "master_orchestrator.db",
            "trae_ai.db",
            "content_agent.db",
        ],
        "description": "Databases requiring evaluation based on access patterns and usage frequency",
    },
}


class DatabaseStorageManager:
    """Manages database storage strategy for local vs cloud deployment"""

    def __init__(self):
        self.config = DATABASE_STORAGE_CONFIG

    def is_performance_critical(self, db_name: str) -> bool:
        """Check if database must remain local for performance"""
        return db_name in self.config["local_databases"]["performance_critical"]

    def can_move_to_cloud(self, db_name: str) -> bool:
        """Check if database can be moved to cloud storage"""
        for category in self.config["cloud_databases"].values():
            if isinstance(category, list) and db_name in category:
                return True
        return False

    def requires_evaluation(self, db_name: str) -> bool:
        """Check if database requires case-by-case evaluation"""
        return db_name in self.config["hybrid_databases"]["evaluate_case_by_case"]

    def get_storage_recommendation(self, db_name: str) -> Dict[str, str]:
        """Get storage recommendation for a database"""
        if self.is_performance_critical(db_name):
            return {
                "recommendation": "local",
                "reason": "Performance-critical for video/avatar creation",
                "category": "performance_critical",
            }
        elif self.can_move_to_cloud(db_name):
            return {
                "recommendation": "cloud",
                "reason": "Non-performance critical, suitable for cloud storage",
                "category": self._get_cloud_category(db_name),
            }
        elif self.requires_evaluation(db_name):
            return {
                "recommendation": "evaluate",
                "reason": "Requires case-by-case evaluation based on usage patterns",
                "category": "hybrid",
            }
        else:
            return {
                "recommendation": "unknown",
                "reason": "Database not found in configuration",
                "category": "uncategorized",
            }

    def _get_cloud_category(self, db_name: str) -> str:
        """Get the cloud storage category for a database"""
        for category, dbs in self.config["cloud_databases"].items():
            if isinstance(dbs, list) and db_name in dbs:
                return category
        return "unknown"

    def generate_migration_plan(self) -> Dict[str, Any]:
        """Generate a comprehensive migration plan"""
        plan = {
            "local_count": len(self.config["local_databases"]["performance_critical"]),
            "cloud_count": sum(
                len(dbs)
                for dbs in self.config["cloud_databases"].values()
                if isinstance(dbs, list)
            ),
            "evaluation_count": len(
                self.config["hybrid_databases"]["evaluate_case_by_case"]
            ),
            "migration_strategy": {
                "phase_1": "Keep performance-critical databases local",
                "phase_2": "Migrate analytics and business databases to cloud",
                "phase_3": "Evaluate hybrid databases based on usage patterns",
            },
            "estimated_storage_savings": "~80% reduction in local storage requirements",
        }
        return plan


class DatabaseManager:
    """Manages database connections and operations"""

    def __init__(self, db_path: str = "data/app.db"):
        self.db_path = db_path
        self.connection = None
        self.storage_manager = DatabaseStorageManager()
        self._ensure_db_directory()

    def _ensure_db_directory(self):
        """Ensure the database directory exists"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize the database and create tables"""
        try:
            if async_db_available and aiosqlite:
                async with aiosqlite.connect(self.db_path) as db:
                    await self._create_tables(db)
                    await db.commit()
            else:
                with sqlite3.connect(self.db_path) as db:
                    self._create_tables_sync(db)
                    db.commit()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    async def _create_tables(self, db):
        """Create necessary database tables"""
        # Users table
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Sessions table
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """
        )

        # Tasks table
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """
        )

        # Settings table
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

    async def execute_query(
        self, query: str, params: tuple[Any, ...] = ()
    ) -> list[dict[str, Any]]:
        """Execute a SELECT query and return results"""
        try:
            if async_db_available and aiosqlite:
                async with aiosqlite.connect(self.db_path) as db:
                    db.row_factory = aiosqlite.Row
                    async with db.execute(query, params) as cursor:
                        rows = await cursor.fetchall()
                        return [dict(row) for row in rows]
            else:
                with sqlite3.connect(self.db_path) as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.execute(query, params)
                    rows = cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise

    async def execute_update(self, query: str, params: tuple[Any, ...] = ()) -> int:
        """Execute an INSERT, UPDATE, or DELETE query"""
        try:
            if async_db_available and aiosqlite:
                async with aiosqlite.connect(self.db_path) as db:
                    cursor = await db.execute(query, params)
                    await db.commit()
                    return cursor.rowcount
            else:
                with sqlite3.connect(self.db_path) as db:
                    cursor = db.execute(query, params)
                    db.commit()
                    return cursor.rowcount
        except Exception as e:
            logger.error(f"Update execution failed: {e}")
            raise

    def _create_tables_sync(self, db):
        """Create necessary database tables synchronously"""
        # Users table
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Sessions table
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """
        )

        # Tasks table
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """
        )

        # Settings table
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

    async def get_user_by_id(self, user_id: int) -> Optional[dict[str, Any]]:
        """Get user by ID"""
        results = await self.execute_query(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        )
        return results[0] if results else None

    async def get_user_by_username(self, username: str) -> Optional[dict[str, Any]]:
        """Get user by username"""
        results = await self.execute_query(
            "SELECT * FROM users WHERE username = ?", (username,)
        )
        return results[0] if results else None

    async def create_user(self, username: str, email: str, password_hash: str) -> int:
        """Create a new user"""
        await self.execute_update(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash),
        )
        results = await self.execute_query(
            "SELECT id FROM users WHERE username = ?", (username,)
        )
        return results[0]["id"] if results else 0

    async def create_session(
        self, session_id: str, user_id: int, data: dict[str, Any], expires_at: datetime
    ) -> bool:
        """Create a new session"""
        try:
            await self.execute_update(
                "INSERT INTO sessions (id, user_id, data, expires_at) VALUES (?, ?, ?, ?)",
                (session_id, user_id, json.dumps(data), expires_at),
            )
            return True
        except Exception:
            return False

    async def get_session(self, session_id: str) -> Optional[dict[str, Any]]:
        """Get session by ID"""
        results = await self.execute_query(
            "SELECT * FROM sessions WHERE id = ? AND expires_at > CURRENT_TIMESTAMP",
            (session_id,),
        )
        if results:
            session = results[0]
            session["data"] = json.loads(session["data"]) if session["data"] else {}
            return session
        return None

    async def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        rowcount = await self.execute_update(
            "DELETE FROM sessions WHERE id = ?", (session_id,)
        )
        return rowcount > 0

    async def create_task(
        self,
        user_id: int,
        title: str,
        description: str = "",
        status: str = "pending",
        priority: str = "medium",
    ) -> str:
        """Create a new task"""
        import uuid

        task_id = str(uuid.uuid4())
        await self.execute_update(
            "INSERT INTO tasks (id, user_id, title, description, status, priority) VALUES (?, ?, ?, ?, ?, ?)",
            (task_id, user_id, title, description, status, priority),
        )
        return task_id

    async def get_user_tasks(self, user_id: int) -> list[dict[str, Any]]:
        """Get all tasks for a user"""
        return await self.execute_query(
            "SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC", (user_id,)
        )

    async def update_task_status(self, task_id: str, status: str) -> bool:
        """Update task status"""
        rowcount = await self.execute_update(
            "UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, task_id),
        )
        return rowcount > 0

    async def get_setting(self, key: str) -> Optional[str]:
        """Get a setting value"""
        results = await self.execute_query(
            "SELECT value FROM settings WHERE key = ?", (key,)
        )
        return results[0]["value"] if results else None

    async def set_setting(self, key: str, value: str) -> bool:
        """Set a setting value"""
        try:
            await self.execute_update(
                "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (key, value),
            )
            return True
        except Exception:
            return False

    async def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        await self.execute_update(
            "DELETE FROM sessions WHERE expires_at <= CURRENT_TIMESTAMP"
        )

    async def get_status(self) -> dict[str, Any]:
        """Get database status"""
        try:
            # Test connection
            await self.execute_query("SELECT 1")

            # Get table counts
            users_count = await self.execute_query(
                "SELECT COUNT(*) as count FROM users"
            )
            sessions_count = await self.execute_query(
                "SELECT COUNT(*) as count FROM sessions"
            )
            tasks_count = await self.execute_query(
                "SELECT COUNT(*) as count FROM tasks"
            )

            return {
                "status": "healthy",
                "database_path": self.db_path,
                "tables": {
                    "users": users_count[0]["count"],
                    "sessions": sessions_count[0]["count"],
                    "tasks": tasks_count[0]["count"],
                },
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}


# Global database manager instance
database_manager = DatabaseManager()
