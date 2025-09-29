#!/usr/bin/env python3
"""
AI Systems Tracker - Monitor All 6 AI Code Systems
Tracks and manages: Trae.ai, Cursor AI, Bolt.diy, Firebase AI, VS Code AI, Windsurf AI
"""

import os
import json
import time
import logging
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_systems_tracker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AISystemsTracker:
    """Comprehensive tracker for all 6 AI code systems"""
    
    def __init__(self):
        self.systems = {
            "trae_ai": {
                "name": "Trae.ai",
                "status": "unknown",
                "process": None,
                "port": 8000,
                "health_endpoint": "http://localhost:8000/api/trae-ai/status",
                "config_file": "config/trae_ai_config.json",
                "integration_file": "trae_integration.py",
                "last_check": None,
                "capabilities": ["autonomous_development", "documentation", "solo_mode"]
            },
            "cursor_ai": {
                "name": "Cursor AI",
                "status": "unknown", 
                "process": None,
                "executable": "/Applications/Cursor.app/Contents/MacOS/Cursor",
                "workspace": "monkey-paw.code-workspace",
                "integration_file": "cursor_integration.py",
                "last_check": None,
                "capabilities": ["multi_file_editing", "codebase_understanding", "ai_workflows"]
            },
            "bolt_diy": {
                "name": "Bolt.diy",
                "status": "unknown",
                "process": None,
                "url": "https://bolt.diy",
                "local_port": 5173,
                "integration_file": "bolt_integration.py",
                "last_check": None,
                "capabilities": ["rapid_prototyping", "full_stack_dev", "zero_setup"]
            },
            "firebase_ai": {
                "name": "Firebase AI",
                "status": "unknown",
                "process": None,
                "project_id": "monkey-paw-production-v4",
                "config_file": "firebase.json",
                "integration_file": "firebase_integration.py",
                "last_check": None,
                "capabilities": ["backend_services", "cloud_functions", "ai_deployment"]
            },
            "vscode_ai": {
                "name": "VS Code AI (GitHub Copilot)",
                "status": "unknown",
                "process": None,
                "executable": "/Applications/Visual Studio Code.app/Contents/MacOS/Electron",
                "extensions": ["github.copilot", "continue.continue"],
                "last_check": None,
                "capabilities": ["code_completion", "debugging", "intellisense"]
            },
            "windsurf_ai": {
                "name": "Windsurf AI",
                "status": "unknown",
                "process": None,
                "executable": "/Applications/Windsurf.app/Contents/MacOS/Windsurf",
                "integration_service": "src/services/AICollaborationService.ts",
                "last_check": None,
                "capabilities": ["collaborative_flows", "project_management", "cascade_system"]
            }
        }
        
        self.tracking_active = False
        self.check_interval = 30  # seconds
        
    def check_system_status(self, system_id: str) -> Dict[str, Any]:
        """Check the status of a specific AI system"""
        system = self.systems.get(system_id)
        if not system:
            return {"error": f"Unknown system: {system_id}"}
            
        status_info = {
            "system_id": system_id,
            "name": system["name"],
            "timestamp": datetime.now().isoformat(),
            "status": "offline",
            "details": {}
        }
        
        try:
            # Check if process is running
            if "executable" in system:
                status_info["details"]["process_running"] = self._check_process_running(system["executable"])
            
            # Check specific endpoints/files
            if system_id == "trae_ai":
                status_info.update(self._check_trae_ai())
            elif system_id == "cursor_ai":
                status_info.update(self._check_cursor_ai())
            elif system_id == "bolt_diy":
                status_info.update(self._check_bolt_diy())
            elif system_id == "firebase_ai":
                status_info.update(self._check_firebase_ai())
            elif system_id == "vscode_ai":
                status_info.update(self._check_vscode_ai())
            elif system_id == "windsurf_ai":
                status_info.update(self._check_windsurf_ai())
                
            system["last_check"] = datetime.now().isoformat()
            system["status"] = status_info["status"]
            
        except Exception as e:
            logger.error(f"Error checking {system_id}: {e}")
            status_info["error"] = str(e)
            
        return status_info
    
    def _check_process_running(self, executable_path: str) -> bool:
        """Check if a process is running by executable path"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                if proc.info['exe'] and executable_path in proc.info['exe']:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        return False
    
    def _check_trae_ai(self) -> Dict[str, Any]:
        """Check Trae.ai specific status"""
        result = {"status": "offline", "details": {}}
        
        # Check if integration file exists
        if os.path.exists("trae_integration.py"):
            result["details"]["integration_file"] = "present"
        
        # Check if config exists
        if os.path.exists("config/trae_ai_config.json"):
            result["details"]["config_file"] = "present"
            
        # Check if API is responding
        try:
            response = requests.get("http://localhost:8000/api/trae-ai/status", timeout=5)
            if response.status_code == 200:
                result["status"] = "online"
                result["details"]["api_response"] = response.json()
        except requests.RequestException:
            result["details"]["api_response"] = "unreachable"
            
        return result
    
    def _check_cursor_ai(self) -> Dict[str, Any]:
        """Check Cursor AI specific status"""
        result = {"status": "offline", "details": {}}
        
        # Check if Cursor is installed
        cursor_path = "/Applications/Cursor.app"
        if os.path.exists(cursor_path):
            result["details"]["installation"] = "present"
            result["status"] = "installed"
            
        # Check if workspace file exists
        if os.path.exists("monkey-paw.code-workspace"):
            result["details"]["workspace"] = "configured"
            
        # Check if integration file exists
        if os.path.exists("cursor_integration.py"):
            result["details"]["integration"] = "present"
            
        return result
    
    def _check_bolt_diy(self) -> Dict[str, Any]:
        """Check Bolt.diy specific status"""
        result = {"status": "offline", "details": {}}
        
        # Check integration file
        if os.path.exists("bolt_integration.py"):
            result["details"]["integration_file"] = "present"
            result["status"] = "configured"
            
        # Check if local dev server might be running
        try:
            response = requests.get("http://localhost:5173", timeout=3)
            result["details"]["local_server"] = "running"
            result["status"] = "online"
        except requests.RequestException:
            result["details"]["local_server"] = "offline"
            
        return result
    
    def _check_firebase_ai(self) -> Dict[str, Any]:
        """Check Firebase AI specific status"""
        result = {"status": "offline", "details": {}}
        
        # Check Firebase config
        if os.path.exists("firebase.json"):
            result["details"]["config"] = "present"
            
        if os.path.exists(".firebaserc"):
            result["details"]["project_config"] = "present"
            
        # Check Firebase CLI
        try:
            firebase_result = subprocess.run(
                ["firebase", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if firebase_result.returncode == 0:
                result["details"]["cli_version"] = firebase_result.stdout.strip()
                result["status"] = "configured"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            result["details"]["cli"] = "not_installed"
            
        return result
    
    def _check_vscode_ai(self) -> Dict[str, Any]:
        """Check VS Code AI specific status"""
        result = {"status": "offline", "details": {}}
        
        # Check if VS Code is installed
        vscode_path = "/Applications/Visual Studio Code.app"
        if os.path.exists(vscode_path):
            result["details"]["installation"] = "present"
            result["status"] = "installed"
            
        # Check for AI extensions config
        vscode_settings = Path.home() / "Library/Application Support/Code/User/settings.json"
        if vscode_settings.exists():
            result["details"]["settings"] = "configured"
            
        return result
    
    def _check_windsurf_ai(self) -> Dict[str, Any]:
        """Check Windsurf AI specific status"""
        result = {"status": "offline", "details": {}}
        
        # Check if Windsurf is installed
        windsurf_path = "/Applications/Windsurf.app"
        if os.path.exists(windsurf_path):
            result["details"]["installation"] = "present"
            result["status"] = "installed"
            
        # Check integration service
        if os.path.exists("src/services/AICollaborationService.ts"):
            result["details"]["collaboration_service"] = "present"
            
        return result
    
    def check_all_systems(self) -> Dict[str, Any]:
        """Check status of all AI systems"""
        logger.info("🔍 Checking all AI systems...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_systems": len(self.systems),
            "systems": {},
            "summary": {
                "online": 0,
                "configured": 0,
                "installed": 0,
                "offline": 0
            }
        }
        
        for system_id in self.systems.keys():
            system_status = self.check_system_status(system_id)
            results["systems"][system_id] = system_status
            
            # Update summary
            status = system_status.get("status", "offline")
            if status == "online":
                results["summary"]["online"] += 1
            elif status == "configured":
                results["summary"]["configured"] += 1
            elif status == "installed":
                results["summary"]["installed"] += 1
            else:
                results["summary"]["offline"] += 1
                
        return results
    
    def start_continuous_tracking(self):
        """Start continuous monitoring of all AI systems"""
        logger.info("🚀 Starting continuous AI systems tracking...")
        self.tracking_active = True
        
        while self.tracking_active:
            try:
                results = self.check_all_systems()
                
                # Log summary
                summary = results["summary"]
                logger.info(f"📊 AI Systems Status: {summary['online']} online, "
                          f"{summary['configured']} configured, {summary['installed']} installed, "
                          f"{summary['offline']} offline")
                
                # Save results to file
                with open("ai_systems_status.json", "w") as f:
                    json.dump(results, f, indent=2)
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("🛑 Stopping AI systems tracking...")
                self.tracking_active = False
                break
            except Exception as e:
                logger.error(f"❌ Error in tracking loop: {e}")
                time.sleep(5)
    
    def get_system_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all AI systems"""
        capabilities = {}
        for system_id, system in self.systems.items():
            capabilities[system_id] = {
                "name": system["name"],
                "capabilities": system["capabilities"],
                "status": system["status"]
            }
        return capabilities
    
    def generate_status_report(self) -> str:
        """Generate a comprehensive status report"""
        results = self.check_all_systems()
        
        report = f"""
🤖 AI SYSTEMS STATUS REPORT
Generated: {results['timestamp']}

📊 SUMMARY
Total Systems: {results['total_systems']}
Online: {results['summary']['online']}
Configured: {results['summary']['configured']}
Installed: {results['summary']['installed']}
Offline: {results['summary']['offline']}

🔍 DETAILED STATUS
"""
        
        for system_id, status in results['systems'].items():
            report += f"\n{status['name']} ({system_id}): {status['status'].upper()}"
            if 'details' in status:
                for key, value in status['details'].items():
                    report += f"\n  - {key}: {value}"
        
        report += f"\n\n💡 CAPABILITIES OVERVIEW"
        capabilities = self.get_system_capabilities()
        for system_id, info in capabilities.items():
            report += f"\n{info['name']}: {', '.join(info['capabilities'])}"
            
        return report

def main():
    """Main function to run the AI systems tracker"""
    tracker = AISystemsTracker()
    
    print("🤖 AI Systems Tracker - Monitoring 6 AI Code Systems")
    print("=" * 60)
    
    # Generate initial report
    report = tracker.generate_status_report()
    print(report)
    
    # Save report to file
    with open("ai_systems_report.txt", "w") as f:
        f.write(report)
    
    print("\n📄 Report saved to: ai_systems_report.txt")
    print("📊 Status data saved to: ai_systems_status.json")
    
    # Ask if user wants continuous monitoring
    try:
        response = input("\n🔄 Start continuous monitoring? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            tracker.start_continuous_tracking()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()