"""
Authentication models and database schemas.

This module defines the data models for users, sessions, and authentication-related
entities in the TRAE.AI system.

Author: TRAE.AI System
"""

from datetime import datetime, timezone
from typing import Optional, Any
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum
import uuid

# Enums


class UserRole(str, Enum):
    """User role enumeration"""

    ADMIN = "admin"
    USER = "user"
    DEVELOPER = "developer"
    VIEWER = "viewer"


class UserStatus(str, Enum):
    """User status enumeration"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class SessionStatus(str, Enum):
    """Session status enumeration"""

    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


# Base models


class AuthBaseModel(BaseModel):
    """Base model with common fields"""

    class Config:
        use_enum_values = True
        json_encoders = {datetime: lambda v: v.isoformat()}


# User models


class UserBase(AuthBaseModel):
    """Base user model"""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: bool = True
    roles: list[UserRole] = Field(default=[UserRole.USER])

    @validator("username")
    def validate_username(cls, v):
        if not v.isalnum() and "_" not in v and "-" not in v:
            raise ValueError(
                "Username must contain only alphanumeric characters, underscores, or hyphens"
            )
        return v.lower()


class UserCreate(UserBase):
    """User creation model"""

    password: str = Field(..., min_length=8)
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(AuthBaseModel):
    """User update model"""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    roles: Optional[list[UserRole]] = None


class UserInDB(UserBase):
    """User model as stored in database"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None
    login_attempts: int = 0
    locked_until: Optional[datetime] = None
    email_verified: bool = False
    profile_data: dict[str, Any] = Field(default_factory=dict)


class UserResponse(UserBase):
    """User response model (public data)"""

    id: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    email_verified: bool = False


# Authentication models


class LoginRequest(AuthBaseModel):
    """Login request model"""

    username: str
    password: str
    remember_me: bool = False


class LoginResponse(AuthBaseModel):
    """Login response model"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class RefreshTokenRequest(AuthBaseModel):
    """Refresh token request model"""

    refresh_token: str


class ChangePasswordRequest(AuthBaseModel):
    """Change password request model"""

    current_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class ResetPasswordRequest(AuthBaseModel):
    """Reset password request model"""

    email: EmailStr


class ResetPasswordConfirm(AuthBaseModel):
    """Reset password confirmation model"""

    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v


# Session models


class SessionBase(AuthBaseModel):
    """Base session model"""

    user_id: str
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class SessionCreate(SessionBase):
    """Session creation model"""

    access_token: str
    refresh_token: str


class SessionInDB(SessionBase):
    """Session model as stored in database"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    access_token_hash: str
    refresh_token_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime
    last_used: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: SessionStatus = SessionStatus.ACTIVE


class SessionResponse(AuthBaseModel):
    """Session response model"""

    id: str
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime
    last_used: datetime
    status: SessionStatus


# API Key models


class APIKeyBase(AuthBaseModel):
    """Base API key model"""

    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    permissions: list[str] = Field(default_factory=list)


class APIKeyCreate(APIKeyBase):
    """API key creation model"""

    expires_at: Optional[datetime] = None


class APIKeyInDB(APIKeyBase):
    """API key model as stored in database"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    key_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    is_active: bool = True


class APIKeyResponse(APIKeyBase):
    """API key response model"""

    id: str
    key: str  # Only returned on creation
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    is_active: bool


# Audit models


class AuditLogEntry(AuthBaseModel):
    """Audit log entry model"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    action: str
    resource: str
    resource_id: Optional[str] = None
    details: dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    success: bool = True


# Error models


class AuthError(AuthBaseModel):
    """Authentication error model"""

    error: str
    message: str
    details: Optional[dict[str, Any]] = None


class ValidationError(AuthBaseModel):
    """Validation error model"""

    field: str
    message: str
    value: Optional[Any] = None


# Response models


class MessageResponse(AuthBaseModel):
    """Generic message response"""

    message: str
    success: bool = True


class PaginatedResponse(AuthBaseModel):
    """Paginated response model"""

    items: list[Any]
    total: int
    page: int
    size: int
    pages: int


# Export all models
__all__ = [
    # Enums
    "UserRole",
    "UserStatus",
    "SessionStatus",
    # User models
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "UserResponse",
    # Authentication models
    "LoginRequest",
    "LoginResponse",
    "RefreshTokenRequest",
    "ChangePasswordRequest",
    "ResetPasswordRequest",
    "ResetPasswordConfirm",
    # Session models
    "SessionBase",
    "SessionCreate",
    "SessionInDB",
    "SessionResponse",
    # API Key models
    "APIKeyBase",
    "APIKeyCreate",
    "APIKeyInDB",
    "APIKeyResponse",
    # Audit models
    "AuditLogEntry",
    # Error models
    "AuthError",
    "ValidationError",
    # Response models
    "MessageResponse",
    "PaginatedResponse",
]
