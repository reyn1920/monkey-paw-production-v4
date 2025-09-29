#!/usr/bin/env python3
"""
Monkey Paw Integration Backend API
ChatGPT ↔ Gemini Integration with Single-User Dashboard
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from typing import Dict, Any, Optional
import asyncio
import httpx

app = FastAPI(title="Monkey Paw Integration API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
CONFIG_FILE = "_mp_integration/config/integration_config.json"
DEFAULT_CONFIG = {
    "chatgpt_api_key": "",
    "gemini_api_key": "",
    "public_mode": False,
    "dashboard_enabled": True,
    "ai_diagnostics": True
}

class ChatRequest(BaseModel):
    message: str
    provider: str = "chatgpt"  # chatgpt or gemini
    
class ConfigUpdate(BaseModel):
    public_mode: Optional[bool] = None
    dashboard_enabled: Optional[bool] = None
    ai_diagnostics: Optional[bool] = None

def load_config() -> Dict[str, Any]:
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

@app.get("/api/status")
async def get_status():
    """Get system status"""
    config = load_config()
    return {
        "status": "online",
        "public_mode": config.get("public_mode", False),
        "dashboard_enabled": config.get("dashboard_enabled", True),
        "ai_diagnostics": config.get("ai_diagnostics", True),
        "providers": {
            "chatgpt": bool(config.get("chatgpt_api_key")),
            "gemini": bool(config.get("gemini_api_key"))
        }
    }

@app.post("/api/toggle")
async def toggle_mode(update: ConfigUpdate):
    """Toggle public/private mode and other settings"""
    config = load_config()
    
    if update.public_mode is not None:
        config["public_mode"] = update.public_mode
    if update.dashboard_enabled is not None:
        config["dashboard_enabled"] = update.dashboard_enabled
    if update.ai_diagnostics is not None:
        config["ai_diagnostics"] = update.ai_diagnostics
    
    save_config(config)
    return {"success": True, "config": config}

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Chat with AI providers"""
    config = load_config()
    
    if request.provider == "chatgpt":
        api_key = config.get("chatgpt_api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="ChatGPT API key not configured")
        
        # ChatGPT API call simulation
        response = await simulate_chatgpt_call(request.message, api_key)
        
    elif request.provider == "gemini":
        api_key = config.get("gemini_api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="Gemini API key not configured")
        
        # Gemini API call simulation
        response = await simulate_gemini_call(request.message, api_key)
        
    else:
        raise HTTPException(status_code=400, detail="Invalid provider")
    
    return {
        "provider": request.provider,
        "response": response,
        "timestamp": "2024-01-01T00:00:00Z"
    }

async def simulate_chatgpt_call(message: str, api_key: str) -> str:
    """Simulate ChatGPT API call"""
    # This would be replaced with actual OpenAI API call
    await asyncio.sleep(0.1)  # Simulate API delay
    return f"ChatGPT response to: {message}"

async def simulate_gemini_call(message: str, api_key: str) -> str:
    """Simulate Gemini API call"""
    # This would be replaced with actual Gemini API call
    await asyncio.sleep(0.1)  # Simulate API delay
    return f"Gemini response to: {message}"

@app.get("/api/diagnostics")
async def get_diagnostics():
    """Get AI system diagnostics"""
    config = load_config()
    
    if not config.get("ai_diagnostics", True):
        raise HTTPException(status_code=403, detail="Diagnostics disabled")
    
    return {
        "system_health": "good",
        "api_latency": {
            "chatgpt": "120ms",
            "gemini": "95ms"
        },
        "error_rate": "0.1%",
        "uptime": "99.9%"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)