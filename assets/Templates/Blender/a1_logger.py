#!/usr/bin/env python3
"""
TRAE.AI Centralized Logging System

Production-ready logging configuration with automatic log rotation,
structured formatting, and multiple output handlers.

Author: TRAE.AI System
Version: 1.0.0
"""

import json
import logging
import logging.handlers
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, Any


# Global logger instances
_loggers: dict[str, logging.Logger] = {}
_lock = threading.Lock()


def get_logger(name: str = "trae_ai", level: str = "INFO") -> logging.Logger:
    """
    Get or create a logger instance with the specified name and level.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    with _lock:
        if name in _loggers:
            return _loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))

        # Prevent duplicate handlers
        if logger.handlers:
            _loggers[name] = logger
            return logger

        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / f"{name}.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,  # 10MB
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        _loggers[name] = logger
        return logger


def log_api_request(
    endpoint: str,
    method: str,
    status_code: int,
    response_time: float,
    user_id: Optional[str] = None,
) -> None:
    """
    Log API request details for monitoring and debugging.

    Args:
        endpoint: API endpoint path
        method: HTTP method
        status_code: Response status code
        response_time: Request processing time in seconds
        user_id: Optional user identifier
    """
    logger = get_logger("api")

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "method": method,
        "status_code": status_code,
        "response_time": response_time,
        "user_id": user_id,
    }

    if status_code >= 400:
        logger.error(f"API Error: {json.dumps(log_data)}")
    else:
        logger.info(f"API Request: {json.dumps(log_data)}")


def log_error(error: Exception, context: Optional[dict[str, Any]] = None) -> None:
    """
    Log error with context information.

    Args:
        error: Exception instance
        context: Additional context information
    """
    logger = get_logger("error")

    error_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context or {},
    }

    logger.error(f"Error: {json.dumps(error_data)}", exc_info=True)


# Initialize default logger
default_logger = get_logger()
