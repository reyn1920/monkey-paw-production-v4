"""
Security utilities for authentication and authorization.

This module provides JWT token management, password hashing, and security utilities
for the TRAE.AI authentication system.

Author: TRAE.AI System
"""

import os
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import secrets
import hashlib
import logging

logger = logging.getLogger(__name__)

# Security configuration


class SecurityConfig:
    """Security configuration settings"""

    def __init__(self):
        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY", self._generate_secret_key())
        self.jwt_algorithm = "HS256"
        self.access_token_expire_minutes = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        )
        self.refresh_token_expire_days = int(
            os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
        )
        self.password_min_length = 8
        self.max_login_attempts = 5
        self.lockout_duration_minutes = 15

    def _generate_secret_key(self) -> str:
        """Generate a secure secret key if none is provided"""
        return secrets.token_urlsafe(32)


security_config = SecurityConfig()

# Token models


class TokenData(BaseModel):
    """Token data structure"""

    user_id: str
    username: str
    roles: list[str] = []
    token_type: str = "access"
    exp: Optional[datetime] = None
    iat: Optional[datetime] = None


class TokenResponse(BaseModel):
    """Token response structure"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_info: dict[str, Any]


# Password utilities


class PasswordManager:
    """Password hashing and verification utilities"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        if len(password) < security_config.password_min_length:
            raise ValueError(
                f"Password must be at least {
                    security_config.password_min_length
                } characters long"
            )

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"), hashed_password.encode("utf-8")
            )
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False

    @staticmethod
    def generate_secure_password(length: int = 16) -> str:
        """Generate a secure random password"""
        return secrets.token_urlsafe(length)


# JWT utilities


class JWTManager:
    """JWT token management utilities"""

    @staticmethod
    def create_access_token(
        user_id: str,
        username: str,
        roles: list[str] = None,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """Create a JWT access token"""
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=security_config.access_token_expire_minutes
            )

        payload = {
            "user_id": user_id,
            "username": username,
            "roles": roles or [],
            "token_type": "access",
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "jti": secrets.token_urlsafe(16),  # JWT ID for token revocation
        }

        return jwt.encode(
            payload,
            security_config.jwt_secret_key,
            algorithm=security_config.jwt_algorithm,
        )

    @staticmethod
    def create_refresh_token(
        user_id: str, username: str, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT refresh token"""
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                days=security_config.refresh_token_expire_days
            )

        payload = {
            "user_id": user_id,
            "username": username,
            "token_type": "refresh",
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "jti": secrets.token_urlsafe(16),
        }

        return jwt.encode(
            payload,
            security_config.jwt_secret_key,
            algorithm=security_config.jwt_algorithm,
        )

    @staticmethod
    def verify_token(token: str) -> TokenData:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(
                token,
                security_config.jwt_secret_key,
                algorithms=[security_config.jwt_algorithm],
            )

            # Check if token is expired
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
                timezone.utc
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
                )

            return TokenData(
                user_id=payload.get("user_id"),
                username=payload.get("username"),
                roles=payload.get("roles", []),
                token_type=payload.get("token_type", "access"),
                exp=(
                    datetime.fromtimestamp(payload.get("exp"))
                    if payload.get("exp")
                    else None
                ),
                iat=(
                    datetime.fromtimestamp(payload.get("iat"))
                    if payload.get("iat")
                    else None
                ),
            )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

    @staticmethod
    def create_token_response(
        user_id: str,
        username: str,
        roles: list[str] = None,
        user_info: dict[str, Any] = None,
    ) -> TokenResponse:
        """Create a complete token response"""
        access_token = JWTManager.create_access_token(user_id, username, roles)
        refresh_token = JWTManager.create_refresh_token(user_id, username)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=security_config.access_token_expire_minutes * 60,
            user_info=user_info
            or {"user_id": user_id, "username": username, "roles": roles or []},
        )


# Security middleware


class SecurityMiddleware:
    """Security middleware for request validation"""

    def __init__(self):
        self.bearer_scheme = HTTPBearer()

    async def get_current_user(
        self, credentials: HTTPAuthorizationCredentials
    ) -> TokenData:
        """Get current user from JWT token"""
        token = credentials.credentials
        token_data = JWTManager.verify_token(token)

        if token_data.token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )

        return token_data

    def require_roles(self, required_roles: list[str]):
        """Decorator to require specific roles"""

        def decorator(func):
            async def wrapper(*args, **kwargs):
                # This would be used with dependency injection in FastAPI
                # Implementation depends on how it's integrated with routes
                return await func(*args, **kwargs)

            return wrapper

        return decorator


# Rate limiting utilities


class RateLimiter:
    """Simple in-memory rate limiter for authentication attempts"""

    def __init__(self):
        self.attempts = {}  # In production, use Redis or database

    def is_rate_limited(self, identifier: str) -> bool:
        """Check if an identifier is rate limited"""
        now = datetime.now()
        if identifier not in self.attempts:
            return False

        attempts = self.attempts[identifier]
        # Remove old attempts
        attempts = [
            attempt
            for attempt in attempts
            if now - attempt
            < timedelta(minutes=security_config.lockout_duration_minutes)
        ]
        self.attempts[identifier] = attempts

        return len(attempts) >= security_config.max_login_attempts

    def record_attempt(self, identifier: str, success: bool = False):
        """Record a login attempt"""
        now = datetime.now()

        if identifier not in self.attempts:
            self.attempts[identifier] = []

        if success:
            # Clear attempts on successful login
            self.attempts[identifier] = []
        else:
            # Record failed attempt
            self.attempts[identifier].append(now)


# Security utilities


class SecurityUtils:
    """Additional security utilities"""

    @staticmethod
    def generate_api_key() -> str:
        """Generate a secure API key"""
        return f"trae_{secrets.token_urlsafe(32)}"

    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash an API key for storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()

    @staticmethod
    def verify_api_key(api_key: str, hashed_key: str) -> bool:
        """Verify an API key against its hash"""
        return hashlib.sha256(api_key.encode()).hexdigest() == hashed_key

    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Basic input sanitization"""
        if not isinstance(input_str, str):
            return ""

        # Remove potentially dangerous characters
        dangerous_chars = ["<", ">", '"', "'", "&", "\x00"]
        for char in dangerous_chars:
            input_str = input_str.replace(char, "")

        return input_str.strip()


# Initialize global instances
password_manager = PasswordManager()
jwt_manager = JWTManager()
security_middleware = SecurityMiddleware()
rate_limiter = RateLimiter()
security_utils = SecurityUtils()

# Export main components
__all__ = [
    "SecurityConfig",
    "TokenData",
    "TokenResponse",
    "PasswordManager",
    "JWTManager",
    "SecurityMiddleware",
    "RateLimiter",
    "SecurityUtils",
    "password_manager",
    "jwt_manager",
    "security_middleware",
    "rate_limiter",
    "security_utils",
    "security_config",
]
