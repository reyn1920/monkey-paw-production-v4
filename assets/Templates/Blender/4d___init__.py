"""
Backend Models Module
Contains data models and database schemas
"""

# Import common models if they exist
try:
    from .user import User
except ImportError:
    pass

try:
    from .base import BaseModel
except ImportError:
    pass

__all__ = ["User", "BaseModel"]
