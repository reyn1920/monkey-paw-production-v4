"""Agentic Protocol Implementation

This module defines the core protocol for agent communication and coordination
in the online production system.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Optional, Any, Callable
from uuid import uuid4

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Types of messages in the agentic protocol."""

    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    STATUS_UPDATE = "status_update"
    ERROR = "error"
    HEARTBEAT = "heartbeat"
    COORDINATION = "coordination"
    RESOURCE_REQUEST = "resource_request"
    RESOURCE_RESPONSE = "resource_response"


class AgentStatus(Enum):
    """Status of an agent."""

    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"
    INITIALIZING = "initializing"


class TaskStatus(Enum):
    """Status of a task."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentCapability:
    """Represents a capability that an agent possesses."""

    name: str
    version: str
    description: str
    parameters: dict[str, Any]


@dataclass
class AgentInfo:
    """Information about an agent."""

    agent_id: str
    name: str
    status: AgentStatus
    capabilities: list[AgentCapability]
    last_heartbeat: datetime
    metadata: dict[str, Any]


@dataclass
class Task:
    """Represents a task in the system."""

    task_id: str
    task_type: str
    payload: dict[str, Any]
    priority: int = 0
    timeout: Optional[int] = None
    created_at: Optional[datetime] = None
    assigned_to: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[dict[str, Any]] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()


@dataclass
class Message:
    """Base message structure for agent communication."""

    message_id: str
    message_type: MessageType
    sender_id: str
    recipient_id: Optional[str]
    timestamp: datetime
    payload: dict[str, Any]
    correlation_id: Optional[str] = None

    def __post_init__(self):
        if not self.message_id:
            self.message_id = str(uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow()

    def to_dict(self) -> dict[str, Any]:
        """Convert message to dictionary."""
        result = asdict(self)
        result["message_type"] = self.message_type.value
        result["timestamp"] = self.timestamp.isoformat()
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Message":
        """Create message from dictionary."""
        data["message_type"] = MessageType(data["message_type"])
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


class MessageHandler(ABC):
    """Abstract base class for message handlers."""

    @abstractmethod
    async def handle_message(self, message: Message) -> Optional[Message]:
        """Handle an incoming message and optionally return a response."""


class AgentState(Enum):
    """Agent execution states"""

    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    COMPLETED = "completed"


class BaseAgent(ABC):
    """Base class for all agents in the system"""

    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.state = AgentState.IDLE
        self.logger = logging.getLogger(f"agent.{name}")
        self.created_at = datetime.now()
        self.last_activity = datetime.now()

    @abstractmethod
    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """Execute a task"""

    @abstractmethod
    def validate_task(self, task: dict[str, Any]) -> bool:
        """Validate if task can be executed"""

    def get_status(self) -> dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
        }


class AgentProtocol(ABC):
    """Abstract base class for agent protocol implementation."""

    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.status = AgentStatus.INITIALIZING
        self.capabilities: list[AgentCapability] = []
        self.message_handlers: dict[MessageType, MessageHandler] = {}
        self.tasks: dict[str, Task] = {}
        self.last_heartbeat = datetime.utcnow()
        self.metadata: dict[str, Any] = {}

    @abstractmethod
    async def send_message(self, message: Message) -> bool:
        """Send a message to another agent or the coordinator."""

    @abstractmethod
    async def receive_message(self) -> Optional[Message]:
        """Receive a message from the message queue."""

    def register_handler(self, message_type: MessageType, handler: MessageHandler):
        """Register a message handler for a specific message type."""
        self.message_handlers[message_type] = handler

    def add_capability(self, capability: AgentCapability):
        """Add a capability to this agent."""
        self.capabilities.append(capability)

    async def process_message(self, message: Message) -> Optional[Message]:
        """Process an incoming message using registered handlers."""
        handler = self.message_handlers.get(message.message_type)
        if handler:
            try:
                return await handler.handle_message(message)
            except Exception as e:
                logger.error(
                    f"Error processing message {
                        message.message_id}: {e}"
                )
                return self.create_error_message(message, str(e))
        else:
            logger.warning(
                f"No handler for message type {
                    message.message_type}"
            )
            return None

    def create_message(
        self,
        message_type: MessageType,
        recipient_id: Optional[str],
        payload: dict[str, Any],
        correlation_id: Optional[str] = None,
    ) -> Message:
        """Create a new message."""
        return Message(
            message_id=str(uuid4()),
            message_type=message_type,
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            timestamp=datetime.utcnow(),
            payload=payload,
            correlation_id=correlation_id,
        )

    def create_error_message(self, original_message: Message, error: str) -> Message:
        """Create an error response message."""
        return self.create_message(
            MessageType.ERROR,
            original_message.sender_id,
            {"error": error, "original_message_id": original_message.message_id},
            original_message.message_id,
        )

    def create_task_response(
        self, task: Task, success: bool, result: Optional[dict[str, Any]] = None
    ) -> Message:
        """Create a task response message."""
        payload = {
            "task_id": task.task_id,
            "success": success,
            "result": result or {},
            "status": task.status.value,
        }
        return self.create_message(MessageType.TASK_RESPONSE, None, payload)

    async def send_heartbeat(self):
        """Send a heartbeat message."""
        self.last_heartbeat = datetime.utcnow()
        heartbeat_message = self.create_message(
            MessageType.HEARTBEAT,
            None,  # Broadcast to coordinator
            {
                "status": self.status.value,
                "capabilities": [asdict(cap) for cap in self.capabilities],
                "metadata": self.metadata,
            },
        )
        await self.send_message(heartbeat_message)

    async def request_task(
        self, task_type: str, payload: dict[str, Any], priority: int = 0
    ) -> str:
        """Request a new task to be executed."""
        task_id = str(uuid4())
        task_request = self.create_message(
            MessageType.TASK_REQUEST,
            None,  # Send to coordinator
            {
                "task_id": task_id,
                "task_type": task_type,
                "payload": payload,
                "priority": priority,
            },
        )
        await self.send_message(task_request)
        return task_id

    async def update_status(self, status: AgentStatus):
        """Update agent status."""
        self.status = status
        status_message = self.create_message(
            MessageType.STATUS_UPDATE,
            None,
            {"status": status.value, "timestamp": datetime.utcnow().isoformat()},
        )
        await self.send_message(status_message)

    def get_info(self) -> AgentInfo:
        """Get agent information."""
        return AgentInfo(
            agent_id=self.agent_id,
            name=self.name,
            status=self.status,
            capabilities=self.capabilities,
            last_heartbeat=self.last_heartbeat,
            metadata=self.metadata,
        )


class TaskHandler(MessageHandler):
    """Handler for task-related messages."""

    def __init__(self, agent: AgentProtocol, task_executor: Callable[[Task], Any]):
        self.agent = agent
        self.task_executor = task_executor

    async def handle_message(self, message: Message) -> Optional[Message]:
        """Handle task request messages."""
        if message.message_type == MessageType.TASK_REQUEST:
            return await self.handle_task_request(message)
        return None

    async def handle_task_request(self, message: Message) -> Message:
        """Handle a task request."""
        try:
            payload = message.payload
            task = Task(
                task_id=payload["task_id"],
                task_type=payload["task_type"],
                payload=payload["payload"],
                priority=payload.get("priority", 0),
            )

            # Update agent status
            await self.agent.update_status(AgentStatus.BUSY)

            # Execute the task
            task.status = TaskStatus.IN_PROGRESS
            self.agent.tasks[task.task_id] = task

            try:
                result = await self.task_executor(task)
                task.result = result
                task.status = TaskStatus.COMPLETED
                success = True
            except Exception as e:
                task.error = str(e)
                task.status = TaskStatus.FAILED
                success = False
                logger.error(f"Task {task.task_id} failed: {e}")

            # Update agent status back to idle
            await self.agent.update_status(AgentStatus.IDLE)

            return self.agent.create_task_response(task, success, task.result)

        except Exception as e:
            logger.error(f"Error handling task request: {e}")
            return self.agent.create_error_message(message, str(e))


class CoordinationProtocol:
    """Protocol for coordinating multiple agents."""

    def __init__(self):
        self.agents: dict[str, AgentInfo] = {}
        self.pending_tasks: dict[str, Task] = {}
        self.completed_tasks: dict[str, Task] = {}

    def register_agent(self, agent_info: AgentInfo):
        """Register an agent with the coordinator."""
        self.agents[agent_info.agent_id] = agent_info
        logger.info(
            f"Agent {
                agent_info.name} ({
                agent_info.agent_id}) registered"
        )

    def unregister_agent(self, agent_id: str):
        """Unregister an agent."""
        if agent_id in self.agents:
            agent_info = self.agents.pop(agent_id)
            logger.info(f"Agent {agent_info.name} ({agent_id}) unregistered")

    def find_capable_agents(self, required_capability: str) -> list[AgentInfo]:
        """Find agents with a specific capability."""
        capable_agents = []
        for agent_info in self.agents.values():
            if agent_info.status == AgentStatus.IDLE:
                for capability in agent_info.capabilities:
                    if capability.name == required_capability:
                        capable_agents.append(agent_info)
                        break
        return capable_agents

    def assign_task(self, task: Task, agent_id: str) -> bool:
        """Assign a task to a specific agent."""
        if agent_id in self.agents:
            agent_info = self.agents[agent_id]
            if agent_info.status == AgentStatus.IDLE:
                task.assigned_to = agent_id
                task.status = TaskStatus.IN_PROGRESS
                self.pending_tasks[task.task_id] = task
                agent_info.status = AgentStatus.BUSY
                return True
        return False

    def complete_task(self, task_id: str, result: dict[str, Any]):
        """Mark a task as completed."""
        if task_id in self.pending_tasks:
            task = self.pending_tasks.pop(task_id)
            task.status = TaskStatus.COMPLETED
            task.result = result
            self.completed_tasks[task_id] = task

            # Update agent status back to idle
            if task.assigned_to and task.assigned_to in self.agents:
                self.agents[task.assigned_to].status = AgentStatus.IDLE

    def fail_task(self, task_id: str, error: str):
        """Mark a task as failed."""
        if task_id in self.pending_tasks:
            task = self.pending_tasks.pop(task_id)
            task.status = TaskStatus.FAILED
            task.error = error
            self.completed_tasks[task_id] = task

            # Update agent status back to idle
            if task.assigned_to and task.assigned_to in self.agents:
                self.agents[task.assigned_to].status = AgentStatus.IDLE

    def get_system_status(self) -> dict[str, Any]:
        """Get overall system status."""
        return {
            "total_agents": len(self.agents),
            "idle_agents": len(
                [a for a in self.agents.values() if a.status == AgentStatus.IDLE]
            ),
            "busy_agents": len(
                [a for a in self.agents.values() if a.status == AgentStatus.BUSY]
            ),
            "pending_tasks": len(self.pending_tasks),
            "completed_tasks": len(self.completed_tasks),
            "agents": {aid: asdict(info) for aid, info in self.agents.items()},
        }


# Global coordination protocol instance
coordinator = CoordinationProtocol()


def create_agent(
    agent_id: str, name: str, capabilities: list[AgentCapability]
) -> AgentProtocol:
    """Factory function to create a new agent."""
    # This would be implemented by specific agent types
    raise NotImplementedError("Specific agent implementations should override this")


async def start_agent_system():
    """Initialize and start the agent system."""
    logger.info("Starting agent system...")
    # Initialize coordination protocol
    # Start message brokers
    # Register default agents
    logger.info("Agent system started successfully")


async def shutdown_agent_system():
    """Gracefully shutdown the agent system."""
    logger.info("Shutting down agent system...")
    # Cleanup resources
    # Stop message brokers
    # Save state if needed
    logger.info("Agent system shutdown complete")
