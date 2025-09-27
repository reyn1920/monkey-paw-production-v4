"""
WebSocket Manager

This module provides WebSocket connection management and real-time communication
capabilities for the TRAE.AI dashboard system.
"""

import asyncio
import json
import logging
import uuid
from typing import Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConnectionStatus(Enum):
    """WebSocket connection status enumeration"""

    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    RECONNECTING = "reconnecting"


class MessageType(Enum):
    """WebSocket message type enumeration"""

    PING = "ping"
    PONG = "pong"
    DATA = "data"
    COMMAND = "command"
    RESPONSE = "response"
    ERROR = "error"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"


@dataclass
class WebSocketMessage:
    """WebSocket message data structure"""

    id: str
    type: MessageType
    payload: dict[str, Any]
    timestamp: datetime
    sender: Optional[str] = None
    recipient: Optional[str] = None


@dataclass
class ConnectionInfo:
    """Connection information data structure"""

    connection_id: str
    user_id: Optional[str]
    session_id: Optional[str]
    connected_at: datetime
    last_activity: datetime
    status: ConnectionStatus
    metadata: dict[str, Any]


class WebSocketConnection:
    """Individual WebSocket connection wrapper"""

    def __init__(self, connection_id: str, websocket, user_id: Optional[str] = None):
        self.connection_id = connection_id
        self.websocket = websocket
        self.user_id = user_id
        self.session_id = str(uuid.uuid4())
        self.connected_at = datetime.now(timezone.utc)
        self.last_activity = datetime.now(timezone.utc)
        self.status = ConnectionStatus.CONNECTED
        self.metadata: dict[str, Any] = {}
        self.subscriptions: set[str] = set()

    async def send_message(self, message: WebSocketMessage) -> bool:
        """Send a message through this connection"""
        try:
            message_data = {
                "id": message.id,
                "type": message.type.value,
                "payload": message.payload,
                "timestamp": message.timestamp.isoformat(),
                "sender": message.sender,
                "recipient": message.recipient,
            }

            await self.websocket.send(json.dumps(message_data))
            self.last_activity = datetime.now(timezone.utc)
            return True

        except Exception as e:
            logger.error(
                f"Failed to send message to connection {self.connection_id}: {e}"
            )
            self.status = ConnectionStatus.ERROR
            return False

    async def send_json(self, data: dict[str, Any]) -> bool:
        """Send JSON data through this connection"""
        try:
            await self.websocket.send(json.dumps(data))
            self.last_activity = datetime.now(timezone.utc)
            return True
        except Exception as e:
            logger.error(f"Failed to send JSON to connection {self.connection_id}: {e}")
            self.status = ConnectionStatus.ERROR
            return False

    def get_info(self) -> ConnectionInfo:
        """Get connection information"""
        return ConnectionInfo(
            connection_id=self.connection_id,
            user_id=self.user_id,
            session_id=self.session_id,
            connected_at=self.connected_at,
            last_activity=self.last_activity,
            status=self.status,
            metadata=self.metadata,
        )


