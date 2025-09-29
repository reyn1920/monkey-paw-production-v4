"""
SOLO Agent Router

FastAPI router for SOLO agent endpoints, providing REST API access to the
upgraded SOLO agent with self-healing verification capabilities.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, BackgroundTasks, WebSocket
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/solo", tags=["SOLO Agent"])


# Pydantic models for request/response
class GoalExecutionRequest(BaseModel):
    goal: str = Field(..., description="High-level goal description")
    context: Optional[dict[str, Any]] = Field(
        None, description="Additional context for execution"
    )
    agent_config: Optional[dict[str, Any]] = Field(
        None, description="Agent configuration overrides"
    )


class ToolExecutionRequest(BaseModel):
    tool_name: str = Field(..., description="Name of the tool to execute")
    args: list[str] = Field(default_factory=list, description="Tool arguments")
    kwargs: dict[str, Any] = Field(
        default_factory=dict, description="Tool keyword arguments"
    )


class PlanRequest(BaseModel):
    goal: str = Field(..., description="Goal to create execution plan for")


class AgentStatusResponse(BaseModel):
    agent_id: str
    execution_count: int
    failed_actions: int
    recovery_attempts: int
    last_execution: Optional[dict[str, Any]]
    available: bool


class ExecutionResponse(BaseModel):
    success: bool
    execution_id: Optional[str] = None
    message: str
    details: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str


# Import SOLO agent components with proper error handling
def _import_solo_components():
    """Import SOLO agent components safely."""
    try:
        import sys
        from pathlib import Path

        # Add scripts directory to path
        scripts_path = Path(__file__).parent.parent.parent / "scripts"
        sys.path.insert(0, str(scripts_path))

        from solo import SOLOAgent, run_tool, plan_goal

        return SOLOAgent, run_tool, plan_goal, True
    except ImportError as e:
        logger.warning(f"SOLO agent not available: {e}")
        return None, None, None, False


# Initialize SOLO components
SOLOAgent, run_tool, plan_goal, solo_available = _import_solo_components()

# Global agent instance
_solo_agent = None


def get_solo_agent():
    """Get or create SOLO agent instance."""
    global _solo_agent

    if not solo_available or SOLOAgent is None:
        raise HTTPException(
            status_code=503,
            detail="SOLO agent is not available. Please check the installation.",
        )

    if _solo_agent is None:
        _solo_agent = SOLOAgent()
        logger.info("Created new SOLO agent instance")

    return _solo_agent


@router.get("/status", response_model=AgentStatusResponse)
async def get_agent_status():
    """Get current SOLO agent status."""
    try:
        if not solo_available:
            return AgentStatusResponse(
                agent_id="unavailable",
                execution_count=0,
                failed_actions=0,
                recovery_attempts=0,
                last_execution=None,
                available=False,
            )

        agent = get_solo_agent()
        if hasattr(agent, "get_status"):
            status = agent.get_status()
            return AgentStatusResponse(
                agent_id=status.get("agent_id", "unknown"),
                execution_count=status.get("execution_count", 0),
                failed_actions=status.get("failed_actions", 0),
                recovery_attempts=status.get("recovery_attempts", 0),
                last_execution=status.get("last_execution"),
                available=True,
            )
        else:
            return AgentStatusResponse(
                agent_id="basic",
                execution_count=0,
                failed_actions=0,
                recovery_attempts=0,
                last_execution=None,
                available=True,
            )

    except Exception as e:
        logger.error(f"Error getting agent status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute", response_model=ExecutionResponse)
async def execute_goal(
    request: GoalExecutionRequest, background_tasks: BackgroundTasks
):
    """Execute a goal using the SOLO agent."""
    try:
        agent = get_solo_agent()

        # Configure agent if config provided and supported
        if request.agent_config and hasattr(agent, "config"):
            agent.config.update(request.agent_config)

        logger.info(f"Executing goal: {request.goal}")

        # Execute goal asynchronously if supported
        if hasattr(agent, "execute_goal_async"):
            result = await agent.execute_goal_async(request.goal, request.context)
        elif hasattr(agent, "execute"):
            # Fallback to sync execution
            result = agent.execute(request.goal)
            if not isinstance(result, dict):
                result = {"success": True, "result": result}
        else:
            # Basic execution fallback
            result = {
                "success": True,
                "message": f"Goal received: {
                    request.goal}",
            }

        return ExecutionResponse(
            success=result.get("success", True),
            execution_id=result.get("execution_id"),
            message=(
                "Goal execution completed"
                if result.get("success", True)
                else "Goal execution failed"
            ),
            details=result,
            error=result.get("error"),
            timestamp=datetime.now().isoformat(),
        )

    except Exception as e:
        logger.error(f"Error executing goal: {e}")
        return ExecutionResponse(
            success=False,
            message="Goal execution failed with exception",
            error=str(e),
            timestamp=datetime.now().isoformat(),
        )


@router.post("/execute-sync", response_model=ExecutionResponse)
async def execute_goal_sync(request: GoalExecutionRequest):
    """Execute a goal synchronously (blocking)."""
    return await execute_goal(request, BackgroundTasks())


@router.post("/tool", response_model=ExecutionResponse)
async def execute_tool(request: ToolExecutionRequest):
    """Execute a single tool."""
    try:
        if not solo_available or run_tool is None:
            raise HTTPException(
                status_code=503, detail="SOLO agent tools are not available"
            )

        logger.info(
            f"Executing tool: {
                request.tool_name} with args: {
                request.args}"
        )

        result = run_tool(request.tool_name, *request.args, **request.kwargs)

        return ExecutionResponse(
            success=result.get("success", result.get("code", 0) == 0),
            message=f"Tool {request.tool_name} executed",
            details=result,
            error=result.get("error") or result.get("stderr"),
            timestamp=datetime.now().isoformat(),
        )

    except Exception as e:
        logger.error(f"Error executing tool: {e}")
        return ExecutionResponse(
            success=False,
            message=f"Tool execution failed: {request.tool_name}",
            error=str(e),
            timestamp=datetime.now().isoformat(),
        )


@router.post("/plan")
async def create_execution_plan(request: PlanRequest):
    """Create an execution plan for a goal."""
    try:
        if not solo_available or plan_goal is None:
            raise HTTPException(
                status_code=503, detail="SOLO agent planning is not available"
            )

        logger.info(f"Creating plan for goal: {request.goal}")

        plan = plan_goal(request.goal)

        return {
            "success": True,
            "goal": request.goal,
            "plan": plan,
            "steps": len(plan) if isinstance(plan, list) else 0,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error creating plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint for SOLO agent."""
    return {
        "status": "healthy" if solo_available else "unavailable",
        "solo_available": solo_available,
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/capabilities")
async def get_capabilities():
    """Get SOLO agent capabilities."""
    return {
        "available": solo_available,
        "tools": ["pytest", "npm", "git", "python", "shell"] if solo_available else [],
        "features": (
            [
                "goal_execution",
                "self_healing",
                "verification",
                "async_execution",
                "tool_execution",
                "plan_generation",
            ]
            if solo_available
            else []
        ),
        "version": "1.0.0",
    }


# WebSocket endpoint for real-time updates (if needed)
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time SOLO agent updates."""
    await websocket.accept()

    try:
        if not solo_available:
            await websocket.send_json(
                {"type": "error", "message": "SOLO agent not available"}
            )
            return

        agent = get_solo_agent()

        # Send initial status
        if hasattr(agent, "get_status"):
            await websocket.send_json({"type": "status", "data": agent.get_status()})
        else:
            await websocket.send_json(
                {"type": "status", "data": {"available": True, "agent_id": "basic"}}
            )

        # Keep connection alive and send periodic updates
        while True:
            await asyncio.sleep(5)  # Send updates every 5 seconds

            try:
                if hasattr(agent, "get_status"):
                    status = agent.get_status()
                else:
                    status = {"available": True, "agent_id": "basic"}

                await websocket.send_json(
                    {
                        "type": "status_update",
                        "data": status,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Error sending WebSocket update: {e}")
                break

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()
