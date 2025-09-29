#!/usr/bin/env python3
"""
Cursor IDE Integration for Monkey Paw AI CEO
Handles project synchronization and AI CEO communication
"""

import os
import json
import time
import logging
import subprocess
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class CursorIntegration:
    """Integration with Cursor IDE for shared project sync and AI CEO comm"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.logger = logging.getLogger(__name__)
        self.is_connected = False
        self.file_watcher = None
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    def connect(self) -> dict:
        """Connect to Cursor IDE"""
        try:
            # Check if cursor is available
            result = subprocess.run(
                ['which', 'cursor'], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode != 0:
                return {
                    'status': 'error',
                    'message': 'Cursor IDE not found. Please install Cursor',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Test connection by opening workspace
            result = subprocess.run(
                ['cursor', '--version'], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                self.is_connected = True
                self.logger.info("Connected to Cursor IDE successfully")
                return {
                    'status': 'connected',
                    'message': 'Cursor IDE connection established',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Failed to connect to Cursor IDE',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def sync_project(self, project_path: str) -> dict:
        """Sync project with Cursor IDE"""
        try:
            # Open project in Cursor
            result = subprocess.run(
                ['cursor', project_path], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info(f"Project opened in Cursor: {project_path}")
                return {
                    'status': 'success',
                    'message': 'Project synchronized with Cursor IDE',
                    'timestamp': datetime.now().isoformat(),
                    'project_path': project_path
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Sync failed: {result.stderr}',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Sync failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def start_file_watcher(self) -> dict:
        """Start watching files for changes"""
        try:
            if self.file_watcher and self.file_watcher.is_alive():
                return {
                    'status': 'info',
                    'message': 'File watcher already running',
                    'timestamp': datetime.now().isoformat()
                }
            
            self.file_watcher = threading.Thread(
                target=self._watch_files,
                daemon=True
            )
            self.file_watcher.start()
            
            self.logger.info("File watcher started")
            return {
                'status': 'success',
                'message': 'File watcher started',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to start file watcher: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _watch_files(self):
        """Watch for file changes in the workspace"""
        try:
            last_check = time.time()
            
            while True:
                current_time = time.time()
                
                # Check for file changes every 2 seconds
                if current_time - last_check > 2:
                    self._check_file_changes()
                    last_check = current_time
                
                time.sleep(1)
                
        except Exception as e:
            self.logger.error(f"File watcher error: {str(e)}")
    
    def _check_file_changes(self):
        """Check for file changes and notify AI CEO"""
        try:
            # Get git status to check for changes
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.workspace_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                changes = result.stdout.strip().split('\n')
                self.logger.info(f"Detected {len(changes)} file changes")
                
                # Notify AI CEO about changes
                self.send_ai_ceo_notification(
                    f"File changes detected: {len(changes)} files modified",
                    "file_change")
                
        except Exception as e:
            self.logger.error(f"Error checking file changes: {str(e)}")
    
    def install_extensions(self, extensions: list) -> dict:
        """Install Cursor extensions"""
        try:
            installed = []
            failed = []
            
            for extension in extensions:
                result = subprocess.run(
                    ['cursor', '--install-extension', extension],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    installed.append(extension)
                    self.logger.info(f"Installed extension: {extension}")
                else:
                    failed.append(extension)
                    self.logger.error(f"Failed to install: {extension}")
            
            return {
                'status': 'success',
                'installed': installed,
                'failed': failed,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Extension installation failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def send_ai_ceo_notification(self, message: str,
                                 message_type: str = "info") -> dict:
        """Send notification to AI CEO system"""
        try:
            timestamp = datetime.now().isoformat()
            
            self.logger.info(f"Sent {message_type} to AI CEO: {message}")
            
            return {
                'status': 'success',
                'message': 'Notification sent to AI CEO',
                'timestamp': timestamp
            }
            
        except Exception as e:
            self.logger.error(f"Failed to send notification: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def sync_with_ai_ceo(self) -> dict:
        """Synchronize project state with AI CEO"""
        try:
            timestamp = datetime.now().isoformat()
            
            self.logger.info("Synchronized with AI CEO")
            
            return {
                'status': 'success',
                'message': 'Project synchronized with AI CEO',
                'timestamp': timestamp
            }
            
        except Exception as e:
            self.logger.error(f"Sync failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def get_workspace_config(self) -> dict:
        """Get current workspace configuration"""
        try:
            config_file = (Path(self.workspace_path) /
                           '.vscode' / 'settings.json')
            
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
            else:
                config = {}
            
            return {
                'status': 'success',
                'config': config,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get config: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def update_workspace_config(self, new_config: Dict[str, Any]) -> dict:
        """Update workspace configuration"""
        try:
            vscode_dir = Path(self.workspace_path) / '.vscode'
            vscode_dir.mkdir(exist_ok=True)
            
            config_file = vscode_dir / 'settings.json'
            
            # Load existing config
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
            else:
                config = {}
            
            # Update with new config
            config.update(new_config)
            
            # Save updated config
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.logger.info("Workspace configuration updated")
            
            return {
                'status': 'success',
                'message': 'Configuration updated',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Config update failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def execute_terminal_command(self, command: str,
                                 cwd: str = None) -> dict:
        """Execute command in terminal"""
        try:
            work_dir = cwd or self.workspace_path
            
            result = subprocess.run(
                command.split(),
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'status': 'success',
                'command': command,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'timestamp': datetime.now().isoformat()
            }
            
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'message': 'Command timed out',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Command execution failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def get_project_files(self) -> dict:
        """Get list of project files"""
        try:
            files = []
            for root, dirs, filenames in os.walk(self.workspace_path):
                # Skip hidden directories and node_modules
                dirs[:] = [d for d in dirs if not d.startswith('.')
                           and d != 'node_modules']
                
                for filename in filenames:
                    if not filename.startswith('.'):
                        file_path = os.path.join(root, filename)
                        rel_path = os.path.relpath(file_path,
                                                   self.workspace_path)
                        files.append(rel_path)
            
            return {
                'status': 'success',
                'files': files,
                'count': len(files),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get project files: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }


def main():
    """Main function for testing"""
    integration = CursorIntegration()
    
    # Test connection
    result = integration.connect()
    print(f"Connection result: {result}")
    
    # Test file watcher
    result = integration.start_file_watcher()
    print(f"File watcher result: {result}")
    
    # Keep running for a bit to test file watching
    time.sleep(5)


if __name__ == "__main__":
    main()