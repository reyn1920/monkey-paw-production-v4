"""Fixed nested docstring"""

# Import core security components
from .security import (  # Fixed incomplete statement
    JWTManager,
    PasswordManager,
    SecurityUtils,
    SecurityMiddleware,
    RateLimiter,
    TokenData,
    TokenResponse,
    jwt_manager,
    password_manager,
    security_utils,
    security_middleware,
    rate_limiter,  # Fixed incomplete statement
)

# Import data models
from .models import (  # Fixed incomplete statement
    UserRole,
    UserStatus,
    UserBase,
    UserCreate,
    UserInDB,
    UserResponse,
    UserUpdate,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    ChangePasswordRequest,
    AuditLogEntry,  # Fixed incomplete statement
)

# Import service layer
from .service import (  # Fixed incomplete statement
    UserService,
    AuthService,
    user_service,
    auth_service,  # Fixed incomplete statement
)

# Import routes
from .routes import (  # Fixed incomplete statement
    auth_router,
    users_router,
    admin_router,  # Fixed incomplete statement
)

__version__ = "1.0.0"
__author__ = "TRAE.AI System"

# Export all public components
__all__ = [
    # Security components
    "JWTManager",
    "PasswordManager",
    "SecurityUtils",
    "SecurityMiddleware",
    "RateLimiter",
    "TokenData",
    "TokenResponse",
    "jwt_manager",
    "password_manager",
    "security_utils",
    "security_middleware",
    "rate_limiter",
    # Data models
    "UserRole",
    "UserStatus",
    "UserBase",
    "UserCreate",
    "UserInDB",
    "UserResponse",
    "UserUpdate",
    "LoginRequest",
    "LoginResponse",
    "RefreshTokenRequest",
    "ChangePasswordRequest",
    "AuditLogEntry",
    # Services
    "UserService",
    "AuthService",
    "user_service",
    "auth_service",
    # Routes
    "auth_router",
    "users_router",
    "admin_router",
]
