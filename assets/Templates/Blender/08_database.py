"""
Database infrastructure for VidScript Pro
Async SQLAlchemy setup with connection management
"""

import logging
from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool

from src.backend.core.config import get_settings

logger = logging.getLogger(__name__)

# Database metadata and base
metadata = MetaData()
Base = declarative_base(metadata=metadata)


class DatabaseManager:
    """Database connection and session manager."""
    
    def __init__(self) -> None:
        """Initialize database manager."""
        self.settings = get_settings()
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None
    
    async def initialize(self) -> None:
        """Initialize database engine and session factory."""
        logger.info("Initializing database connection...")
        
        # Create async engine
        connect_args = {}
        if "sqlite" in self.settings.database_url:
            # SQLite specific configuration
            connect_args = {
                "check_same_thread": False,
            }
            poolclass = StaticPool
        else:
            poolclass = None
        
        self.engine = create_async_engine(
            self.settings.database_url,
            echo=self.settings.debug,
            connect_args=connect_args,
            poolclass=poolclass,
        )
        
        # Create session factory
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        # Create tables
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database initialized successfully")
    
    async def close(self) -> None:
        """Close database connections."""
        if self.engine:
            logger.info("Closing database connections...")
            await self.engine.dispose()
            logger.info("Database connections closed")
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session.
        
        Yields:
            Database session
        """
        if not self.session_factory:
            raise RuntimeError("Database not initialized")
        
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Global database manager instance
db_manager = DatabaseManager()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    async for session in db_manager.get_session():
        yield session