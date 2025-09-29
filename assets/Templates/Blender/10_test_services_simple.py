"""
Simple unit tests for the services layer.

Tests basic functionality of services with minimal mocking.
"""

import pytest
import tempfile
import os
from unittest.mock import Mock

# Import services
from src.services.registry import ServiceRegistry, get_service_registry
from src.services.auth import AuthenticationService, UserRole
from src.services.data import DataService
from src.services.data_blueprint import DatabaseConfig
from src.core.config import Config


class TestServiceRegistry:
    """Test cases for the ServiceRegistry."""

    def test_registry_creation(self):
        """Test that registry can be created."""
        registry = ServiceRegistry()
        assert registry is not None

    def test_get_service_registry(self):
        """Test global service registry access."""
        registry = get_service_registry()
        assert registry is not None
        assert isinstance(registry, ServiceRegistry)

    def test_service_registration_by_type(self):
        """Test service registration using type-based approach."""
        registry = ServiceRegistry()

        # Create a mock config
        config = Mock(spec=Config)
        config.get_api_key.return_value = "test_secret"

        # Register service using factory
        def create_auth_service():
            return AuthenticationService(config, registry)

        registry.register_factory(AuthenticationService, create_auth_service)

        # Get service
        auth_service = registry.get(AuthenticationService)
        assert auth_service is not None
        assert isinstance(auth_service, AuthenticationService)


class TestAuthenticationService:
    """Test cases for the AuthenticationService."""

    @pytest.fixture
    def mock_config(self):
        """Create a mock config for testing."""
        config = Mock(spec=Config)
        config.get_api_key.return_value = "test_secret_key_12345"
        return config

    @pytest.fixture
    def auth_service(self, mock_config):
        """Create an AuthenticationService instance for testing."""
        registry = ServiceRegistry()
        service = AuthenticationService(mock_config, registry)
        return service

    def test_auth_service_creation(self, auth_service):
        """Test that auth service can be created."""
        assert auth_service is not None

    def test_password_hashing(self, auth_service):
        """Test password hashing functionality."""
        password = "test_password_123"

        # Hash password
        hashed = auth_service._hash_password(password)

        # Verify it's different from original
        assert hashed != password
        assert len(hashed) > 0

        # Verify password verification works
        assert auth_service._verify_password(password, hashed) is True
        assert auth_service._verify_password("wrong_password", hashed) is False

    @pytest.mark.asyncio
    async def test_user_registration(self, auth_service):
        """Test user registration."""
        username = "testuser"
        email = "test@example.com"
        password = "testpass123"

        # Register user
        user = await auth_service.register_user(username, email, password, [UserRole.USER.value])

        # Verify user was created
        assert user is not None
        assert user.username == username
        assert user.email == email
        assert UserRole.USER.value in user.roles
        assert user.is_active is True

    @pytest.mark.asyncio
    async def test_user_authentication(self, auth_service):
        """Test user authentication."""
        username = "testuser"
        email = "test@example.com"
        password = "testpass123"

        # Register user first
        user = await auth_service.register_user(username, email, password, [UserRole.USER.value])

        # Authenticate user
        token = await auth_service.authenticate(username, password)

        # Verify authentication
        assert token is not None
        assert token.user_id == user.id
        assert len(token.token) > 0

    @pytest.mark.asyncio
    async def test_token_validation(self, auth_service):
        """Test token validation."""
        username = "testuser"
        email = "test@example.com"
        password = "testpass123"

        # Register and authenticate user
        user = await auth_service.register_user(username, email, password, [UserRole.USER.value])
        token = await auth_service.authenticate(username, password)

        # Validate token
        validated_user = await auth_service.validate_token(token.token)

        # Verify validation
        assert validated_user is not None
        assert validated_user.id == user.id
        assert validated_user.username == username


class TestDataService:
    """Test cases for the DataService."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_path = f.name
        yield temp_path
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    @pytest.fixture
    def mock_config(self):
        """Create a mock configuration."""
        config = Mock()
        config.database_path = ":memory:"
        return config

    def test_data_service_creation(self, temp_db):
        """Test that DataService can be created."""
        service = DataService(database_path=temp_db)
        assert service is not None
        assert isinstance(service, DataService)

    def test_data_service_initialization(self, temp_db):
        """Test that DataService initializes properly."""
        service = DataService(database_path=temp_db)
        # Test that the service has the expected attributes
        assert hasattr(service, 'database_path')
        assert service.database_path == temp_db

    def test_database_operations(self, temp_db):
        """Test basic database operations."""
        service = DataService(database_path=temp_db)
        # This is a basic test - in a real scenario, you'd test actual database operations
        assert service is not None

    @pytest.fixture
    def data_service(self, temp_db):
        """Create a DataService instance for testing."""
        return DataService(database_path=temp_db)

    @pytest.mark.asyncio
    async def test_service_initialization(self, data_service):
        """Test service initialization."""
        await data_service.initialize()
        assert data_service.is_initialized is True

    @pytest.mark.asyncio
    async def test_database_operations(self, data_service):
        """Test basic database operations."""
        # Initialize service
        await data_service.initialize()

        # Create test table
        create_query = """
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            value INTEGER
        )
        """

        result = await data_service.execute_query(create_query)
        assert result.row_count >= 0  # CREATE TABLE doesn't return rows

        # Insert test data
        insert_query = "INSERT INTO test_table (name, value) VALUES (?, ?)"
        params = ("test_item", 42)

        result = await data_service.execute_query(insert_query, params)
        assert result.affected_rows == 1

        # Query test data
        select_query = "SELECT * FROM test_table WHERE name = ?"
        result = await data_service.execute_query(select_query, ("test_item",))

        assert result.row_count == 1
        assert len(result.rows) == 1
        assert result.rows[0]["name"] == "test_item"
        assert result.rows[0]["value"] == 42


class TestServiceIntegration:
    """Integration tests for services working together."""

    @pytest.fixture
    def mock_config(self):
        """Create a mock config for testing."""
        config = Mock(spec=Config)
        config.get_api_key.return_value = "test_secret_key_12345"
        return config

    @pytest.fixture
    def service_registry(self, mock_config):
        """Create a service registry with services."""
        registry = ServiceRegistry()

        # Register services using factories
        def create_auth_service():
            return AuthenticationService(mock_config, registry)

        def create_data_service():
            return DataService(database_path=":memory:")

        registry.register_factory(AuthenticationService, create_auth_service)
        registry.register_factory(DataService, create_data_service)

        return registry

    def test_service_retrieval(self, service_registry):
        """Test that services can be retrieved from registry."""
        auth_service = service_registry.get(AuthenticationService)
        data_service = service_registry.get(DataService)

        assert auth_service is not None
        assert data_service is not None
        assert isinstance(auth_service, AuthenticationService)
        assert isinstance(data_service, DataService)

    @pytest.mark.asyncio
    async def test_service_lifecycle(self, service_registry):
        """Test service lifecycle management."""
        # Initialize all services
        await service_registry.initialize_all()

        # Verify services are initialized
        auth_service = service_registry.get(AuthenticationService)
        data_service = service_registry.get(DataService)

        assert auth_service.is_initialized is True
        assert data_service.is_initialized is True

        # Shutdown all services
        await service_registry.shutdown_all()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
