"""
Authentication routes for the TRAE.AI system.

This module provides FastAPI routes for user authentication, registration,
and user management operations.

Author: TRAE.AI System
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from .models import (
    UserCreate,
    UserResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    UserUpdate,
    ChangePasswordRequest,
    UserRole,
)
from .service import user_service, auth_service
from .security import jwt_manager, TokenData

logger = logging.getLogger(__name__)
security = HTTPBearer()

# Create routers
auth_router = APIRouter(prefix="/auth", tags=["authentication"])
users_router = APIRouter(prefix="/users", tags=["users"])
admin_router = APIRouter(prefix="/admin", tags=["admin"])

# Helper functions


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenData:
    """Get current authenticated user from JWT token"""
    try:
        token_data = jwt_manager.verify_token(credentials.credentials)
        user = user_service.get_user_by_id(token_data.user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return token_data
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


async def get_admin_user(
    current_user: TokenData = Depends(get_current_user),
) -> TokenData:
    """Require admin role for access"""
    user = user_service.get_user_by_id(current_user.user_id)
    if not user or UserRole.ADMIN not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user


# Authentication routes


@auth_router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        user = user_service.create_user(user_data)
        return user_service.to_user_response(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        )


@auth_router.post("/login", response_model=LoginResponse)
async def login_user(login_data: LoginRequest):
    """Login user and return access token"""
    try:
        result = auth_service.login(login_data)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        return LoginResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            token_type=result["token_type"],
            expires_in=result["expires_in"],
            user=result["user"],
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed"
        )


@auth_router.post("/refresh")
async def refresh_access_token(refresh_data: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    try:
        result = auth_service.refresh_token(refresh_data.refresh_token)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        return {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": result["token_type"],
            "expires_in": result["expires_in"],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed",
        )


@auth_router.post("/logout")
async def logout_user(current_user: TokenData = Depends(get_current_user)):
    """Logout user (invalidate token)"""
    # In a real implementation, you would invalidate the token
    # For now, we just return success
    return {"message": "Successfully logged out"}


@auth_router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: TokenData = Depends(get_current_user)):
    """Get current user information"""
    user = user_service.get_user_by_id(current_user.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_service.to_user_response(user)


# User management routes


@users_router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate, current_user: TokenData = Depends(get_current_user)
):
    """Update current user information"""
    try:
        user = user_service.update_user(current_user.user_id, user_update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user_service.to_user_response(user)
    except Exception as e:
        logger.error(f"User update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User update failed",
        )


@users_router.post("/change-password")
async def change_user_password(
    password_data: ChangePasswordRequest,
    current_user: TokenData = Depends(get_current_user),
):
    """Change user password"""
    try:
        success = user_service.change_password(
            current_user.user_id,
            password_data.current_password,
            password_data.new_password,
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid current password",
            )
        return {"message": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password change error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed",
        )


# Admin routes


@admin_router.get("/users", response_model=list[UserResponse])
async def list_all_users(admin_user: TokenData = Depends(get_admin_user)):
    """List all users (admin only)"""
    try:
        users = user_service.list_users()
        return [user_service.to_user_response(user) for user in users]
    except Exception as e:
        logger.error(f"User list error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users",
        )


@admin_router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str, admin_user: TokenData = Depends(get_admin_user)):
    """Get user by ID (admin only)"""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_service.to_user_response(user)


@admin_router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_by_id(
    user_id: str,
    user_update: UserUpdate,
    admin_user: TokenData = Depends(get_admin_user),
):
    """Update user by ID (admin only)"""
    try:
        user = user_service.update_user(user_id, user_update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user_service.to_user_response(user)
    except Exception as e:
        logger.error(f"Admin user update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User update failed",
        )


# Health check


@auth_router.get("/health")
async def auth_health_check():
    """Authentication service health check"""
    return {"status": "healthy", "service": "authentication", "version": "1.0.0"}


# Export routers
__all__ = ["auth_router", "users_router", "admin_router"]
