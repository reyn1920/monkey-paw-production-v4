#!/usr/bin/env python3
"""
Database Setup and Initialization Module

This module handles database setup, schema creation, and initial data population
for the TRAE.AI system.

Author: TRAE.AI System
Version: 2.0.0
Date: 2024
"""

import os
import sqlite3
from pathlib import Path
from typing import Optional, Any

# Import utilities
from utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseSetup:
    """
    Database setup and initialization manager.

    Handles schema creation, initial data population, and database migrations.
    """

    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv(
            "DATABASE_URL", "sqlite:///data/trae_master.db"
        )
        self.db_path = self._extract_db_path()

    def _extract_db_path(self) -> Path:
        """Extract database file path from URL"""
        if self.database_url.startswith("sqlite:///"):
            db_path = self.database_url[10:]  # Remove 'sqlite:///'
        else:
            db_path = self.database_url
        return Path(db_path)

    def setup_database(self) -> bool:
        """
        Setup the complete database with schema and initial data.

        Returns:
            bool: True if setup successful, False otherwise
        """
        try:
            # Ensure database directory exists
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

            # Create database connection
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.execute("PRAGMA foreign_keys = ON")

                # Check if database is already initialized
                if self._is_database_initialized(conn):
                    logger.info("Database already initialized")
                    return True

                # Create schema
                self._create_schema(conn)

                # Insert initial data
                self._insert_initial_data(conn)

                logger.info(f"Database setup completed: {self.db_path}")
                return True

        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            return False

    def _is_database_initialized(self, conn: sqlite3.Connection) -> bool:
        """Check if database is already initialized"""
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='task_queue'"
        )
        return cursor.fetchone() is not None

    def _create_schema(self, conn: sqlite3.Connection) -> None:
        """Create database schema"""
        # Use fallback schema for now to avoid issues with complex schema.sql
        logger.info("Creating fallback schema")
        self._create_fallback_schema(conn)

    def _create_fallback_schema(self, conn: sqlite3.Connection) -> None:
        """Create basic fallback schema"""
        schema_sql = """
        -- Core system tables
        CREATE TABLE IF NOT EXISTS task_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT UNIQUE NOT NULL,
            task_type TEXT NOT NULL DEFAULT 'system',
            priority TEXT NOT NULL DEFAULT 'medium',
            status TEXT NOT NULL DEFAULT 'pending',
            agent_id TEXT,
            payload TEXT,
            result TEXT,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            retry_count INTEGER DEFAULT 0,
            max_retries INTEGER DEFAULT 3
        );

        CREATE TABLE IF NOT EXISTS api_registry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            endpoint_url TEXT NOT NULL,
            api_key TEXT,
            status TEXT DEFAULT 'active',
            last_health_check TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS system_status (
            id INTEGER PRIMARY KEY,
            component TEXT NOT NULL,
            status TEXT NOT NULL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS api_discovery_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Indexes for performance
        CREATE INDEX IF NOT EXISTS idx_task_status ON task_queue(status);
        CREATE INDEX IF NOT EXISTS idx_task_type ON task_queue(task_type);
        CREATE INDEX IF NOT EXISTS idx_agent_id ON task_queue(agent_id);
        CREATE INDEX IF NOT EXISTS idx_api_service ON api_registry(service_name);
        CREATE INDEX IF NOT EXISTS idx_system_component ON system_status(component);
        """

        conn.executescript(schema_sql)

    def _insert_initial_data(self, conn: sqlite3.Connection) -> None:
        """Insert initial system data"""
        # Insert initial system status
        conn.execute(
            "INSERT OR REPLACE INTO system_status (id, component, status) VALUES (1, 'database', 'initialized')"
        )

        # Insert initial API discovery tasks
        initial_tasks = [
            ("system_health_check", "pending"),
            ("api_endpoint_discovery", "pending"),
            ("service_registration", "pending"),
        ]

        for task_name, status in initial_tasks:
            conn.execute(
                "INSERT OR IGNORE INTO api_discovery_tasks (task_name, status) VALUES (?, ?)",
                (task_name, status),
            )

        conn.commit()
        logger.info("Initial data inserted")

    def reset_database(self) -> bool:
        """
        Reset the database by dropping all tables and recreating schema.

        Returns:
            bool: True if reset successful, False otherwise
        """
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                # Get all table names
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
                tables = [row[0] for row in cursor.fetchall()]

                # Drop all tables
                for table in tables:
                    conn.execute(f"DROP TABLE IF EXISTS {table}")

                # Recreate schema
                self._create_schema(conn)
                self._insert_initial_data(conn)

                logger.info("Database reset completed")
                return True

        except Exception as e:
            logger.error(f"Database reset failed: {e}")
            return False

    def health_check(self) -> dict[str, Any]:
        """
        Perform database health check.

        Returns:
            dict: Health check results
        """
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                # Test basic connectivity
                conn.execute("SELECT 1")

                # Check if core tables exist
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
                tables = [row[0] for row in cursor.fetchall()]

                required_tables = ["task_queue", "api_registry", "system_status"]
                missing_tables = [t for t in required_tables if t not in tables]

                return {
                    "status": "healthy" if not missing_tables else "degraded",
                    "database_path": str(self.db_path),
                    "tables_found": len(tables),
                    "missing_tables": missing_tables,
                    "database_exists": self.db_path.exists(),
                }

        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "database_path": str(self.db_path),
                "database_exists": self.db_path.exists(),
            }


# Convenience functions
def setup_database(database_url: Optional[str] = None) -> bool:
    """Setup database with schema and initial data"""
    db_setup = DatabaseSetup(database_url)
    return db_setup.setup_database()


def reset_database(database_url: Optional[str] = None) -> bool:
    """Reset database by dropping and recreating all tables"""
    db_setup = DatabaseSetup(database_url)
    return db_setup.reset_database()


def database_health_check(database_url: Optional[str] = None) -> dict[str, Any]:
    """Perform database health check"""
    db_setup = DatabaseSetup(database_url)
    return db_setup.health_check()


if __name__ == "__main__":
    # Command line interface for database setup
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "setup":
            success = setup_database()
            # DEBUG_REMOVED: print(f"Database setup: {'SUCCESS' if success else 'FAILED'}")
            sys.exit(0 if success else 1)

        elif command == "reset":
            success = reset_database()
            # DEBUG_REMOVED: print(f"Database reset: {'SUCCESS' if success else 'FAILED'}")
            sys.exit(0 if success else 1)

        elif command == "health":
            health = database_health_check()
            # DEBUG_REMOVED: print(f"Database health: {health}")
            sys.exit(0 if health["status"] == "healthy" else 1)

        else:
            # DEBUG_REMOVED: print(f"Unknown command: {command}")
            # DEBUG_REMOVED: print("Available commands: setup, reset, health")
            sys.exit(1)
    else:
        # Default: setup database
        success = setup_database()
        # DEBUG_REMOVED: print(f"Database setup: {'SUCCESS' if success else 'FAILED'}")
        sys.exit(0 if success else 1)
