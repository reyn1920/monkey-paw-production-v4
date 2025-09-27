"""
Advanced Action System with Maximum Features
Provides comprehensive action management with batch processing, scheduling, and optimization
"""

import logging
import asyncio
from datetime import datetime, timedelta
from enum import Enum
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
import time
from typing import Optional
from typing import Callable
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionPriority(Enum):
    """Action priority levels"""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class ActionCategory(Enum):
    """Action categories for organization"""

    SYSTEM = "system"
    USER = "user"
    AUTOMATION = "automation"
    MAINTENANCE = "maintenance"
    ANALYTICS = "analytics"
    SECURITY = "security"


class ExecutionMode(Enum):
    """Action execution modes"""

    SYNC = "sync"
    ASYNC = "async"
    BATCH = "batch"
    SCHEDULED = "scheduled"
    PARALLEL = "parallel"


@dataclass
class ActionMetrics:
    """Metrics for action performance tracking"""

    execution_count: int = 0
    total_execution_time: float = 0.0
    average_execution_time: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    last_execution: Optional[datetime] = None

    def update(self, execution_time: float, success: bool):
        """Update metrics with new execution data"""
        self.execution_count += 1
        self.total_execution_time += execution_time
        self.average_execution_time = self.total_execution_time / self.execution_count

        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

        self.last_execution = datetime.now()


@dataclass
class ActionSchedule:
    """Schedule configuration for actions"""

    enabled: bool = False
    interval: Optional[timedelta] = None
    cron_expression: Optional[str] = None
    next_run: Optional[datetime] = None
    max_runs: Optional[int] = None
    current_runs: int = 0


class AdvancedAction:
    """
    Advanced action with comprehensive features
    """

    def __init__(
        self,
        action_id: str,
        handler: Callable[..., Any],
        category: ActionCategory = ActionCategory.USER,
        priority: ActionPriority = ActionPriority.NORMAL,
        execution_mode: ExecutionMode = ExecutionMode.ASYNC,
        description: str = "",
        tags: Optional[set[str]] = None,
        timeout: Optional[float] = None,
        retry_count: int = 0,
        retry_delay: float = 1.0,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """Initialize an advanced action"""
        self.action_id = action_id
        self.handler = handler
        self.category = category
        self.priority = priority
        self.execution_mode = execution_mode
        self.description = description
        self.tags = tags or set()
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.metadata = metadata or {}

        # Runtime state
        self.created_at = datetime.now()
        self.metrics = ActionMetrics()
        self.schedule = ActionSchedule()
        self.dependencies: set[str] = set()
        self.dependents: set[str] = set()

        # Execution state
        self.is_running = False
        self.last_result = None
        self.last_error = None

    async def execute(self, *args, **kwargs) -> Any:
        """Execute the action with comprehensive error handling and metrics"""
        if self.is_running:
            raise RuntimeError(f"Action {self.action_id} is already running")

        self.is_running = True
        start_time = time.time()
        success = False

        try:
            # Execute with retry logic
            for attempt in range(self.retry_count + 1):
                try:
                    if self.timeout:
                        result = await asyncio.wait_for(
                            self._execute_handler(*args, **kwargs), timeout=self.timeout
                        )
                    else:
                        result = await self._execute_handler(*args, **kwargs)

                    self.last_result = result
                    success = True
                    break

                except Exception as e:
                    if attempt < self.retry_count:
                        logger.warning(
                            f"Action {
                                self.action_id} failed (attempt {
                                attempt +
                                1}), retrying: {e}"
                        )
                        await asyncio.sleep(self.retry_delay)
                    else:
                        raise

            return result

        except Exception as e:
            self.last_error = str(e)
            logger.error(
                f"Action {
                    self.action_id} failed after all retries: {e}"
            )
            raise

        finally:
            execution_time = time.time() - start_time
            self.metrics.update(execution_time, success)
            self.is_running = False

    async def _execute_handler(self, *args, **kwargs) -> Any:
        """Execute the handler function"""
        if asyncio.iscoroutinefunction(self.handler):
            return await self.handler(*args, **kwargs)
        else:
            # Run sync functions in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                return await loop.run_in_executor(
                    executor, lambda: self.handler(*args, **kwargs)
                )

    def add_dependency(self, action_id: str):
        """Add a dependency to this action"""
        self.dependencies.add(action_id)

    def add_dependent(self, action_id: str):
        """Add a dependent action"""
        self.dependents.add(action_id)

    def set_schedule(
        self,
        interval: Optional[timedelta] = None,
        cron_expression: Optional[str] = None,
        max_runs: Optional[int] = None,
    ):
        """Set scheduling for the action"""
        self.schedule.enabled = True
        self.schedule.interval = interval
        self.schedule.cron_expression = cron_expression
        self.schedule.max_runs = max_runs

        if interval:
            self.schedule.next_run = datetime.now() + interval

    def to_dict(self) -> dict[str, Any]:
        """Convert action to dictionary"""
        return {
            "action_id": self.action_id,
            "category": self.category.value,
            "priority": self.priority.value,
            "execution_mode": self.execution_mode.value,
            "description": self.description,
            "tags": list(self.tags),
            "timeout": self.timeout,
            "retry_count": self.retry_count,
            "created_at": self.created_at.isoformat(),
            "is_running": self.is_running,
            "metrics": {
                "execution_count": self.metrics.execution_count,
                "average_execution_time": self.metrics.average_execution_time,
                "success_count": self.metrics.success_count,
                "failure_count": self.metrics.failure_count,
                "last_execution": (
                    self.metrics.last_execution.isoformat()
                    if self.metrics.last_execution
                    else None
                ),
            },
            "dependencies": list(self.dependencies),
            "dependents": list(self.dependents),
            "metadata": self.metadata,
        }


