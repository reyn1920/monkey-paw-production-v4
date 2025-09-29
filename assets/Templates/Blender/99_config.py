"""
Configuration management for the application.
"""

import os
from typing import Optional, Dict, Any
from functools import lru_cache


class Config:
    """Configuration class for application settings."""
    
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY", "default_secret_key_for_testing")
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///app.db")
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.api_key = os.getenv("API_KEY", "test_api_key")
    
    def get_api_key(self, key_name: Optional[str] = None) -> str:
        """Get the API key."""
        if key_name:
            return os.getenv(key_name, "")
        return self.api_key
    
    def get_secret_key(self) -> str:
        """Get the secret key."""
        return self.secret_key
    
    def get_database_url(self) -> str:
        """Get the database URL."""
        return self.database_url
    
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.debug
    
    def get_environment(self) -> str:
        """Get the current environment."""
        return self.environment
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'secret_key': self.secret_key,
            'database_url': self.database_url,
            'debug': self.debug,
            'environment': self.environment,
            'api_key': self.api_key
        }


@lru_cache()
def get_config() -> Config:
    """Get the application configuration."""
    return Config()