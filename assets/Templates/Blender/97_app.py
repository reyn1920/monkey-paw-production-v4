#!/usr/bin/env python3
"""
Backend FastAPI Application
Main FastAPI application with comprehensive API endpoints
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()


# Pydantic Models
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0"
    uptime: float
    environment: str


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class TaskRequest(BaseModel):
    task_type: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    priority: str = "medium"
    description: Optional[str] = None


class TaskResponse(BaseModel):
    task_id: str
    status: str
    created_at: datetime
    estimated_completion: Optional[datetime] = None


class UserRequest(BaseModel):
    name: str
    email: str
    role: str = "user"
    metadata: dict[str, Any] = Field(default_factory=dict)


class UserResponse(BaseModel):
    user_id: str
    name: str
    email: str
    role: str
    created_at: datetime
    last_active: Optional[datetime] = None


class MetricsResponse(BaseModel):
    total_requests: int
    active_tasks: int
    system_health: str
    response_time_avg: float
    error_rate: float
    uptime_percentage: float


class ConfigRequest(BaseModel):
    key: str
    value: Any
    category: str = "general"
    description: Optional[str] = None


# Global state
app_state: dict[str, Any] = {
    "start_time": datetime.now(),
    "request_count": 0,
    "error_count": 0,
    "active_tasks": {},
    "users": {},
    "config": {},
    "metrics": {"response_times": [], "request_history": [], "error_history": []},
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting FastAPI application...")

    # Initialize default configuration
    config_dict = app_state["config"]
    if isinstance(config_dict, dict):
        config_dict.update(
            {
                "max_tasks": 100,
                "task_timeout": 300,
                "rate_limit": 1000,
                "debug_mode": os.getenv("DEBUG", "false").lower() == "true",
                "environment": os.getenv("ENVIRONMENT", "development"),
            }
        )

    # Start background tasks
    asyncio.create_task(cleanup_expired_tasks())
    asyncio.create_task(collect_metrics())

    logger.info("FastAPI application started successfully")

    yield

    # Shutdown
    logger.info("Shutting down FastAPI application...")
    # Cleanup tasks here if needed
    logger.info("FastAPI application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Backend API",
    description="Comprehensive backend API for the application",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # Configure appropriately for production
)


# Middleware for request tracking
@app.middleware("http")
async def track_requests(request: Request, call_next):
    start_time = datetime.now()
    if isinstance(app_state["request_count"], int):
        app_state["request_count"] += 1

    try:
        response = await call_next(request)

        # Record response time
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        app_state["metrics"]["response_times"].append(response_time)

        # Keep only last 1000 response times
        if len(app_state["metrics"]["response_times"]) > 1000:
            app_state["metrics"]["response_times"] = app_state["metrics"][
                "response_times"
            ][-1000:]

        return response

    except Exception as e:
        app_state["error_count"] += 1
        app_state["metrics"]["error_history"].append(
            {"timestamp": datetime.now(), "error": str(e), "path": request.url.path}
        )
        raise


# Authentication dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Simple token validation - replace with proper authentication"""
    token = credentials.credentials

    # Simple token validation (replace with proper JWT validation)
    if token == "demo-token" or token.startswith("sk-"):
        return {"user_id": "demo-user", "role": "admin"}

    raise HTTPException(status_code=401, detail="Invalid authentication credentials")


# Optional authentication dependency
async def get_current_user_optional(request: Request):
    """Optional authentication for public endpoints"""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            if token == "demo-token" or token.startswith("sk-"):
                return {"user_id": "demo-user", "role": "admin"}
        except:
            pass
    return None


# Background tasks
async def cleanup_expired_tasks():
    """Clean up expired tasks periodically"""
    while True:
        try:
            current_time = datetime.now()
            expired_tasks = []

            for task_id, task_info in app_state["active_tasks"].items():
                if "expires_at" in task_info and current_time > task_info["expires_at"]:
                    expired_tasks.append(task_id)

            for task_id in expired_tasks:
                del app_state["active_tasks"][task_id]
                logger.info(f"Cleaned up expired task: {task_id}")

            await asyncio.sleep(60)  # Run every minute

        except Exception as e:
            logger.error(f"Error in cleanup task: {e}")
            await asyncio.sleep(60)


