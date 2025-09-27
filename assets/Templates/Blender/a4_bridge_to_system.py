"""
System Bridge for inter-service communication and system integration.
Provides APIs for connecting different system components and external services.
"""

import asyncio
import json
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import websockets
from abc import ABC, abstractmethod
import uuid
import time
from typing import Optional
from typing import Any
from typing import Callable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServiceType(Enum):
    """Types of services that can be bridged."""

    DATABASE = "database"
    API = "api"
    WEBSOCKET = "websocket"
    MESSAGE_QUEUE = "message_queue"
    CACHE = "cache"
    FILE_SYSTEM = "file_system"
    EXTERNAL_API = "external_api"


class ConnectionStatus(Enum):
    """Connection status for services."""

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    ERROR = "error"
    TIMEOUT = "timeout"


class MessageType(Enum):
    """Types of messages that can be sent through the bridge."""

    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"


@dataclass
class ServiceConfig:
    """Configuration for a service connection."""

    service_id: str
    service_type: ServiceType
    endpoint: str
    credentials: Optional[dict[str, str]] = None
    timeout: int = 30
    retry_attempts: int = 3
    health_check_interval: int = 60


@dataclass
class Message:
    """Message structure for inter-service communication."""

    id: str
    message_type: MessageType
    source_service: str
    target_service: str
    payload: dict[str, Any]
    timestamp: datetime
    correlation_id: Optional[str] = None
    ttl: Optional[int] = None


@dataclass
class ServiceHealth:
    """Health status of a service."""

    service_id: str
    status: ConnectionStatus
    last_check: datetime
    response_time: float
    error_count: int = 0
    uptime_percentage: float = 100.0


class ServiceConnector(ABC):
    """Abstract base class for service connectors."""

    def __init__(self, config: ServiceConfig):
        self.config = config
        self.status = ConnectionStatus.DISCONNECTED
        self.last_activity = datetime.now()
        self.error_count = 0

    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the service."""

    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from the service."""

    @abstractmethod
    async def send_message(self, message: Message) -> Optional[Message]:
        """Send a message to the service."""

    @abstractmethod
    async def health_check(self) -> ServiceHealth:
        """Check the health of the service."""


