#!/usr/bin/env python3
"""
Sublime AI Integration for Monkey Paw Production v4
Handles Build 4200, automation reports, project configs, and Package Control
"""

import os
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path


class SublimeIntegration:
    """Integration with Sublime Text for AI-enhanced development"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.logger = logging.getLogger(__name__)
        self.is_connected = False
        self.sublime_path = self._find_sublime_path()
        self.packages_path = None
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    def _find_sublime_path(self) -> str:
        """Find Sublime Text installation path"""
        possible_paths = [
            "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl",
            "/usr/local/bin/subl",
            "/opt/sublime_text/sublime_text"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def connect(self) -> dict:
        """Connect to Sublime Text"""
        try:
            if not self.sublime_path:
                return {
                    'status': 'error',
                    'message': 'Sublime Text not found. Please install Sublime Text',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Test Sublime Text connection
            result = subprocess.run(
                [self.sublime_path, '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.is_connected = True
                
                # Find packages path
                if "Darwin" in os.uname().sysname:  # macOS
                    self.packages_path = Path.home() / "Library" / "Application Support" / "Sublime Text" / "Packages"
                else:  # Linux/Windows
                    self.packages_path = Path.home() / ".config" / "sublime-text" / "Packages"
                
                self.logger.info("Connected to Sublime Text successfully")
                
                return {
                    'status': 'success',
                    'message': 'Connected to Sublime Text',
                    'version': result.stdout.strip(),
                    'packages_path': str(self.packages_path),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Failed to connect to Sublime Text',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Sublime connection failed: {str(e)}")
            return {
                'status': 'error',
                'message': f'Connection failed: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def setup_package_control(self) -> dict:
        """Setup Package Control and AI packages"""
        try:
            if not self.packages_path:
                return {
                    'status': 'error',
                    'message': 'Packages path not found',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Create User package directory
            user_dir = self.packages_path / "User"
            user_dir.mkdir(parents=True, exist_ok=True)
            
            # Package Control settings
            pc_settings = {
                "bootstrapped": True,
                "in_process_packages": [],
                "installed_packages": [
                    "Package Control",
                    "LSP",
                    "LSP-pyright",
                    "LSP-typescript",
                    "SublimeLinter",
                    "SublimeLinter-eslint",
                    "SublimeLinter-flake8",
                    "GitGutter",
                    "BracketHighlighter",
                    "AutoFileName",
                    "Emmet",
                    "SideBarEnhancements",
                    "Terminal",
                    "ColorPicker",
                    "DocBlockr",
                    "Markdown Preview",
                    "Pretty JSON",
                    "Python Improved",
                    "JavaScript Completions",
                    "TypeScript",
                    "React ES6 Snippets"
                ]
            }
            
            with open(user_dir / "Package Control.sublime-settings", 'w') as f:
                json.dump(pc_settings, f, indent=2)
            
            # AI-enhanced preferences
            preferences = {
                "theme": "Adaptive.sublime-theme",
                "color_scheme": "Monokai.sublime-color-scheme",
                "font_size": 12,
                "tab_size": 4,
                "translate_tabs_to_spaces": True,
                "trim_trailing_white_space_on_save": True,
                "ensure_newline_at_eof_on_save": True,
                "auto_complete": True,
                "auto_complete_delay": 50,
                "auto_complete_selector": "source, text",
                "auto_complete_triggers": [
                    {"selector": "source.python", "characters": "."},
                    {"selector": "source.js", "characters": "."},
                    {"selector": "source.ts", "characters": "."}
                ],
                "word_wrap": True,
                "rulers": [79, 120],
                "show_line_endings": True,
                "show_encoding": True,
                "highlight_line": True,
                "caret_style": "phase",
                "wide_caret": True,
                "caret_extra_width": 1,
                "bold_folder_labels": True,
                "highlight_modified_tabs": True,
                "show_tab_close_buttons": True,
                "preview_on_click": False,
                "tree_animation_enabled": False,
                "animation_enabled": False,
                "gpu_window_buffer": True,
                "hardware_acceleration": "opengl"
            }
            
            with open(user_dir / "Preferences.sublime-settings", 'w') as f:
                json.dump(preferences, f, indent=2)
            
            self.logger.info("Package Control and AI packages configured")
            
            return {
                'status': 'success',
                'message': 'Package Control configured with AI packages',
                'packages': len(pc_settings['installed_packages']),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Package Control setup failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def create_project_config(self) -> dict:
        """Create Sublime Text project configuration"""
        try:
            project_name = Path(self.workspace_path).name
            project_file = Path(self.workspace_path) / f"{project_name}.sublime-project"
            
            # Project configuration
            project_config = {
                "folders": [
                    {
                        "path": ".",
                        "folder_exclude_patterns": [
                            ".git",
                            "__pycache__",
                            "node_modules",
                            ".pytest_cache",
                            ".coverage",
                            "dist",
                            "build",
                            ".venv",
                            "venv"
                        ],
                        "file_exclude_patterns": [
                            "*.pyc",
                            "*.pyo",
                            "*.exe",
                            "*.dll",
                            "*.obj",
                            "*.o",
                            "*.a",
                            "*.lib",
                            "*.so",
                            "*.dylib",
                            "*.ncb",
                            "*.sdf",
                            "*.suo",
                            "*.pdb",
                            "*.idb",
                            ".DS_Store",
                            "*.class",
                            "*.psd",
                            "*.db",
                            "*.sublime-workspace"
                        ]
                    }
                ],
                "settings": {
                    "tab_size": 4,
                    "translate_tabs_to_spaces": True,
                    "rulers": [79, 120],
                    "word_wrap": True,
                    "wrap_width": 79,
                    "auto_complete": True,
                    "auto_complete_delay": 50,
                    "show_definitions": True,
                    "show_line_endings": True,
                    "trim_trailing_white_space_on_save": True,
                    "ensure_newline_at_eof_on_save": True
                },
                "build_systems": [
                    {
                        "name": "Python - Current File",
                        "cmd": ["python", "-u", "$file"],
                        "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
                        "selector": "source.python"
                    },
                    {
                        "name": "Node.js - Current File",
                        "cmd": ["node", "$file"],
                        "selector": "source.js"
                    },
                    {
                        "name": "FastAPI Server",
                        "cmd": ["python", "-m", "uvicorn", "main:app", "--reload"],
                        "working_dir": "$project_path",
                        "variants": [
                            {
                                "name": "FastAPI - Production",
                                "cmd": ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
                            }
                        ]
                    },
                    {
                        "name": "React Development",
                        "cmd": ["npm", "start"],
                        "working_dir": "$project_path",
                        "variants": [
                            {
                                "name": "React - Build",
                                "cmd": ["npm", "run", "build"]
                            },
                            {
                                "name": "React - Test",
                                "cmd": ["npm", "test"]
                            }
                        ]
                    }
                ]
            }
            
            with open(project_file, 'w') as f:
                json.dump(project_config, f, indent=2)
            
            self.logger.info(f"Project configuration created: {project_file}")
            
            return {
                'status': 'success',
                'message': 'Project configuration created',
                'project_file': str(project_file),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Project config creation failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def setup_automation_reports(self) -> dict:
        """Setup automation reporting system"""
        try:
            reports_dir = Path(self.workspace_path) / "reports" / "sublime"
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            # Create report generator script
            report_generator_path = reports_dir / "report_generator.py"
            with open(report_generator_path, 'w') as f:
                f.write("""#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

