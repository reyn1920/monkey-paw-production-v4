"""
Test configuration and fixtures for pytest.
"""

import pytest
import asyncio
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Import core modules
from src.core.config import Config
from src.services.registry import ServiceRegistry


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def config():
    """Provide a test configuration instance."""
    return Config()


@pytest.fixture
def service_registry():
    """Provide a clean service registry for tests."""
    registry = ServiceRegistry()
    return registry


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    os.environ.setdefault("TESTING", "true")
    os.environ.setdefault("LOG_LEVEL", "DEBUG")
    yield
    # Cleanup after test
    if "TESTING" in os.environ:
        del os.environ["TESTING"]
