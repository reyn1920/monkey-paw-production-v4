"""
SecretStoreBridge - Secure secret management for TRAE.AI applications
"""

import os
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


class SecretStoreBridge:
    """Bridge for managing secrets and environment variables securely."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the SecretStoreBridge.

        Args:
            config_path: Optional path to configuration file
        """
        self.config_path = config_path or os.path.join(os.getcwd(), ".env")
        self.secrets = {}
        self._load_secrets()

    def _load_secrets(self):
        """Load secrets from environment and configuration files."""
        # Load from environment variables
        for key, value in os.environ.items():
            if key.startswith(("API_", "SECRET_", "TOKEN_", "KEY_")):
                self.secrets[key] = value

        # Load from .env file if it exists
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            self.secrets[key.strip()] = value.strip()
            except Exception as e:
                logger.warning(
                    f"Could not load secrets from {
                        self.config_path}: {e}"
                )

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a secret value by key.

        Args:
            key: The secret key to retrieve
            default: Default value if key not found

        Returns:
            The secret value or default
        """
        return self.secrets.get(key, default)

    def set_secret(self, key: str, value: str):
        """Set a secret value.

        Args:
            key: The secret key
            value: The secret value
        """
        self.secrets[key] = value

    def has_secret(self, key: str) -> bool:
        """Check if a secret exists.

        Args:
            key: The secret key to check

        Returns:
            True if secret exists, False otherwise
        """
        return key in self.secrets

    def list_secrets(self) -> List[str]:
        """List all secret keys (not values for security).

        Returns:
            List of secret keys
        """
        return list(self.secrets.keys())

    def validate_required_secrets(self, required_keys: List[str]) -> bool:
        """Validate that all required secrets are present.

        Args:
            required_keys: List of required secret keys

        Returns:
            True if all required secrets are present
        """
        missing_keys = [key for key in required_keys if key not in self.secrets]
        if missing_keys:
            logger.error(f"Missing required secrets: {missing_keys}")
            return False
        return True
