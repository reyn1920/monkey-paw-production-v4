import asyncio
from datetime import datetime
import logging
from enum import Enum
import uuid
from typing import Any
from typing import Optional
from typing import Callable


class TaskStatus(Enum):
    """Task status enumeration"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task:
    """Task representation"""

    def __init__(
        self, task_id: str, task_type: str, data: dict[str, Any], priority: int = 0
    ):
        self.task_id = task_id
        self.task_type = task_type
        self.data = data
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
        self.retry_count = 0
        self.max_retries = 3


class TaskQueueManager:
    """Task Queue Manager for handling asynchronous tasks"""

    def __init__(self, config: Optional[dict[str, Any]] = None):
        self.config = config or {}
        self.task_queue = asyncio.Queue()
        self.active_tasks = {}
        self.completed_tasks = []
        self.failed_tasks = []
        self.task_handlers = {}
        self.workers = []
        self.is_running = False
        self.max_workers = self.config.get("max_workers", 5)
        self.logger = logging.getLogger(__name__)

    async def start(self):
        """Start the task queue manager"""
        if self.is_running:
            return

        self.is_running = True
        self.logger.info(
            f"Starting TaskQueueManager with {
                self.max_workers} workers"
        )

        # Start worker tasks
        for i in range(self.max_workers):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self.workers.append(worker)

    async def stop(self):
        """Stop the task queue manager"""
        if not self.is_running:
            return

        self.is_running = False
        self.logger.info("Stopping TaskQueueManager")

        # Cancel all workers
        for worker in self.workers:
            worker.cancel()

        # Wait for workers to finish
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers.clear()

    def register_handler(
        self, task_type: str, handler: Callable[[dict[str, Any]], Any]
    ):
        """Register a task handler for a specific task type"""
        self.task_handlers[task_type] = handler
        self.logger.info(f"Registered handler for task type: {task_type}")

    async def add_task(
        self, task_type: str, data: dict[str, Any], priority: int = 0
    ) -> str:
        """Add a task to the queue"""
        task_id = str(uuid.uuid4())
        task = Task(task_id, task_type, data, priority)

        await self.task_queue.put(task)
        self.logger.info(f"Added task {task_id} of type {task_type} to queue")

        return task_id

    async def get_task_status(self, task_id: str) -> Optional[dict[str, Any]]:
        """Get the status of a specific task"""
        # Check active tasks
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            return self._task_to_dict(task)

        # Check completed tasks
        for task in self.completed_tasks:
            if task.task_id == task_id:
                return self._task_to_dict(task)

        # Check failed tasks
        for task in self.failed_tasks:
            if task.task_id == task_id:
                return self._task_to_dict(task)

        return None

    async def _worker(self, worker_name: str):
        """Worker coroutine to process tasks"""
        self.logger.info(f"Worker {worker_name} started")

        while self.is_running:
            try:
                # Get task from queue with timeout
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)

                # Add to active tasks
                self.active_tasks[task.task_id] = task
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now()

                self.logger.info(
                    f"Worker {worker_name} processing task {
                        task.task_id}"
                )

                try:
                    # Execute task
                    result = await self._execute_task(task)

                    # Mark as completed
                    task.status = TaskStatus.COMPLETED
                    task.completed_at = datetime.now()
                    task.result = result

                    # Move to completed tasks
                    self.completed_tasks.append(task)
                    del self.active_tasks[task.task_id]

                    self.logger.info(
                        f"Task {
                            task.task_id} completed successfully"
                    )

                except Exception as e:
                    # Handle task failure
                    task.error = str(e)
                    task.retry_count += 1

                    if task.retry_count < task.max_retries:
                        # Retry task
                        task.status = TaskStatus.PENDING
                        await self.task_queue.put(task)
                        del self.active_tasks[task.task_id]
                        self.logger.warning(
                            f"Task {task.task_id} failed, retrying ({task.retry_count}/{task.max_retries})"
                        )
                    else:
                        # Mark as failed
                        task.status = TaskStatus.FAILED
                        task.completed_at = datetime.now()

                        # Move to failed tasks
                        self.failed_tasks.append(task)
                        del self.active_tasks[task.task_id]

                        self.logger.error(
                            f"Task {task.task_id} failed permanently: {str(e)}"
                        )

                # Mark task as done in queue
                self.task_queue.task_done()

            except asyncio.TimeoutError:
                # No tasks available, continue
                continue
            except Exception as e:
                self.logger.error(f"Worker {worker_name} error: {str(e)}")

        self.logger.info(f"Worker {worker_name} stopped")

    async def _execute_task(self, task: Task) -> Any:
        """Execute a specific task"""
        handler = self.task_handlers.get(task.task_type)

        if handler is None:
            # Default handler
            await asyncio.sleep(0.1)  # Simulate processing
            return {
                "status": "completed",
                "message": f"Task {task.task_type} processed",
            }

        # Execute custom handler
        if asyncio.iscoroutinefunction(handler):
            return await handler(task.data)
        else:
            return handler(task.data)

    def _task_to_dict(self, task: Task) -> dict[str, Any]:
        """Convert task to dictionary"""
        return {
            "task_id": task.task_id,
            "task_type": task.task_type,
            "status": task.status.value,
            "priority": task.priority,
            "created_at": task.created_at.isoformat(),
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": (
                task.completed_at.isoformat() if task.completed_at else None
            ),
            "result": task.result,
            "error": task.error,
            "retry_count": task.retry_count,
            "max_retries": task.max_retries,
        }

    def get_status(self) -> dict[str, Any]:
        """Get queue manager status"""
        return {
            "is_running": self.is_running,
            "max_workers": self.max_workers,
            "active_workers": len(self.workers),
            "queue_size": self.task_queue.qsize(),
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "registered_handlers": list(self.task_handlers.keys()),
            "timestamp": datetime.now().isoformat(),
        }
