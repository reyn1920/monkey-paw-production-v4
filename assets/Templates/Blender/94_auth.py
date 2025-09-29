"""
Authentication system for the application.
Provides user authentication, authorization, and session management.
"""

import secrets
import jwt
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import bcrypt
import asyncio
from functools import wraps
import logging
from typing import Optional
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserRole(Enum):
    """User roles for authorization."""

    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"
    MODERATOR = "moderator"


class AuthStatus(Enum):
    """Authentication status."""

    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid_credentials"
    USER_NOT_FOUND = "user_not_found"
    ACCOUNT_LOCKED = "account_locked"
    TOKEN_EXPIRED = "token_expired"
    INSUFFICIENT_PERMISSIONS = "insufficient_permissions"


@dataclass
class User:
    """User data model."""

    id: str
    username: str
    email: str
    password_hash: str
    role: UserRole
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None


@dataclass
class Session:
    """User session data model."""

    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True


@dataclass
class AuthResult:
    """Authentication result."""

    status: AuthStatus
    user: Optional[User] = None
    token: Optional[str] = None
    session: Optional[Session] = None
    message: str = ""


class PasswordManager:
    """Handles password hashing and verification."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    @staticmethod
    def generate_secure_token() -> str:
        """Generate a secure random token."""
        return secrets.token_urlsafe(32)


class JWTManager:
    """Handles JWT token creation and validation."""

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(
        self, user_id: str, role: UserRole, expires_in_hours: int = 24
    ) -> str:
        """Create a JWT token for a user."""
        payload = {
            "user_id": user_id,
            "role": role.value,
            "exp": datetime.utcnow() + timedelta(hours=expires_in_hours),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[dict[str, Any]]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None


class SessionManager:
    """Manages user sessions."""

    def __init__(self):
        self.sessions: dict[str, Session] = {}

    def create_session(
        self, user_id: str, ip_address: str, user_agent: str, expires_in_hours: int = 24
    ) -> Session:
        """Create a new user session."""
        session_id = secrets.token_urlsafe(32)
        session = Session(
            session_id=session_id,
            user_id=user_id,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=expires_in_hours),
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        session = self.sessions.get(session_id)
        if session and session.expires_at > datetime.now() and session.is_active:
            return session
        return None

    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate a session."""
        if session_id in self.sessions:
            self.sessions[session_id].is_active = False
            return True
        return False

    def cleanup_expired_sessions(self):
        """Remove expired sessions."""
        current_time = datetime.now()
        expired_sessions = [
            sid
            for sid, session in self.sessions.items()
            if session.expires_at <= current_time
        ]
        for sid in expired_sessions:
            del self.sessions[sid]


class UserManager:
    """Manages user accounts."""

    def __init__(self):
        self.users: dict[str, User] = {}
        self.users_by_email: dict[str, str] = {}  # email -> user_id mapping
        self.password_manager = PasswordManager()

    def create_user(
        self, username: str, email: str, password: str, role: UserRole = UserRole.USER
    ) -> User:
        """Create a new user account."""
        if email in self.users_by_email:
            raise ValueError("Email already exists")

        user_id = secrets.token_urlsafe(16)
        password_hash = self.password_manager.hash_password(password)

        user = User(
            id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            created_at=datetime.now(),
        )

        self.users[user_id] = user
        self.users_by_email[email] = user_id

        logger.info(f"Created user: {username} ({email})")
        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        user_id = self.users_by_email.get(email)
        return self.users.get(user_id) if user_id else None

    def update_user_role(self, user_id: str, new_role: UserRole) -> bool:
        """Update a user's role."""
        user = self.get_user_by_id(user_id)
        if user:
            user.role = new_role
            logger.info(
                f"Updated role for user {
                    user.username} to {
                    new_role.value}"
            )
            return True
        return False

    def lock_user_account(self, user_id: str, lock_duration_hours: int = 1):
        """Lock a user account temporarily."""
        user = self.get_user_by_id(user_id)
        if user:
            user.locked_until = datetime.now() + timedelta(hours=lock_duration_hours)
            logger.warning(f"Locked user account: {user.username}")

    def is_account_locked(self, user: User) -> bool:
        """Check if a user account is locked."""
        if user.locked_until and user.locked_until > datetime.now():
            return True
        return False


