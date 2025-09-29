#!/usr/bin/env python3
"""
Monkey Paw Integration - Merge to Project Script
Merges staged files into current project under _mp_integration/
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime


class ProjectMerger:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.staging_dir = self.base_dir / "staging"
        self.project_root = self.base_dir.parent
        self.merge_target = self.base_dir
        
    def merge_staged_files(self):
        """Merge all staged files into project"""
        if not self.staging_dir.exists():
            print("No staging directory found. Run copy_ingestion.py first.")
            return
            
        print("Merging staged files into project...")
        
        # Copy downloads
        downloads_staged = self.staging_dir / "downloads"
        if downloads_staged.exists():
            target = self.merge_target / "imports" / "downloads"
            target.mkdir(parents=True, exist_ok=True)
            for file in downloads_staged.iterdir():
                if file.is_file():
                    shutil.copy2(file, target)
                    print(f"Merged: {file.name} -> imports/downloads/")
        
        # Copy desktop monkey paw
        desktop_staged = self.staging_dir / "desktop" / "monkey_paw"
        if desktop_staged.exists():
            target = self.merge_target / "imports" / "desktop"
            target.mkdir(parents=True, exist_ok=True)
            shutil.copytree(desktop_staged, target / "monkey_paw", dirs_exist_ok=True)
            print(f"Merged: desktop/monkey_paw -> imports/desktop/")
        
        # Copy drive online production
        drive_staged = self.staging_dir / "drive" / "online_production"
        if drive_staged.exists():
            target = self.merge_target / "imports" / "drive"
            target.mkdir(parents=True, exist_ok=True)
            shutil.copytree(drive_staged, target / "online_production", dirs_exist_ok=True)
            print(f"Merged: drive/online_production -> imports/drive/")
        
        print("Merge complete!")
        
    def create_vscode_tasks(self):
        """Create .vscode/tasks.json"""
        vscode_dir = self.project_root / ".vscode"
        vscode_dir.mkdir(exist_ok=True)
        
        tasks = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "MP Integration: Copy Ingestion",
                    "type": "shell",
                    "command": "python3",
                    "args": ["_mp_integration/merge/copy_ingestion.py"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "MP Integration: Merge to Project",
                    "type": "shell",
                    "command": "python3",
                    "args": ["_mp_integration/merge_to_project.py"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "MP Integration: Full Process",
                    "dependsOrder": "sequence",
                    "dependsOn": [
                        "MP Integration: Copy Ingestion",
                        "MP Integration: Merge to Project"
                    ]
                }
            ]
        }
        
        tasks_file = vscode_dir / "tasks.json"
        with open(tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)
        
        print(f"Created: {tasks_file}")
        
    def create_makefile(self):
        """Create Makefile"""
        makefile_content = """# Monkey Paw Integration Makefile

.PHONY: mp-copy mp-merge mp-full mp-clean

mp-copy:
	@echo "Running copy ingestion..."
	python3 _mp_integration/merge/copy_ingestion.py

mp-merge:
	@echo "Merging to project..."
	python3 _mp_integration/merge_to_project.py

mp-full: mp-copy mp-merge
	@echo "Full integration complete!"

mp-clean:
	@echo "Cleaning staging area..."
	rm -rf _mp_integration/staging/*
	@echo "Staging area cleaned."

mp-status:
	@echo "Integration Status:"
	@echo "Staging files:"
	@find _mp_integration/staging -type f 2>/dev/null | wc -l || echo "0"
	@echo "Imported files:"
	@find _mp_integration/imports -type f 2>/dev/null | wc -l || echo "0"
"""
        
        makefile_path = self.project_root / "Makefile.mp"
        with open(makefile_path, 'w') as f:
            f.write(makefile_content)
        
        print(f"Created: {makefile_path}")


if __name__ == "__main__":
    merger = ProjectMerger()
    merger.merge_staged_files()
    merger.create_vscode_tasks()
    merger.create_makefile()