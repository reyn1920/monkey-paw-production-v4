"""
Authentication service for user management.
"""
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID

from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.backend.core.config import get_settings
from src.backend.domain.models import User, UserRole

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service for user management."""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate password hash."""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token."""
        settings = get_settings()
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        """Verify JWT token and return email if valid."""
        settings = get_settings()
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            email: Optional[str] = payload.get("sub")
            return email
        except JWTError:
            return None
    
    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
        """Get user by email."""
        try:
            result = await session.execute(select(User).where(User.email == email))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching user by email {email}: {e}")
            return None
    
    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        try:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching user by ID {user_id}: {e}")
            return None
    
    @staticmethod
    async def create_user(
        session: AsyncSession,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: UserRole = UserRole.USER
    ) -> Optional[User]:
        """Create a new user."""
        try:
            # Check if user already exists
            existing_user = await AuthService.get_user_by_email(session, email)
            if existing_user:
                logger.warning(f"User with email {email} already exists")
                return None
            
            # Create new user
            hashed_password = AuthService.get_password_hash(password)
            user = User(
                email=email,
                hashed_password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                role=role,
                is_active=True,
                is_verified=False
            )
            
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
            logger.info(f"Created new user: {email}")
            return user
            
        except Exception as e:
            logger.error(f"Error creating user {email}: {e}")
            await session.rollback()
            return None
    
    @staticmethod
    async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        try:
            user = await AuthService.get_user_by_email(session, email)
            if not user:
                logger.warning(f"Authentication failed: user {email} not found")
                return None
            
            # Access the actual value from the SQLAlchemy model
            if not user.is_active:
                logger.warning(f"Authentication failed: user {email} is inactive")
                return None
            
            # Access the actual hashed_password value from the model
            if not AuthService.verify_password(password, user.hashed_password):
                logger.warning(f"Authentication failed: invalid password for {email}")
                return None
            
            logger.info(f"User {email} authenticated successfully")
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user {email}: {e}")
            return None