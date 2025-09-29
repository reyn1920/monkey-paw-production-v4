"""
Database infrastructure for VidScript Pro
SQLAlchemy async setup with proper connection management
"""

import logging
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.backend.core.config import get_settings

logger = logging.getLogger(__name__)

# Create declarative base
Base = declarative_base()


class DatabaseManager:
    """Database connection and session manager."""
    
    def __init__(self):
        self.engine = None
        self.async_session_maker = None
        self.settings = get_settings()
    
    async def initialize(self) -> None:
        """Initialize database connection."""
        try:
            # Create async engine
            self.engine = create_async_engine(
                self.settings.database_url,
                echo=self.settings.debug,
                future=True,
            )
            
            # Create session maker
            self.async_session_maker = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            
            logger.info("Database connection initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    async def close(self) -> None:
        """Close database connection."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection closed")
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session."""
        if not self.async_session_maker:
            raise RuntimeError("Database not initialized")
        
        async with self.async_session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Global database manager instance
db_manager = DatabaseManager()