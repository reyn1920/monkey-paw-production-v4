#!/usr/bin/env python3
"""
VS Code AI Integration for Monkey Paw Production v4
Handles Debug Agent System with LangGraph, extensions, and IntelliSense
"""

import os
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path


class VSCodeAIIntegration:
    """Integration with VS Code for AI-enhanced development"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.logger = logging.getLogger(__name__)
        self.is_connected = False
        self.vscode_path = self._find_vscode_path()
        self.extensions_path = None
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('vscode_ai_integration.log'),
                logging.StreamHandler()
            ]
        )
        
    def _find_vscode_path(self) -> str:
        """Find VS Code installation path"""
        possible_paths = [
            "/Applications/Visual Studio Code.app/Contents/Resources/"
            "app/bin/code",
            "/usr/local/bin/code",
            "/usr/bin/code",
            "/opt/visual-studio-code/bin/code"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Try to find code in PATH
        try:
            result = subprocess.run(['which', 'code'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None
    
    def connect(self) -> dict:
        """Connect to VS Code"""
        try:
            if not self.vscode_path:
                return {
                    'status': 'error',
                    'message': 'VS Code not found. Please install VS Code',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Test VS Code connection
            result = subprocess.run(
                [self.vscode_path, '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.is_connected = True
                
                # Find extensions path
                if "Darwin" in os.uname().sysname:  # macOS
                    self.extensions_path = Path.home() / ".vscode" / "extensions"
                else:  # Linux/Windows
                    self.extensions_path = Path.home() / ".vscode" / "extensions"
                
                self.logger.info("Connected to VS Code successfully")
                
                return {
                    'status': 'success',
                    'message': 'Connected to VS Code',
                    'version': result.stdout.strip(),
                    'extensions_path': str(self.extensions_path),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Failed to connect to VS Code',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"VS Code connection failed: {str(e)}")
            return {
                'status': 'error',
                'message': f'Connection failed: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def install_ai_extensions(self) -> dict:
        """Install AI-enhanced extensions"""
        try:
            if not self.vscode_path:
                return {
                    'status': 'error',
                    'message': 'VS Code not found',
                    'timestamp': datetime.now().isoformat()
                }
            
            # AI Extensions to install
            extensions = [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-python.debugpy",
                "ms-vscode.vscode-typescript-next",
                "bradlc.vscode-tailwindcss",
                "esbenp.prettier-vscode",
                "ms-vscode.vscode-eslint",
                "ms-vscode.vscode-json",
                "redhat.vscode-yaml",
                "ms-vscode.vscode-markdown",
                "ms-vscode.vscode-git",
                "ms-vscode.vscode-github",
                "ms-vscode.vscode-docker",
                "ms-vscode.vscode-remote-containers",
                "ms-vscode.vscode-remote-ssh",
                "ms-vscode.vscode-live-server",
                "ms-vscode.vscode-intellicode",
                "ms-vscode.vscode-copilot",
                "continue.continue",
                "tabnine.tabnine-vscode",
                "github.copilot",
                "github.copilot-chat",
                "ms-toolsai.jupyter",
                "ms-toolsai.vscode-jupyter-cell-tags",
                "ms-toolsai.vscode-jupyter-slideshow",
                "ms-dotnettools.vscode-dotnet-runtime",
                "ms-vscode.vscode-node-debug2",
                "ms-vscode.vscode-chrome-debug",
                "ms-vscode.vscode-firefox-debug"
            ]
            
            installed = []
            failed = []
            
            for extension in extensions:
                try:
                    result = subprocess.run(
                        [self.vscode_path, '--install-extension', extension],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        installed.append(extension)
                        self.logger.info(f"Installed extension: {extension}")
                    else:
                        failed.append(extension)
                        self.logger.warning(f"Failed to install: {extension}")
                        
                except Exception as e:
                    failed.append(extension)
                    self.logger.error(f"Error installing {extension}: {str(e)}")
            
            return {
                'status': 'success' if installed else 'error',
                'message': f'Installed {len(installed)} extensions',
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
    
    def setup_debug_agent_system(self) -> dict:
        """Setup Debug Agent System with LangGraph"""
        try:
            debug_dir = Path(self.workspace_path) / "debug_agents"
            debug_dir.mkdir(parents=True, exist_ok=True)
            
            # Debug Agent System with LangGraph
            debug_agent_code = '''#!/usr/bin/env python3
"""
Debug Agent System with LangGraph Integration
AI-powered debugging and code analysis
"""

import json
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class DebugContext:
    """Debug context information"""
    file_path: str
    line_number: int
    error_type: str
    error_message: str
    stack_trace: List[str]
    variables: Dict[str, Any]
    timestamp: str


class LangGraphDebugAgent:
    """LangGraph-powered debug agent"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.logger = logging.getLogger(__name__)
        self.debug_sessions = {}
        self.analysis_cache = {}
        
    async def analyze_error(self, context: DebugContext) -> Dict[str, Any]:
        """Analyze error using LangGraph reasoning"""
        try:
            analysis = {
                'error_id': f"err_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'context': context,
                'analysis': {
                    'error_category': self._categorize_error(context.error_type),
                    'severity': self._assess_severity(context.error_message),
                    'potential_causes': self._identify_causes(context),
                    'suggested_fixes': self._generate_fixes(context),
                    'related_files': self._find_related_files(context.file_path),
                    'test_suggestions': self._suggest_tests(context)
                },
                'timestamp': datetime.now().isoformat()
            }
            
            # Cache analysis for future reference
            self.analysis_cache[analysis['error_id']] = analysis
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analysis failed: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _categorize_error(self, error_type: str) -> str:
        """Categorize error type"""
        categories = {
            'SyntaxError': 'syntax',
            'NameError': 'variable',
            'TypeError': 'type',
            'ValueError': 'value',
            'AttributeError': 'attribute',
            'ImportError': 'import',
            'ModuleNotFoundError': 'module',
            'FileNotFoundError': 'file',
            'KeyError': 'dictionary',
            'IndexError': 'list',
            'ZeroDivisionError': 'arithmetic',
            'RuntimeError': 'runtime'
        }
        
        return categories.get(error_type, 'unknown')
    
    def _assess_severity(self, error_message: str) -> str:
        """Assess error severity"""
        critical_keywords = ['fatal', 'critical', 'crash', 'abort']
        high_keywords = ['error', 'exception', 'failed']
        medium_keywords = ['warning', 'deprecated']
        
        message_lower = error_message.lower()
        
        if any(keyword in message_lower for keyword in critical_keywords):
            return 'critical'
        elif any(keyword in message_lower for keyword in high_keywords):
            return 'high'
        elif any(keyword in message_lower for keyword in medium_keywords):
            return 'medium'
        else:
            return 'low'
    
    def _identify_causes(self, context: DebugContext) -> List[str]:
        """Identify potential causes"""
        causes = []
        
        # Common cause patterns
        if 'NameError' in context.error_type:
            causes.extend([
                'Variable not defined before use',
                'Typo in variable name',
                'Variable out of scope',
                'Missing import statement'
            ])
        elif 'TypeError' in context.error_type:
            causes.extend([
                'Incorrect argument types',
                'Missing required arguments',
                'Calling non-callable object',
                'Type mismatch in operation'
            ])
        elif 'ImportError' in context.error_type:
            causes.extend([
                'Module not installed',
                'Incorrect module path',
                'Circular import dependency',
                'Missing __init__.py file'
            ])
        
        return causes
    
    def _generate_fixes(self, context: DebugContext) -> List[str]:
        """Generate suggested fixes"""
        fixes = []
        
        # Fix suggestions based on error type
        if 'NameError' in context.error_type:
            fixes.extend([
                'Check variable spelling and case',
                'Ensure variable is defined before use',
                'Add missing import statements',
                'Check variable scope and indentation'
            ])
        elif 'TypeError' in context.error_type:
            fixes.extend([
                'Verify function arguments and types',
                'Add type checking or conversion',
                'Check method availability on object',
                'Review function signature'
            ])
        elif 'ImportError' in context.error_type:
            fixes.extend([
                'Install missing package with pip',
                'Check module path and spelling',
                'Resolve circular import dependencies',
                'Add __init__.py to package directories'
            ])
        
        return fixes
    
    def _find_related_files(self, file_path: str) -> List[str]:
        """Find files related to the error"""
        related = []
        current_file = Path(file_path)
        
        if current_file.exists():
            # Find files in same directory
            for file in current_file.parent.glob('*.py'):
                if file != current_file:
                    related.append(str(file))
            
            # Find test files
            test_patterns = [
                f"test_{current_file.stem}.py",
                f"{current_file.stem}_test.py",
                f"tests/test_{current_file.stem}.py"
            ]
            
            for pattern in test_patterns:
                test_file = current_file.parent / pattern
                if test_file.exists():
                    related.append(str(test_file))
        
        return related[:10]  # Limit to 10 files
    
    def _suggest_tests(self, context: DebugContext) -> List[str]:
        """Suggest tests to prevent similar errors"""
        suggestions = []
        
        if 'NameError' in context.error_type:
            suggestions.extend([
                'Add unit tests for variable initialization',
                'Test function with various input types',
                'Add integration tests for module imports'
            ])
        elif 'TypeError' in context.error_type:
            suggestions.extend([
                'Add type checking tests',
                'Test function with edge cases',
                'Add parameter validation tests'
            ])
        
        return suggestions
    
    async def start_debug_session(self, session_id: str) -> Dict[str, Any]:
        """Start a new debug session"""
        session = {
            'id': session_id,
            'start_time': datetime.now().isoformat(),
            'status': 'active',
            'breakpoints': [],
            'variables': {},
            'call_stack': [],
            'analysis_history': []
        }
        
        self.debug_sessions[session_id] = session
        
        return {
            'status': 'success',
            'session': session,
            'timestamp': datetime.now().isoformat()
        }
    
    async def add_breakpoint(self, session_id: str, file_path: str, 
                           line_number: int) -> Dict[str, Any]:
        """Add breakpoint to debug session"""
        if session_id not in self.debug_sessions:
            return {
                'status': 'error',
                'message': 'Debug session not found',
                'timestamp': datetime.now().isoformat()
            }
        
        breakpoint = {
            'file_path': file_path,
            'line_number': line_number,
            'condition': None,
            'hit_count': 0,
            'enabled': True,
            'timestamp': datetime.now().isoformat()
        }
        
        self.debug_sessions[session_id]['breakpoints'].append(breakpoint)
        
        return {
            'status': 'success',
            'breakpoint': breakpoint,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get debug session status"""
        if session_id not in self.debug_sessions:
            return {
                'status': 'error',
                'message': 'Debug session not found',
                'timestamp': datetime.now().isoformat()
            }
        
        session = self.debug_sessions[session_id]
        
        return {
            'status': 'success',
            'session': session,
            'active_breakpoints': len([bp for bp in session['breakpoints'] 
                                     if bp['enabled']]),
            'timestamp': datetime.now().isoformat()
        }


class VSCodeDebugIntegration:
    """Integration with VS Code debugging"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.debug_agent = LangGraphDebugAgent(workspace_path)
        self.logger = logging.getLogger(__name__)
    
    def setup_launch_configuration(self) -> Dict[str, Any]:
        """Setup VS Code launch configuration"""
        try:
            vscode_dir = self.workspace_path / ".vscode"
            vscode_dir.mkdir(exist_ok=True)
            
            launch_config = {
                "version": "0.2.0",
                "configurations": [
                    {
                        "name": "Python: Current File",
                        "type": "python",
                        "request": "launch",
                        "program": "${file}",
                        "console": "integratedTerminal",
                        "justMyCode": False,
                        "env": {
                            "PYTHONPATH": "${workspaceFolder}"
                        }
                    },
                    {
                        "name": "Python: FastAPI",
                        "type": "python",
                        "request": "launch",
                        "module": "uvicorn",
                        "args": ["main:app", "--reload", "--host", "0.0.0.0"],
                        "console": "integratedTerminal",
                        "justMyCode": False
                    },
                    {
                        "name": "Node.js: Current File",
                        "type": "node",
                        "request": "launch",
                        "program": "${file}",
                        "console": "integratedTerminal"
                    },
                    {
                        "name": "Debug Agent System",
                        "type": "python",
                        "request": "launch",
                        "program": "${workspaceFolder}/debug_agents/debug_agent.py",
                        "console": "integratedTerminal",
                        "args": ["--session", "debug_session_1"]
                    }
                ]
            }
            
            launch_file = vscode_dir / "launch.json"
            with open(launch_file, 'w') as f:
                json.dump(launch_config, f, indent=2)
            
            return {
                'status': 'success',
                'message': 'Launch configuration created',
                'file': str(launch_file),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Launch config setup failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def handle_debug_event(self, event_type: str, 
                                data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle debug events from VS Code"""
        try:
            if event_type == 'breakpoint_hit':
                context = DebugContext(
                    file_path=data.get('file_path', ''),
                    line_number=data.get('line_number', 0),
                    error_type=data.get('error_type', ''),
                    error_message=data.get('error_message', ''),
                    stack_trace=data.get('stack_trace', []),
                    variables=data.get('variables', {}),
                    timestamp=datetime.now().isoformat()
                )
                
                analysis = await self.debug_agent.analyze_error(context)
                
                return {
                    'status': 'success',
                    'event_type': event_type,
                    'analysis': analysis,
                    'timestamp': datetime.now().isoformat()
                }
            
            return {
                'status': 'success',
                'event_type': event_type,
                'message': 'Event processed',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Debug event handling failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }


async def main():
    """Main function for testing debug agent system"""
    workspace_path = "."
    debug_integration = VSCodeDebugIntegration(workspace_path)
    
    print("🐛 VS Code Debug Agent System Test")
    print("=" * 50)
    
    # Setup launch configuration
    launch_result = debug_integration.setup_launch_configuration()
    print(f"Launch Config: {launch_result['status']}")
    
    # Test debug agent
    debug_agent = debug_integration.debug_agent
    
    # Start debug session
    session_result = await debug_agent.start_debug_session("test_session")
    print(f"Debug Session: {session_result['status']}")
    
    # Test error analysis
    test_context = DebugContext(
        file_path="test.py",
        line_number=42,
        error_type="NameError",
        error_message="name 'undefined_var' is not defined",
        stack_trace=["File test.py, line 42, in main"],
        variables={"x": 10, "y": "hello"},
        timestamp=datetime.now().isoformat()
    )
    
    analysis = await debug_agent.analyze_error(test_context)
    print(f"Error Analysis: {'success' if 'error_id' in analysis else 'error'}")
    
    if 'analysis' in analysis:
        print(f"Error Category: {analysis['analysis']['error_category']}")
        print(f"Severity: {analysis['analysis']['severity']}")
        print(f"Suggested Fixes: {len(analysis['analysis']['suggested_fixes'])}")


if __name__ == "__main__":
    asyncio.run(main())
'''
            
            with open(debug_dir / "debug_agent.py", 'w') as f:
                f.write(debug_agent_code)
            
            # Debug configuration
            debug_config = {
                "enabled": True,
                "auto_analysis": True,
                "breakpoint_suggestions": True,
                "error_categorization": True,
                "fix_suggestions": True,
                "test_generation": True,
                "session_timeout": 3600,
                "max_analysis_cache": 1000
            }
            
            with open(debug_dir / "config.json", 'w') as f:
                json.dump(debug_config, f, indent=2)
            
            self.logger.info("Debug Agent System configured")
            
            return {
                'status': 'success',
                'message': 'Debug Agent System with LangGraph configured',
                'components': ['debug_agent.py', 'config.json'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Debug Agent System setup failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def setup_intellisense_config(self) -> dict:
        """Setup IntelliSense configuration"""
        try:
            vscode_dir = Path(self.workspace_path) / ".vscode"
            vscode_dir.mkdir(exist_ok=True)
            
            # Settings for enhanced IntelliSense
            settings = {
                "python.defaultInterpreterPath": "./venv/bin/python",
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": True,
                "python.linting.flake8Enabled": True,
                "python.linting.mypyEnabled": True,
                "python.formatting.provider": "black",
                "python.sortImports.args": ["--profile", "black"],
                "python.analysis.typeCheckingMode": "strict",
                "python.analysis.autoImportCompletions": True,
                "python.analysis.completeFunctionParens": True,
                "python.analysis.autoSearchPaths": True,
                "typescript.preferences.includePackageJsonAutoImports": "on",
                "typescript.suggest.autoImports": True,
                "typescript.suggest.completeFunctionCalls": True,
                "javascript.suggest.autoImports": True,
                "javascript.suggest.completeFunctionCalls": True,
                "editor.quickSuggestions": {
                    "other": True,
                    "comments": False,
                    "strings": True
                },
                "editor.suggestSelection": "first",
                "editor.tabCompletion": "on",
                "editor.wordBasedSuggestions": True,
                "editor.parameterHints.enabled": True,
                "editor.hover.enabled": True,
                "editor.hover.delay": 300,
                "intelliSenseEngine": "Pylance",
                "vsintellicode.modify.editor.suggestSelection": "automaticallyOverrodeDefaultValue"
            }
            
            settings_file = vscode_dir / "settings.json"
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            # Tasks configuration
            tasks = {
                "version": "2.0.0",
                "tasks": [
                    {
                        "label": "Python: Lint",
                        "type": "shell",
                        "command": "python",
                        "args": ["-m", "flake8", "${workspaceFolder}"],
                        "group": "build",
                        "presentation": {
                            "echo": True,
                            "reveal": "always",
                            "focus": False,
                            "panel": "shared"
                        }
                    },
                    {
                        "label": "Python: Format",
                        "type": "shell",
                        "command": "python",
                        "args": ["-m", "black", "${workspaceFolder}"],
                        "group": "build"
                    },
                    {
                        "label": "Python: Type Check",
                        "type": "shell",
                        "command": "python",
                        "args": ["-m", "mypy", "${workspaceFolder}"],
                        "group": "build"
                    },
                    {
                        "label": "Node: Lint",
                        "type": "shell",
                        "command": "npm",
                        "args": ["run", "lint"],
                        "group": "build"
                    },
                    {
                        "label": "Node: Format",
                        "type": "shell",
                        "command": "npm",
                        "args": ["run", "format"],
                        "group": "build"
                    }
                ]
            }
            
            tasks_file = vscode_dir / "tasks.json"
            with open(tasks_file, 'w') as f:
                json.dump(tasks, f, indent=2)
            
            self.logger.info("IntelliSense configuration created")
            
            return {
                'status': 'success',
                'message': 'IntelliSense configuration created',
                'files': ['settings.json', 'tasks.json'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"IntelliSense config setup failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_status(self) -> dict:
        """Get VS Code integration status"""
        return {
            'status': 'online' if self.is_connected else 'offline',
            'connected': self.is_connected,
            'vscode_path': self.vscode_path,
            'extensions_path': str(self.extensions_path) if self.extensions_path else None,
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Main function for testing VS Code integration"""
    vscode = VSCodeAIIntegration()
    
    print("🔧 VS Code AI Integration Test")
    print("=" * 50)
    
    # Test connection
    result = vscode.connect()
    print(f"Connection: {result['status']}")
    
    if result['status'] == 'success':
        # Install AI extensions
        ext_result = vscode.install_ai_extensions()
        print(f"Extensions: {ext_result['status']} ({len(ext_result.get('installed', []))} installed)")
        
        # Setup Debug Agent System
        debug_result = vscode.setup_debug_agent_system()
        print(f"Debug Agent System: {debug_result['status']}")
        
        # Setup IntelliSense
        intellisense_result = vscode.setup_intellisense_config()
        print(f"IntelliSense: {intellisense_result['status']}")
        
        # Get status
        status = vscode.get_status()
        print(f"Final Status: {status['status']}")


if __name__ == "__main__":
    main()