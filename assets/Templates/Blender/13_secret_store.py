import os
from typing import Any, Optional
from datetime import datetime
import logging


class SecretStore:
    """Secret Store for managing sensitive configuration and API keys"""

    def __init__(self, config: Optional[dict[str, Any]] = None):
        self.config = config or {}
        self.secrets = {}
        self.logger = logging.getLogger(__name__)
        self._load_secrets()

    def _load_secrets(self):
        """Load secrets from environment variables and config"""
        # Load from environment variables
        env_secrets = {
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
            "google_api_key": os.getenv("GOOGLE_API_KEY"),
            "database_url": os.getenv("DATABASE_URL"),
            "redis_url": os.getenv("REDIS_URL"),
            "jwt_secret": os.getenv("JWT_SECRET"),
            "encryption_key": os.getenv("ENCRYPTION_KEY"),
        }

        # Filter out None values
        self.secrets = {k: v for k, v in env_secrets.items() if v is not None}

        # Load additional secrets from config
        if "secrets" in self.config:
            self.secrets.update(self.config["secrets"])

        self.logger.info(f"Loaded {len(self.secrets)} secrets")

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a secret by key"""
        secret = self.secrets.get(key, default)
        if secret is None:
            self.logger.warning(f"Secret '{key}' not found")
        return secret

    def set_secret(self, key: str, value: str) -> None:
        """Set a secret (runtime only, not persisted)"""
        self.secrets[key] = value
        self.logger.info(f"Secret '{key}' updated")

    def has_secret(self, key: str) -> bool:
        """Check if a secret exists"""
        return key in self.secrets and self.secrets[key] is not None

    def get_database_config(self) -> dict[str, Any]:
        """Get database configuration"""
        return {
            "url": self.get_secret("database_url", "sqlite:///./app.db"),
            "echo": False,
            "pool_pre_ping": True,
        }

    def get_redis_config(self) -> dict[str, Any]:
        """Get Redis configuration"""
        return {
            "url": self.get_secret("redis_url", "redis://localhost:6379"),
            "decode_responses": True,
        }

    def get_jwt_config(self) -> dict[str, Any]:
        """Get JWT configuration"""
        return {
            "secret": self.get_secret(
                "jwt_secret", "default-jwt-secret-change-in-production"
            ),
            "algorithm": "HS256",
            "expire_minutes": 30,
        }

    def get_api_keys(self) -> dict[str, str]:
        """Get all API keys (filtered)"""
        api_keys = {}
        for key, value in self.secrets.items():
            if "api_key" in key.lower() and value:
                api_keys[key] = value
        return api_keys

    def validate_required_secrets(self, required_keys: list[str]) -> dict[str, bool]:
        """Validate that required secrets are present"""
        validation_result = {}
        for key in required_keys:
            validation_result[key] = self.has_secret(key)
            if not validation_result[key]:
                self.logger.error(f"Required secret '{key}' is missing")
        return validation_result

    def get_encryption_key(self) -> str:
        """Get encryption key for sensitive data"""
        return (
            self.get_secret(
                "encryption_key", "default-encryption-key-change-in-production"
            )
            or "default-encryption-key-change-in-production"
        )

    def mask_secret(self, secret: str) -> str:
        """Mask a secret for logging purposes"""
        if not secret or len(secret) < 8:
            return "***"
        return secret[:4] + "*" * (len(secret) - 8) + secret[-4:]

    def get_status(self) -> dict[str, Any]:
        """Get secret store status"""
        return {
            "total_secrets": len(self.secrets),
            "available_secrets": list(self.secrets.keys()),
            "masked_values": {k: self.mask_secret(v) for k, v in self.secrets.items()},
            "timestamp": datetime.now().isoformat(),
        }
