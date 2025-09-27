#!/usr/bin/env python3
"""
TRAE AI Disaster Recovery System
Unified interface for all disaster recovery operations.
"""

import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(
            f"disaster_recovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        ),
        logging.StreamHandler(),
    ],
)


class DisasterRecoverySystem:
    """Unified disaster recovery system for TRAE AI projects."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.project_root = Path(__file__).parent.parent
        self.scripts_dir = self.project_root / "scripts"

    def print_header(self, title: str):
        """Print a formatted header."""
        print("\n" + "=" * 60)
        print(f"🚨 {title}")
        print("=" * 60)

    def print_success(self, message: str):
        """Print success message."""
        print(f"✅ {message}")

    def print_error(self, message: str):
        """Print error message."""
        print(f"❌ {message}")

    def print_warning(self, message: str):
        """Print warning message."""
        print(f"⚠️  {message}")

    def print_info(self, message: str):
        """Print info message."""
        print(f"ℹ️  {message}")

    def run_command(
        self, command: List[str], cwd: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Run a command and return the result."""
        try:
            self.logger.info(f"Running command: {' '.join(command)}")
            result = subprocess.run(
                command,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                check=False,
            )

            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except Exception as e:
            self.logger.error(f"Command failed: {e}")
            return {"success": False, "returncode": -1, "stdout": "", "stderr": str(e)}

    def check_system_health(self) -> bool:
        """Run comprehensive system health check."""
        self.print_header("SYSTEM HEALTH CHECK")

        # Use Phoenix Protocol for health check
        phoenix_script = self.scripts_dir / "phoenix_protocol.sh"
        if phoenix_script.exists():
            self.print_info("Running Phoenix Protocol health check...")
            result = self.run_command(["bash", str(phoenix_script), "health"])

            if result["success"]:
                self.print_success("System health check passed")
                return True
            else:
                self.print_error("System health check failed")
                print(result["stderr"])
                return False
        else:
            self.print_error("Phoenix Protocol not found")
            return False

    def git_time_machine_recovery(self, target_file: str) -> bool:
        """Recover a specific file using Git Time Machine."""
        self.print_header("GIT TIME MACHINE RECOVERY")

        reconstruct_script = self.scripts_dir / "reconstruct.py"
        if not reconstruct_script.exists():
            self.print_error("Git Time Machine (reconstruct.py) not found")
            return False

        self.print_info(f"Attempting to recover: {target_file}")
        result = self.run_command(["python3", str(reconstruct_script), target_file])

        if result["success"]:
            self.print_success(f"Successfully recovered {target_file}")
            return True
        else:
            self.print_error(f"Failed to recover {target_file}")
            print(result["stderr"])
            return False

    def production_rollback(self) -> bool:
        """Perform production rollback."""
        self.print_header("PRODUCTION ROLLBACK")

        rollback_script = self.scripts_dir / "rollback-production.sh"
        if not rollback_script.exists():
            self.print_error("Production rollback script not found")
            return False

        self.print_warning("This will initiate a production rollback!")
        self.print_info("Running production rollback script...")

        # Run interactively to allow user input
        try:
            subprocess.run(["bash", str(rollback_script)], cwd=self.project_root)
            return True
        except Exception as e:
            self.print_error(f"Rollback failed: {e}")
            return False

    def system_backup(self) -> bool:
        """Create system backup."""
        self.print_header("SYSTEM BACKUP")

        phoenix_script = self.scripts_dir / "phoenix_protocol.sh"
        if phoenix_script.exists():
            self.print_info("Creating system backup...")
            result = self.run_command(["bash", str(phoenix_script), "backup"])

            if result["success"]:
                self.print_success("System backup completed")
                return True
            else:
                self.print_error("System backup failed")
                print(result["stderr"])
                return False
        else:
            self.print_error("Phoenix Protocol not found")
            return False

    def security_scan(self) -> bool:
        """Run security scan."""
        self.print_header("SECURITY SCAN")

        phoenix_script = self.scripts_dir / "phoenix_protocol.sh"
        if phoenix_script.exists():
            self.print_info("Running security scan...")
            result = self.run_command(["bash", str(phoenix_script), "security-scan"])

            if result["success"]:
                self.print_success("Security scan completed")
                return True
            else:
                self.print_error("Security scan failed")
                print(result["stderr"])
                return False
        else:
            self.print_error("Phoenix Protocol not found")
            return False

    def full_system_recovery(self) -> bool:
        """Perform full system recovery."""
        self.print_header("FULL SYSTEM RECOVERY")

        recovery_steps = [
            ("System Health Check", self.check_system_health),
            ("System Backup", self.system_backup),
            ("Security Scan", self.security_scan),
        ]

        for step_name, step_func in recovery_steps:
            self.print_info(f"Executing: {step_name}")
            if not step_func():
                self.print_error(f"Recovery step failed: {step_name}")
                return False

        self.print_success("Full system recovery completed successfully")
        return True

    def show_recovery_options(self):
        """Show available recovery options."""
        self.print_header("DISASTER RECOVERY OPTIONS")

        options = [
            "1. System Health Check - Check overall system health",
            "2. Git Time Machine - Recover specific files from Git history",
            "3. Production Rollback - Rollback production deployment",
            "4. System Backup - Create comprehensive system backup",
            "5. Security Scan - Run security vulnerability scan",
            "6. Full System Recovery - Complete recovery process",
            "7. Exit",
        ]

        for option in options:
            print(f"   {option}")

        print("\nEnter your choice (1-7): ", end="")

    def interactive_recovery(self):
        """Interactive disaster recovery menu."""
        while True:
            self.show_recovery_options()

            try:
                choice = input().strip()

                if choice == "1":
                    self.check_system_health()
                elif choice == "2":
                    target_file = input("Enter file path to recover: ").strip()
                    if target_file:
                        self.git_time_machine_recovery(target_file)
                    else:
                        self.print_error("No file path provided")
                elif choice == "3":
                    self.production_rollback()
                elif choice == "4":
                    self.system_backup()
                elif choice == "5":
                    self.security_scan()
                elif choice == "6":
                    self.full_system_recovery()
                elif choice == "7":
                    self.print_info("Exiting disaster recovery system")
                    break
                else:
                    self.print_error("Invalid choice. Please select 1-7.")

            except KeyboardInterrupt:
                self.print_info("\nExiting disaster recovery system")
                break
            except Exception as e:
                self.print_error(f"An error occurred: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="TRAE AI Disaster Recovery System")
    parser.add_argument("--health", action="store_true", help="Run system health check")
    parser.add_argument(
        "--recover", type=str, help="Recover specific file using Git Time Machine"
    )
    parser.add_argument(
        "--rollback", action="store_true", help="Perform production rollback"
    )
    parser.add_argument("--backup", action="store_true", help="Create system backup")
    parser.add_argument("--security", action="store_true", help="Run security scan")
    parser.add_argument(
        "--full-recovery", action="store_true", help="Perform full system recovery"
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Interactive recovery mode"
    )

    args = parser.parse_args()

    recovery_system = DisasterRecoverySystem()

    # If no arguments provided, start interactive mode
    if len(sys.argv) == 1:
        recovery_system.interactive_recovery()
        return

    # Handle specific commands
    if args.health:
        recovery_system.check_system_health()
    elif args.recover:
        recovery_system.git_time_machine_recovery(args.recover)
    elif args.rollback:
        recovery_system.production_rollback()
    elif args.backup:
        recovery_system.system_backup()
    elif args.security:
        recovery_system.security_scan()
    elif args.full_recovery:
        recovery_system.full_system_recovery()
    elif args.interactive:
        recovery_system.interactive_recovery()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
