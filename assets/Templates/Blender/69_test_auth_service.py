"""Tests for AuthService."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.services.auth_service import AuthService
from src.backend.domain.models import User, UserRole


@pytest.fixture
def mock_session():
    """Mock async session."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def sample_user():
    """Sample user for testing."""
    user = MagicMock(spec=User)
    user.id = "test-user-id"
    user.email = "test@example.com"
    user.first_name = "Test"
    user.last_name = "User"
    user.is_active = True
    user.hashed_password = AuthService.get_password_hash("testpassword")
    return user


class TestAuthService:
    """Test cases for AuthService."""
    
    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "testpassword"
        hashed = AuthService.get_password_hash(password)
        assert AuthService.verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "testpassword"
        wrong_password = "wrongpassword"
        hashed = AuthService.get_password_hash(password)
        assert AuthService.verify_password(wrong_password, hashed) is False
    
    def test_get_password_hash(self):
        """Test password hashing."""
        password = "testpassword"
        hashed = AuthService.get_password_hash(password)
        assert hashed != password
        assert len(hashed) > 0
    
    def test_create_access_token(self):
        """Test access token creation."""
        data = {"sub": "test@example.com"}
        token = AuthService.create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_token_valid(self):
        """Test token verification with valid token."""
        data = {"sub": "test@example.com"}
        token = AuthService.create_access_token(data)
        email = AuthService.verify_token(token)
        assert email == "test@example.com"
    
    def test_verify_token_invalid(self):
        """Test token verification with invalid token."""
        invalid_token = "invalid.token.here"
        email = AuthService.verify_token(invalid_token)
        assert email is None
    
    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, mock_session, sample_user):
        """Test successful user authentication."""
        # Mock the get_user_by_email method
        AuthService.get_user_by_email = AsyncMock(return_value=sample_user)
        
        result = await AuthService.authenticate_user(
            mock_session, "test@example.com", "testpassword"
        )
        
        assert result == sample_user
        AuthService.get_user_by_email.assert_called_once_with(mock_session, "test@example.com")
    
    @pytest.mark.asyncio
    async def test_authenticate_user_not_found(self, mock_session):
        """Test authentication with non-existent user."""
        # Mock the get_user_by_email method to return None
        AuthService.get_user_by_email = AsyncMock(return_value=None)
        
        result = await AuthService.authenticate_user(
            mock_session, "nonexistent@example.com", "password"
        )
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_authenticate_user_inactive(self, mock_session, sample_user):
        """Test authentication with inactive user."""
        sample_user.is_active = False
        AuthService.get_user_by_email = AsyncMock(return_value=sample_user)
        
        result = await AuthService.authenticate_user(
            mock_session, "test@example.com", "testpassword"
        )
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self, mock_session, sample_user):
        """Test authentication with wrong password."""
        AuthService.get_user_by_email = AsyncMock(return_value=sample_user)
        
        result = await AuthService.authenticate_user(
            mock_session, "test@example.com", "wrongpassword"
        )
        
        assert result is None