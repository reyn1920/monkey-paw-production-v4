"""API Discovery routes for exposing available endpoints and documentation."""

from typing import Optional
import logging

# Proper FastAPI imports
try:
    from fastapi import APIRouter, HTTPException, status
    from pydantic import BaseModel
except ImportError:
    # Simple fallback classes for missing dependencies
    class APIRouter:
        def __init__(self, **kwargs):
            self.routes = []

        def get(self, path: str, **kwargs):
            def decorator(func):
                self.routes.append({"method": "GET", "path": path, "func": func})
                return func

            return decorator

        def post(self, path: str, **kwargs):
            def decorator(func):
                self.routes.append({"method": "POST", "path": path, "func": func})
                return func

            return decorator

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str):
            self.status_code = status_code
            self.detail = detail
            super().__init__(detail)

    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    class status:
        HTTP_500_INTERNAL_SERVER_ERROR = 500
        HTTP_404_NOT_FOUND = 404
        HTTP_200_OK = 200


# Logger setup
logger = logging.getLogger(__name__)

# Pydantic Models


class APIEndpoint(BaseModel):
    def __init__(
        self,
        path: str = "",
        method: str = "",
        description: str = "",
        tags: Optional[list[str]] = None,
        **kwargs,
    ):
        self.path = path
        self.method = method
        self.description = description
        self.tags = tags or []
        super().__init__(**kwargs)


class APIDiscoveryResponse(BaseModel):
    def __init__(
        self,
        service_name: str = "",
        version: str = "",
        endpoints: Optional[list[APIEndpoint]] = None,
        health_check: str = "",
        **kwargs,
    ):
        self.service_name = service_name
        self.version = version
        self.endpoints = endpoints or []
        self.health_check = health_check
        super().__init__(**kwargs)


class ServiceInfo(BaseModel):
    def __init__(
        self,
        name: str = "",
        status: str = "",
        version: str = "",
        uptime: Optional[str] = None,
        **kwargs,
    ):
        self.name = name
        self.status = status
        self.version = version
        self.uptime = uptime
        super().__init__(**kwargs)


# Service Class


class APIDiscoveryService:
    """Service for API discovery and documentation."""

    @staticmethod
    def get_available_endpoints() -> list[APIEndpoint]:
        """Get all available API endpoints."""
        try:
            # Define available endpoints
            endpoints = [
                APIEndpoint(
                    path="/api/health",
                    method="GET",
                    description="Health check endpoint",
                    tags=["health"],
                ),
                APIEndpoint(
                    path="/api/channels",
                    method="GET",
                    description="Get all channels",
                    tags=["channels"],
                ),
                APIEndpoint(
                    path="/api/channels",
                    method="POST",
                    description="Create a new channel",
                    tags=["channels"],
                ),
                APIEndpoint(
                    path="/api/channels/{channel_id}",
                    method="GET",
                    description="Get a specific channel",
                    tags=["channels"],
                ),
                APIEndpoint(
                    path="/api/channels/{channel_id}",
                    method="PUT",
                    description="Update a channel",
                    tags=["channels"],
                ),
                APIEndpoint(
                    path="/api/channels/{channel_id}",
                    method="DELETE",
                    description="Delete a channel",
                    tags=["channels"],
                ),
                APIEndpoint(
                    path="/api/pets",
                    method="GET",
                    description="Get all pets",
                    tags=["pets"],
                ),
                APIEndpoint(
                    path="/api/pets",
                    method="POST",
                    description="Create a new pet",
                    tags=["pets"],
                ),
                APIEndpoint(
                    path="/api/pets/{pet_id}",
                    method="GET",
                    description="Get a specific pet",
                    tags=["pets"],
                ),
                APIEndpoint(
                    path="/api/pets/{pet_id}",
                    method="PUT",
                    description="Update a pet",
                    tags=["pets"],
                ),
                APIEndpoint(
                    path="/api/pets/{pet_id}",
                    method="DELETE",
                    description="Delete a pet",
                    tags=["pets"],
                ),
                APIEndpoint(
                    path="/api/upload",
                    method="POST",
                    description="Upload files",
                    tags=["upload"],
                ),
                APIEndpoint(
                    path="/api/discovery",
                    method="GET",
                    description="API discovery endpoint",
                    tags=["discovery"],
                ),
            ]

            return endpoints
        except Exception as e:
            logger.error(f"Error getting available endpoints: {e}")
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to get endpoints"
            )

    @staticmethod
    def get_service_info() -> ServiceInfo:
        """Get service information."""
        try:
            return ServiceInfo(
                name="Online Production API",
                status="healthy",
                version="1.0.0",
                uptime="Available",
            )
        except Exception as e:
            logger.error(f"Error getting service info: {e}")
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to get service info"
            )

    @staticmethod
    def get_api_discovery() -> APIDiscoveryResponse:
        """Get complete API discovery information."""
        try:
            service_info = APIDiscoveryService.get_service_info()
            endpoints = APIDiscoveryService.get_available_endpoints()

            return APIDiscoveryResponse(
                service_name=service_info.name,
                version=service_info.version,
                endpoints=endpoints,
                health_check="/api/health",
            )
        except Exception as e:
            logger.error(f"Error getting API discovery: {e}")
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to get API discovery"
            )


# API Router
router = APIRouter(prefix="/api", tags=["discovery"])


@router.get("/discovery", response_model=APIDiscoveryResponse)
def get_api_discovery():
    """Get API discovery information including all available endpoints."""
    return APIDiscoveryService.get_api_discovery()


@router.get("/endpoints", response_model=list[APIEndpoint])
def get_endpoints():
    """Get list of all available endpoints."""
    return APIDiscoveryService.get_available_endpoints()


@router.get("/service-info", response_model=ServiceInfo)
def get_service_info():
    """Get service information."""
    return APIDiscoveryService.get_service_info()


@router.get("/docs")
def get_api_docs():
    """Get API documentation."""
    return {
        "message": "API Documentation",
        "swagger_ui": "/docs",
        "redoc": "/redoc",
        "openapi_json": "/openapi.json",
        "discovery": "/api/discovery",
    }


@router.get("/health")
def health_check():
    """Health check endpoint for API discovery service."""
    return {"status": "healthy", "service": "api-discovery"}
