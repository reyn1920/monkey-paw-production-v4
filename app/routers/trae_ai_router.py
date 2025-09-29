"""
TRAE.AI Router for FastAPI
Provides endpoints for TRAE.AI integration with ChatGPT, Gemini, and Abacus AI
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import asyncio
import time
import json
from datetime import datetime

from ..trae_ai_simple import SimpleTraeAI, test_simple_trae_ai_connection, TEST_PROMPT

router = APIRouter(prefix="/api/trae-ai", tags=["TRAE.AI Integration"])

# Global TRAE.AI instance
_trae_ai_instance: Optional[SimpleTraeAI] = None

def get_trae_ai() -> SimpleTraeAI:
    """Get or create TRAE.AI instance"""
    global _trae_ai_instance
    if _trae_ai_instance is None:
        _trae_ai_instance = SimpleTraeAI()
    return _trae_ai_instance

# Pydantic Models
class ContentGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Content generation prompt")
    content_type: str = Field(default="video", description="Type of content to generate")
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="Additional parameters")
    cross_validate: Optional[bool] = Field(default=True, description="Enable cross-validation across AI platforms")

class ResearchRequest(BaseModel):
    query: str = Field(..., description="Research query")
    sources: Optional[List[str]] = Field(default=None, description="Research sources")
    depth: str = Field(default="comprehensive", description="Research depth")

class VideoCreationRequest(BaseModel):
    script: str = Field(..., description="Video script")
    voice_settings: Optional[Dict[str, Any]] = Field(default=None, description="Voice settings")
    video_settings: Optional[Dict[str, Any]] = Field(default=None, description="Video settings")

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: str
    execution_time_ms: Optional[int] = None

# Endpoints

@router.get("/status")
async def get_system_status():
    """Get TRAE.AI system status"""
    try:
        trae_ai = get_trae_ai()
        status = await trae_ai.get_system_status()
        return JSONResponse(content={
            "ok": True,
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting system status: {str(e)}")

@router.get("/test-connection")
async def test_connection():
    """Test TRAE.AI connection and all AI platforms"""
    try:
        result = await test_simple_trae_ai_connection()
        return JSONResponse(content={
            "ok": True,
            "test_result": result,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")

@router.post("/generate-content", response_model=TaskResponse)
async def generate_content(request: ContentGenerationRequest, background_tasks: BackgroundTasks):
    """Generate content using all AI platforms with cross-validation"""
    try:
        trae_ai = get_trae_ai()
        task_id = f"content_{int(time.time())}"

        # Generate content
        result = await trae_ai.generate_content(
            prompt=request.prompt,
            content_type=request.content_type,
            parameters=request.parameters,
            cross_validate=request.cross_validate
        )

        return TaskResponse(
            task_id=task_id,
            status="completed",
            result=result,
            created_at=datetime.now().isoformat(),
            execution_time_ms=int(time.time() * 1000) - int(task_id.split('_')[1]) * 1000
        )

    except Exception as e:
        return TaskResponse(
            task_id=f"content_{int(time.time())}",
            status="failed",
            error=str(e),
            created_at=datetime.now().isoformat()
        )

@router.post("/research", response_model=TaskResponse)
async def research_analyze(request: ResearchRequest, background_tasks: BackgroundTasks):
    """Perform research analysis using all AI platforms"""
    try:
        trae_ai = get_trae_ai()
        task_id = f"research_{int(time.time())}"

        # Perform research
        result = await trae_ai.research_analyze(
            query=request.query,
            sources=request.sources,
            depth=request.depth
        )

        return TaskResponse(
            task_id=task_id,
            status="completed",
            result=result,
            created_at=datetime.now().isoformat(),
            execution_time_ms=int(time.time() * 1000) - int(task_id.split('_')[1]) * 1000
        )

    except Exception as e:
        return TaskResponse(
            task_id=f"research_{int(time.time())}",
            status="failed",
            error=str(e),
            created_at=datetime.now().isoformat()
        )

@router.post("/create-video", response_model=TaskResponse)
async def create_video(request: VideoCreationRequest, background_tasks: BackgroundTasks):
    """Create video using TRAE.AI video production pipeline"""
    try:
        trae_ai = get_trae_ai()
        task_id = f"video_{int(time.time())}"

        # Create video
        result = await trae_ai.create_video(
            script=request.script,
            voice_settings=request.voice_settings,
            video_settings=request.video_settings
        )

        return TaskResponse(
            task_id=task_id,
            status="completed" if "error" not in result else "failed",
            result=result,
            error=result.get("error") if "error" in result else None,
            created_at=datetime.now().isoformat(),
            execution_time_ms=int(time.time() * 1000) - int(task_id.split('_')[1]) * 1000
        )

    except Exception as e:
        return TaskResponse(
            task_id=f"video_{int(time.time())}",
            status="failed",
            error=str(e),
            created_at=datetime.now().isoformat()
        )

@router.get("/platforms/status")
async def get_platforms_status():
    """Get status of all AI platforms"""
    try:
        trae_ai = get_trae_ai()

        # Test each platform individually
        platforms_status = {}

        # Test ChatGPT
        try:
            chatgpt_result = await trae_ai.chatgpt_client.generate_content(
                TEST_PROMPT, "text", {}
            )
            platforms_status["chatgpt"] = {
                "status": "active" if "error" not in chatgpt_result else "error",
                "confidence": chatgpt_result.get("confidence", 0),
                "error": chatgpt_result.get("error")
            }
        except Exception as e:
            platforms_status["chatgpt"] = {
                "status": "error",
                "error": str(e)
            }

        # Test Gemini
        try:
            gemini_result = await trae_ai.gemini_client.generate_content(
                TEST_PROMPT, "text", {}
            )
            platforms_status["gemini"] = {
                "status": "active" if "error" not in gemini_result else "error",
                "confidence": gemini_result.get("confidence", 0),
                "error": gemini_result.get("error")
            }
        except Exception as e:
            platforms_status["gemini"] = {
                "status": "error",
                "error": str(e)
            }

        # Test Abacus
        try:
            abacus_result = await trae_ai.abacus_client.generate_content(
                TEST_PROMPT, "text", {}
            )
            platforms_status["abacus"] = {
                "status": "active" if "error" not in abacus_result else "error",
                "confidence": abacus_result.get("confidence", 0),
                "error": abacus_result.get("error")
            }
        except Exception as e:
            platforms_status["abacus"] = {
                "status": "error",
                "error": str(e)
            }

        return JSONResponse(content={
            "ok": True,
            "platforms": platforms_status,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting platforms status: {str(e)}")

@router.get("/config")
async def get_configuration():
    """Get current TRAE.AI configuration (without sensitive data)"""
    try:
        trae_ai = get_trae_ai()

        # Return config without API keys
        safe_config = {
            "base_url": trae_ai.config.get("base_url"),
            "cross_validate": trae_ai.config.get("cross_validate"),
            "confidence_threshold": trae_ai.config.get("confidence_threshold"),
            "platforms": {
                "chatgpt": {
                    "base_url": trae_ai.config.get("chatgpt", {}).get("base_url"),
                    "model": trae_ai.config.get("chatgpt", {}).get("model"),
                    "configured": bool(trae_ai.config.get("chatgpt", {}).get("api_key"))
                },
                "gemini": {
                    "base_url": trae_ai.config.get("gemini", {}).get("base_url"),
                    "model": trae_ai.config.get("gemini", {}).get("model"),
                    "configured": bool(trae_ai.config.get("gemini", {}).get("api_key"))
                },
                "abacus": {
                    "base_url": trae_ai.config.get("abacus", {}).get("base_url"),
                    "app_id": trae_ai.config.get("abacus", {}).get("app_id"),
                    "configured": bool(trae_ai.config.get("abacus", {}).get("api_key"))
                }
            }
        }

        return JSONResponse(content={
            "ok": True,
            "config": safe_config,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting configuration: {str(e)}")

@router.post("/reload-config")
async def reload_configuration():
    """Reload TRAE.AI configuration"""
    try:
        global _trae_ai_instance
        _trae_ai_instance = None  # Force recreation with new config

        # Test the new configuration
        result = await test_simple_trae_ai_connection()

        return JSONResponse(content={
            "ok": True,
            "message": "Configuration reloaded successfully",
            "test_result": result,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reloading configuration: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for TRAE.AI integration"""
    try:
        trae_ai = get_trae_ai()

        # Quick system status check
        status = await trae_ai.get_system_status()

        # Check if any platforms are configured
        platforms_configured = sum([
            bool(trae_ai.config.get("chatgpt", {}).get("api_key")),
            bool(trae_ai.config.get("gemini", {}).get("api_key")),
            bool(trae_ai.config.get("abacus", {}).get("api_key"))
        ])

        health_status = "healthy" if platforms_configured > 0 else "warning"

        return JSONResponse(content={
            "status": health_status,
            "platforms_configured": platforms_configured,
            "total_platforms": 3,
            "system_status": status,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

# Webhook endpoints for TRAE.AI callbacks
@router.post("/webhook/task-completed")
async def webhook_task_completed(request: Dict[str, Any]):
    """Handle task completion webhooks from TRAE.AI"""
    try:
        task_id = request.get("task_id")
        status = request.get("status")
        result = request.get("result")

        # Log the webhook
        print(f"TRAE.AI Webhook - Task {task_id} completed with status: {status}")

        # Process the completed task
        if status == "completed":
            # Handle successful completion
            print(f"Task {task_id} completed successfully: {result}")
        elif status == "failed":
            # Handle failure
            error = request.get("error")
            print(f"Task {task_id} failed: {error}")

        return JSONResponse(content={
            "ok": True,
            "message": "Webhook received",
            "task_id": task_id,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")

@router.post("/webhook/task-progress")
async def webhook_task_progress(request: Dict[str, Any]):
    """Handle task progress webhooks from TRAE.AI"""
    try:
        task_id = request.get("task_id")
        progress = request.get("progress", {})

        # Log the progress update
        print(f"TRAE.AI Webhook - Task {task_id} progress: {progress}")

        return JSONResponse(content={
            "ok": True,
            "message": "Progress webhook received",
            "task_id": task_id,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing progress webhook: {str(e)}")

# Batch operations
@router.post("/batch/generate-content")
async def batch_generate_content(requests: List[ContentGenerationRequest], background_tasks: BackgroundTasks):
    """Generate multiple content pieces in batch"""
    try:
        trae_ai = get_trae_ai()
        results = []

        for i, request in enumerate(requests):
            task_id = f"batch_content_{int(time.time())}_{i}"

            try:
                result = await trae_ai.generate_content(
                    prompt=request.prompt,
                    content_type=request.content_type,
                    parameters=request.parameters,
                    cross_validate=request.cross_validate
                )

                results.append(TaskResponse(
                    task_id=task_id,
                    status="completed",
                    result=result,
                    created_at=datetime.now().isoformat()
                ))

            except Exception as e:
                results.append(TaskResponse(
                    task_id=task_id,
                    status="failed",
                    error=str(e),
                    created_at=datetime.now().isoformat()
                ))

        return JSONResponse(content={
            "ok": True,
            "batch_results": results,
            "total_tasks": len(requests),
            "completed_tasks": len([r for r in results if r.status == "completed"]),
            "failed_tasks": len([r for r in results if r.status == "failed"]),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in batch generation: {str(e)}")

# Analytics and metrics
@router.get("/analytics/usage")
async def get_usage_analytics():
    """Get usage analytics for TRAE.AI integration"""
    try:
        # This would typically come from a database or analytics service
        # For now, return mock data
        analytics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "platform_usage": {
                "chatgpt": 0,
                "gemini": 0,
                "abacus": 0
            },
            "content_types": {
                "video": 0,
                "text": 0,
                "audio": 0
            },
            "average_response_time_ms": 0,
            "last_24_hours": {
                "requests": 0,
                "success_rate": 0.0
            }
        }

        return JSONResponse(content={
            "ok": True,
            "analytics": analytics,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting analytics: {str(e)}")
