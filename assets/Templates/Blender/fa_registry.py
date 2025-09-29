"""
Service Registry for managing application services.
"""

from typing import Dict, Any, Type, TypeVar, Callable, Optional
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class BaseService:
    """Base class for all services."""
    
    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__
    
    async def initialize(self):
        """Initialize the service."""
        pass
    
    async def shutdown(self):
        """Shutdown the service."""
        pass


class ServiceRegistry:
    """Registry for managing application services."""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[Type[Any], Callable[[], Any]] = {}
        self._instances: Dict[Type[Any], Any] = {}
    
    def register_service(self, name: str, service: Any):
        """Register a service by name."""
        self._services[name] = service
        logger.info(f"Registered service: {name}")
    
    def get_service(self, name: str) -> Any:
        """Get a service by name."""
        if name not in self._services:
            raise KeyError(f"Service '{name}' not found")
        return self._services[name]
    
    def has_service(self, name: str) -> bool:
        """Check if a service is registered."""
        return name in self._services
    
    def register(self, service_type: Type[T], instance: T):
        """Register a service instance by type."""
        self._instances[service_type] = instance
        logger.info(f"Registered instance for: {service_type.__name__}")

    def register_factory(self, service_type: Type[T], factory: Callable[[], T]):
        """Register a factory for a service type."""
        self._factories[service_type] = factory
        logger.info(f"Registered factory for: {service_type.__name__}")
    
    def get(self, service_type: Type[T]) -> T:
        """Get a service instance by type."""
        if service_type in self._instances:
            return self._instances[service_type]
        
        if service_type in self._factories:
            instance = self._factories[service_type]()
            self._instances[service_type] = instance
            return instance
        
        raise ValueError(f"No factory registered for {service_type.__name__}")
    
    def list_services(self) -> Dict[str, Any]:
        """List all registered services."""
        return self._services.copy()
    
    async def initialize_all(self):
        """Initialize all services."""
        for service in self._services.values():
            if hasattr(service, 'initialize'):
                await service.initialize()
        
        for instance in self._instances.values():
            if hasattr(instance, 'initialize'):
                await instance.initialize()
    
    async def shutdown_all(self):
        """Shutdown all services."""
        for service in self._services.values():
            if hasattr(service, 'shutdown'):
                await service.shutdown()
        
        for instance in self._instances.values():
            if hasattr(instance, 'shutdown'):
                await instance.shutdown()


# Global service registry instance
_global_registry: Optional[ServiceRegistry] = None


def get_service_registry() -> ServiceRegistry:
    """Get the global service registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = ServiceRegistry()
    return _global_registry


def set_service_registry(registry: ServiceRegistry):
    """Set the global service registry."""
    global _global_registry
    _global_registry = registry