#!/usr/bin/env python3
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
