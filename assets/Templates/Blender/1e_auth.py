"""Authentication API endpoints."""
import logging
from datetime import timedelta
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.core.config import get_settings
from src.backend.infrastructure.database import db_manager
from src.backend.services.auth_service import AuthService
from src.backend.domain.models import User

logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Router
router = APIRouter(prefix="/auth", tags=["authentication"])


# Pydantic models
class UserLogin(BaseModel):
    """User login request model."""
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """User registration request model."""
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserResponse(BaseModel):
    """User response model."""
    id: str
    email: str
    first_name: str
    last_name: str
    is_active: bool


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(db_manager.get_session)
) -> User:
    """Get current authenticated user."""
    try:
        # Extract token from credentials
        token = credentials.credentials
        
        # Verify token and get user email
        email = AuthService.verify_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        user = await AuthService.get_user_by_email(session, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# API endpoints
@router.post("/login", response_model=Dict[str, Any])
async def login(
    user_data: UserLogin,
    session: AsyncSession = Depends(db_manager.get_session)
) -> Dict[str, Any]:
    """Authenticate user and return access token."""
    try:
        # Authenticate user
        user = await AuthService.authenticate_user(session, user_data.email, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token = AuthService.create_access_token(data={"sub": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": str(user.email),
                "first_name": str(user.first_name),
                "last_name": str(user.last_name),
                "is_active": bool(user.is_active)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/register", response_model=Dict[str, Any])
async def register(
    user_data: UserRegister,
    session: AsyncSession = Depends(db_manager.get_session)
) -> Dict[str, Any]:
    """Register a new user."""
    try:
        # Check if user already exists
        existing_user = await AuthService.get_user_by_email(session, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user = await AuthService.create_user(
            session=session,
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        # Create access token
        access_token = AuthService.create_access_token(data={"sub": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": str(user.email),
                "first_name": str(user.first_name),
                "last_name": str(user.last_name),
                "is_active": bool(user.is_active)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Get current user information."""
    return UserResponse(
        id=str(current_user.id),
        email=str(current_user.email),
        first_name=str(current_user.first_name),
        last_name=str(current_user.last_name),
        is_active=bool(current_user.is_active)
    )


@router.post("/logout")
async def logout() -> Dict[str, str]:
    """Logout user (client-side token removal)."""
    return {"message": "Successfully logged out"}