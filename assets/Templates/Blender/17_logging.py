"""
Logging configuration and utilities.
"""

import logging
import sys
from typing import Optional
from pathlib import Path


class Logger:
    """Application logger with configurable levels and formatting."""
    
    def __init__(self, name: str = "app", level: str = "INFO"):
        self.name = name
        self.level = level.upper()
        self._logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up the logger with proper formatting."""
        logger = logging.getLogger(self.name)
        logger.setLevel(getattr(logging, self.level))
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, self.level))
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        return logger
    
    def debug(self, message: str) -> None:
        """Log debug message."""
        self._logger.debug(message)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        # Handle extra parameter for compatibility
        if 'extra' in kwargs:
            # For now, just log the message without the extra context
            pass
        self._logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        self._logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message."""
        self._logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log critical message."""
        self._logger.critical(message)


class StructuredLogger(Logger):
    """Structured logger with additional context support."""
    
    def __init__(self, name: str = "app", level: str = "INFO"):
        super().__init__(name, level)
    
    def log_with_context(self, level: str, message: str, context: dict[str, str] | None = None):
        """Log message with additional context."""
        if context:
            message = f"{message} | Context: {context}"
        getattr(self._logger, level.lower())(message)


def get_logger(name: str = "app", level: str = "INFO") -> Logger:
    """Get a configured logger instance."""
    return Logger(name, level)


def get_structured_logger(name: str = "app", level: str = "INFO") -> StructuredLogger:
    """Get a structured logger instance."""
    return StructuredLogger(name, level)


logger = get_logger()