class WebSocketManager:
    """
    WebSocket Manager for handling multiple WebSocket connections and real-time communication
    """

    def __init__(self):
        self.connections: dict[str, WebSocketConnection] = {}
        self.user_connections: dict[str, set[str]] = {}  # user_id -> connection_ids
        self.subscriptions: dict[str, set[str]] = {}  # topic -> connection_ids
        self.message_handlers: dict[
            MessageType, list[Callable[[str, WebSocketMessage], Any]]
        ] = {}
        self.heartbeat_interval = 30  # seconds
        self.heartbeat_task: Optional[asyncio.Task[None]] = None
        self.running = False

    async def start(self):
        """Start the WebSocket manager"""
        logger.info("Starting WebSocket Manager")
        self.running = True

        # Start heartbeat task
        self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())

    async def stop(self):
        """Stop the WebSocket manager"""
        logger.info("Stopping WebSocket Manager")
        self.running = False

        # Cancel heartbeat task
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass

        # Close all connections
        await self.disconnect_all()

    async def add_connection(self, websocket, user_id: Optional[str] = None) -> str:
        """Add a new WebSocket connection"""
        connection_id = str(uuid.uuid4())
        connection = WebSocketConnection(connection_id, websocket, user_id)

        self.connections[connection_id] = connection

        # Track user connections
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = set()
            self.user_connections[user_id].add(connection_id)

        logger.info(f"Added WebSocket connection {connection_id} for user {user_id}")
        return connection_id

    async def remove_connection(self, connection_id: str):
        """Remove a WebSocket connection"""
        if connection_id not in self.connections:
            return

        connection = self.connections[connection_id]

        # Remove from user connections
        if connection.user_id and connection.user_id in self.user_connections:
            self.user_connections[connection.user_id].discard(connection_id)
            if not self.user_connections[connection.user_id]:
                del self.user_connections[connection.user_id]

        # Remove from subscriptions
        for topic in list(connection.subscriptions):
            await self.unsubscribe(connection_id, topic)

        # Remove connection
        del self.connections[connection_id]

        logger.info(f"Removed WebSocket connection {connection_id}")

    async def send_to_connection(
        self, connection_id: str, message: WebSocketMessage
    ) -> bool:
        """Send a message to a specific connection"""
        if connection_id not in self.connections:
            logger.warning(f"Connection {connection_id} not found")
            return False

        connection = self.connections[connection_id]
        return await connection.send_message(message)

    async def send_to_user(self, user_id: str, message: WebSocketMessage) -> int:
        """Send a message to all connections for a specific user"""
        if user_id not in self.user_connections:
            logger.warning(f"No connections found for user {user_id}")
            return 0

        sent_count = 0
        for connection_id in list(self.user_connections[user_id]):
            if await self.send_to_connection(connection_id, message):
                sent_count += 1

        return sent_count

    async def broadcast(
        self, message: WebSocketMessage, exclude_connections: Optional[set[str]] = None
    ) -> int:
        """Broadcast a message to all connections"""
        exclude_connections = exclude_connections or set()
        sent_count = 0

        for connection_id in list(self.connections.keys()):
            if connection_id not in exclude_connections:
                if await self.send_to_connection(connection_id, message):
                    sent_count += 1

        return sent_count

    async def subscribe(self, connection_id: str, topic: str) -> bool:
        """Subscribe a connection to a topic"""
        if connection_id not in self.connections:
            return False

        connection = self.connections[connection_id]
        connection.subscriptions.add(topic)

        if topic not in self.subscriptions:
            self.subscriptions[topic] = set()
        self.subscriptions[topic].add(connection_id)

        logger.info(f"Connection {connection_id} subscribed to topic {topic}")
        return True

    async def unsubscribe(self, connection_id: str, topic: str) -> bool:
        """Unsubscribe a connection from a topic"""
        if connection_id not in self.connections:
            return False

        connection = self.connections[connection_id]
        connection.subscriptions.discard(topic)

        if topic in self.subscriptions:
            self.subscriptions[topic].discard(connection_id)
            if not self.subscriptions[topic]:
                del self.subscriptions[topic]

        logger.info(f"Connection {connection_id} unsubscribed from topic {topic}")
        return True

    async def publish_to_topic(self, topic: str, message: WebSocketMessage) -> int:
        """Publish a message to all subscribers of a topic"""
        if topic not in self.subscriptions:
            return 0

        sent_count = 0
        for connection_id in list(self.subscriptions[topic]):
            if await self.send_to_connection(connection_id, message):
                sent_count += 1

        return sent_count

    def add_message_handler(
        self, message_type: MessageType, handler: Callable[[str, WebSocketMessage], Any]
    ):
        """Add a message handler for a specific message type"""
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)

    async def handle_message(self, connection_id: str, raw_message: str):
        """Handle an incoming message from a connection"""
        try:
            data = json.loads(raw_message)

            # Update connection activity
            if connection_id in self.connections:
                self.connections[connection_id].last_activity = datetime.now(
                    timezone.utc
                )

            # Create message object
            message = WebSocketMessage(
                id=data.get("id", str(uuid.uuid4())),
                type=MessageType(data.get("type", "data")),
                payload=data.get("payload", {}),
                timestamp=datetime.fromisoformat(
                    data.get("timestamp", datetime.now(timezone.utc).isoformat())
                ),
                sender=data.get("sender"),
                recipient=data.get("recipient"),
            )

            # Handle ping/pong
            if message.type == MessageType.PING:
                await self._handle_ping(connection_id, message)
                return

            # Call registered handlers
            if message.type in self.message_handlers:
                for handler in self.message_handlers[message.type]:
                    try:
                        await handler(connection_id, message)
                    except Exception as e:
                        logger.error(f"Error in message handler: {e}")

        except Exception as e:
            logger.error(f"Error handling message from connection {connection_id}: {e}")

            # Send error response
            error_message = WebSocketMessage(
                id=str(uuid.uuid4()),
                type=MessageType.ERROR,
                payload={"error": "Invalid message format", "details": str(e)},
                timestamp=datetime.now(timezone.utc),
            )
            await self.send_to_connection(connection_id, error_message)

    async def _handle_ping(self, connection_id: str, ping_message: WebSocketMessage):
        """Handle ping message by sending pong response"""
        pong_message = WebSocketMessage(
            id=str(uuid.uuid4()),
            type=MessageType.PONG,
            payload={"ping_id": ping_message.id},
            timestamp=datetime.now(timezone.utc),
        )
        await self.send_to_connection(connection_id, pong_message)

    async def _heartbeat_loop(self):
        """Heartbeat loop to maintain connection health"""
        while self.running:
            try:
                await asyncio.sleep(self.heartbeat_interval)

                if not self.running:
                    break

                # Send heartbeat to all connections
                heartbeat_message = WebSocketMessage(
                    id=str(uuid.uuid4()),
                    type=MessageType.HEARTBEAT,
                    payload={"timestamp": datetime.now(timezone.utc).isoformat()},
                    timestamp=datetime.now(timezone.utc),
                )

                # Remove stale connections
                stale_connections = []
                current_time = datetime.now(timezone.utc)

                for connection_id, connection in self.connections.items():
                    time_since_activity = (
                        current_time - connection.last_activity
                    ).total_seconds()

                    if (
                        time_since_activity > self.heartbeat_interval * 3
                    ):  # 3 missed heartbeats
                        stale_connections.append(connection_id)
                    else:
                        await connection.send_message(heartbeat_message)

                # Clean up stale connections
                for connection_id in stale_connections:
                    logger.info(f"Removing stale connection {connection_id}")
                    await self.remove_connection(connection_id)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in heartbeat loop: {e}")

    async def disconnect_all(self):
        """Disconnect all WebSocket connections"""
        connection_ids = list(self.connections.keys())
        for connection_id in connection_ids:
            await self.remove_connection(connection_id)

    def get_connection_count(self) -> int:
        """Get the total number of active connections"""
        return len(self.connections)

    def get_user_connection_count(self, user_id: str) -> int:
        """Get the number of connections for a specific user"""
        return len(self.user_connections.get(user_id, set()))

    def get_topic_subscriber_count(self, topic: str) -> int:
        """Get the number of subscribers for a specific topic"""
        return len(self.subscriptions.get(topic, set()))

    def get_status(self) -> dict[str, Any]:
        """Get WebSocket manager status"""
        return {
            "running": self.running,
            "total_connections": self.get_connection_count(),
            "total_users": len(self.user_connections),
            "total_topics": len(self.subscriptions),
            "heartbeat_interval": self.heartbeat_interval,
        }

    def get_connections_info(self) -> list[dict[str, Any]]:
        """Get information about all connections"""
        return [
            asdict(connection.get_info()) for connection in self.connections.values()
        ]


# Global WebSocket manager instance
websocket_manager = WebSocketManager()


async def main():
    """Main function for testing"""
    manager = WebSocketManager()
    await manager.start()

    print("WebSocket Manager started")
    print(f"Status: {manager.get_status()}")

    await asyncio.sleep(1)
    await manager.stop()
    print("WebSocket Manager stopped")


if __name__ == "__main__":
    asyncio.run(main())
