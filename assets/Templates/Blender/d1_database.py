#!/usr/bin/env python3
"""
TRAE.AI Production Database Connection Manager

This module provides database connection management for both development (SQLite)
and production (PostgreSQL) environments. It automatically detects the environment
and uses the appropriate database configuration.

Author: TRAE.AI System
Version: 2.0.0
Date: 2024
"""

import os
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

# Import utilities
from utils.logger import get_logger

# Try to import PostgreSQL dependencies
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from psycopg2.pool import ThreadedConnectionPool

    postgres_available = True
except ImportError:
    psycopg2 = None
    RealDictCursor = None
    ThreadedConnectionPool = None
    postgres_available = False

# Try to import SQLAlchemy for advanced database operations
try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    sqlalchemy_available = True
except ImportError:
    create_engine = None
    text = None
    sessionmaker = None
    StaticPool = None
    sqlalchemy_available = False

logger = get_logger(__name__)


class DatabaseError(Exception):
    """Custom exception for database operations"""


class ProductionDatabaseManager:
    """
    Production-ready database connection manager for TRAE.AI system.

    Supports both SQLite (development) and PostgreSQL (production) based on
    the DATABASE_URL environment variable. Provides connection pooling,
    automatic failover, and environment-specific optimizations.
    """

    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv(
            "DATABASE_URL", "sqlite:///data/trae_master.db"
        )
        self._local = threading.local()
        self._connection_pool = None
        self._engine = None
        self._session_factory = None

        # Parse database URL to determine type
        self.db_type = self._parse_database_type()

        # Initialize based on database type
        if self.db_type == "postgresql":
            self._initialize_postgresql()
        else:
            self._initialize_sqlite()

    def _parse_database_type(self) -> str:
        """Parse database URL to determine database type"""
        if self.database_url.startswith("postgresql://"):
            return "postgresql"
        elif self.database_url.startswith("sqlite://"):
            return "sqlite"
        else:
            # Default to SQLite for file paths
            return "sqlite"

    def _initialize_postgresql(self):
        """Initialize PostgreSQL connection pool"""
        if not postgres_available:
            raise DatabaseError(
                "PostgreSQL dependencies not installed. Run: pip install psycopg2-binary"
            )

        try:
            # Parse PostgreSQL URL
            parsed = urlparse(self.database_url)

            # Create connection pool
            if ThreadedConnectionPool and RealDictCursor:
                self._connection_pool = ThreadedConnectionPool(
                    minconn=1,
                    maxconn=20,
                    host=parsed.hostname,
                    port=parsed.port or 5432,
                    database=parsed.path[1:],  # Remove leading slash
                    user=parsed.username,
                    password=parsed.password,
                    cursor_factory=RealDictCursor,
                )

            # Initialize SQLAlchemy engine if available
            if sqlalchemy_available and create_engine and sessionmaker:
                self._engine = create_engine(
                    self.database_url,
                    pool_size=10,
                    max_overflow=20,
                    pool_pre_ping=True,
                    pool_recycle=3600,
                )
                self._session_factory = sessionmaker(bind=self._engine)

            logger.info("PostgreSQL connection pool initialized")

        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL: {e}")
            raise DatabaseError(f"PostgreSQL initialization failed: {e}")

    def _initialize_sqlite(self):
        """Initialize SQLite database"""
        # Extract path from SQLite URL
        if self.database_url.startswith("sqlite:///"):
            db_path = self.database_url[10:]  # Remove 'sqlite:///'
        else:
            db_path = self.database_url

        self.db_path = Path(db_path)
        self._ensure_db_directory()

        # Initialize SQLAlchemy engine if available
        if sqlalchemy_available and create_engine and sessionmaker and StaticPool:
            self._engine = create_engine(
                f"sqlite:///{self.db_path}",
                poolclass=StaticPool,
                connect_args={"check_same_thread": False, "timeout": 30},
                echo=False,
            )
            self._session_factory = sessionmaker(bind=self._engine)

        # Initialize database schema
        self._initialize_sqlite_database()

        logger.info(f"SQLite database initialized: {self.db_path}")

    def _ensure_db_directory(self):
        """Ensure the database directory exists"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _initialize_sqlite_database(self):
        """Initialize SQLite database with schema if needed"""
        try:
            with self.get_connection() as conn:
                if self.db_type == "sqlite":
                    conn.execute("PRAGMA foreign_keys = ON")

                # Check if database is initialized
                if self.db_type == "sqlite":
                    cursor = conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name='task_queue'"
                    )
                else:
                    cursor = conn.execute(
                        "SELECT table_name FROM information_schema.tables WHERE table_name='task_queue'"
                    )

                if not cursor.fetchone():
                    logger.info("Initializing database schema")
                    self._create_schema(conn)

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise DatabaseError(f"Database initialization failed: {e}")

    def _create_schema(self, conn):
        """Create database schema from schema.sql or fallback schema"""
        schema_path = Path("schema.sql")
        if schema_path.exists():
            with open(schema_path) as f:
                schema_sql = f.read()

            if self.db_type == "sqlite":
                conn.executescript(schema_sql)
            else:
                # For PostgreSQL, execute statements individually
                statements = [
                    stmt.strip() for stmt in schema_sql.split(";") if stmt.strip()
                ]
                for stmt in statements:
                    if stmt and not stmt.startswith("--"):
                        conn.execute(stmt)
        else:
            # Fallback basic schema
            self._create_fallback_schema(conn)

    def _create_fallback_schema(self, conn):
        """Create basic fallback schema"""
        if self.db_type == "sqlite":
            schema_sql = """
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

                CREATE INDEX IF NOT EXISTS idx_task_status ON task_queue(status);
                CREATE INDEX IF NOT EXISTS idx_task_type ON task_queue(task_type);
                CREATE INDEX IF NOT EXISTS idx_agent_id ON task_queue(agent_id);
            """
            conn.executescript(schema_sql)
        else:
            # PostgreSQL schema
            schema_statements = [
                """
                CREATE TABLE IF NOT EXISTS task_queue (
                    id SERIAL PRIMARY KEY,
                    task_id VARCHAR(255) UNIQUE NOT NULL,
                    task_type VARCHAR(100) NOT NULL DEFAULT 'system',
                    priority VARCHAR(50) NOT NULL DEFAULT 'medium',
                    status VARCHAR(50) NOT NULL DEFAULT 'pending',
                    agent_id VARCHAR(255),
                    payload TEXT,
                    result TEXT,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    retry_count INTEGER DEFAULT 0,
                    max_retries INTEGER DEFAULT 3
                )
                """,
                "CREATE INDEX IF NOT EXISTS idx_task_status ON task_queue(status)",
                "CREATE INDEX IF NOT EXISTS idx_task_type ON task_queue(task_type)",
                "CREATE INDEX IF NOT EXISTS idx_agent_id ON task_queue(agent_id)",
            ]

            for stmt in schema_statements:
                conn.execute(stmt)

    @contextmanager
    def get_connection(self):
        """Get a database connection with automatic cleanup"""
        if self.db_type == "postgresql":
            conn = None
            try:
                conn = self._connection_pool.getconn()
                conn.autocommit = False
                yield conn
                conn.commit()
            except Exception as e:
                if conn:
                    conn.rollback()
                logger.error(f"PostgreSQL connection error: {e}")
                raise DatabaseError(f"Database operation failed: {e}")
            finally:
                if conn:
                    self._connection_pool.putconn(conn)
        else:
            # SQLite connection
            conn = None
            try:
                conn = sqlite3.connect(str(self.db_path), timeout=30.0)
                conn.row_factory = sqlite3.Row
                conn.execute("PRAGMA foreign_keys = ON")
                yield conn
            except Exception as e:
                if conn:
                    conn.rollback()
                logger.error(f"SQLite connection error: {e}")
                raise DatabaseError(f"Database operation failed: {e}")
            finally:
                if conn:
                    conn.close()

    @contextmanager
    def get_session(self):
        """Get SQLAlchemy session (if available)"""
        if not sqlalchemy_available or not self._session_factory or not sessionmaker:
            raise DatabaseError("SQLAlchemy not available or not initialized")

        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session error: {e}")
            raise DatabaseError(f"Session operation failed: {e}")
        finally:
            session.close()

    def execute_query(
        self, query: str, params: Optional[tuple] = None
    ) -> list[dict[str, Any]]:
        """Execute a SELECT query and return results"""
        with self.get_connection() as conn:
            if self.db_type == "postgresql":
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                return [dict(row) for row in cursor.fetchall()]
            else:
                cursor = conn.execute(query, params or ())
                return [dict(row) for row in cursor.fetchall()]

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
        with self.get_connection() as conn:
            if self.db_type == "postgresql":
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                return cursor.rowcount
            else:
                cursor = conn.execute(query, params or ())
                return cursor.rowcount

    def execute_script(self, script: str) -> None:
        """Execute a SQL script"""
        with self.get_connection() as conn:
            if self.db_type == "postgresql":
                statements = [
                    stmt.strip() for stmt in script.split(";") if stmt.strip()
                ]
                cursor = conn.cursor()
                for stmt in statements:
                    if stmt and not stmt.startswith("--"):
                        cursor.execute(stmt)
            else:
                conn.executescript(script)

    def health_check(self) -> dict[str, Any]:
        """Perform database health check"""
        try:
            with self.get_connection() as conn:
                if self.db_type == "postgresql":
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1")
                    cursor.fetchone()
                else:
                    conn.execute("SELECT 1")

                return {
                    "status": "healthy",
                    "database_type": self.db_type,
                    "database_url": (
                        self.database_url.split("@")[0] + "@***"
                        if "@" in self.database_url
                        else "local"
                    ),
                    "timestamp": str(threading.current_thread().ident),
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "database_type": self.db_type,
                "timestamp": str(threading.current_thread().ident),
            }

    def close(self):
        """Close all connections and cleanup resources"""
        try:
            if self._connection_pool:
                self._connection_pool.closeall()
            if self._engine:
                self._engine.dispose()
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")


# Global database manager instance
db_manager = ProductionDatabaseManager()

# Convenience functions


def get_db_connection():
    """Get database connection context manager"""
    return db_manager.get_connection()


def get_db_session():
    """Get SQLAlchemy session context manager"""
    return db_manager.get_session()


def execute_query(query: str, params: Optional[tuple] = None) -> list[dict[str, Any]]:
    """Execute a SELECT query"""
    return db_manager.execute_query(query, params)


def execute_update(query: str, params: Optional[tuple] = None) -> int:
    """Execute an INSERT/UPDATE/DELETE query"""
    return db_manager.execute_update(query, params)


def database_health_check() -> dict[str, Any]:
    """Perform database health check"""
    return db_manager.health_check()