async def collect_metrics():
    """Collect system metrics periodically"""
    while True:
        try:
            # Record current metrics
            metrics_snapshot = {
                "timestamp": datetime.now(),
                "request_count": app_state["request_count"],
                "error_count": app_state["error_count"],
                "active_tasks": len(app_state["active_tasks"]),
                "memory_usage": 0,  # Placeholder - implement actual memory monitoring
            }

            app_state["metrics"]["request_history"].append(metrics_snapshot)

            # Keep only last 24 hours of metrics
            cutoff_time = datetime.now() - timedelta(hours=24)
            app_state["metrics"]["request_history"] = [
                m
                for m in app_state["metrics"]["request_history"]
                if m["timestamp"] > cutoff_time
            ]

            await asyncio.sleep(300)  # Run every 5 minutes

        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            await asyncio.sleep(300)


# API Routes


@app.get("/", response_model=APIResponse)
async def root():
    """Root endpoint"""
    return APIResponse(
        success=True,
        message="Backend API is running",
        data={
            "version": "1.0.0",
            "environment": app_state["config"].get("environment", "development"),
            "uptime": (datetime.now() - app_state["start_time"]).total_seconds(),
        },
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = (datetime.now() - app_state["start_time"]).total_seconds()

    # Determine health status
    error_rate = (app_state["error_count"] / max(app_state["request_count"], 1)) * 100
    status = "healthy"

    if error_rate > 10:
        status = "unhealthy"
    elif error_rate > 5:
        status = "degraded"

    return HealthResponse(
        status=status,
        timestamp=datetime.now(),
        uptime=uptime,
        environment=app_state["config"].get("environment", "development"),
    )


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics(user: dict = Depends(get_current_user_optional)):
    """Get system metrics"""
    response_times = app_state["metrics"]["response_times"]
    avg_response_time = (
        sum(response_times) / len(response_times) if response_times else 0
    )

    error_rate = (app_state["error_count"] / max(app_state["request_count"], 1)) * 100
    uptime = (datetime.now() - app_state["start_time"]).total_seconds()
    uptime_percentage = 99.9  # Placeholder - implement actual uptime calculation

    system_health = "healthy"
    if error_rate > 10:
        system_health = "critical"
    elif error_rate > 5:
        system_health = "warning"

    return MetricsResponse(
        total_requests=app_state["request_count"],
        active_tasks=len(app_state["active_tasks"]),
        system_health=system_health,
        response_time_avg=avg_response_time,
        error_rate=error_rate,
        uptime_percentage=uptime_percentage,
    )


@app.post("/tasks", response_model=TaskResponse)
async def create_task(
    task_request: TaskRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user),
):
    """Create a new task"""
    import uuid

    task_id = str(uuid.uuid4())

    # Create task
    task_info = {
        "id": task_id,
        "type": task_request.task_type,
        "parameters": task_request.parameters,
        "priority": task_request.priority,
        "description": task_request.description,
        "status": "pending",
        "created_at": datetime.now(),
        "created_by": user["user_id"],
        "expires_at": datetime.now()
        + timedelta(seconds=app_state["config"]["task_timeout"]),
    }

    app_state["active_tasks"][task_id] = task_info

    # Add background task to process it
    background_tasks.add_task(process_task, task_id)

    return TaskResponse(
        task_id=task_id,
        status="pending",
        created_at=task_info["created_at"],
        estimated_completion=datetime.now() + timedelta(minutes=5),
    )


@app.get("/tasks/{task_id}", response_model=APIResponse)
async def get_task(task_id: str, user: dict = Depends(get_current_user)):
    """Get task status"""
    if task_id not in app_state["active_tasks"]:
        raise HTTPException(status_code=404, detail="Task not found")

    task_info = app_state["active_tasks"][task_id]

    return APIResponse(
        success=True, message="Task retrieved successfully", data=task_info
    )


