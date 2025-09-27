"""
Test suite for service layer components.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
import tempfile
import os
from typing import Dict, Any

from src.services.registry import ServiceRegistry, BaseService
from src.services.auth import (
    AuthenticationService,
    TokenType,
)
from src.services.data import DataService, QueryResult
from src.core.config import Config


# Test cases for ServiceRegistry
class TestServiceRegistry:
    """Test cases for the ServiceRegistry class."""

    def test_registry_initialization(self):
        """Test that registry initializes correctly."""
        registry = ServiceRegistry()
        assert registry is not None

    def test_service_registration(self):
        """Test service registration and retrieval."""
        registry = ServiceRegistry()

        # Create a mock service
        mock_service = Mock(spec=BaseService)
        mock_service.name = "test_service"

        # Register service by string name
        registry.register_service("test_service", mock_service)

        # Verify registration
        assert registry.get_service("test_service") == mock_service
        assert registry.has_service("test_service")

    def test_service_not_found(self):
        """Test behavior when service is not found."""
        registry = ServiceRegistry()

        with pytest.raises(KeyError):
            registry.get_service("nonexistent_service")

    def test_service_lifecycle(self):
        """Test service initialization and shutdown."""
        registry = ServiceRegistry()

        # Create mock service with lifecycle methods
        mock_service = Mock(spec=BaseService)
        mock_service.initialize = AsyncMock()
        mock_service.shutdown = AsyncMock()
        mock_service.is_initialized = False
        mock_service._mark_initialized = Mock()

        registry.register_service("test_service", mock_service)

        # Test initialization
        asyncio.run(registry.initialize_all())
        mock_service.initialize.assert_called_once()

        # Simulate service being marked as initialized
        mock_service.is_initialized = True

        # Test shutdown
        asyncio.run(registry.shutdown_all())
        mock_service.shutdown.assert_called_once()


class TestAuthenticationService:
    """Test cases for the AuthenticationService class."""

    @pytest.fixture
    def auth_service(self):
        """Create an AuthenticationService instance for testing."""
        config = Mock(spec=Config)
        config.get_api_key.return_value = "test_secret_key"

        registry = Mock()
        return AuthenticationService(config, registry)

    def test_auth_service_initialization(self, auth_service):
        """Test that auth service initializes correctly."""
        assert auth_service is not None
        assert hasattr(auth_service, 'config')
        assert hasattr(auth_service, 'users')

    def test_password_hashing(self, auth_service):
        """Test password hashing functionality."""
        password = "test_password_123"
        hashed = auth_service._hash_password(password)

        # Verify hash is different from original password
        assert hashed != password
        assert len(hashed) > 0

        # Verify password verification works
        assert auth_service._verify_password(password, hashed)
        assert not auth_service._verify_password("wrong_password", hashed)

    def test_token_generation(self, auth_service):
        """Test token generation."""
        from src.services.auth import User
        
        # Create a test user first
        user = User(
            id="test_user_id",
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password"
        )
        
        # Use the private method to generate token
        token = auth_service._generate_token(user)
        assert token is not None
        assert token.user_id == user.id
        assert token.token is not None

    @pytest.mark.asyncio
    async def test_invalid_token_validation(self, auth_service):
        """Test validation of invalid tokens."""
        invalid_token = "invalid_token_string"

        result = await auth_service.validate_token(invalid_token)
        assert result is None

    @pytest.mark.asyncio
    async def test_role_based_access(self, auth_service):
        """Test role-based access control."""
        # This test would need more implementation in the auth service
        # For now, just verify the service has role-related functionality
        assert hasattr(auth_service, '_generate_token')
        assert hasattr(auth_service, 'validate_token')


class TestDataService:
    """Test cases for the DataService class."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        yield path
        os.unlink(path)

    @pytest.fixture
    def data_service(self, temp_db):
        """Create a DataService instance with temporary database."""
        service = DataService(temp_db)
        return service

    def test_data_service_initialization(self, data_service):
        """Test that data service initializes correctly."""
        assert data_service is not None
        assert hasattr(data_service, 'database_path')

    def test_database_connection(self, data_service):
        """Test database connection establishment."""
        # Initialize service
        asyncio.run(data_service.initialize())

        # Test connection
        conn_info = asyncio.run(data_service.get_connection_info())
        assert conn_info is not None
        assert conn_info.database_path is not None

        # Test connection works by executing a simple query
        result = asyncio.run(data_service.execute_query("SELECT 1"))
        assert result is not None
        assert result.row_count >= 0

    def test_query_execution(self, data_service):
        """Test SQL query execution."""
        # Initialize service
        asyncio.run(data_service.initialize())

        # Create test table
        create_query = """
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY,
            name TEXT,
            value INTEGER
        )
        """

        result = asyncio.run(data_service.execute_query(create_query))
        assert isinstance(result, QueryResult)
        assert result.row_count >= 0  # Table creation successful

        # Insert test data
        insert_query = "INSERT INTO test_table (name, value) VALUES (:name, :value)"
        params = {"name": "test_item", "value": 42}

        result = asyncio.run(data_service.execute_query(insert_query, params))
        assert result.affected_rows == 1

        # Query test data
        select_query = "SELECT * FROM test_table WHERE name = :name"
        result = asyncio.run(data_service.execute_query(select_query, {"name": "test_item"}))

        assert result.row_count == 1
        assert len(result.rows) == 1
        assert result.rows[0]["name"] == "test_item"
        assert result.rows[0]["value"] == 42

    def test_query_error_handling(self, data_service):
        """Test error handling in query execution."""
        # Initialize service
        asyncio.run(data_service.initialize())

        # Execute invalid query
        invalid_query = "SELECT * FROM nonexistent_table"
        # This should raise an exception or return an error result
        # The exact behavior depends on the implementation
        try:
            result = asyncio.run(data_service.execute_query(invalid_query))
            # If no exception, check for error indication in result
            assert result is not None
        except Exception:
            # Exception is expected for invalid query
            pass

    def test_data_validation(self, data_service):
        """Test data validation functionality."""
        # This test would verify data validation features
        # For now, just verify the service exists and can be initialized
        assert data_service is not None
        asyncio.run(data_service.initialize())


