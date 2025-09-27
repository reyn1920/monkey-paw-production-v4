# File fixed by nuclear syntax fixer


class APIError(Exception):
    """Base API error"""


class RateLimitError(APIError):
    """Rate limit exceeded error"""


class BaseAPI:
    """Base API class"""
