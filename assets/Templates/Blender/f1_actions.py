"""
Action Registry System
Provides centralized action management and execution
"""

import logging
import asyncio
from datetime import datetime
from enum import Enum
from typing import Callable
from typing import Any
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Enumeration of action types"""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    VALIDATE = "validate"
    TRANSFORM = "transform"


class ActionStatus(Enum):
    """Enumeration of action statuses"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Action:
    """
    Represents a single action in the system
    """

    def __init__(
        self,
        action_id: str,
        action_type: ActionType,
        handler: Callable[..., Any],
        description: str = "",
        metadata: Optional[dict[str, Any]] = None,
    ):
        """Initialize an action"""
        self.action_id = action_id
        self.action_type = action_type
        self.handler = handler
        self.description = description
        self.metadata = metadata or {}
        self.status = ActionStatus.PENDING
        self.created_at = datetime.now()
        self.executed_at = None
        self.result = None
        self.error = None

    async def execute(self, *args, **kwargs) -> Any:
        """Execute the action"""
        try:
            self.status = ActionStatus.RUNNING
            self.executed_at = datetime.now()

            if asyncio.iscoroutinefunction(self.handler):
                self.result = await self.handler(*args, **kwargs)
            else:
                self.result = self.handler(*args, **kwargs)

            self.status = ActionStatus.COMPLETED
            logger.info(f"Action {self.action_id} completed successfully")
            return self.result

        except Exception as e:
            self.status = ActionStatus.FAILED
            self.error = str(e)
            logger.error(f"Action {self.action_id} failed: {e}")
            raise

    def to_dict(self) -> dict[str, Any]:
        """Convert action to dictionary"""
        return {
            "action_id": self.action_id,
            "action_type": self.action_type.value,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "executed_at": self.executed_at.isoformat() if self.executed_at else None,
            "metadata": self.metadata,
            "error": self.error,
        }


class ActionRegistry:
    """
    Central registry for managing actions
    """

    def __init__(self):
        """Initialize the action registry"""
        self.actions: dict[str, Action] = {}
        self.action_history: list[dict[str, Any]] = []
        self.initialized = False
        logger.info("ActionRegistry initialized")

    async def initialize(self) -> bool:
        """Initialize the action registry"""
        try:
            # Register default actions
            await self._register_default_actions()
            self.initialized = True
            logger.info("ActionRegistry initialization completed")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize ActionRegistry: {e}")
            return False

    async def _register_default_actions(self):
        """Register default system actions"""
        # Health check action
        await self.register_action(
            "health_check", ActionType.READ, self._health_check, "System health check"
        )

        # Status action
        await self.register_action(
            "get_status", ActionType.READ, self._get_status, "Get system status"
        )

    async def register_action(
        self,
        action_id: str,
        action_type: ActionType,
        handler: Callable[..., Any],
        description: str = "",
        metadata: Optional[dict[str, Any]] = None,
    ) -> bool:
        """Register a new action"""
        try:
            if action_id in self.actions:
                logger.warning(f"Action {action_id} already exists, overwriting")

            action = Action(action_id, action_type, handler, description, metadata)
            self.actions[action_id] = action

            logger.info(f"Action {action_id} registered successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to register action {action_id}: {e}")
            return False

    async def execute_action(self, action_id: str, *args, **kwargs) -> Any:
        """Execute an action by ID"""
        if not self.initialized:
            await self.initialize()

        if action_id not in self.actions:
            raise ValueError(f"Action {action_id} not found")

        action = self.actions[action_id]
        result = await action.execute(*args, **kwargs)

        # Add to history
        self.action_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": action.to_dict(),
                "result": (
                    str(result)[:1000] if result else None
                ),  # Truncate large results
            }
        )

        return result

    def get_action(self, action_id: str) -> Optional[Action]:
        """Get an action by ID"""
        return self.actions.get(action_id)

    def list_actions(self) -> list[dict[str, Any]]:
        """List all registered actions"""
        return [action.to_dict() for action in self.actions.values()]

    def get_action_history(self, limit: int = 100) -> list[dict[str, Any]]:
        """Get action execution history"""
        return self.action_history[-limit:]

    async def _health_check(self) -> dict[str, Any]:
        """Default health check action"""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "actions_registered": len(self.actions),
            "actions_executed": len(self.action_history),
        }

    async def _get_status(self) -> dict[str, Any]:
        """Default status action"""
        return {
            "initialized": self.initialized,
            "total_actions": len(self.actions),
            "total_executions": len(self.action_history),
            "action_types": list(
                {action.action_type.value for action in self.actions.values()}
            ),
        }


# Global action registry instance
action_registry = ActionRegistry()


async def register_action(
    action_id: str,
    action_type: ActionType,
    handler: Callable[..., Any],
    description: str = "",
    metadata: Optional[dict[str, Any]] = None,
) -> bool:
    """Convenience function to register an action"""
    return await action_registry.register_action(
        action_id, action_type, handler, description, metadata
    )


async def execute_action(action_id: str, *args, **kwargs) -> Any:
    """Convenience function to execute an action"""
    return await action_registry.execute_action(action_id, *args, **kwargs)


def get_action_registry() -> ActionRegistry:
    """Get the global action registry instance"""
    return action_registry


async def main():
    """Main function for testing"""
    try:
        # Initialize the action registry
        await action_registry.initialize()

        # Test health check
        result = await execute_action("health_check")
        print(f"Health check result: {result}")

        # Test status
        status = await execute_action("get_status")
        print(f"Status: {status}")

        # List all actions
        actions = action_registry.list_actions()
        print(f"Registered actions: {len(actions)}")

    except Exception as e:
        logger.error(f"Error in main: {e}")


if __name__ == "__main__":
    asyncio.run(main())
