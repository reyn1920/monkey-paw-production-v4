"""WebSocket router for real-time AI systems status updates."""

import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..websocket_manager import manager
from .ai_systems_status import get_ai_systems_status


router = APIRouter()


@router.websocket("/ws/ai-status")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time AI systems status updates."""
    await manager.connect(websocket)
    
    try:
        # Send initial status
        initial_status = await get_ai_systems_status()
        await manager.send_personal_message(
            json.dumps({
                "type": "ai_status_update",
                "data": initial_status,
                "timestamp": asyncio.get_event_loop().time()
            }),
            websocket
        )
        
        # Keep connection alive and send periodic updates
        while True:
            try:
                # Wait for client message or timeout
                await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            except asyncio.TimeoutError:
                # Send periodic status update
                current_status = await get_ai_systems_status()
                await manager.send_personal_message(
                    json.dumps({
                        "type": "ai_status_update", 
                        "data": current_status,
                        "timestamp": asyncio.get_event_loop().time()
                    }),
                    websocket
                )
            except WebSocketDisconnect:
                break
                
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)


@router.post("/api/broadcast-status")
async def broadcast_status():
    """Manually trigger a status broadcast to all connected clients."""
    current_status = await get_ai_systems_status()
    await manager.broadcast_ai_status(current_status)
    return {
        "message": "Status broadcast sent", 
        "connections": len(manager.active_connections)
    }