class AuthenticationSystem:
    """Main authentication system."""

    def __init__(self, jwt_secret: str):
        self.user_manager = UserManager()
        self.session_manager = SessionManager()
        self.jwt_manager = JWTManager(jwt_secret)
        self.password_manager = PasswordManager()
        self.max_failed_attempts = 5

    async def authenticate(
        self, email: str, password: str, ip_address: str = "", user_agent: str = ""
    ) -> AuthResult:
        """Authenticate a user with email and password."""
        user = self.user_manager.get_user_by_email(email)

        if not user:
            return AuthResult(
                status=AuthStatus.USER_NOT_FOUND, message="User not found"
            )

        if not user.is_active:
            return AuthResult(
                status=AuthStatus.ACCOUNT_LOCKED, message="Account is deactivated"
            )

        if self.user_manager.is_account_locked(user):
            return AuthResult(
                status=AuthStatus.ACCOUNT_LOCKED,
                message="Account is temporarily locked",
            )

        if not self.password_manager.verify_password(password, user.password_hash):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= self.max_failed_attempts:
                self.user_manager.lock_user_account(user.id)

            return AuthResult(
                status=AuthStatus.INVALID_CREDENTIALS, message="Invalid credentials"
            )

        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.last_login = datetime.now()

        # Create session and token
        session = self.session_manager.create_session(user.id, ip_address, user_agent)
        token = self.jwt_manager.create_token(user.id, user.role)

        logger.info(f"User authenticated: {user.username}")

        return AuthResult(
            status=AuthStatus.SUCCESS,
            user=user,
            token=token,
            session=session,
            message="Authentication successful",
        )

    def verify_token(self, token: str) -> Optional[User]:
        """Verify a JWT token and return the user."""
        payload = self.jwt_manager.verify_token(token)
        if payload:
            user = self.user_manager.get_user_by_id(payload["user_id"])
            return user
        return None

    def logout(self, session_id: str) -> bool:
        """Log out a user by invalidating their session."""
        return self.session_manager.invalidate_session(session_id)

    def require_role(self, required_role: UserRole):
        """Decorator to require a specific role for access."""

        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # This would typically extract user from request context
                # For now, it's a placeholder for the decorator pattern
                return await func(*args, **kwargs)

            return wrapper

        return decorator

    async def cleanup_expired_data(self):
        """Clean up expired sessions and other temporary data."""
        self.session_manager.cleanup_expired_sessions()
        logger.info("Cleaned up expired authentication data")


# Global authentication instance (would be configured with proper secret
# in production)
auth_system = AuthenticationSystem("your-secret-key-here")


async def main():
    """Example usage of the authentication system."""
    # Create a test user
    user = auth_system.user_manager.create_user(
        username="testuser",
        email="test@example.com",
        password="securepassword123",
        role=UserRole.USER,
    )

    # Authenticate the user
    result = await auth_system.authenticate(
        email="test@example.com",
        password="securepassword123",
        ip_address="127.0.0.1",
        user_agent="Test Client",
    )

    if (
        result.status == AuthStatus.SUCCESS
        and result.user
        and result.session
        and result.token
    ):
        print(f"Authentication successful for user: {result.user.username}")
        print(f"Token: {result.token}")
        print(f"Session ID: {result.session.session_id}")

        # Verify token
        verified_user = auth_system.verify_token(result.token)
        if verified_user:
            print(f"Token verified for user: {verified_user.username}")
    else:
        print(f"Authentication failed: {result.message}")

    # Cleanup
    await auth_system.cleanup_expired_data()


if __name__ == "__main__":
    asyncio.run(main())
