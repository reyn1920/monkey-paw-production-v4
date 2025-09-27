"""
Security Middleware for web application security.
Provides authentication, authorization, rate limiting, CSRF protection, and security headers.
"""

import asyncio
import hashlib
import hmac
import json
import logging
import secrets
import time
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Security levels for different endpoints."""

    PUBLIC = "public"
    AUTHENTICATED = "authenticated"
    ADMIN = "admin"
    SYSTEM = "system"


class RateLimitType(Enum):
    """Types of rate limiting."""

    PER_IP = "per_ip"
    PER_USER = "per_user"
    PER_ENDPOINT = "per_endpoint"
    GLOBAL = "global"


class SecurityEventType(Enum):
    """Security event types."""

    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    CSRF_VIOLATION = "csrf_violation"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"


@dataclass
class SecurityConfig:
    """Security configuration."""

    jwt_secret: str
    jwt_expiry_hours: int = 24
    csrf_token_expiry_minutes: int = 60
    rate_limit_requests: int = 100
    rate_limit_window_minutes: int = 15
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 30
    require_https: bool = True
    allowed_origins: Optional[list[str]] = None
    security_headers: Optional[dict[str, str]] = None

    def __post_init__(self):
        if self.allowed_origins is None:
            self.allowed_origins = ["http://localhost:3000", "http://localhost:8000"]

        if self.security_headers is None:
            self.security_headers = {
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "X-XSS-Protection": "1; mode=block",
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
                "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
                "Referrer-Policy": "strict-origin-when-cross-origin",
            }


@dataclass
class RateLimitRule:
    """Rate limiting rule."""

    limit: int
    window_seconds: int
    rule_type: RateLimitType
    endpoint_pattern: Optional[str] = None


@dataclass
class SecurityEventRecord:
    """Security event record."""

    event_type: SecurityEventType
    timestamp: datetime
    ip_address: str
    user_id: Optional[str] = None
    endpoint: Optional[str] = None
    details: Optional[dict[str, Any]] = None


@dataclass
class AuthToken:
    """Authentication token."""

    user_id: str
    username: str
    roles: list[str]
    issued_at: datetime
    expires_at: datetime
    token_id: str


class RateLimiter:
    """Rate limiting implementation."""

    def __init__(self):
        self.requests: dict[str, list[float]] = defaultdict(list)
        self.blocked_ips: dict[str, float] = {}
        self.cleanup_interval = 300  # 5 minutes
        self.last_cleanup = time.time()

    def is_allowed(self, key: str, rule: RateLimitRule) -> bool:
        """Check if request is allowed under rate limit."""
        current_time = time.time()

        # Clean up old entries periodically
        if current_time - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_entries()
            self.last_cleanup = current_time

        # Check if IP is temporarily blocked
        if key in self.blocked_ips:
            if current_time < self.blocked_ips[key]:
                return False
            else:
                del self.blocked_ips[key]

        # Get request history for this key
        request_times = self.requests[key]

        # Remove requests outside the window
        window_start = current_time - rule.window_seconds
        request_times[:] = [t for t in request_times if t > window_start]

        # Check if limit exceeded
        if len(request_times) >= rule.limit:
            # Block IP for window duration
            self.blocked_ips[key] = current_time + rule.window_seconds
            logger.warning(
                f"Rate limit exceeded for {key}: {len(request_times)} requests in {rule.window_seconds}s"
            )
            return False

        # Record this request
        request_times.append(current_time)
        return True

    def _cleanup_old_entries(self):
        """Clean up old request entries."""
        current_time = time.time()
        max_age = 3600  # Keep entries for 1 hour max

        for key in list(self.requests.keys()):
            self.requests[key] = [
                t for t in self.requests[key] if current_time - t < max_age
            ]
            if not self.requests[key]:
                del self.requests[key]

        # Clean up expired blocks
        for ip in list(self.blocked_ips.keys()):
            if current_time >= self.blocked_ips[ip]:
                del self.blocked_ips[ip]


class CSRFProtection:
    """CSRF protection implementation."""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode()
        self.tokens: dict[str, float] = {}

    def generate_token(self, session_id: str) -> str:
        """Generate CSRF token for session."""
        timestamp = str(int(time.time()))
        token_data = f"{session_id}:{timestamp}"
        signature = hmac.new(
            self.secret_key, token_data.encode(), hashlib.sha256
        ).hexdigest()

        token = f"{token_data}:{signature}"
        encoded_token = secrets.token_urlsafe(32)

        # Store token with expiry
        self.tokens[encoded_token] = time.time() + 3600  # 1 hour expiry

        return encoded_token

    def validate_token(self, token: str, session_id: str) -> bool:
        """Validate CSRF token."""
        if not token or token not in self.tokens:
            return False

        # Check if token expired
        if time.time() > self.tokens[token]:
            del self.tokens[token]
            return False

        return True

    def cleanup_expired_tokens(self):
        """Remove expired tokens."""
        current_time = time.time()
        expired_tokens = [
            token for token, expiry in self.tokens.items() if current_time > expiry
        ]
        for token in expired_tokens:
            del self.tokens[token]


class SecurityAuditor:
    """Security event auditing and monitoring."""

    def __init__(self):
        self.events: list[SecurityEventRecord] = []
        self.suspicious_ips: set[str] = set()
        self.failed_login_attempts: dict[str, list[float]] = defaultdict(list)

    def log_event(
        self,
        event_type: SecurityEventType,
        ip_address: str,
        user_id: Optional[str] = None,
        endpoint: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        """Log a security event."""
        event = SecurityEventRecord(
            event_type=event_type,
            timestamp=datetime.now(),
            ip_address=ip_address,
            user_id=user_id,
            endpoint=endpoint,
            details=details or {},
        )

        self.events.append(event)

        # Keep only last 1000 events
        if len(self.events) > 1000:
            self.events = self.events[-1000:]

        # Track failed login attempts
        if event_type == SecurityEventType.LOGIN_FAILURE:
            self.failed_login_attempts[ip_address].append(time.time())
            self._check_suspicious_activity(ip_address)

        logger.info(f"Security event: {event_type.value} from {ip_address}")

    def _check_suspicious_activity(self, ip_address: str):
        """Check for suspicious activity patterns."""
        current_time = time.time()
        recent_failures = [
            t
            for t in self.failed_login_attempts[ip_address]
            if current_time - t < 300  # Last 5 minutes
        ]

        if len(recent_failures) >= 5:
            self.suspicious_ips.add(ip_address)
            self.log_event(
                SecurityEventType.SUSPICIOUS_ACTIVITY,
                ip_address,
                details={"failed_attempts": len(recent_failures)},
            )

    def is_suspicious_ip(self, ip_address: str) -> bool:
        """Check if IP is marked as suspicious."""
        return ip_address in self.suspicious_ips

    def get_security_summary(self) -> dict[str, Any]:
        """Get security summary statistics."""
        recent_events = [
            e for e in self.events if e.timestamp > datetime.now() - timedelta(hours=24)
        ]

        event_counts = defaultdict(int)
        for event in recent_events:
            event_counts[event.event_type.value] += 1

        return {
            "total_events_24h": len(recent_events),
            "event_breakdown": dict(event_counts),
            "suspicious_ips": len(self.suspicious_ips),
            "failed_logins_24h": event_counts.get("login_failure", 0),
            "rate_limit_violations_24h": event_counts.get("rate_limit_exceeded", 0),
        }


class JWTManager:
    """JWT token management."""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode()

    def create_token(
        self, user_id: str, username: str, roles: list[str], expiry_hours: int = 24
    ) -> str:
        """Create JWT token."""
        issued_at = datetime.now()
        expires_at = issued_at + timedelta(hours=expiry_hours)
        token_id = secrets.token_hex(16)

        payload = {
            "user_id": user_id,
            "username": username,
            "roles": roles,
            "iat": int(issued_at.timestamp()),
            "exp": int(expires_at.timestamp()),
            "jti": token_id,
        }

        # Simple JWT implementation (in production, use a proper JWT library)
        header = {"alg": "HS256", "typ": "JWT"}

        # Encode header and payload
        import base64

        header_encoded = (
            base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
        )

        payload_encoded = (
            base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        )

        # Create signature
        message = f"{header_encoded}.{payload_encoded}"
        signature = hmac.new(self.secret_key, message.encode(), hashlib.sha256).digest()

        signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip("=")

        return f"{message}.{signature_encoded}"

    def verify_token(self, token: str) -> Optional[AuthToken]:
        """Verify and decode JWT token."""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None

            header_encoded, payload_encoded, signature_encoded = parts

            # Verify signature
            message = f"{header_encoded}.{payload_encoded}"
            expected_signature = hmac.new(
                self.secret_key, message.encode(), hashlib.sha256
            ).digest()

            import base64

            # Add padding if needed
            signature_encoded += "=" * (4 - len(signature_encoded) % 4)
            actual_signature = base64.urlsafe_b64decode(signature_encoded)

            if not hmac.compare_digest(expected_signature, actual_signature):
                return None

            # Decode payload
            payload_encoded += "=" * (4 - len(payload_encoded) % 4)
            payload_json = base64.urlsafe_b64decode(payload_encoded).decode()
            payload = json.loads(payload_json)

            # Check expiry
            if payload.get("exp", 0) < time.time():
                return None

            return AuthToken(
                user_id=payload["user_id"],
                username=payload["username"],
                roles=payload["roles"],
                issued_at=datetime.fromtimestamp(payload["iat"]),
                expires_at=datetime.fromtimestamp(payload["exp"]),
                token_id=payload["jti"],
            )

        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return None


class SecurityMiddleware:
    """Main security middleware class."""

    def __init__(self, config: SecurityConfig):
        self.config = config
        self.rate_limiter = RateLimiter()
        self.csrf_protection = CSRFProtection(config.jwt_secret)
        self.security_auditor = SecurityAuditor()
        self.jwt_manager = JWTManager(config.jwt_secret)

        # Default rate limit rules
        self.rate_limit_rules = [
            RateLimitRule(
                limit=config.rate_limit_requests,
                window_seconds=config.rate_limit_window_minutes * 60,
                rule_type=RateLimitType.PER_IP,
            ),
            RateLimitRule(
                limit=10,
                window_seconds=60,
                rule_type=RateLimitType.PER_IP,
                endpoint_pattern="/api/auth/login",
            ),
        ]

        # Protected endpoints
        self.endpoint_security = {
            "/api/admin/*": SecurityLevel.ADMIN,
            "/api/user/*": SecurityLevel.AUTHENTICATED,
            "/api/auth/logout": SecurityLevel.AUTHENTICATED,
            "/api/public/*": SecurityLevel.PUBLIC,
        }

    async def process_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Process incoming request through security middleware."""
        response = {
            "allowed": True,
            "status_code": 200,
            "headers": {},
            "user": None,
            "csrf_token": None,
            "errors": [],
        }

        try:
            # Extract request info
            method = request.get("method", "GET")
            path = request.get("path", "/")
            headers = request.get("headers", {})
            ip_address = request.get("ip", "unknown")

            # Apply security headers
            response["headers"].update(self.config.security_headers)

            # Check HTTPS requirement
            if self.config.require_https and not request.get("is_secure", False):
                if not path.startswith("/health"):  # Allow health checks over HTTP
                    response["allowed"] = False
                    response["status_code"] = 403
                    response["errors"].append("HTTPS required")
                    return response

            # CORS handling
            origin = headers.get("origin")
            if origin and origin in self.config.allowed_origins:
                response["headers"]["Access-Control-Allow-Origin"] = origin
                response["headers"]["Access-Control-Allow-Credentials"] = "true"
                response["headers"][
                    "Access-Control-Allow-Methods"
                ] = "GET, POST, PUT, DELETE, OPTIONS"
                response["headers"][
                    "Access-Control-Allow-Headers"
                ] = "Content-Type, Authorization, X-CSRF-Token"

            # Handle preflight requests
            if method == "OPTIONS":
                return response

            # Rate limiting
            if not await self._check_rate_limits(ip_address, path):
                response["allowed"] = False
                response["status_code"] = 429
                response["errors"].append("Rate limit exceeded")
                self.security_auditor.log_event(
                    SecurityEventType.RATE_LIMIT_EXCEEDED, ip_address, endpoint=path
                )
                return response

            # Check if IP is suspicious
            if self.security_auditor.is_suspicious_ip(ip_address):
                response["allowed"] = False
                response["status_code"] = 403
                response["errors"].append("Access denied")
                return response

            # Authentication and authorization
            auth_result = await self._check_authentication(request, path)
            if not auth_result["allowed"]:
                response.update(auth_result)
                return response

            response["user"] = auth_result.get("user")

            # CSRF protection for state-changing requests
            if method in ["POST", "PUT", "DELETE", "PATCH"]:
                csrf_result = await self._check_csrf_protection(request)
                if not csrf_result["allowed"]:
                    response.update(csrf_result)
                    return response

            # Generate CSRF token for authenticated users
            if response["user"]:
                session_id = request.get("session_id", response["user"]["user_id"])
                response["csrf_token"] = self.csrf_protection.generate_token(session_id)

            return response

        except Exception as e:
            logger.error(f"Security middleware error: {e}")
            response["allowed"] = False
            response["status_code"] = 500
            response["errors"].append("Internal security error")
            return response

    async def _check_rate_limits(self, ip_address: str, path: str) -> bool:
        """Check rate limits for request."""
        for rule in self.rate_limit_rules:
            key = ip_address

            # Check if rule applies to this endpoint
            if rule.endpoint_pattern:
                if not self._matches_pattern(path, rule.endpoint_pattern):
                    continue
                key = f"{ip_address}:{path}"

            if not self.rate_limiter.is_allowed(key, rule):
                return False

        return True

    async def _check_authentication(
        self, request: dict[str, Any], path: str
    ) -> dict[str, Any]:
        """Check authentication and authorization."""
        result = {"allowed": True, "user": None}

        # Determine required security level
        required_level = self._get_required_security_level(path)

        if required_level == SecurityLevel.PUBLIC:
            return result

        # Extract token from Authorization header
        headers = request.get("headers", {})
        auth_header = headers.get("authorization", "")

        if not auth_header.startswith("Bearer "):
            result["allowed"] = False
            result["status_code"] = 401
            result["errors"] = ["Authentication required"]
            self.security_auditor.log_event(
                SecurityEventType.UNAUTHORIZED_ACCESS,
                request.get("ip", "unknown"),
                endpoint=path,
            )
            return result

        token = auth_header[7:]  # Remove "Bearer " prefix
        auth_token = self.jwt_manager.verify_token(token)

        if not auth_token:
            result["allowed"] = False
            result["status_code"] = 401
            result["errors"] = ["Invalid or expired token"]
            return result

        # Check authorization
        if not self._check_authorization(auth_token, required_level):
            result["allowed"] = False
            result["status_code"] = 403
            result["errors"] = ["Insufficient permissions"]
            return result

        result["user"] = {
            "user_id": auth_token.user_id,
            "username": auth_token.username,
            "roles": auth_token.roles,
        }

        return result

    async def _check_csrf_protection(self, request: dict[str, Any]) -> dict[str, Any]:
        """Check CSRF protection."""
        result = {"allowed": True}

        headers = request.get("headers", {})
        csrf_token = headers.get("x-csrf-token")
        session_id = request.get("session_id", "")

        if not csrf_token or not self.csrf_protection.validate_token(
            csrf_token, session_id
        ):
            result["allowed"] = False
            result["status_code"] = 403
            result["errors"] = ["CSRF token validation failed"]
            self.security_auditor.log_event(
                SecurityEventType.CSRF_VIOLATION,
                request.get("ip", "unknown"),
                endpoint=request.get("path"),
            )

        return result

    def _get_required_security_level(self, path: str) -> SecurityLevel:
        """Get required security level for path."""
        for pattern, level in self.endpoint_security.items():
            if self._matches_pattern(path, pattern):
                return level

        # Default to authenticated for API endpoints
        if path.startswith("/api/"):
            return SecurityLevel.AUTHENTICATED

        return SecurityLevel.PUBLIC

    def _matches_pattern(self, path: str, pattern: str) -> bool:
        """Check if path matches pattern (supports wildcards)."""
        if "*" not in pattern:
            return path == pattern

        # Convert pattern to regex
        regex_pattern = pattern.replace("*", ".*")
        return bool(re.match(f"^{regex_pattern}$", path))

    def _check_authorization(
        self, auth_token: AuthToken, required_level: SecurityLevel
    ) -> bool:
        """Check if user has required authorization level."""
        user_roles = set(auth_token.roles)

        if required_level == SecurityLevel.PUBLIC:
            return True
        elif required_level == SecurityLevel.AUTHENTICATED:
            return True  # Already authenticated
        elif required_level == SecurityLevel.ADMIN:
            return "admin" in user_roles or "superuser" in user_roles
        elif required_level == SecurityLevel.SYSTEM:
            return "system" in user_roles

        return False

    def create_user_token(self, user_id: str, username: str, roles: list[str]) -> str:
        """Create authentication token for user."""
        return self.jwt_manager.create_token(
            user_id, username, roles, self.config.jwt_expiry_hours
        )

    def get_security_status(self) -> dict[str, Any]:
        """Get current security status."""
        return {
            "rate_limiter": {
                "active_limits": len(self.rate_limiter.requests),
                "blocked_ips": len(self.rate_limiter.blocked_ips),
            },
            "csrf_protection": {"active_tokens": len(self.csrf_protection.tokens)},
            "security_events": self.security_auditor.get_security_summary(),
            "config": {
                "require_https": self.config.require_https,
                "rate_limit_requests": self.config.rate_limit_requests,
                "rate_limit_window_minutes": self.config.rate_limit_window_minutes,
            },
        }

    async def cleanup(self):
        """Cleanup expired tokens and old data."""
        self.csrf_protection.cleanup_expired_tokens()
        # Rate limiter cleanup happens automatically


# Global security middleware instance
security_config = SecurityConfig(
    jwt_secret="your-secret-key-change-in-production",
    jwt_expiry_hours=24,
    rate_limit_requests=100,
    rate_limit_window_minutes=15,
)

security_middleware = SecurityMiddleware(security_config)


async def main():
    """Example usage of security middleware."""
    # Simulate a request
    request = {
        "method": "GET",
        "path": "/api/user/profile",
        "headers": {
            "authorization": "Bearer invalid-token",
            "origin": "http://localhost:3000",
        },
        "ip": "192.168.1.100",
        "is_secure": True,
        "session_id": "session123",
    }

    # Process request
    result = await security_middleware.process_request(request)
    print(f"Security check result: {json.dumps(result, indent=2, default=str)}")

    # Create a valid token
    token = security_middleware.create_user_token("user123", "testuser", ["user"])
    print(f"Created token: {token}")

    # Test with valid token
    request["headers"]["authorization"] = f"Bearer {token}"
    result = await security_middleware.process_request(request)
    print(f"With valid token: {json.dumps(result, indent=2, default=str)}")

    # Get security status
    status = security_middleware.get_security_status()
    print(f"Security status: {json.dumps(status, indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())