class SublimeReportGenerator:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.reports = {}
        
    def generate_productivity_report(self):
        report = {
            'timestamp': datetime.now().isoformat(),
            'project_path': str(self.project_path),
            'metrics': {}
        }
        
        file_stats = self._get_file_statistics()
        report['metrics']['files'] = file_stats
        
        git_stats = self._get_git_statistics()
        if git_stats:
            report['metrics']['git'] = git_stats
        
        quality_stats = self._get_code_quality()
        report['metrics']['quality'] = quality_stats
        
        return report
    
    def _get_file_statistics(self):
        stats = {
            'total_files': 0,
            'python_files': 0,
            'javascript_files': 0,
            'json_files': 0,
            'markdown_files': 0,
            'total_lines': 0
        }
        
        for file_path in self.project_path.rglob('*'):
            if file_path.is_file() and not self._should_ignore_file(file_path):
                stats['total_files'] += 1
                
                suffix = file_path.suffix.lower()
                if suffix == '.py':
                    stats['python_files'] += 1
                elif suffix in ['.js', '.jsx', '.ts', '.tsx']:
                    stats['javascript_files'] += 1
                elif suffix == '.json':
                    stats['json_files'] += 1
                elif suffix in ['.md', '.markdown']:
                    stats['markdown_files'] += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        stats['total_lines'] += len(f.readlines())
                except:
                    pass
        
        return stats
    
    def _get_git_statistics(self):
        try:
            result = subprocess.run(['git', 'status'], 
                                  cwd=self.project_path,
                                  capture_output=True, text=True)
            if result.returncode != 0:
                return None
            
            stats = {}
            
            result = subprocess.run(['git', 'rev-list', '--count', 'HEAD'],
                                  cwd=self.project_path,
                                  capture_output=True, text=True)
            if result.returncode == 0:
                stats['total_commits'] = int(result.stdout.strip())
            
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            result = subprocess.run(['git', 'rev-list', '--count', 
                                   f'--since={week_ago}', 'HEAD'],
                                  cwd=self.project_path,
                                  capture_output=True, text=True)
            if result.returncode == 0:
                stats['commits_last_week'] = int(result.stdout.strip())
            
            result = subprocess.run(['git', 'shortlog', '-sn'],
                                  cwd=self.project_path,
                                  capture_output=True, text=True)
            if result.returncode == 0:
                contributors = len(result.stdout.strip().split('\\n'))
                stats['contributors'] = contributors
            
            return stats
            
        except Exception:
            return None
    
    def _get_code_quality(self):
        quality = {
            'linting_errors': 0,
            'test_coverage': 0,
            'documentation_ratio': 0
        }
        
        python_files = list(self.project_path.rglob('*.py'))
        if python_files:
            documented_functions = 0
            total_functions = 0
            
            for py_file in python_files:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    lines = content.split('\\n')
                    for line in lines:
                        if line.strip().startswith('def '):
                            total_functions += 1
                            line_idx = lines.index(line)
                            for i in range(line_idx + 1, min(line_idx + 5, len(lines))):
                                if '\"\"\"' in lines[i] or \"'''\" in lines[i]:
                                    documented_functions += 1
                                    break
                except:
                    pass
            
            if total_functions > 0:
                quality['documentation_ratio'] = documented_functions / total_functions
        
        return quality
    
    def _should_ignore_file(self, file_path: Path):
        ignore_patterns = [
            '.git', '__pycache__', 'node_modules', '.pytest_cache',
            '.coverage', 'dist', 'build', '.venv', 'venv'
        ]
        
        return any(pattern in str(file_path) for pattern in ignore_patterns)
    
    def save_report(self, report: dict, filename: str = None):
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"productivity_report_{timestamp}.json"
        
        report_path = self.project_path / "reports" / "sublime" / filename
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return str(report_path)

