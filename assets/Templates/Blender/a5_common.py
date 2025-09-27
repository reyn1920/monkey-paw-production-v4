#!/usr/bin/env python3
"""
TRAE.AI Common Utilities

Provides common utility functions and classes for the TRAE.AI system.
"""

import os
import logging
import time
from enum import Enum
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional


class Provider(Enum):
    """Enumeration of supported service providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE = "azure"
    LOCAL = "local"
    CUSTOM = "custom"


def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Retrieve a secret from environment variables.

    Args:
        key: The environment variable key
        default: Default value if key is not found

    Returns:
        The secret value or default
    """
    return os.getenv(key, default)


class SimpleHTTPResponse:
    """Simple HTTP response wrapper."""

    def __init__(
        self, status_code: int, text: str, headers: Optional[dict[str, str]] = None
    ):
        self.status_code = status_code
        self.text = text
        self.headers = headers or {}

    def raise_for_status(self):
        """Raise an exception for HTTP error status codes."""
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}: {self.text}")


def http_with_fallback(url: str, method: str = "GET", **kwargs) -> SimpleHTTPResponse:
    """
    Make HTTP request with retry logic and fallback handling.

    Args:
        url: The URL to request
        method: HTTP method (GET, POST, etc.)
        **kwargs: Additional arguments for the request

    Returns:
        SimpleHTTPResponse object

    Raises:
        urllib.error.URLError: If all retry attempts fail
    """
    max_retries = 3
    backoff_factor = 1

    data = kwargs.get("data")
    headers = kwargs.get("headers", {})

    if data and isinstance(data, dict):
        data = urllib.parse.urlencode(data).encode("utf-8")
    elif data and isinstance(data, str):
        data = data.encode("utf-8")

    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)

            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read().decode("utf-8")
                status_code = response.getcode()
                response_headers = dict(response.headers)

                return SimpleHTTPResponse(status_code, content, response_headers)

        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            if attempt == max_retries:
                logging.error(
                    f"HTTP request failed for {url} after {max_retries} retries: {e}"
                )
                raise

            # Exponential backoff
            sleep_time = backoff_factor * (2**attempt)
            logging.warning(
                f"HTTP request failed (attempt {attempt + 1}/{max_retries + 1}), retrying in {sleep_time}s: {e}"
            )
            time.sleep(sleep_time)

        except Exception as e:
            logging.error(f"Unexpected error during HTTP request to {url}: {e}")
            raise

    # This should never be reached due to the raise in the except block
    raise urllib.error.URLError(
        f"Failed to complete request to {url} after {max_retries} retries"
    )