class HTTPConnector(ServiceConnector):
    """HTTP/REST API connector."""

    def __init__(self, config: ServiceConfig):
        super().__init__(config)
        self.session: Optional[aiohttp.ClientSession] = None

    async def connect(self) -> bool:
        """Establish HTTP session."""
        try:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )
            self.status = ConnectionStatus.CONNECTED
            logger.info(f"HTTP connector established for {self.config.service_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to establish HTTP connector: {e}")
            self.status = ConnectionStatus.ERROR
            return False

    async def disconnect(self) -> bool:
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None
        self.status = ConnectionStatus.DISCONNECTED
        return True

    async def send_message(self, message: Message) -> Optional[Message]:
        """Send HTTP request."""
        if not self.session or self.status != ConnectionStatus.CONNECTED:
            return None

        try:
            headers = {"Content-Type": "application/json"}
            if self.config.credentials:
                headers.update(self.config.credentials)

            async with self.session.post(
                self.config.endpoint, json=asdict(message), headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return Message(
                        id=str(uuid.uuid4()),
                        message_type=MessageType.RESPONSE,
                        source_service=message.target_service,
                        target_service=message.source_service,
                        payload=data,
                        timestamp=datetime.now(),
                        correlation_id=message.id,
                    )
        except Exception as e:
            logger.error(f"HTTP send failed: {e}")
            self.error_count += 1

        return None

    async def health_check(self) -> ServiceHealth:
        """Check HTTP service health."""
        start_time = time.time()
        try:
            if self.session:
                async with self.session.get(
                    f"{self.config.endpoint}/health"
                ) as response:
                    response_time = time.time() - start_time
                    status = (
                        ConnectionStatus.CONNECTED
                        if response.status == 200
                        else ConnectionStatus.ERROR
                    )
            else:
                status = ConnectionStatus.DISCONNECTED
                response_time = 0
        except Exception:
            status = ConnectionStatus.ERROR
            response_time = time.time() - start_time

        return ServiceHealth(
            service_id=self.config.service_id,
            status=status,
            last_check=datetime.now(),
            response_time=response_time,
            error_count=self.error_count,
        )


class WebSocketConnector(ServiceConnector):
    """WebSocket connector for real-time communication."""

    def __init__(self, config: ServiceConfig):
        super().__init__(config)
        self.websocket: Optional[Any] = None
        self.message_handlers: list[Callable[[Message], None]] = []

    async def connect(self) -> bool:
        """Establish WebSocket connection."""
        try:
            self.websocket = await websockets.connect(self.config.endpoint)
            self.status = ConnectionStatus.CONNECTED
            logger.info(f"WebSocket connector established for {self.config.service_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to establish WebSocket connector: {e}")
            self.status = ConnectionStatus.ERROR
            return False

    async def disconnect(self) -> bool:
        """Close WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
        self.status = ConnectionStatus.DISCONNECTED
        return True

    async def send_message(self, message: Message) -> Optional[Message]:
        """Send WebSocket message."""
        if not self.websocket or self.status != ConnectionStatus.CONNECTED:
            return None

        try:
            await self.websocket.send(json.dumps(asdict(message)))
            return message
        except Exception as e:
            logger.error(f"WebSocket send failed: {e}")
            self.error_count += 1
            return None

    async def health_check(self) -> ServiceHealth:
        """Check WebSocket service health."""
        status = (
            ConnectionStatus.CONNECTED
            if self.websocket and not self.websocket.closed
            else ConnectionStatus.DISCONNECTED
        )

        return ServiceHealth(
            service_id=self.config.service_id,
            status=status,
            last_check=datetime.now(),
            response_time=0.0,
            error_count=self.error_count,
        )


class MessageRouter:
    """Routes messages between services."""

    def __init__(self):
        self.routes: dict[str, list[str]] = {}
        self.message_handlers: dict[str, Callable[[Message], None]] = {}

    def add_route(self, source_service: str, target_services: list[str]):
        """Add a routing rule."""
        self.routes[source_service] = target_services

    def add_message_handler(self, service_id: str, handler: Callable[[Message], None]):
        """Add a message handler for a service."""
        self.message_handlers[service_id] = handler

    async def route_message(
        self, message: Message, bridge: "SystemBridge"
    ) -> list[Message]:
        """Route a message to appropriate services."""
        results = []
        target_services = self.routes.get(
            message.source_service, [message.target_service]
        )

        for target_service in target_services:
            if target_service in bridge.connectors:
                routed_message = Message(
                    id=str(uuid.uuid4()),
                    message_type=message.message_type,
                    source_service=message.source_service,
                    target_service=target_service,
                    payload=message.payload,
                    timestamp=datetime.now(),
                    correlation_id=message.correlation_id or message.id,
                )

                result = await bridge.send_message(target_service, routed_message)
                if result:
                    results.append(result)

        return results


class SystemBridge:
    """Main system bridge for managing service connections and communication."""

    def __init__(self):
        self.connectors: dict[str, ServiceConnector] = {}
        self.message_router = MessageRouter()
        self.health_monitor_task: Optional[asyncio.Task[None]] = None
        self.message_queue: asyncio.Queue[Message] = asyncio.Queue()
        self.running = False

    def register_service(self, config: ServiceConfig) -> bool:
        """Register a new service with the bridge."""
        try:
            if (
                config.service_type == ServiceType.API
                or config.service_type == ServiceType.EXTERNAL_API
            ):
                connector = HTTPConnector(config)
            elif config.service_type == ServiceType.WEBSOCKET:
                connector = WebSocketConnector(config)
            else:
                # For other service types, use HTTP as default
                connector = HTTPConnector(config)

            self.connectors[config.service_id] = connector
            logger.info(f"Registered service: {config.service_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to register service {config.service_id}: {e}")
            return False

    async def connect_all_services(self) -> dict[str, bool]:
        """Connect to all registered services."""
        results = {}
        for service_id, connector in self.connectors.items():
            try:
                results[service_id] = await connector.connect()
            except Exception as e:
                logger.error(f"Failed to connect to {service_id}: {e}")
                results[service_id] = False
        return results

    async def disconnect_all_services(self) -> dict[str, bool]:
        """Disconnect from all services."""
        results = {}
        for service_id, connector in self.connectors.items():
            try:
                results[service_id] = await connector.disconnect()
            except Exception as e:
                logger.error(f"Failed to disconnect from {service_id}: {e}")
                results[service_id] = False
        return results

    async def send_message(
        self, target_service: str, message: Message
    ) -> Optional[Message]:
        """Send a message to a specific service."""
        connector = self.connectors.get(target_service)
        if not connector:
            logger.error(f"Service not found: {target_service}")
            return None

        return await connector.send_message(message)

    async def broadcast_message(
        self, message: Message, exclude_services: Optional[list[str]] = None
    ) -> list[Message]:
        """Broadcast a message to all connected services."""
        exclude_services = exclude_services or []
        results = []

        for service_id, connector in self.connectors.items():
            if (
                service_id not in exclude_services
                and connector.status == ConnectionStatus.CONNECTED
            ):
                result = await connector.send_message(message)
                if result:
                    results.append(result)

        return results

    async def get_service_health(self, service_id: str) -> Optional[ServiceHealth]:
        """Get health status of a specific service."""
        connector = self.connectors.get(service_id)
        if connector:
            return await connector.health_check()
        return None

    async def get_all_service_health(self) -> dict[str, ServiceHealth]:
        """Get health status of all services."""
        health_status = {}
        for service_id, connector in self.connectors.items():
            health_status[service_id] = await connector.health_check()
        return health_status

    async def start_health_monitoring(self, interval: int = 60):
        """Start periodic health monitoring."""

        async def monitor():
            while self.running:
                try:
                    health_status = await self.get_all_service_health()
                    for service_id, health in health_status.items():
                        if health.status == ConnectionStatus.ERROR:
                            logger.warning(
                                f"Service {service_id} is unhealthy: {health.status}"
                            )

                    await asyncio.sleep(interval)
                except Exception as e:
                    logger.error(f"Health monitoring error: {e}")
                    await asyncio.sleep(interval)

        self.running = True
        self.health_monitor_task = asyncio.create_task(monitor())

    async def stop_health_monitoring(self):
        """Stop health monitoring."""
        self.running = False
        if self.health_monitor_task:
            self.health_monitor_task.cancel()
            try:
                await self.health_monitor_task
            except asyncio.CancelledError:
                pass

    async def process_message_queue(self):
        """Process messages from the queue."""
        while self.running:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                await self.message_router.route_message(message, self)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Message processing error: {e}")


# Global bridge instance
system_bridge = SystemBridge()


async def main():
    """Example usage of the system bridge."""
    # Register services
    api_config = ServiceConfig(
        service_id="user_api",
        service_type=ServiceType.API,
        endpoint="http://localhost:8001/api",
        timeout=30,
    )

    ws_config = ServiceConfig(
        service_id="notification_ws",
        service_type=ServiceType.WEBSOCKET,
        endpoint="ws://localhost:8002/ws",
        timeout=30,
    )

    system_bridge.register_service(api_config)
    system_bridge.register_service(ws_config)

    # Connect to services
    connection_results = await system_bridge.connect_all_services()
    print(f"Connection results: {connection_results}")

    # Send a test message
    test_message = Message(
        id=str(uuid.uuid4()),
        message_type=MessageType.REQUEST,
        source_service="bridge",
        target_service="user_api",
        payload={"action": "get_user", "user_id": "123"},
        timestamp=datetime.now(),
    )

    response = await system_bridge.send_message("user_api", test_message)
    if response:
        print(f"Received response: {response.payload}")

    # Check health
    health_status = await system_bridge.get_all_service_health()
    for service_id, health in health_status.items():
        print(
            f"Service {service_id}: {health.status} (Response time: {health.response_time:.3f}s)"
        )

    # Start monitoring
    await system_bridge.start_health_monitoring()

    # Simulate running for a short time
    await asyncio.sleep(5)

    # Cleanup
    await system_bridge.stop_health_monitoring()
    await system_bridge.disconnect_all_services()


if __name__ == "__main__":
    asyncio.run(main())
