"""Production Initialization Module

This module handles the initialization and configuration of the production environment,
including database setup, logging configuration, and system health checks.
"""

import asyncio
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("production.log")],
)

logger = logging.getLogger(__name__)

# Optional imports with fallbacks
try:
    import uvicorn
except ImportError:
    uvicorn = None
    logger.warning("uvicorn not installed")

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.middleware.gzip import GZipMiddleware
    from fastapi.middleware.trustedhost import TrustedHostMiddleware
except ImportError:
    FastAPI = None
    CORSMiddleware = None
    GZipMiddleware = None
    TrustedHostMiddleware = None
    logger.warning("FastAPI not installed")

try:
    import psutil
except ImportError:
    psutil = None
    logger.warning("psutil not installed")


class ProductionConfig:
    """Production configuration settings."""

    def __init__(self):
        self.debug = False
        self.testing = False
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", 8000))
        self.workers = int(os.getenv("WORKERS", 4))
        self.reload = False
        self.access_log = True
        self.log_level = "info"

        # Security settings
        self.allowed_hosts = os.getenv("ALLOWED_HOSTS", "*").split(",")
        self.cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")

        # Database settings
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./production.db")
        self.database_pool_size = int(os.getenv("DATABASE_POOL_SIZE", 10))
        self.database_max_overflow = int(os.getenv("DATABASE_MAX_OVERFLOW", 20))

        # Redis settings
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

        # API settings
        self.api_rate_limit = int(os.getenv("API_RATE_LIMIT", 100))
        self.api_timeout = int(os.getenv("API_TIMEOUT", 30))

        # Monitoring settings
        self.enable_metrics = os.getenv("ENABLE_METRICS", "true").lower() == "true"
        self.metrics_port = int(os.getenv("METRICS_PORT", 9090))

        # Feature flags
        self.enable_caching = os.getenv("ENABLE_CACHING", "true").lower() == "true"
        self.enable_compression = (
            os.getenv("ENABLE_COMPRESSION", "true").lower() == "true"
        )
        self.enable_rate_limiting = (
            os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
        )

    def validate(self) -> bool:
        """Validate configuration settings."""
        try:
            # Validate port range
            if not (1 <= self.port <= 65535):
                raise ValueError(f"Invalid port: {self.port}")

            # Validate workers count
            if self.workers < 1:
                raise ValueError(f"Invalid workers count: {self.workers}")

            # Validate database URL
            if not self.database_url:
                raise ValueError("Database URL is required")

            logger.info("Configuration validation passed")
            return True

        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False


