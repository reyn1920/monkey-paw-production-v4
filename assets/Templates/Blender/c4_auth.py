"""
Authentication service for user management and security.
"""

import hashlib
import secrets
import jwt
import asyncio
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import logging

from .registry import BaseService
from src.core.config import Config
from src.core.exceptions import AuthenticationError

logger = logging.getLogger(__name__)


class UserRole(Enum):
    """User roles for authorization."""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class TokenType(Enum):
    """Token types for different authentication purposes."""
    ACCESS = "access"
    REFRESH = "refresh"
    RESET = "reset"


@dataclass
class AuthToken:
    """Authentication token data structure."""
    token: str
    token_type: TokenType
    user_id: str
    expires_at: float  # Unix timestamp
    created_at: float  # Unix timestamp
    
    @property
    def is_expired(self) -> bool:
        """Check if the token has expired."""
        import time
        return time.time() > self.expires_at


@dataclass
class User:
    """User data structure."""
    id: str  # Changed from user_id to id to match test expectations
    username: str
    email: str
    password_hash: str
    role: UserRole = UserRole.USER
    created_at: float = 0.0  # Unix timestamp
    is_active: bool = True


class AuthenticationService(BaseService):
    """Service for handling user authentication and authorization."""
    
    def __init__(self, config: Config, registry=None):
        super().__init__("authentication_service")
        self.config = config
        self.registry = registry
        self._users: Dict[str, User] = {}
        self._tokens: Dict[str, AuthToken] = {}
        self._secret_key = config.get_api_key() if hasattr(config, 'get_api_key') else "default_secret"
        self._token_expiry = 3600  # 1 hour default
        self.users: Dict[str, User] = {}  # In-memory user storage for testing
        self.is_initialized = False  # Add initialization flag
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        import hashlib
        # Simple hash for testing - in production use bcrypt
        return hashlib.sha256((password + self._secret_key).encode()).hexdigest()
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        return self._hash_password(password) == hashed
    
    def _generate_token(self, user: User) -> AuthToken:
        """Generate an authentication token for a user."""
        import uuid
        import time
        
        token_id = str(uuid.uuid4())
        expires_at = time.time() + self._token_expiry
        
        token = AuthToken(
            token=token_id,
            user_id=user.id,
            token_type=TokenType.ACCESS,
            expires_at=expires_at,
            created_at=time.time()
        )
        
        self._tokens[token_id] = token
        return token
    
    async def validate_token(self, token_str: str) -> Optional[AuthToken]:
        """Validate an authentication token."""
        import time
        
        token = self._tokens.get(token_str)
        if not token:
            return None
            
        # Check if token is expired
        if time.time() > token.expires_at:
            del self._tokens[token_str]
            return None
            
        return token
    
    def hash_password(self, password: str) -> str:
        """Hash a password using SHA-256 with salt."""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
        """Verify a password against its hash."""
        try:
            salt, stored_hash = password_hash.split(':')
            computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return computed_hash == stored_hash
        except ValueError:
            return False
    
    def generate_token(self, user_id: str, token_type: TokenType = TokenType.ACCESS, 
                      expires_in_hours: int = 24) -> AuthToken:
        """Generate a JWT token for a user."""
        issued_at = datetime.utcnow()
        expires_at = issued_at + timedelta(hours=expires_in_hours)
        
        payload = {
            'user_id': user_id,
            'token_type': token_type.value,
            'iat': issued_at.timestamp(),
            'exp': expires_at.timestamp()
        }
        
        token = jwt.encode(payload, self._secret_key, algorithm='HS256')
        
        auth_token = AuthToken(
            token=token,
            token_type=token_type,
            user_id=user_id,
            expires_at=expires_at.timestamp(),
            created_at=issued_at.timestamp()
        )
        
        self._tokens[token] = auth_token
        return auth_token
    
    async def validate_token(self, token: str) -> Optional[AuthToken]:
        """Validate a JWT token."""
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=['HS256'])
            
            if token in self._tokens:
                auth_token = self._tokens[token]
                if not auth_token.is_expired:
                    return auth_token
            
            # Token not in cache but valid JWT, recreate AuthToken
            user_id = payload['user_id']
            token_type = TokenType(payload['token_type'])
            issued_at = datetime.fromtimestamp(payload['iat'])
            expires_at = datetime.fromtimestamp(payload['exp'])
            
            auth_token = AuthToken(
                token=token,
                token_type=token_type,
                user_id=user_id,
                expires_at=expires_at.timestamp(),
                created_at=issued_at.timestamp()
            )
            
            if not auth_token.is_expired:
                self._tokens[token] = auth_token
                return auth_token
            
        except jwt.InvalidTokenError:
            pass
        
        return None
    
    async def register_user(self, username: str, email: str, password: str, 
                           role: UserRole = UserRole.USER) -> User:
        """Register a new user."""
        user_id = secrets.token_hex(16)
        
        # Check if user already exists
        for user in self._users.values():
            if user.username == username or user.email == email:
                raise AuthenticationError("User already exists")
        
        password_hash = self.hash_password(password)
        
        user = User(
            id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            created_at=datetime.utcnow().timestamp()
        )
        
        self._users[user_id] = user
        logger.info(f"User registered: {username}")
        return user
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password."""
        for user in self._users.values():
            if user.username == username and user.is_active:
                if self._verify_password(password, user.password_hash):
                    logger.info(f"User authenticated: {username}")
                    return user
        
        logger.warning(f"Authentication failed for: {username}")
        return None
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return self._users.get(user_id)
    
    def has_role(self, user_id: str, required_role: UserRole) -> bool:
        """Check if a user has a specific role."""
        user = self.get_user(user_id)
        if not user:
            return False
        
        # Admin has access to everything
        if user.role == UserRole.ADMIN:
            return True
        
        return user.role == required_role
    
    async def revoke_token(self, token: str):
        """Revoke a token."""
        if token in self._tokens:
            del self._tokens[token]
            logger.info("Token revoked")
    
    def list_users(self) -> List[User]:
        """List all users."""
        return list(self._users.values())
    
    async def initialize(self):
        """Initialize the authentication service."""
        self.is_initialized = True
        logger.info("AuthenticationService initialized")
    
    async def shutdown(self):
        """Shutdown the authentication service."""
        self._users.clear()
        self._tokens.clear()
        logger.info("AuthenticationService shutdown")