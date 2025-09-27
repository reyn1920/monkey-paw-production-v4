"""Orchestrator Module

Provides task orchestration, workflow management, and agent coordination.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from typing import Any
from typing import Callable


class TaskStatus(Enum):
    """Task execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class TaskPriority(Enum):
    """Task priority levels."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class TaskResult:
    """Task execution result."""

    task_id: str
    status: TaskStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """Orchestrator task definition."""

    id: str
    name: str
    handler: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.MEDIUM
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: Optional[float] = None
    dependencies: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retry_count: int = 0
    result: Optional[TaskResult] = None
    metadata: dict[str, Any] = field(default_factory=dict)


class WorkflowStatus(Enum):
    """Workflow execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Workflow:
    """Workflow definition containing multiple tasks."""

    id: str
    name: str
    tasks: list[Task] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: dict[str, Any] = field(default_factory=dict)


class TaskOrchestrator:
    """Main orchestrator for managing tasks and workflows."""

    def __init__(self, max_workers: int = 10, max_concurrent_tasks: int = 50):
        self.logger = logging.getLogger(__name__)
        self.max_workers = max_workers
        self.max_concurrent_tasks = max_concurrent_tasks

        # Task management
        self.tasks: dict[str, Task] = {}
        self.workflows: dict[str, Workflow] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.running_tasks: dict[str, asyncio.Task] = {}

        # Execution control
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.is_running = False
        self.worker_tasks: list[asyncio.Task] = []

        # Event handlers
        self.event_handlers: dict[str, list[Callable]] = {
            "task_started": [],
            "task_completed": [],
            "task_failed": [],
            "workflow_started": [],
            "workflow_completed": [],
            "workflow_failed": [],
        }

    async def start(self):
        """Start the orchestrator."""
        if self.is_running:
            return

        self.is_running = True
        self.logger.info("Starting task orchestrator")

        # Start worker tasks
        for i in range(self.max_workers):
            worker_task = asyncio.create_task(self._worker(f"worker-{i}"))
            self.worker_tasks.append(worker_task)

        # Start monitoring task
        monitor_task = asyncio.create_task(self._monitor_tasks())
        self.worker_tasks.append(monitor_task)

    async def stop(self):
        """Stop the orchestrator."""
        if not self.is_running:
            return

        self.is_running = False
        self.logger.info("Stopping task orchestrator")

        # Cancel all worker tasks
        for worker_task in self.worker_tasks:
            worker_task.cancel()

        # Wait for workers to finish
        await asyncio.gather(*self.worker_tasks, return_exceptions=True)
        self.worker_tasks.clear()

        # Cancel running tasks
        for task_id, running_task in self.running_tasks.items():
            running_task.cancel()
            self.tasks[task_id].status = TaskStatus.CANCELLED

        self.running_tasks.clear()
        self.executor.shutdown(wait=True)

    def add_task(
        self,
        name: str,
        handler: Callable,
        args: tuple = (),
        kwargs: Optional[dict[str, Any]] = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: Optional[float] = None,
        dependencies: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """Add a task to the orchestrator."""
        task_id = str(uuid.uuid4())

        task = Task(
            id=task_id,
            name=name,
            handler=handler,
            args=args,
            kwargs=kwargs or {},
            priority=priority,
            max_retries=max_retries,
            retry_delay=retry_delay,
            timeout=timeout,
            dependencies=dependencies or [],
            metadata=metadata or {},
        )

        self.tasks[task_id] = task

        # Queue task if dependencies are satisfied
        if self._are_dependencies_satisfied(task):
            asyncio.create_task(self._queue_task(task))

        self.logger.info(f"Added task {task_id}: {name}")
        return task_id

    def create_workflow(
        self, name: str, metadata: Optional[dict[str, Any]] = None
    ) -> str:
        """Create a new workflow."""
        workflow_id = str(uuid.uuid4())

        workflow = Workflow(id=workflow_id, name=name, metadata=metadata or {})

        self.workflows[workflow_id] = workflow
        self.logger.info(f"Created workflow {workflow_id}: {name}")
        return workflow_id

    def add_task_to_workflow(self, workflow_id: str, task_id: str):
        """Add a task to a workflow."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")

        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")

        workflow = self.workflows[workflow_id]
        task = self.tasks[task_id]

        if task not in workflow.tasks:
            workflow.tasks.append(task)
            self.logger.info(f"Added task {task_id} to workflow {workflow_id}")

    async def execute_workflow(self, workflow_id: str) -> bool:
        """Execute a workflow."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")

        workflow = self.workflows[workflow_id]
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.now()

        await self._emit_event("workflow_started", workflow)

        try:
            # Execute tasks in dependency order
            for task in workflow.tasks:
                if not self._are_dependencies_satisfied(task):
                    continue

                await self._queue_task(task)

            # Wait for all workflow tasks to complete
            workflow_tasks = [t for t in workflow.tasks]
            while workflow_tasks:
                completed_tasks = []
                for task in workflow_tasks:
                    if task.status in [
                        TaskStatus.COMPLETED,
                        TaskStatus.FAILED,
                        TaskStatus.CANCELLED,
                    ]:
                        completed_tasks.append(task)

                for task in completed_tasks:
                    workflow_tasks.remove(task)

                if workflow_tasks:
                    await asyncio.sleep(0.1)

            # Check if all tasks completed successfully
            failed_tasks = [t for t in workflow.tasks if t.status == TaskStatus.FAILED]
            if failed_tasks:
                workflow.status = WorkflowStatus.FAILED
                await self._emit_event("workflow_failed", workflow)
                return False
            else:
                workflow.status = WorkflowStatus.COMPLETED
                workflow.completed_at = datetime.now()
                await self._emit_event("workflow_completed", workflow)
                return True

        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.completed_at = datetime.now()
            self.logger.error(f"Workflow {workflow_id} failed: {e}")
            await self._emit_event("workflow_failed", workflow)
            return False

    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get the status of a task."""
        task = self.tasks.get(task_id)
        return task.status if task else None

    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowStatus]:
        """Get the status of a workflow."""
        workflow = self.workflows.get(workflow_id)
        return workflow.status if workflow else None

    def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        """Get the result of a task."""
        task = self.tasks.get(task_id)
        return task.result if task else None

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task."""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]

        if task_id in self.running_tasks:
            self.running_tasks[task_id].cancel()
            del self.running_tasks[task_id]

        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.now()

        self.logger.info(f"Cancelled task {task_id}")
        return True

    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a workflow and all its tasks."""
        if workflow_id not in self.workflows:
            return False

        workflow = self.workflows[workflow_id]
        workflow.status = WorkflowStatus.CANCELLED
        workflow.completed_at = datetime.now()

        # Cancel all workflow tasks
        for task in workflow.tasks:
            self.cancel_task(task.id)

        self.logger.info(f"Cancelled workflow {workflow_id}")
        return True

    def add_event_handler(self, event_type: str, handler: Callable):
        """Add an event handler."""
        if event_type in self.event_handlers:
            self.event_handlers[event_type].append(handler)

    def get_statistics(self) -> dict[str, Any]:
        """Get orchestrator statistics."""
        total_tasks = len(self.tasks)
        completed_tasks = len(
            [t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]
        )
        failed_tasks = len(
            [t for t in self.tasks.values() if t.status == TaskStatus.FAILED]
        )
        running_tasks = len(
            [t for t in self.tasks.values() if t.status == TaskStatus.RUNNING]
        )
        pending_tasks = len(
            [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
        )

        total_workflows = len(self.workflows)
        completed_workflows = len(
            [w for w in self.workflows.values() if w.status == WorkflowStatus.COMPLETED]
        )
        failed_workflows = len(
            [w for w in self.workflows.values() if w.status == WorkflowStatus.FAILED]
        )
        running_workflows = len(
            [w for w in self.workflows.values() if w.status == WorkflowStatus.RUNNING]
        )

        return {
            "orchestrator_status": "running" if self.is_running else "stopped",
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "failed": failed_tasks,
                "running": running_tasks,
                "pending": pending_tasks,
            },
            "workflows": {
                "total": total_workflows,
                "completed": completed_workflows,
                "failed": failed_workflows,
                "running": running_workflows,
            },
            "workers": {
                "max_workers": self.max_workers,
                "active_workers": len(self.worker_tasks),
            },
        }

    async def _worker(self, worker_name: str):
        """Worker coroutine for processing tasks."""
        self.logger.info(f"Started worker: {worker_name}")

        while self.is_running:
            try:
                # Get task from queue with timeout
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)

                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    # Put task back in queue if at capacity
                    await self.task_queue.put(task)
                    await asyncio.sleep(0.1)
                    continue

                # Execute task
                execution_task = asyncio.create_task(self._execute_task(task))
                self.running_tasks[task.id] = execution_task

                # Don't await here - let task run concurrently

            except asyncio.TimeoutError:
                # No tasks in queue, continue
                continue
            except Exception as e:
                self.logger.error(f"Worker {worker_name} error: {e}")
                await asyncio.sleep(1.0)

        self.logger.info(f"Stopped worker: {worker_name}")

    async def _execute_task(self, task: Task):
        """Execute a single task."""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()

        await self._emit_event("task_started", task)

        start_time = datetime.now()

        try:
            # Execute task with timeout
            if asyncio.iscoroutinefunction(task.handler):
                if task.timeout:
                    result = await asyncio.wait_for(
                        task.handler(*task.args, **task.kwargs), timeout=task.timeout
                    )
                else:
                    result = await task.handler(*task.args, **task.kwargs)
            else:
                # Run sync function in executor
                if task.timeout:
                    result = await asyncio.wait_for(
                        asyncio.get_event_loop().run_in_executor(
                            self.executor,
                            lambda: task.handler(*task.args, **task.kwargs),
                        ),
                        timeout=task.timeout,
                    )
                else:
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.executor, lambda: task.handler(*task.args, **task.kwargs)
                    )

            # Task completed successfully
            execution_time = (datetime.now() - start_time).total_seconds()

            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = TaskResult(
                task_id=task.id,
                status=TaskStatus.COMPLETED,
                result=result,
                execution_time=execution_time,
            )

            await self._emit_event("task_completed", task)
            self.logger.info(f"Task {task.id} completed successfully")

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            error_msg = str(e)

            # Handle retries
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.RETRYING

                self.logger.warning(
                    f"Task {task.id} failed, retrying ({task.retry_count}/{
                        task.max_retries
                    }): {error_msg}"
                )

                # Schedule retry
                await asyncio.sleep(task.retry_delay)
                await self._queue_task(task)
            else:
                # Task failed permanently
                task.status = TaskStatus.FAILED
                task.completed_at = datetime.now()
                task.result = TaskResult(
                    task_id=task.id,
                    status=TaskStatus.FAILED,
                    error=error_msg,
                    execution_time=execution_time,
                )

                await self._emit_event("task_failed", task)
                self.logger.error(
                    f"Task {
                        task.id} failed permanently: {error_msg}"
                )

        finally:
            # Remove from running tasks
            if task.id in self.running_tasks:
                del self.running_tasks[task.id]

    async def _queue_task(self, task: Task):
        """Queue a task for execution."""
        await self.task_queue.put(task)

    def _are_dependencies_satisfied(self, task: Task) -> bool:
        """Check if task dependencies are satisfied."""
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                return False

            dep_task = self.tasks[dep_id]
            if dep_task.status != TaskStatus.COMPLETED:
                return False

        return True

    async def _monitor_tasks(self):
        """Monitor tasks and handle dependency resolution."""
        while self.is_running:
            try:
                # Check for tasks with satisfied dependencies
                for task in self.tasks.values():
                    if (
                        task.status == TaskStatus.PENDING
                        and self._are_dependencies_satisfied(task)
                    ):
                        await self._queue_task(task)

                await asyncio.sleep(1.0)

            except Exception as e:
                self.logger.error(f"Task monitor error: {e}")
                await asyncio.sleep(5.0)

    async def _emit_event(self, event_type: str, data: Any):
        """Emit an event to registered handlers."""
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(data)
                    else:
                        handler(data)
                except Exception as e:
                    self.logger.error(f"Event handler error for {event_type}: {e}")


# Global orchestrator instance
orchestrator = TaskOrchestrator()


# Convenience functions
async def add_task(name: str, handler: Callable, **kwargs) -> str:
    """Add a task to the global orchestrator."""
    return orchestrator.add_task(name, handler, **kwargs)


async def create_workflow(name: str, **kwargs) -> str:
    """Create a workflow in the global orchestrator."""
    return orchestrator.create_workflow(name, **kwargs)


async def execute_workflow(workflow_id: str) -> bool:
    """Execute a workflow in the global orchestrator."""
    return await orchestrator.execute_workflow(workflow_id)


def get_orchestrator_stats() -> dict[str, Any]:
    """Get global orchestrator statistics."""
    return orchestrator.get_statistics()
