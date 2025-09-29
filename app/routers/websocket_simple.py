"""Simplified WebSocket router for real-time AI systems status updates."""

import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any


router = APIRouter()


# Simple connection manager without database dependencies
class SimpleConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        if not self.active_connections:
            return
        
        message_str = json.dumps(message)
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_str)
            except Exception:
                disconnected.append(connection)
        
        for connection in disconnected:
            self.disconnect(connection)


manager = SimpleConnectionManager()


# Mock AI systems status without database
def get_mock_ai_status():
    return {
        "timestamp": asyncio.get_event_loop().time(),
        "systems": {
            "cursor": {"status": "online", "health": "healthy"},
            "bolt-diy": {"status": "online", "health": "healthy"},
            "firebase": {"status": "online", "health": "healthy"},
            "trae-ai": {"status": "online", "health": "healthy"},
            "vscode": {"status": "configured", "health": "healthy"},
            "windsurf": {"status": "configured", "health": "healthy"}
        }
    }


@router.websocket("/ws/ai-status")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time AI systems status updates."""
    await manager.connect(websocket)
    
    try:
        # Send initial status
        initial_status = get_mock_ai_status()
        await websocket.send_text(json.dumps({
            "type": "ai_status_update",
            "data": initial_status
        }))
        
        # Keep connection alive
        while True:
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            except asyncio.TimeoutError:
                # Send periodic update
                current_status = get_mock_ai_status()
                await websocket.send_text(json.dumps({
                    "type": "ai_status_update", 
                    "data": current_status
                }))
            except WebSocketDisconnect:
                break
                
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)


@router.post("/api/broadcast-status")
async def broadcast_status():
    """Manually trigger a status broadcast."""
    current_status = get_mock_ai_status()
    await manager.broadcast({
        "type": "ai_status_update",
        "data": current_status
    })
    return {
        "message": "Status broadcast sent", 
        "connections": len(manager.active_connections)
    }