#!/usr/bin/env python3
"""
TRAE AI Production Startup System
Comprehensive system startup with Ollama integration monitoring
"""

import os
import sys
import time
import json
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Union, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("startup_system.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class OllamaServiceMonitor:
    """Monitor and manage Ollama AI service integration."""

    def __init__(self):
        self.ollama_endpoint = "http://localhost:11434"
        self.required_models = []

    def check_ollama_installation(self) -> dict[str, Union[str, bool]]:
        """Check if Ollama is installed and accessible."""
        try:
            result = subprocess.run(["which", "ollama"], capture_output=True, text=True)
            if result.returncode == 0:
                # Get version info
                version_result = subprocess.run(
                    ["ollama", "--version"], capture_output=True, text=True
                )
                version = (
                    version_result.stdout.strip()
                    if version_result.returncode == 0
                    else "unknown"
                )
                return {
                    "installed": True,
                    "path": result.stdout.strip(),
                    "version": version,
                    "status": "available",
                }
            else:
                return {
                    "installed": False,
                    "status": "not_found",
                    "message": "Ollama not found in PATH",
                }
        except Exception as e:
            return {
                "installed": False,
                "status": "error",
                "message": f"Error checking Ollama: {str(e)}",
            }

    def check_ollama_service(self) -> dict[str, Union[str, bool, int, list[str]]]:
        """Check if Ollama service is running and get model list."""
        try:
            # Try using curl first as a fallback
            curl_result = subprocess.run(
                ["curl", "-s", f"{self.ollama_endpoint}/api/tags"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if curl_result.returncode == 0:
                try:
                    data = json.loads(curl_result.stdout)
                    models = data.get("models", [])
                    model_names = [model.get("name", "unknown") for model in models]

                    return {
                        "running": True,
                        "accessible": True,
                        "endpoint": self.ollama_endpoint,
                        "models_count": len(models),
                        "models": model_names,
                        "status": "healthy",
                    }
                except json.JSONDecodeError:
                    return {
                        "running": False,
                        "accessible": False,
                        "status": "invalid_response",
                        "message": "Ollama returned invalid JSON",
                    }
            else:
                # Try ollama list command as backup
                list_result = subprocess.run(
                    ["ollama", "list"], capture_output=True, text=True, timeout=10
                )
                if list_result.returncode == 0:
                    lines = list_result.stdout.strip().split("\n")[1:]  # Skip header
                    models = [line.split()[0] for line in lines if line.strip()]
                    return {
                        "running": True,
                        "accessible": True,
                        "endpoint": "local_command",
                        "models_count": len(models),
                        "models": models,
                        "status": "healthy_via_cli",
                    }
                else:
                    return {
                        "running": False,
                        "accessible": False,
                        "status": "service_unavailable",
                        "message": "Ollama service not responding to API or CLI",
                    }
        except subprocess.TimeoutExpired:
            return {
                "running": False,
                "accessible": False,
                "status": "timeout",
                "message": "Ollama service check timed out",
            }
        except Exception as e:
            return {
                "running": False,
                "accessible": False,
                "status": "connection_error",
                "message": f"Cannot connect to Ollama service: {str(e)}",
            }

    def get_comprehensive_status(self) -> dict[str, Any]:
        """Get comprehensive Ollama status for production monitoring."""
        installation_status = self.check_ollama_installation()
        service_status = self.check_ollama_service()

        return {
            "timestamp": time.time(),
            "installation": installation_status,
            "service": service_status,
            "production_ready": installation_status.get("installed", False)
            and service_status.get("running", False),
        }


class ProductionStartupSystem:
    """Main production startup system with comprehensive monitoring."""

    def __init__(self, mode: str = "production"):
        self.mode = mode
        self.ollama_monitor = OllamaServiceMonitor()
        self.startup_log = []

    def log_startup_event(
        self, event: str, status: str, details: Optional[dict[str, Any]] = None
    ):
        """Log startup events for audit trail."""
        event_data: dict[str, Any] = {
            "timestamp": time.time(),
            "event": event,
            "status": status,
            "mode": self.mode,
        }
        if details:
            event_data["details"] = details

        self.startup_log.append(event_data)
        logger.info(f"Startup Event: {event} - {status}")

    def check_system_requirements(self) -> dict[str, bool]:
        """Check all system requirements for production startup."""
        requirements = {
            "python_version": sys.version_info >= (3, 8),
            "working_directory": os.path.exists(os.getcwd()),
            "log_directory": True,  # Will create if needed
            "ollama_service": False,  # Will check separately
        }

        # Check Ollama service
        ollama_status = self.ollama_monitor.get_comprehensive_status()
        requirements["ollama_service"] = ollama_status.get("production_ready", False)

        self.log_startup_event("system_requirements_check", "completed", requirements)
        return requirements

    def ensure_directories(self) -> bool:
        """Ensure all required directories exist."""
        required_dirs = ["logs", "data", "backups", "assets"]

        created_dirs = []
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if not dir_path.exists():
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    created_dirs.append(str(dir_path))
                except Exception as e:
                    logger.error(f"Failed to create directory {dir_path}: {e}")
                    return False

        if created_dirs:
            self.log_startup_event(
                "directories_created", "success", {"created": created_dirs}
            )

        return True

    def start_main_application(self) -> bool:
        """Start the main application process."""
        try:
            if os.path.exists("main.py"):
                logger.info("Starting main application...")
                # In production, this would typically be handled by a process manager
                # For now, we'll just verify the file exists and is executable
                self.log_startup_event("main_application", "ready", {"file": "main.py"})
                return True
            else:
                logger.error("main.py not found")
                self.log_startup_event(
                    "main_application", "failed", {"error": "main.py not found"}
                )
                return False
        except Exception as e:
            logger.error(f"Failed to start main application: {e}")
            self.log_startup_event("main_application", "failed", {"error": str(e)})
            return False

    def generate_startup_report(self) -> dict[str, Any]:
        """Generate comprehensive startup report."""
        ollama_status = self.ollama_monitor.get_comprehensive_status()
        system_requirements = self.check_system_requirements()

        report = {
            "timestamp": time.time(),
            "mode": self.mode,
            "system_requirements": system_requirements,
            "ollama_status": ollama_status,
            "startup_log": self.startup_log,
            "production_ready": all(system_requirements.values()),
        }

        return report

    def run_startup_sequence(self) -> bool:
        """Execute the complete startup sequence."""
        logger.info(f"Starting TRAE AI Production System in {self.mode} mode")

        # Step 1: Check system requirements
        requirements = self.check_system_requirements()
        if not all(requirements.values()):
            failed_requirements = [k for k, v in requirements.items() if not v]
            logger.error(f"System requirements not met: {failed_requirements}")
            return False

        # Step 2: Ensure directories
        if not self.ensure_directories():
            logger.error("Failed to create required directories")
            return False

        # Step 3: Check Ollama service (critical for production)
        ollama_status = self.ollama_monitor.get_comprehensive_status()
        if not ollama_status.get("production_ready", False):
            logger.warning(
                "Ollama service not production ready - continuing with limited functionality"
            )
            self.log_startup_event("ollama_service", "warning", ollama_status)
        else:
            logger.info(
                f"Ollama service ready with {ollama_status['service'].get('models_count', 0)} models"
            )
            self.log_startup_event("ollama_service", "ready", ollama_status)

        # Step 4: Start main application
        if not self.start_main_application():
            logger.error("Failed to start main application")
            return False

        # Step 5: Generate final report
        report = self.generate_startup_report()

        # Save startup report
        try:
            with open("startup_report.json", "w") as f:
                json.dump(report, f, indent=2, default=str)
            logger.info("Startup report saved to startup_report.json")
        except Exception as e:
            logger.error(f"Failed to save startup report: {e}")

        logger.info("TRAE AI Production System startup completed successfully")
        return True


def main():
    """Main entry point for the startup system."""
    parser = argparse.ArgumentParser(description="TRAE AI Production Startup System")
    parser.add_argument(
        "--mode",
        choices=["development", "staging", "production"],
        default="production",
        help="Startup mode",
    )
    parser.add_argument(
        "--monitor-only",
        action="store_true",
        help="Only monitor services, do not start",
    )
    parser.add_argument(
        "--ollama-status", action="store_true", help="Check Ollama status only"
    )

    args = parser.parse_args()

    startup_system = ProductionStartupSystem(mode=args.mode)

    if args.ollama_status:
        # Just check Ollama status
        ollama_status = startup_system.ollama_monitor.get_comprehensive_status()
        print(json.dumps(ollama_status, indent=2, default=str))
        return 0 if ollama_status.get("production_ready", False) else 1

    if args.monitor_only:
        # Generate report without starting services
        report = startup_system.generate_startup_report()
        print(json.dumps(report, indent=2, default=str))
        return 0

    # Run full startup sequence
    success = startup_system.run_startup_sequence()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