class ProductionInitializer:
    """Handles production environment initialization."""

    def __init__(self, config: ProductionConfig):
        self.config = config
        self.app: Optional[Any] = None
        self.startup_time = datetime.utcnow()
        self.health_checks: dict[str, bool] = {}

    async def initialize_database(self) -> bool:
        """Initialize database connections and run migrations."""
        try:
            logger.info("Initializing database...")

            # Try to import database modules
            try:
                from sqlalchemy import create_engine, text
            except ImportError:
                logger.warning(
                    "SQLAlchemy not installed, skipping database initialization"
                )
                self.health_checks["database"] = False
                return False

            # Create database engine
            engine = create_engine(
                self.config.database_url,
                pool_size=self.config.database_pool_size,
                max_overflow=self.config.database_max_overflow,
                echo=False,
            )

            # Test database connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                if result.fetchone()[0] != 1:
                    raise Exception("Database connection test failed")

            logger.info("Database initialized successfully")
            self.health_checks["database"] = True
            return True

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            self.health_checks["database"] = False
            return False

    async def initialize_redis(self) -> bool:
        """Initialize Redis connection."""
        try:
            logger.info("Initializing Redis...")

            try:
                import redis.asyncio as redis
            except ImportError:
                logger.warning("Redis not installed, skipping Redis initialization")
                self.health_checks["redis"] = False
                return False

            # Create Redis client
            redis_client = redis.from_url(self.config.redis_url)

            # Test Redis connection
            await redis_client.ping()
            await redis_client.close()

            logger.info("Redis initialized successfully")
            self.health_checks["redis"] = True
            return True

        except Exception as e:
            logger.error(f"Redis initialization failed: {e}")
            self.health_checks["redis"] = False
            return False

    def setup_middleware(self, app: Any) -> None:
        """Setup application middleware."""
        if not FastAPI or not CORSMiddleware:
            logger.warning("FastAPI not available, skipping middleware setup")
            return

        logger.info("Setting up middleware...")

        # CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Trusted host middleware
        if self.config.allowed_hosts != ["*"] and TrustedHostMiddleware:
            app.add_middleware(
                TrustedHostMiddleware, allowed_hosts=self.config.allowed_hosts
            )

        # Compression middleware
        if self.config.enable_compression and GZipMiddleware:
            app.add_middleware(GZipMiddleware, minimum_size=1000)

        logger.info("Middleware setup completed")

    def setup_logging(self) -> None:
        """Setup production logging configuration."""
        logger.info("Setting up production logging...")

        # Configure uvicorn logging if available
        if uvicorn:
            uvicorn_logger = logging.getLogger("uvicorn")
            uvicorn_logger.setLevel(logging.INFO)

            # Configure access logging
            access_logger = logging.getLogger("uvicorn.access")
            access_logger.setLevel(logging.INFO)

        # Configure application logging
        app_logger = logging.getLogger("app")
        app_logger.setLevel(logging.INFO)

        logger.info("Production logging configured")

    async def run_health_checks(self) -> dict[str, bool]:
        """Run comprehensive health checks."""
        logger.info("Running health checks...")

        # Database health check
        await self.initialize_database()

        # Redis health check
        await self.initialize_redis()

        # File system health check
        try:
            test_file = Path("health_check.tmp")
            test_file.write_text("health check")
            test_file.unlink()
            self.health_checks["filesystem"] = True
        except Exception as e:
            logger.error(f"Filesystem health check failed: {e}")
            self.health_checks["filesystem"] = False

        # Memory health check
        if psutil:
            try:
                memory = psutil.virtual_memory()
                if memory.percent > 90:
                    logger.warning(f"High memory usage: {memory.percent}%")
                self.health_checks["memory"] = memory.percent < 95
            except Exception as e:
                logger.error(f"Memory health check failed: {e}")
                self.health_checks["memory"] = False
        else:
            self.health_checks["memory"] = True  # Skip if psutil not available

        # Disk space health check
        try:
            disk_usage = shutil.disk_usage("/")
            free_percent = (disk_usage.free / disk_usage.total) * 100
            if free_percent < 10:
                logger.warning(f"Low disk space: {free_percent:.1f}% free")
            self.health_checks["disk"] = free_percent > 5
        except Exception as e:
            logger.error(f"Disk health check failed: {e}")
            self.health_checks["disk"] = False

        logger.info(f"Health checks completed: {self.health_checks}")
        return self.health_checks

    async def initialize_app(self, app: Any) -> bool:
        """Initialize the FastAPI application for production."""
        try:
            logger.info("Initializing application for production...")

            self.app = app

            # Setup middleware
            self.setup_middleware(app)

            # Setup logging
            self.setup_logging()

            # Run health checks
            health_results = await self.run_health_checks()

            # Check if critical services are healthy
            critical_services = ["filesystem"]
            for service in critical_services:
                if not health_results.get(service, False):
                    logger.error(f"Critical service {service} is not healthy")
                    return False

            logger.info("Application initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Application initialization failed: {e}")
            return False

    def get_server_config(self) -> dict[str, Any]:
        """Get uvicorn server configuration."""
        return {
            "host": self.config.host,
            "port": self.config.port,
            "workers": self.config.workers,
            "reload": self.config.reload,
            "access_log": self.config.access_log,
            "log_level": self.config.log_level,
        }

    def get_system_info(self) -> dict[str, Any]:
        """Get system information for monitoring."""
        try:
            import platform

            info = {
                "startup_time": self.startup_time.isoformat(),
                "uptime_seconds": (
                    datetime.utcnow() - self.startup_time
                ).total_seconds(),
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "health_checks": self.health_checks,
            }

            if psutil:
                info.update(
                    {
                        "cpu_count": psutil.cpu_count(),
                        "memory_total": psutil.virtual_memory().total,
                        "memory_available": psutil.virtual_memory().available,
                    }
                )

            try:
                disk_usage = shutil.disk_usage("/")
                info["disk_usage"] = {
                    "total": disk_usage.total,
                    "used": disk_usage.used,
                    "free": disk_usage.free,
                }
            except Exception:
                pass

            return info

        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return {"startup_time": self.startup_time.isoformat(), "error": str(e)}


async def initialize_production_environment(app: Any) -> ProductionInitializer:
    """Initialize the production environment."""
    logger.info("Starting production environment initialization...")

    # Load configuration
    config = ProductionConfig()

    # Validate configuration
    if not config.validate():
        raise RuntimeError("Configuration validation failed")

    # Create initializer
    initializer = ProductionInitializer(config)

    # Initialize application
    success = await initializer.initialize_app(app)
    if not success:
        raise RuntimeError("Application initialization failed")

    logger.info("Production environment initialized successfully")
    return initializer


def run_production_server(app: Any) -> None:
    """Run the production server."""
    if not uvicorn:
        logger.error("uvicorn not available, cannot start server")
        sys.exit(1)

    logger.info("Starting production server...")

    # Initialize production environment
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        initializer = loop.run_until_complete(initialize_production_environment(app))

        # Get server configuration
        server_config = initializer.get_server_config()

        # Start the server
        uvicorn.run(app, **server_config)

    except Exception as e:
        logger.error(f"Failed to start production server: {e}")
        sys.exit(1)
    finally:
        loop.close()


if __name__ == "__main__":
    # This can be used for testing the production initialization
    if FastAPI:
        app = FastAPI(title="Production Test")
        run_production_server(app)
    else:
        logger.error("FastAPI not available for testing")
        sys.exit(1)
