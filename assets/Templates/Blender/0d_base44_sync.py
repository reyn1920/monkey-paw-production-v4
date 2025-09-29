#!/usr/bin/env python3
"""
Base44 Synchronization System
Automatically applies Base44 updates to online production environment
"""

import os
import sys
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("base44_sync.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class Base44Sync:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.base44_dir = self.base_dir / "trae_ai_base44"
        self.production_dir = self.base_dir
        self.config_file = self.base_dir / "base44_sync_config.json"
        self.last_sync_file = self.base_dir / ".last_base44_sync"

    def load_config(self) -> dict[str, Any]:
        """Load synchronization configuration"""
        default_config = {
            "sync_files": [
                "backend/app.py",
                "backend/requirements.txt",
                "frontend/index.html",
                "configs/env.local.example",
            ],
            "exclude_patterns": ["__pycache__", ".git", ".venv", "node_modules"],
            "auto_backup": True,
            "backup_dir": "backups/base44_sync",
        }

        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    config = json.load(f)
                    # Merge with defaults
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                logger.warning(f"Failed to load config: {e}. Using defaults.")

        # Save default config
        self.save_config(default_config)
        return default_config

    def save_config(self, config: dict[str, Any]):
        """Save synchronization configuration"""
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def get_last_sync_time(self) -> Optional[datetime]:
        """Get timestamp of last synchronization"""
        if self.last_sync_file.exists():
            try:
                with open(self.last_sync_file) as f:
                    timestamp = f.read().strip()
                    return datetime.fromisoformat(timestamp)
            except Exception as e:
                logger.warning(f"Failed to read last sync time: {e}")
        return None

    def update_last_sync_time(self):
        """Update last synchronization timestamp"""
        try:
            with open(self.last_sync_file, "w") as f:
                f.write(datetime.now().isoformat())
        except Exception as e:
            logger.error(f"Failed to update last sync time: {e}")

    def check_base44_updates(self) -> bool:
        """Check if Base44 has been updated since last sync"""
        if not self.base44_dir.exists():
            logger.error("Base44 directory not found")
            return False

        last_sync = self.get_last_sync_time()
        if not last_sync:
            logger.info("No previous sync found, assuming updates available")
            return True

        # Check modification times of key files
        for root, dirs, files in os.walk(self.base44_dir):
            # Skip excluded directories
            dirs[:] = [
                d
                for d in dirs
                if not any(pattern in d for pattern in [".git", "__pycache__", ".venv"])
            ]

            for file in files:
                file_path = Path(root) / file
                try:
                    mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mod_time > last_sync:
                        logger.info(f"Found updated file: {file_path}")
                        return True
                except Exception as e:
                    logger.warning(f"Failed to check {file_path}: {e}")

        return False

    def create_backup(self, config: dict[str, Any]) -> Optional[Path]:
        """Create backup of current production files"""
        if not config.get("auto_backup", True):
            return None

        backup_base = self.production_dir / config["backup_dir"]
        backup_dir = backup_base / datetime.now().strftime("%Y%m%d_%H%M%S")

        try:
            backup_dir.mkdir(parents=True, exist_ok=True)

            # Backup key files
            for file_pattern in config["sync_files"]:
                source_file = self.production_dir / file_pattern
                if source_file.exists():
                    dest_file = backup_dir / file_pattern
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, dest_file)
                    logger.info(f"Backed up: {source_file} -> {dest_file}")

            logger.info(f"Backup created: {backup_dir}")
            return backup_dir

        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None

    def sync_file(self, source: Path, dest: Path) -> bool:
        """Synchronize a single file"""
        try:
            # Ensure destination directory exists
            dest.parent.mkdir(parents=True, exist_ok=True)

            # Copy file with metadata
            shutil.copy2(source, dest)
            logger.info(f"Synced: {source} -> {dest}")
            return True

        except Exception as e:
            logger.error(f"Failed to sync {source} -> {dest}: {e}")
            return False

    def sync_base44_updates(self) -> bool:
        """Synchronize Base44 updates to production"""
        config = self.load_config()

        # Create backup
        backup_dir = self.create_backup(config)

        success_count = 0
        total_count = 0

        # Sync configured files
        for file_pattern in config["sync_files"]:
            source_file = self.base44_dir / file_pattern
            dest_file = self.production_dir / file_pattern

            if source_file.exists():
                total_count += 1
                if self.sync_file(source_file, dest_file):
                    success_count += 1
            else:
                logger.warning(f"Source file not found: {source_file}")

        # Update environment configuration
        self.update_env_config()

        # Update last sync time
        if success_count > 0:
            self.update_last_sync_time()
            logger.info(f"Sync completed: {success_count}/{total_count} files updated")
            return True
        else:
            logger.error("Sync failed: No files were updated")
            return False

    def update_env_config(self):
        """Update environment configuration with Base44 settings"""
        try:
            env_example = self.production_dir / ".env.example"
            if env_example.exists():
                with open(env_example) as f:
                    content = f.read()

                # Ensure Base44 configuration is present
                if "BASE44_ENABLED" not in content:
                    base44_config = """
# Base44 Integration Configuration
BASE44_ENABLED=true
BASE44_API_URL=http://127.0.0.1:7860
BASE44_SYNC_INTERVAL=300
BASE44_AUTO_UPDATE=true
BASE44_BACKUP_ENABLED=true
"""
                    content += base44_config

                    with open(env_example, "w") as f:
                        f.write(content)

                    logger.info("Updated .env.example with Base44 configuration")

        except Exception as e:
            logger.error(f"Failed to update environment config: {e}")

    def restart_services(self) -> bool:
        """Restart production services after sync"""
        try:
            # Check if services are running and restart them
            logger.info("Checking for running services...")

            # This would typically restart your production services
            # For now, we'll just log the action
            logger.info("Services restart would be triggered here")
            return True

        except Exception as e:
            logger.error(f"Failed to restart services: {e}")
            return False

    def run_sync(self, force: bool = False) -> bool:
        """Run the synchronization process"""
        logger.info("Starting Base44 synchronization...")

        if not self.base44_dir.exists():
            logger.error(f"Base44 directory not found: {self.base44_dir}")
            return False

        # Check for updates unless forced
        if not force and not self.check_base44_updates():
            logger.info("No Base44 updates found since last sync")
            return True

        # Perform synchronization
        if self.sync_base44_updates():
            logger.info("Base44 synchronization completed successfully")
            return True
        else:
            logger.error("Base44 synchronization failed")
            return False


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Base44 Synchronization System")
    parser.add_argument(
        "--force", action="store_true", help="Force sync even if no updates detected"
    )
    parser.add_argument(
        "--check-only", action="store_true", help="Only check for updates, don't sync"
    )
    parser.add_argument("--config", help="Path to configuration file")

    args = parser.parse_args()

    sync = Base44Sync()

    if args.config:
        sync.config_file = Path(args.config)

    if args.check_only:
        has_updates = sync.check_base44_updates()
        # DEBUG_REMOVED: print(f"Base44 updates available: {has_updates}")
        sys.exit(0 if has_updates else 1)

    success = sync.run_sync(force=args.force)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
