"""
Database configuration and blueprint for data services.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class DatabaseConfig:
    """Configuration for database connections."""
    database_path: str = ":memory:"
    connection_timeout: int = 30
    max_connections: int = 10
    enable_foreign_keys: bool = True
    journal_mode: str = "WAL"
    synchronous: str = "NORMAL"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'database_path': self.database_path,
            'connection_timeout': self.connection_timeout,
            'max_connections': self.max_connections,
            'enable_foreign_keys': self.enable_foreign_keys,
            'journal_mode': self.journal_mode,
            'synchronous': self.synchronous
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DatabaseConfig':
        """Create from dictionary."""
        return cls(**data)
    
    def get_connection_string(self) -> str:
        """Get SQLite connection string."""
        return self.database_path