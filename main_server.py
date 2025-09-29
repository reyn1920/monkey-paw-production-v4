"""
Trae.ai Unified Development Environment - Main FastAPI Server
Provides endpoints for SOLO agent execution, Genesis interviews, and orchestrator events.
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
import logging
from typing import Any, Optional
import uvicorn
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Trae.ai Unified Development Environment",
    description="Main server for SOLO agent execution, Genesis interviews, and orchestrator events",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class SOLOExecuteRequest(BaseModel):
    goal: str
    context: Optional[dict[str, Any]] = None
    priority: Optional[str] = "medium"


class SOLOExecuteResponse(BaseModel):
    task_id: str
    status: str
    message: str
    timestamp: str


class GenesisInterviewRequest(BaseModel):
    project_type: str
    requirements: Optional[dict[str, Any]] = None
    user_preferences: Optional[dict[str, Any]] = None


class GenesisInterviewResponse(BaseModel):
    interview_id: str
    status: str
    next_question: Optional[str] = None
    progress: float
    timestamp: str


# In-memory storage for demo purposes (use proper database in production)
active_tasks: dict[str, dict[str, Any]] = {}
active_interviews: dict[str, dict[str, Any]] = {}
websocket_connections: dict[str, WebSocket] = {}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Trae.ai Unified Development Environment Server",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "solo_execute": "/solo/execute_goal",
            "genesis_interview": "/genesis/start_interview",
            "orchestrator_ws": "/ws/orchestrator_events",
        },
    }


@app.post("/solo/execute_goal", response_model=SOLOExecuteResponse)
async def execute_solo_goal(request: SOLOExecuteRequest):
    """
    Trigger SOLO agent to execute a specific goal
    """
    try:
        # Generate unique task ID
        task_id = f"solo_task_{len(active_tasks) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create task record
        task_data = {
            "goal": request.goal,
            "context": request.context or {},
            "priority": request.priority,
            "status": "initiated",
            "created_at": datetime.now().isoformat(),
            "progress": 0.0,
        }

        active_tasks[task_id] = task_data

        # Log the task initiation
        logger.info(f"SOLO task initiated: {task_id} - Goal: {request.goal}")

        # Simulate task processing (replace with actual SOLO agent integration)
        asyncio.create_task(simulate_solo_execution(task_id))

        # Broadcast to WebSocket connections
        await broadcast_orchestrator_event(
            {
                "type": "solo_task_started",
                "task_id": task_id,
                "goal": request.goal,
                "timestamp": datetime.now().isoformat(),
            }
        )

        return SOLOExecuteResponse(
            task_id=task_id,
            status="initiated",
            message=f"SOLO agent task '{task_id}' has been initiated successfully",
            timestamp=datetime.now().isoformat(),
        )

    except Exception as e:
        logger.error(f"Error executing SOLO goal: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to execute SOLO goal: {str(e)}"
        )


@app.post("/genesis/start_interview", response_model=GenesisInterviewResponse)
async def start_genesis_interview(request: GenesisInterviewRequest):
    """
    Start a Genesis application design interview
    """
    try:
        # Generate unique interview ID
        interview_id = f"genesis_interview_{len(active_interviews) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create interview record
        interview_data = {
            "project_type": request.project_type,
            "requirements": request.requirements or {},
            "user_preferences": request.user_preferences or {},
            "status": "started",
            "created_at": datetime.now().isoformat(),
            "progress": 0.1,
            "current_question": 1,
            "total_questions": 10,
        }

        active_interviews[interview_id] = interview_data

        # Log the interview initiation
        logger.info(
            f"Genesis interview started: {interview_id} - Project type: {request.project_type}"
        )

        # Generate first question based on project type
        first_question = generate_genesis_question(request.project_type, 1)

        # Broadcast to WebSocket connections
        await broadcast_orchestrator_event(
            {
                "type": "genesis_interview_started",
                "interview_id": interview_id,
                "project_type": request.project_type,
                "timestamp": datetime.now().isoformat(),
            }
        )

        return GenesisInterviewResponse(
            interview_id=interview_id,
            status="started",
            next_question=first_question,
            progress=0.1,
            timestamp=datetime.now().isoformat(),
        )

    except Exception as e:
        logger.error(f"Error starting Genesis interview: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to start Genesis interview: {str(e)}"
        )


@app.websocket("/ws/orchestrator_events")
async def orchestrator_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for streaming orchestrator events
    """
    await websocket.accept()
    connection_id = (
        f"ws_conn_{len(websocket_connections) + 1}_{datetime.now().strftime('%H%M%S')}"
    )
    websocket_connections[connection_id] = websocket

    logger.info(f"WebSocket connection established: {connection_id}")

    try:
        # Send welcome message
        await websocket.send_text(
            json.dumps(
                {
                    "type": "connection_established",
                    "connection_id": connection_id,
                    "message": "Connected to Trae.ai orchestrator events stream",
                    "timestamp": datetime.now().isoformat(),
                }
            )
        )

        # Keep connection alive and handle incoming messages
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)

                # Echo back received message with timestamp
                response = {
                    "type": "echo",
                    "received_message": message,
                    "connection_id": connection_id,
                    "timestamp": datetime.now().isoformat(),
                }
                await websocket.send_text(json.dumps(response))

            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket error for {connection_id}: {str(e)}")
                break

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {connection_id}")
    finally:
        # Clean up connection
        if connection_id in websocket_connections:
            del websocket_connections[connection_id]


