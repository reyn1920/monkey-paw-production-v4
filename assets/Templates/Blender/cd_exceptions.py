"""
Core exceptions for the application.
"""


class BaseApplicationError(Exception):
    """Base exception for application errors."""
    
    def __init__(self, message: str, error_code: str | None = None, **context):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class AuthenticationError(BaseApplicationError):
    """Exception raised for authentication failures."""
    
    def __init__(self, message: str = "Authentication failed", **context):
        super().__init__(message, "AUTH_ERROR", **context)


class AuthorizationError(BaseApplicationError):
    """Exception raised for authorization failures."""
    
    def __init__(self, message: str = "Access denied", **context):
        super().__init__(message, "AUTHZ_ERROR", **context)


class ValidationError(BaseApplicationError):
    """Exception raised for data validation failures."""
    
    def __init__(self, message: str = "Validation failed", **context):
        super().__init__(message, "VALIDATION_ERROR", **context)


class DatabaseError(BaseApplicationError):
    """Exception raised for database operation failures."""
    
    def __init__(self, message: str = "Database operation failed", **context):
        super().__init__(message, "DB_ERROR", **context)


class ConfigurationError(BaseApplicationError):
    """Exception raised for configuration errors."""
    
    def __init__(self, message: str = "Configuration error", **context):
        super().__init__(message, "CONFIG_ERROR", **context)


class ServiceError(BaseApplicationError):
    """Exception raised for service operation failures."""
    
    def __init__(self, message: str = "Service error", **context):
        super().__init__(message, "SERVICE_ERROR", **context)


# Alias for backward compatibility
ApplicationError = BaseApplicationError