"""
Authentication API endpoints for VidScript Pro
User registration, login, and token management
"""

import logging
from datetime import timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.infrastructure.database import get_db_session
from src.backend.services.auth_service import auth_service
from src.backend.domain.models import User

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Router
router = APIRouter(prefix="/auth", tags=["authentication"])


# Pydantic models
class UserRegister(BaseModel):
    """User registration request model."""
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    """User login request model."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response model."""
    id: UUID
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    is_verified: bool
    
    class Config:
        from_attributes = True


# Dependencies
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> User:
    """Get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP authorization credentials
        db: Database session
        
    Returns:
        Current user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify token
    payload = auth_service.verify_token(credentials.credentials)
    if payload is None:
        raise credentials_exception
    
    # Get user ID from token
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise credentials_exception
    
    # Get user from database
    user = await auth_service.get_user_by_id(db, user_uuid)
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get current active user.
    
    Args:
        current_user: Current user from token
        
    Returns:
        Current active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


# API endpoints
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserResponse:
    """Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        Created user data
        
    Raises:
        HTTPException: If user already exists or validation fails
    """
    try:
        # Check if user already exists
        existing_user = await auth_service.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        # Create new user
        user = await auth_service.create_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        
        logger.info(f"User registered successfully: {user.email}")
        return UserResponse.model_validate(user)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        )


@router.post("/login", response_model=Token)
async def login_user(
    user_data: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Token:
    """Authenticate user and return access token.
    
    Args:
        user_data: User login data
        db: Database session
        
    Returns:
        Access token
        
    Raises:
        HTTPException: If authentication fails
    """
    # Authenticate user
    user = await auth_service.authenticate_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=auth_service.settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    
    logger.info(f"User logged in successfully: {user.email}")
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    """Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user data
    """
    return UserResponse.model_validate(current_user)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Token:
    """Refresh access token.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        New access token
    """
    # Create new access token
    access_token_expires = timedelta(minutes=auth_service.settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": str(current_user.id)},
        expires_delta=access_token_expires,
    )
    
    logger.info(f"Token refreshed for user: {current_user.email}")
    return Token(access_token=access_token)