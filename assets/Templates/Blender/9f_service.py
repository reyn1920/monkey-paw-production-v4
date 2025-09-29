"""
Authentication service layer.

This module provides the business logic for user authentication, registration,
and user management operations.

Author: TRAE.AI System
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Any
import uuid
import logging

from .models import UserCreate, UserInDB, UserResponse, UserUpdate, LoginRequest
from .security import password_manager, jwt_manager

logger = logging.getLogger(__name__)


class UserService:
    """User service for managing user operations"""

    def __init__(self):
        # In-memory storage (replace with database in production)
        self.users_db: dict[str, UserInDB] = {}
        self.sessions_db: dict[str, dict[str, Any]] = {}

    def create_user(self, user_data: UserCreate) -> UserInDB:
        """Create a new user"""
        # Check if user already exists
        if self.get_user_by_username(user_data.username):
            raise ValueError("Username already registered")

        if self.get_user_by_email(user_data.email):
            raise ValueError("Email already registered")

        # Hash password
        hashed_password = password_manager.hash_password(user_data.password)

        # Create user
        user_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        user = UserInDB(
            id=user_id,
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            is_active=True,
            roles=user_data.roles,
            created_at=now,
            updated_at=now,
            last_login=None,
            login_attempts=0,
            locked_until=None,
            email_verified=False,
            profile_data={},
        )

        self.users_db[user_id] = user
        logger.info(f"User created: {user_data.username}")

        return user

    def get_user_by_username(self, username: str) -> Optional[UserInDB]:
        """Get user by username"""
        for user in self.users_db.values():
            if user.username == username:
                return user
        return None

    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get user by email"""
        for user in self.users_db.values():
            if user.email == email:
                return user
        return None

    def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        """Get user by ID"""
        return self.users_db.get(user_id)

    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        """Authenticate user with username and password"""
        user = self.get_user_by_username(username)
        if not user:
            return None

        if not user.is_active:
            return None

        # Check if account is locked
        if user.locked_until and datetime.now(timezone.utc) < user.locked_until:
            return None

        # Verify password
        if not password_manager.verify_password(password, user.hashed_password):
            # Increment login attempts
            user.login_attempts += 1
            if user.login_attempts >= 5:
                user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)

            self.users_db[user.id] = user
            return None

        # Reset login attempts on successful login
        user.login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.now(timezone.utc)
        self.users_db[user.id] = user

        return user

    def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[UserInDB]:
        """Update user information"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        # Update user data
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        user.updated_at = datetime.now(timezone.utc)
        self.users_db[user_id] = user

        logger.info(f"User updated: {user.username}")
        return user

    def change_password(
        self, user_id: str, current_password: str, new_password: str
    ) -> bool:
        """Change user password"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        # Verify current password
        if not password_manager.verify_password(current_password, user.hashed_password):
            return False

        # Hash new password
        user.hashed_password = password_manager.hash_password(new_password)
        user.updated_at = datetime.now(timezone.utc)
        self.users_db[user_id] = user

        logger.info(f"Password changed for user: {user.username}")
        return True

    def list_users(self) -> list[UserInDB]:
        """List all users"""
        return list(self.users_db.values())

    def to_user_response(self, user: UserInDB) -> UserResponse:
        """Convert UserInDB to UserResponse"""
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            roles=user.roles,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
            email_verified=user.email_verified,
        )


class AuthService:
    """Authentication service for token management"""

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def login(self, login_data: LoginRequest) -> Optional[dict[str, Any]]:
        """Login user and return token data"""
        user = self.user_service.authenticate_user(
            login_data.username, login_data.password
        )

        if not user:
            return None

        # Create tokens
        token_response = jwt_manager.create_token_response(
            user_id=user.id,
            username=user.username,
            roles=[role.value for role in user.roles],
            user_info={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "roles": [role.value for role in user.roles],
            },
        )

        return {
            "access_token": token_response.access_token,
            "refresh_token": token_response.refresh_token,
            "token_type": token_response.token_type,
            "expires_in": token_response.expires_in,
            "user": self.user_service.to_user_response(user),
        }

    def refresh_token(self, refresh_token: str) -> Optional[dict[str, Any]]:
        """Refresh access token"""
        try:
            # Verify refresh token
            token_data = jwt_manager.verify_token(refresh_token)

            if token_data.token_type != "refresh":
                return None

            # Get user
            user = self.user_service.get_user_by_id(token_data.user_id)
            if not user or not user.is_active:
                return None

            # Create new tokens
            token_response = jwt_manager.create_token_response(
                user_id=user.id,
                username=user.username,
                roles=[role.value for role in user.roles],
                user_info={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "roles": [role.value for role in user.roles],
                },
            )

            return {
                "access_token": token_response.access_token,
                "refresh_token": token_response.refresh_token,
                "token_type": token_response.token_type,
                "expires_in": token_response.expires_in,
                "user": self.user_service.to_user_response(user),
            }

        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            return None


# Global service instances
user_service = UserService()
auth_service = AuthService(user_service)

# Export services
__all__ = ["UserService", "AuthService", "user_service", "auth_service"]
