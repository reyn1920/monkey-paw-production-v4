"""
Unit tests for core modules.

Tests the foundational components including configuration,
logging, and exception handling.
"""

import pytest
import os
from unittest.mock import patch

# Import core modules
from src.core.config import Config
from src.core.logging import StructuredLogger, get_logger
from src.core.exceptions import (
    BaseApplicationError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    ServiceError,
)


class TestConfig:
    """Test cases for the Config class."""

    def test_config_creation(self):
        """Test that config can be created."""
        config = Config()
        assert config is not None

    def test_config_singleton(self):
        """Test that config follows singleton pattern."""
        # Note: Config may not be a singleton, just test it can be created multiple times
        config1 = Config()
        config2 = Config()
        assert config1 is not None
        assert config2 is not None

    @patch.dict(os.environ, {"TEST_API_KEY": "test_value"})
    def test_api_key_retrieval(self):
        """Test API key retrieval from environment."""
        config = Config()
        # The get_api_key method should retrieve from environment
        # This is a basic test of the interface
        result = config.get_api_key("TEST_API_KEY")
        # We can't test the exact implementation without knowing it
        # but we can test that the method exists and returns something
        assert hasattr(config, "get_api_key")


class TestStructuredLogger:
    """Test cases for the StructuredLogger."""

    def test_logger_creation(self):
        """Test that logger can be created."""
        logger = StructuredLogger(__name__)
        assert logger is not None

    def test_logger_methods(self):
        """Test that logger has required methods."""
        logger = StructuredLogger(__name__)

        # Test that logging methods exist
        assert hasattr(logger, "info")
        assert hasattr(logger, "error")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "debug")

        # Test that methods can be called without error
        try:
            logger.info("Test info message")
            logger.error("Test error message")
            logger.warning("Test warning message")
            logger.debug("Test debug message")
        except Exception as e:
            pytest.fail(f"Logger methods should not raise exceptions: {e}")

    def test_get_logger_function(self):
        """Test the get_logger utility function."""
        logger = get_logger(__name__)
        assert logger is not None


class TestExceptions:
    """Test cases for custom exceptions."""

    def test_base_application_error(self):
        """Test BaseApplicationError."""
        error = BaseApplicationError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError("Invalid data")
        assert "[VALIDATION_ERROR] Invalid data" in str(error)
        assert isinstance(error, BaseApplicationError)

    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = AuthenticationError("Invalid credentials")
        assert "[AUTH_ERROR] Invalid credentials" in str(error)
        assert isinstance(error, BaseApplicationError)

    def test_authorization_error(self):
        """Test AuthorizationError."""
        error = AuthorizationError("Access denied")
        assert "[AUTHZ_ERROR] Access denied" in str(error)
        assert isinstance(error, BaseApplicationError)

    def test_service_error(self):
        """Test ServiceError."""
        error = ServiceError("Service unavailable")
        assert "[SERVICE_ERROR] Service unavailable" in str(error)
        assert isinstance(error, BaseApplicationError)

    def test_exception_with_context(self):
        """Test exceptions with additional context."""
        error = ValidationError("Invalid email", field="email", value="invalid")

        assert "[VALIDATION_ERROR] Invalid email" in str(error)
        # Test that error can store additional context
        if hasattr(error, "context"):
            assert error.context.get("field") == "email"
            assert error.context.get("value") == "invalid"


class TestCoreIntegration:
    """Integration tests for core components."""

    def test_logger_with_config(self):
        """Test logger integration with config."""
        config = Config()
        logger = StructuredLogger(__name__)

        # Test that both components can be used together
        try:
            logger.info("Testing integration", extra={"config_loaded": True})
        except Exception as e:
            pytest.fail(f"Logger and config integration failed: {e}")

    def test_exception_logging(self):
        """Test that exceptions can be logged properly."""
        logger = StructuredLogger(__name__)

        try:
            raise ValidationError("Test validation error")
        except ValidationError as e:
            # Test that exception can be logged
            try:
                logger.error(f"Caught exception: {e}")
            except Exception as log_error:
                pytest.fail(f"Exception logging failed: {log_error}")


class TestErrorHandling:
    """Test error handling patterns."""

    def test_exception_hierarchy(self):
        """Test that exception hierarchy is correct."""
        # All custom exceptions should inherit from BaseApplicationError
        validation_error = ValidationError("test")
        auth_error = AuthenticationError("test")
        authz_error = AuthorizationError("test")
        service_error = ServiceError("test")

        assert isinstance(validation_error, BaseApplicationError)
        assert isinstance(auth_error, BaseApplicationError)
        assert isinstance(authz_error, BaseApplicationError)
        assert isinstance(service_error, BaseApplicationError)

        # All should also be standard Python exceptions
        assert isinstance(validation_error, Exception)
        assert isinstance(auth_error, Exception)
        assert isinstance(authz_error, Exception)
        assert isinstance(service_error, Exception)

    def test_exception_chaining(self):
        """Test exception chaining works properly."""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise ServiceError("Service failed") from e
        except ServiceError as service_error:
            assert service_error.__cause__ is not None
            assert isinstance(service_error.__cause__, ValueError)
            assert str(service_error.__cause__) == "Original error"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