class ActionMaxoutSystem:
    """
    Maximum feature action system with advanced capabilities
    """

    def __init__(self, max_concurrent_actions: int = 10):
        """Initialize the action system"""
        self.actions: dict[str, AdvancedAction] = {}
        self.action_queue: list[str] = []
        self.running_actions: set[str] = set()
        self.max_concurrent_actions = max_concurrent_actions
        self.scheduler_running = False
        self.batch_processor_running = False
        self.initialized = False

        # Performance tracking
        self.system_metrics = {
            "total_actions_executed": 0,
            "total_execution_time": 0.0,
            "average_system_load": 0.0,
            "peak_concurrent_actions": 0,
        }

        logger.info("ActionMaxoutSystem initialized")

    async def initialize(self) -> bool:
        """Initialize the action system"""
        try:
            # Start background services
            asyncio.create_task(self._scheduler_loop())
            asyncio.create_task(self._batch_processor_loop())
            asyncio.create_task(self._metrics_collector_loop())

            self.initialized = True
            logger.info("ActionMaxoutSystem initialization completed")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize ActionMaxoutSystem: {e}")
            return False

    async def register_action(
        self,
        action_id: str,
        handler: Callable[..., Any],
        category: ActionCategory = ActionCategory.USER,
        priority: ActionPriority = ActionPriority.NORMAL,
        execution_mode: ExecutionMode = ExecutionMode.ASYNC,
        description: str = "",
        tags: Optional[set[str]] = None,
        **kwargs,
    ) -> bool:
        """Register a new advanced action"""
        try:
            if action_id in self.actions:
                logger.warning(f"Action {action_id} already exists, overwriting")

            action = AdvancedAction(
                action_id=action_id,
                handler=handler,
                category=category,
                priority=priority,
                execution_mode=execution_mode,
                description=description,
                tags=tags,
                **kwargs,
            )

            self.actions[action_id] = action
            logger.info(f"Action {action_id} registered successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to register action {action_id}: {e}")
            return False

    async def execute_action(self, action_id: str, *args, **kwargs) -> Any:
        """Execute an action with queue management"""
        if not self.initialized:
            await self.initialize()

        if action_id not in self.actions:
            raise ValueError(f"Action {action_id} not found")

        action = self.actions[action_id]

        # Check dependencies
        if not await self._check_dependencies(action_id):
            raise RuntimeError(f"Dependencies not satisfied for action {action_id}")

        # Handle different execution modes
        if action.execution_mode == ExecutionMode.BATCH:
            return await self._queue_for_batch(action_id, args, kwargs)
        elif action.execution_mode == ExecutionMode.SCHEDULED:
            return await self._schedule_action(action_id, args, kwargs)
        else:
            return await self._execute_immediate(action_id, args, kwargs)

    async def _execute_immediate(
        self, action_id: str, args: tuple, kwargs: dict
    ) -> Any:
        """Execute action immediately"""
        # Wait for available slot if at capacity
        while len(self.running_actions) >= self.max_concurrent_actions:
            await asyncio.sleep(0.1)

        self.running_actions.add(action_id)

        try:
            action = self.actions[action_id]
            result = await action.execute(*args, **kwargs)

            # Update system metrics
            self.system_metrics["total_actions_executed"] += 1
            self.system_metrics["peak_concurrent_actions"] = max(
                self.system_metrics["peak_concurrent_actions"],
                len(self.running_actions),
            )

            # Execute dependent actions
            await self._execute_dependents(action_id)

            return result

        finally:
            self.running_actions.discard(action_id)

    async def _check_dependencies(self, action_id: str) -> bool:
        """Check if all dependencies are satisfied"""
        action = self.actions[action_id]

        for dep_id in action.dependencies:
            if dep_id in self.running_actions:
                return False

            dep_action = self.actions.get(dep_id)
            if dep_action and dep_action.metrics.execution_count == 0:
                return False

        return True

    async def _execute_dependents(self, action_id: str):
        """Execute dependent actions"""
        action = self.actions[action_id]

        for dependent_id in action.dependents:
            if dependent_id in self.actions and await self._check_dependencies(
                dependent_id
            ):
                asyncio.create_task(self._execute_immediate(dependent_id, (), {}))

    async def _queue_for_batch(self, action_id: str, args: tuple, kwargs: dict) -> str:
        """Queue action for batch processing"""
        batch_id = str(uuid.uuid4())
        self.action_queue.append(
            {
                "batch_id": batch_id,
                "action_id": action_id,
                "args": args,
                "kwargs": kwargs,
                "queued_at": datetime.now(),
            }
        )
        return batch_id

    async def _schedule_action(self, action_id: str, args: tuple, kwargs: dict) -> bool:
        """Schedule action for later execution"""
        action = self.actions[action_id]
        if not action.schedule.enabled:
            raise ValueError(f"Action {action_id} is not configured for scheduling")

        # Scheduling logic would be handled by the scheduler loop
        return True

    async def _scheduler_loop(self):
        """Background scheduler for scheduled actions"""
        self.scheduler_running = True

        while self.scheduler_running:
            try:
                current_time = datetime.now()

                for action in self.actions.values():
                    if (
                        action.schedule.enabled
                        and action.schedule.next_run
                        and current_time >= action.schedule.next_run
                        and not action.is_running
                    ):
                        # Execute scheduled action
                        asyncio.create_task(
                            self._execute_immediate(action.action_id, (), {})
                        )

                        # Update next run time
                        if action.schedule.interval:
                            action.schedule.next_run = (
                                current_time + action.schedule.interval
                            )

                        action.schedule.current_runs += 1

                        # Check max runs
                        if (
                            action.schedule.max_runs
                            and action.schedule.current_runs >= action.schedule.max_runs
                        ):
                            action.schedule.enabled = False

                await asyncio.sleep(1)  # Check every second

            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(5)

    async def _batch_processor_loop(self):
        """Background batch processor"""
        self.batch_processor_running = True

        while self.batch_processor_running:
            try:
                if self.action_queue:
                    # Process batch of actions
                    batch_size = min(5, len(self.action_queue))
                    batch = self.action_queue[:batch_size]
                    self.action_queue = self.action_queue[batch_size:]

                    # Execute batch in parallel
                    tasks = []
                    for item in batch:
                        task = asyncio.create_task(
                            self._execute_immediate(
                                item["action_id"], item["args"], item["kwargs"]
                            )
                        )
                        tasks.append(task)

                    await asyncio.gather(*tasks, return_exceptions=True)

                await asyncio.sleep(2)  # Process batches every 2 seconds

            except Exception as e:
                logger.error(f"Error in batch processor loop: {e}")
                await asyncio.sleep(5)

    async def _metrics_collector_loop(self):
        """Background metrics collection"""
        while True:
            try:
                # Calculate system load
                active_actions = len(self.running_actions)
                self.system_metrics["average_system_load"] = (
                    active_actions / self.max_concurrent_actions
                )

                await asyncio.sleep(10)  # Update metrics every 10 seconds

            except Exception as e:
                logger.error(f"Error in metrics collector: {e}")
                await asyncio.sleep(30)

    def get_system_status(self) -> dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "initialized": self.initialized,
            "total_actions": len(self.actions),
            "running_actions": len(self.running_actions),
            "queued_actions": len(self.action_queue),
            "max_concurrent": self.max_concurrent_actions,
            "scheduler_running": self.scheduler_running,
            "batch_processor_running": self.batch_processor_running,
            "system_metrics": self.system_metrics,
            "actions_by_category": self._get_actions_by_category(),
            "actions_by_priority": self._get_actions_by_priority(),
        }

    def _get_actions_by_category(self) -> dict[str, int]:
        """Get action count by category"""
        categories = {}
        for action in self.actions.values():
            category = action.category.value
            categories[category] = categories.get(category, 0) + 1
        return categories

    def _get_actions_by_priority(self) -> dict[str, int]:
        """Get action count by priority"""
        priorities = {}
        for action in self.actions.values():
            priority = action.priority.name
            priorities[priority] = priorities.get(priority, 0) + 1
        return priorities


# Global action system instance
action_system = ActionMaxoutSystem()


async def main():
    """Main function for testing"""
    try:
        # Initialize the system
        await action_system.initialize()

        # Register test actions
        await action_system.register_action(
            "test_action",
            lambda: "Test completed",
            category=ActionCategory.SYSTEM,
            priority=ActionPriority.HIGH,
            description="Test action for system validation",
        )

        # Execute test action
        result = await action_system.execute_action("test_action")
        print(f"Test result: {result}")

        # Get system status
        status = action_system.get_system_status()
        print(f"System status: {json.dumps(status, indent=2)}")

    except Exception as e:
        logger.error(f"Error in main: {e}")


if __name__ == "__main__":
    asyncio.run(main())