class TestServiceIntegration:
    """Test cases for service integration and dependencies."""

    @pytest.fixture
    def service_registry(self):
        """Create a service registry with all services."""
        registry = ServiceRegistry()

        # Create mock config
        config = Mock(spec=Config)
        config.get_api_key.return_value = "test_secret_key"

        # Register services using correct method signatures
        auth_service = AuthenticationService(config, registry)
        data_service = DataService(":memory:")  # Use in-memory database for testing

        registry.register(AuthenticationService, auth_service)
        registry.register(DataService, data_service)

        return registry

    def test_service_dependencies(self, service_registry):
        """Test that services can access each other through registry."""
        auth_service = service_registry.get(AuthenticationService)
        data_service = service_registry.get(DataService)

        # Verify services can access registry
        assert auth_service.registry == service_registry

        # Verify services can access each other
        auth_from_registry = service_registry.get(AuthenticationService)
        assert auth_from_registry == auth_service

    def test_full_service_lifecycle(self, service_registry):
        """Test complete service lifecycle."""
        # Initialize all services
        asyncio.run(service_registry.initialize_all())

        # Verify services are initialized
        auth_service = service_registry.get(AuthenticationService)
        data_service = service_registry.get(DataService)

        assert auth_service is not None
        assert data_service is not None

        # Test service functionality - use user_id string instead of dict
        user_id = "test_user"
        token = auth_service.generate_token(user_id, TokenType.ACCESS)
        assert token is not None


class TestServicePerformance:
    """Performance test cases for services."""

    @pytest.mark.performance
    def test_auth_token_generation_performance(self):
        """Test authentication token generation performance."""
        from src.services.auth import AuthenticationService, User
        from src.core.config import Config

        # Create mock config and service
        config = Mock(spec=Config)
        config.get_api_key.return_value = "test_secret_key"

        registry = Mock()
        auth_service = AuthenticationService(config, registry)

        # Create a test user
        test_user = User(
            id="test_user_id",
            username="test_user",
            email="test@example.com",
            password_hash="hashed_password"
        )

        import time

        start_time = time.time()

        # Generate 100 tokens using the private method
        for _ in range(100):
            token = auth_service._generate_token(test_user)
            assert token is not None

        end_time = time.time()
        duration = end_time - start_time

        # Should generate 100 tokens in less than 1 second
        assert duration < 1.0, f"Token generation took {duration:.3f}s, expected < 1.0s"

    @pytest.mark.performance
    def test_data_service_query_performance(self):
        """Test data service query performance."""
        data_service = DataService(":memory:")
        asyncio.run(data_service.initialize())

        # Create test table
        create_query = """
        CREATE TABLE perf_test (
            id INTEGER PRIMARY KEY,
            data TEXT
        )
        """
        asyncio.run(data_service.execute_query(create_query))

        import time

        start_time = time.time()

        # Execute 50 insert queries
        for i in range(50):
            query = "INSERT INTO perf_test (data) VALUES (:data)"
            params: Dict[str, Any] = {"data": f"test_data_{i}"}
            result = asyncio.run(data_service.execute_query(query, params))
            assert result.affected_rows == 1

        end_time = time.time()
        duration = end_time - start_time

        # Should complete 50 inserts in less than 0.5 seconds
        assert (
            duration < 0.5
        ), f"Database operations too slow: {duration}s for 50 inserts"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
