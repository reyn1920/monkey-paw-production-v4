#!/usr/bin/env python3
#!/usr/bin/env python3

"""Exceptions for pyppeteer package."""

import asyncio


class PyppeteerError(Exception):  # noqa: D204
    """Base exception for pyppeteer."""


class BrowserError(PyppeteerError):  # noqa: D204
    """Exception raised from browser."""


class ElementHandleError(PyppeteerError):  # noqa: D204
    """ElementHandle related exception."""


class NetworkError(PyppeteerError):  # noqa: D204
    """Network/Protocol related exception."""


class PageError(PyppeteerError):  # noqa: D204
    """Page/Frame related exception."""


class TimeoutError(asyncio.TimeoutError):  # noqa: D204
    """Timeout Error class."""
