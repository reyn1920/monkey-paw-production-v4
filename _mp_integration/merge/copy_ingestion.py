#!/usr/bin/env python3
"""
Monkey Paw Integration - Copy-based Ingestion Script
Copies files from Downloads/Desktop/Google Drive into staging area
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class CopyIngestion:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.staging_dir = self.base_dir / "staging"
        self.imports_dir = self.base_dir / "imports"
        self.config_file = self.base_dir / "merge_config.json"
        
    def setup_directories(self):
        """Create necessary directories"""
        self.staging_dir.mkdir(exist_ok=True)
        self.imports_dir.mkdir(exist_ok=True)
        
    def load_config(self):
        """Load merge configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "downloads_path": "~/Downloads",
            "desktop_path": "~/Desktop/monkey paw",
            "drive_path": "~/Google Drive/online production",
            "file_patterns": ["*.py", "*.js", "*.ts", "*.json", "*.md"]
        }
    
    def copy_from_downloads(self, config):
        """Copy files from Downloads folder"""
        downloads_path = Path(config["downloads_path"]).expanduser()
        if downloads_path.exists():
            target_dir = self.staging_dir / "downloads"
            target_dir.mkdir(exist_ok=True)
            
            for pattern in config["file_patterns"]:
                for file_path in downloads_path.glob(pattern):
                    if file_path.is_file():
                        shutil.copy2(file_path, target_dir)
                        print(f"Copied: {file_path} -> {target_dir}")
    
    def copy_from_desktop(self, config):
        """Copy monkey paw files from Desktop"""
        desktop_path = Path(config["desktop_path"]).expanduser()
        if desktop_path.exists():
            target_dir = self.staging_dir / "desktop"
            target_dir.mkdir(exist_ok=True)
            
            # Copy entire monkey paw directory structure
            if desktop_path.is_dir():
                shutil.copytree(desktop_path, target_dir / "monkey_paw", dirs_exist_ok=True)
                print(f"Copied directory: {desktop_path} -> {target_dir}")
    
    def copy_from_drive(self, config):
        """Copy files from Google Drive online production"""
        drive_path = Path(config["drive_path"]).expanduser()
        if drive_path.exists():
            target_dir = self.staging_dir / "drive"
            target_dir.mkdir(exist_ok=True)
            
            # Copy online production folder
            if drive_path.is_dir():
                shutil.copytree(drive_path, target_dir / "online_production", dirs_exist_ok=True)
                print(f"Copied directory: {drive_path} -> {target_dir}")
    
    def create_manifest(self):
        """Create manifest of copied files"""
        manifest = {
            "timestamp": datetime.now().isoformat(),
            "copied_files": [],
            "directories": []
        }
        
        for root, dirs, files in os.walk(self.staging_dir):
            for file in files:
                file_path = Path(root) / file
                manifest["copied_files"].append(str(file_path.relative_to(self.staging_dir)))
            for dir in dirs:
                dir_path = Path(root) / dir
                manifest["directories"].append(str(dir_path.relative_to(self.staging_dir)))
        
        manifest_file = self.staging_dir / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"Created manifest: {manifest_file}")
        return manifest
    
    def run_ingestion(self):
        """Run the complete ingestion process"""
        print("Starting copy-based ingestion...")
        
        self.setup_directories()
        config = self.load_config()
        
        # Save config for user editing
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("Copying from Downloads...")
        self.copy_from_downloads(config)
        
        print("Copying from Desktop...")
        self.copy_from_desktop(config)
        
        print("Copying from Google Drive...")
        self.copy_from_drive(config)
        
        manifest = self.create_manifest()
        
        print(f"Ingestion complete! Copied {len(manifest['copied_files'])} files")
        print(f"Edit {self.config_file} to customize source paths")
        
        return manifest

if __name__ == "__main__":
    ingestion = CopyIngestion()
    ingestion.run_ingestion()