@app.delete("/tasks/{task_id}", response_model=APIResponse)
async def cancel_task(task_id: str, user: dict = Depends(get_current_user)):
    """Cancel a task"""
    if task_id not in app_state["active_tasks"]:
        raise HTTPException(status_code=404, detail="Task not found")

    task_info = app_state["active_tasks"][task_id]
    task_info["status"] = "cancelled"
    task_info["cancelled_at"] = datetime.now()

    return APIResponse(
        success=True, message="Task cancelled successfully", data=task_info
    )


@app.get("/tasks", response_model=APIResponse)
async def list_tasks(user: dict = Depends(get_current_user)):
    """List all tasks"""
    tasks = list(app_state["active_tasks"].values())

    return APIResponse(
        success=True,
        message="Tasks retrieved successfully",
        data={"tasks": tasks, "total": len(tasks)},
    )


@app.post("/users", response_model=UserResponse)
async def create_user(
    user_request: UserRequest, current_user: dict = Depends(get_current_user)
):
    """Create a new user"""
    import uuid

    user_id = str(uuid.uuid4())

    user_info = {
        "id": user_id,
        "name": user_request.name,
        "email": user_request.email,
        "role": user_request.role,
        "metadata": user_request.metadata,
        "created_at": datetime.now(),
        "created_by": current_user["user_id"],
    }

    app_state["users"][user_id] = user_info

    return UserResponse(
        user_id=user_id,
        name=user_info["name"],
        email=user_info["email"],
        role=user_info["role"],
        created_at=user_info["created_at"],
    )


@app.get("/users/{user_id}", response_model=APIResponse)
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    """Get user by ID"""
    if user_id not in app_state["users"]:
        raise HTTPException(status_code=404, detail="User not found")

    user_info = app_state["users"][user_id]

    return APIResponse(
        success=True, message="User retrieved successfully", data=user_info
    )


@app.get("/users", response_model=APIResponse)
async def list_users(current_user: dict = Depends(get_current_user)):
    """List all users"""
    users = list(app_state["users"].values())

    return APIResponse(
        success=True,
        message="Users retrieved successfully",
        data={"users": users, "total": len(users)},
    )


@app.post("/config", response_model=APIResponse)
async def set_config(
    config_request: ConfigRequest, user: dict = Depends(get_current_user)
):
    """Set configuration value"""
    app_state["config"][config_request.key] = {
        "value": config_request.value,
        "category": config_request.category,
        "description": config_request.description,
        "updated_at": datetime.now(),
        "updated_by": user["user_id"],
    }

    return APIResponse(
        success=True,
        message="Configuration updated successfully",
        data={"key": config_request.key, "value": config_request.value},
    )


@app.get("/config/{key}", response_model=APIResponse)
async def get_config(key: str, user: dict = Depends(get_current_user_optional)):
    """Get configuration value"""
    if key not in app_state["config"]:
        raise HTTPException(status_code=404, detail="Configuration key not found")

    config_info = app_state["config"][key]

    return APIResponse(
        success=True, message="Configuration retrieved successfully", data=config_info
    )


@app.get("/config", response_model=APIResponse)
async def list_config(user: dict = Depends(get_current_user_optional)):
    """List all configuration"""
    return APIResponse(
        success=True,
        message="Configuration retrieved successfully",
        data=app_state["config"],
    )


# Task processing function
async def process_task(task_id: str):
    """Process a task in the background"""
    try:
        if task_id not in app_state["active_tasks"]:
            return

        task_info = app_state["active_tasks"][task_id]
        task_info["status"] = "processing"
        task_info["started_at"] = datetime.now()

        # Simulate task processing
        await asyncio.sleep(2)  # Simulate work

        # Update task status
        task_info["status"] = "completed"
        task_info["completed_at"] = datetime.now()
        task_info["result"] = {
            "message": f"Task {task_info['type']} completed successfully",
            "processed_at": datetime.now(),
        }

        logger.info(f"Task {task_id} completed successfully")

    except Exception as e:
        logger.error(f"Error processing task {task_id}: {e}")
        if task_id in app_state["active_tasks"]:
            task_info = app_state["active_tasks"][task_id]
            task_info["status"] = "failed"
            task_info["error"] = str(e)
            task_info["failed_at"] = datetime.now()


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path,
        },
    )


if __name__ == "__main__":
    # Run the application
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