if __name__ == "__main__":
    import sys
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    generator = SublimeReportGenerator(project_path)
    report = generator.generate_productivity_report()
    
    report_file = generator.save_report(report)
    print(f"Report saved to: {report_file}")
    
    print("\\nProductivity Summary:")
    print(f"Total Files: {report['metrics']['files']['total_files']}")
    print(f"Total Lines: {report['metrics']['files']['total_lines']}")
    
    if 'git' in report['metrics']:
        print(f"Total Commits: {report['metrics']['git'].get('total_commits', 0)}")
        print(f"Commits Last Week: {report['metrics']['git'].get('commits_last_week', 0)}")
""")
            
            # Report configuration
            report_config = {
                "enabled": True,
                "schedule": "daily",
                "metrics": [
                    "file_statistics",
                    "git_statistics",
                    "code_quality",
                    "productivity_trends"
                ],
                "output_format": "json",
                "retention_days": 30
            }
            
            with open(reports_dir / "config.json", 'w') as f:
                json.dump(report_config, f, indent=2)
            
            self.logger.info("Automation reporting system configured")
            
            return {
                'status': 'success',
                'message': 'Automation reporting system configured',
                'components': ['report_generator.py', 'config.json'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Automation reports setup failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_status(self) -> dict:
        """Get Sublime integration status"""
        return {
            'status': 'online' if self.is_connected else 'offline',
            'connected': self.is_connected,
            'sublime_path': self.sublime_path,
            'packages_path': str(self.packages_path) if self.packages_path else None,
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Main function for testing Sublime integration"""
    sublime = SublimeIntegration()
    
    print("📝 Sublime AI Integration Test")
    print("=" * 50)
    
    # Test connection
    result = sublime.connect()
    print(f"Connection: {result['status']}")
    
    if result['status'] == 'success':
        # Setup Package Control
        pc_result = sublime.setup_package_control()
        print(f"Package Control: {pc_result['status']}")
        
        # Create project config
        project_result = sublime.create_project_config()
        print(f"Project Config: {project_result['status']}")
        
        # Setup automation reports
        reports_result = sublime.setup_automation_reports()
        print(f"Automation Reports: {reports_result['status']}")
        
        # Get status
        status = sublime.get_status()
        print(f"Final Status: {status['status']}")


if __name__ == "__main__":
    main()