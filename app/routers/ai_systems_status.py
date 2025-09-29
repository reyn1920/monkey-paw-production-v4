#!/usr/bin/env python3
"""
AI Systems Status API Router
Provides real-time status updates for all 6 AI systems
"""

import os
import subprocess
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import psutil
import requests
from pathlib import Path

router = APIRouter(
    prefix="/api/ai-systems", 
    tags=["AI Systems Status"]
)


class AISystemsStatusService:
    """Service for monitoring all 6 AI systems in real-time"""
    
    def __init__(self):
        self.systems = {
            "cursor": {
                "name": "Cursor AI",
                "executable": "/Applications/Cursor.app/Contents/MacOS/Cursor",
                "capabilities": ["multi_file_editing", "ai_workflows"]
            },
            "bolt-diy": {
                "name": "Bolt.diy",
                "local_port": 5173,
                "capabilities": ["rapid_prototyping", "full_stack_dev"]
            },
            "firebase": {
                "name": "Google Firebase",
                "config_file": "firebase.json",
                "capabilities": ["backend_services", "cloud_functions"]
            },
            "trae-ai": {
                "name": "Trae.ai",
                "port": 8000,
                "health_endpoint": "http://localhost:8000/api/trae-ai/status",
                "capabilities": ["autonomous_development", "documentation"]
            },
            "vscode": {
                "name": "VS Code AI",
                "executable": (
                    "/Applications/Visual Studio Code.app/"
                    "Contents/MacOS/Electron"
                ),
                "capabilities": ["code_completion", "debugging"]
            },
            "windsurf": {
                "name": "Windsurf AI",
                "executable": (
                    "/Applications/Windsurf.app/Contents/MacOS/Windsurf"
                ),
                "capabilities": ["collaborative_flows", "project_management"]
            }
        }
        self.last_update = None
        self.cached_status = None
    
    def _check_process_running(self, executable_path: str) -> bool:
        """Check if a process is running by executable path"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    if (proc.info['exe'] and
                            executable_path in proc.info['exe']):
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return False
        except Exception:
            return False
    
    def _check_port_active(self, port: int) -> bool:
        """Check if a port is active"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def _check_cursor_status(self) -> Dict[str, Any]:
        """Check Cursor AI status"""
        status = {"status": "offline", "details": {}, "health": "error"}
        
        cursor_path = "/Applications/Cursor.app"
        if os.path.exists(cursor_path):
            status["details"]["installation"] = "present"
            status["status"] = "installed"
            status["health"] = "warning"
            
            cursor_exe = "/Applications/Cursor.app/Contents/MacOS/Cursor"
            if self._check_process_running(cursor_exe):
                status["status"] = "online"
                status["health"] = "healthy"
                status["details"]["process_running"] = True
            else:
                status["details"]["process_running"] = False
        
        return status
    
    def _check_bolt_diy_status(self) -> Dict[str, Any]:
        """Check Bolt.diy status"""
        status = {"status": "offline", "details": {}, "health": "error"}
        
        if os.path.exists("bolt_integration.py"):
            status["details"]["integration_file"] = "present"
            status["status"] = "configured"
            status["health"] = "warning"
        
        if self._check_port_active(5173):
            status["details"]["local_server"] = "running"
            status["status"] = "online"
            status["health"] = "healthy"
        else:
            status["details"]["local_server"] = "offline"
        
        return status
    
    def _check_firebase_status(self) -> Dict[str, Any]:
        """Check Firebase AI status"""
        status = {"status": "offline", "details": {}, "health": "error"}
        
        if os.path.exists("firebase.json"):
            status["details"]["config"] = "present"
            status["status"] = "configured"
            status["health"] = "warning"
        
        try:
            result = subprocess.run(
                ["firebase", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                status["details"]["cli_version"] = result.stdout.strip()
                status["status"] = "configured"
                status["health"] = "healthy"
        except Exception:
            status["details"]["cli_version"] = "not_installed"
        
        return status
    
    def _check_trae_ai_status(self) -> Dict[str, Any]:
        """Check Trae.ai status"""
        status = {"status": "offline", "details": {}, "health": "error"}
        
        if os.path.exists("trae_integration.py"):
            status["details"]["integration_file"] = "present"
            status["status"] = "configured"
            status["health"] = "warning"
        
        try:
            response = requests.get(
                "http://localhost:8000/api/trae-ai/status", 
                timeout=3
            )
            if response.status_code == 200:
                status["status"] = "online"
                status["health"] = "healthy"
                status["details"]["api_response"] = response.json()
            else:
                status["details"]["api_response"] = (
                    f"error_{response.status_code}"
                )
        except requests.RequestException:
            status["details"]["api_response"] = "unreachable"
        
        return status
    
    def _check_vscode_status(self) -> Dict[str, Any]:
        """Check VS Code AI status"""
        status = {"status": "offline", "details": {}, "health": "error"}
        
        vscode_path = "/Applications/Visual Studio Code.app"
        if os.path.exists(vscode_path):
            status["details"]["installation"] = "present"
            status["status"] = "installed"
            status["health"] = "warning"
            
            vscode_exe = (
                "/Applications/Visual Studio Code.app/"
                "Contents/MacOS/Electron"
            )
            if self._check_process_running(vscode_exe):
                status["status"] = "online"
                status["health"] = "healthy"
                status["details"]["process_running"] = True
            else:
                status["details"]["process_running"] = False
        
        vscode_settings = (
            Path.home() / 
            "Library/Application Support/Code/User/settings.json"
        )
        if vscode_settings.exists():
            status["details"]["settings"] = "configured"
        
        return status
    
    def _check_windsurf_status(self) -> Dict[str, Any]:
        """Check Windsurf AI status"""
        status = {"status": "offline", "details": {}, "health": "error"}
        
        windsurf_path = "/Applications/Windsurf.app"
        if os.path.exists(windsurf_path):
            status["details"]["installation"] = "present"
            status["status"] = "installed"
            status["health"] = "warning"
            
            windsurf_exe = (
                "/Applications/Windsurf.app/Contents/MacOS/Windsurf"
            )
            if self._check_process_running(windsurf_exe):
                status["status"] = "online"
                status["health"] = "healthy"
                status["details"]["process_running"] = True
            else:
                status["details"]["process_running"] = False
        
        if os.path.exists("src/services/AICollaborationService.ts"):
            status["details"]["collaboration_service"] = "present"
        
        return status
    
    async def get_all_systems_status(self) -> Dict[str, Any]:
        """Get real-time status of all AI systems"""
        timestamp = datetime.now().isoformat()
        
        systems_status = {
            "cursor": self._check_cursor_status(),
            "bolt-diy": self._check_bolt_diy_status(),
            "firebase": self._check_firebase_status(),
            "trae-ai": self._check_trae_ai_status(),
            "vscode": self._check_vscode_status(),
            "windsurf": self._check_windsurf_status(),
        }
        
        summary = {
            "total_systems": 6,
            "online": 0,
            "configured": 0,
            "installed": 0,
            "offline": 0,
            "healthy": 0,
            "warning": 0,
            "error": 0
        }
        
        for system_status in systems_status.values():
            status = system_status.get("status", "offline")
            health = system_status.get("health", "error")
            
            if status == "online":
                summary["online"] += 1
            elif status == "configured":
                summary["configured"] += 1
            elif status == "installed":
                summary["installed"] += 1
            else:
                summary["offline"] += 1
            
            if health == "healthy":
                summary["healthy"] += 1
            elif health == "warning":
                summary["warning"] += 1
            else:
                summary["error"] += 1
        
        result = {
            "timestamp": timestamp,
            "summary": summary,
            "systems": systems_status,
            "capabilities": {
                system_id: {
                    "name": system_info["name"],
                    "capabilities": system_info["capabilities"]
                }
                for system_id, system_info in self.systems.items()
            }
        }
        
        self.cached_status = result
        self.last_update = timestamp
        
        return result


# Initialize the service
ai_systems_service = AISystemsStatusService()


@router.get("/status")
async def get_ai_systems_status():
    """Get real-time status of all 6 AI systems"""
    try:
        status = await ai_systems_service.get_all_systems_status()
        return JSONResponse(content=status)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error getting AI systems status: {str(e)}"
        )


@router.get("/status/{system_id}")
async def get_system_status(system_id: str):
    """Get status of a specific AI system"""
    try:
        all_status = await ai_systems_service.get_all_systems_status()
        
        if system_id not in all_status["systems"]:
            raise HTTPException(
                status_code=404, 
                detail=f"System '{system_id}' not found"
            )
        
        system_status = all_status["systems"][system_id]
        system_status["timestamp"] = all_status["timestamp"]
        
        return JSONResponse(content=system_status)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error getting system status: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check for the AI systems status service"""
    try:
        status = await ai_systems_service.get_all_systems_status()
        
        return JSONResponse(content={
            "service_status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "systems_monitored": status["summary"]["total_systems"],
            "systems_online": status["summary"]["online"],
            "last_update": ai_systems_service.last_update
        })
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "service_status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@router.post("/refresh")
async def refresh_status():
    """Force refresh of all AI systems status"""
    try:
        status = await ai_systems_service.get_all_systems_status()
        return JSONResponse(content={
            "message": "Status refreshed successfully",
            "timestamp": status["timestamp"],
            "systems_checked": status["summary"]["total_systems"]
        })
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error refreshing status: {str(e)}"
        )