# Helper functions
async def simulate_solo_execution(task_id: str):
    """Simulate SOLO agent execution (replace with actual implementation)"""
    try:
        # Simulate processing stages
        stages = ["analyzing", "planning", "executing", "testing", "completed"]

        for i, stage in enumerate(stages):
            await asyncio.sleep(2)  # Simulate work

            if task_id in active_tasks:
                active_tasks[task_id]["status"] = stage
                active_tasks[task_id]["progress"] = (i + 1) / len(stages)

                # Broadcast progress update
                await broadcast_orchestrator_event(
                    {
                        "type": "solo_task_progress",
                        "task_id": task_id,
                        "status": stage,
                        "progress": active_tasks[task_id]["progress"],
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        logger.info(f"SOLO task completed: {task_id}")

    except Exception as e:
        logger.error(f"Error in SOLO simulation for {task_id}: {str(e)}")
        if task_id in active_tasks:
            active_tasks[task_id]["status"] = "error"
            active_tasks[task_id]["error"] = str(e)


def generate_genesis_question(project_type: str, question_number: int) -> str:
    """Generate Genesis interview questions based on project type"""
    questions = {
        "web_app": [
            "What is the primary purpose of your web application?",
            "Who is your target audience?",
            "What key features do you want to include?",
            "Do you need user authentication?",
            "What data will your application manage?",
            "Do you need real-time features?",
            "What's your preferred UI/UX style?",
            "Do you need third-party integrations?",
            "What's your deployment preference?",
            "Any specific performance requirements?",
        ],
        "api": [
            "What type of API are you building (REST, GraphQL, etc.)?",
            "What data will your API serve?",
            "Who will consume your API?",
            "Do you need authentication/authorization?",
            "What's your expected request volume?",
            "Do you need real-time capabilities?",
            "What database will you use?",
            "Do you need API documentation?",
            "What's your deployment strategy?",
            "Any specific compliance requirements?",
        ],
    }

    project_questions = questions.get(project_type, questions["web_app"])
    if question_number <= len(project_questions):
        return project_questions[question_number - 1]
    else:
        return "Thank you for your responses. Ready to generate your application!"


async def broadcast_orchestrator_event(event: dict[str, Any]):
    """Broadcast event to all connected WebSocket clients"""
    if not websocket_connections:
        return

    message = json.dumps(event)
    disconnected_connections = []

    for connection_id, websocket in websocket_connections.items():
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Failed to send message to {connection_id}: {str(e)}")
            disconnected_connections.append(connection_id)

    # Clean up disconnected connections
    for connection_id in disconnected_connections:
        del websocket_connections[connection_id]


# Additional endpoints for task and interview management
@app.get("/solo/tasks")
async def get_solo_tasks():
    """Get all SOLO tasks"""
    return {"tasks": active_tasks}


@app.get("/solo/tasks/{task_id}")
async def get_solo_task(task_id: str):
    """Get specific SOLO task"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": active_tasks[task_id]}


@app.get("/genesis/interviews")
async def get_genesis_interviews():
    """Get all Genesis interviews"""
    return {"interviews": active_interviews}


@app.get("/genesis/interviews/{interview_id}")
async def get_genesis_interview(interview_id: str):
    """Get specific Genesis interview"""
    if interview_id not in active_interviews:
        raise HTTPException(status_code=404, detail="Interview not found")
    return {"interview": active_interviews[interview_id]}


if __name__ == "__main__":
    uvicorn.run(
        "main_server:app", host="0.0.0.0", port=8001, reload=True, log_level="info"
    )
