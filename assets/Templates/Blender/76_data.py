"""
Data service for database operations and data management.
"""

import sqlite3
import aiosqlite
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import logging

from .registry import BaseService

logger = logging.getLogger(__name__)


@dataclass
class ConnectionInfo:
    """Database connection information."""
    database_path: str
    is_connected: bool
    initialized: bool


@dataclass
class QueryResult:
    """Result of a database query."""
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    rows_affected: int = 0
    
    # Add properties that tests expect
    @property
    def row_count(self) -> int:
        """Number of rows returned."""
        return len(self.data) if self.data else 0
    
    @property
    def affected_rows(self) -> int:
        """Number of rows affected by the query."""
        return self.rows_affected
    
    @property
    def rows(self) -> List[Dict[str, Any]]:
        """Rows returned by the query."""
        return self.data or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'data': self.data,
            'error': self.error,
            'rows_affected': self.rows_affected
        }


class DataService(BaseService):
    """Service for handling database operations."""
    
    def __init__(self, database_path: str = ":memory:"):
        super().__init__("DataService")
        self.database_path = database_path
        self._connection: Optional[aiosqlite.Connection] = None
        self._sync_connection: Optional[sqlite3.Connection] = None
        self._initialized = False
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize the data service and database connection."""
        try:
            self._connection = await aiosqlite.connect(self.database_path)
            self._sync_connection = sqlite3.connect(self.database_path)
            self._sync_connection.row_factory = sqlite3.Row
            
            # Create basic tables for testing
            await self._create_tables()
            self._initialized = True
            self.is_initialized = True
            logger.info(f"DataService initialized with database: {self.database_path}")
        except Exception as e:
            logger.error(f"Failed to initialize DataService: {e}")
            raise
    
    async def _create_tables(self):
        """Create basic tables for testing."""
        if not self._connection:
            return
            
        tables = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS test_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        for table_sql in tables:
            await self._connection.execute(table_sql)
        await self._connection.commit()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get synchronous database connection."""
        if not self._sync_connection:
            self._sync_connection = sqlite3.connect(self.database_path)
            self._sync_connection.row_factory = sqlite3.Row
        return self._sync_connection
    
    async def get_async_connection(self) -> aiosqlite.Connection:
        """Get asynchronous database connection."""
        if not self._connection:
            await self.initialize()
        if not self._connection:
            raise RuntimeError("Failed to initialize database connection")
        return self._connection
    
    async def get_connection_info(self) -> ConnectionInfo:
        """Get database connection information."""
        return ConnectionInfo(
            database_path=self.database_path,
            is_connected=self.is_connected(),
            initialized=self._initialized
        )
    
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._connection is not None and self._initialized
    
    async def execute_query(self, query: str, params: Optional[Union[Dict[str, Any], tuple[Any, ...]]] = None) -> QueryResult:
        """Execute a database query asynchronously."""
        if not self._connection:
            await self.initialize()
        
        if not self._connection:
            return QueryResult(success=False, error="No database connection")
        
        try:
            if params:
                # Handle both dict (named parameters) and tuple (positional parameters)
                cursor = await self._connection.execute(query, params)
            else:
                cursor = await self._connection.execute(query)
            
            # Check if it's a SELECT query
            if query.strip().upper().startswith('SELECT'):
                rows = await cursor.fetchall()
                # Convert aiosqlite rows to dictionaries properly
                if rows:
                    data = []
                    for row in rows:
                        # Convert row to dictionary using column names
                        columns = [description[0] for description in cursor.description]
                        row_dict = {}
                        for i, column in enumerate(columns):
                            row_dict[column] = row[i]
                        data.append(row_dict)
                else:
                    data = []
                return QueryResult(success=True, data=data, rows_affected=len(data))
            else:
                await self._connection.commit()
                return QueryResult(success=True, rows_affected=cursor.rowcount)
                
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return QueryResult(success=False, error=str(e))
    
    async def shutdown(self):
        """Shutdown the data service."""
        if self._connection:
            await self._connection.close()
            self._connection = None
        
        if self._sync_connection:
            self._sync_connection.close()
            self._sync_connection = None
        
        self._initialized = False
        logger.info("DataService shutdown")