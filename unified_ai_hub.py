#!/usr/bin/env python3
"""
Unified AI Integration Hub for Monkey Paw Production v4
Connects all 6 AI platforms: Cursor, Windsurf, Trae, VS Code, Ollama, Sublime
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Import all AI platform integrations
from cursor_integration import CursorIntegration
from windsurf_integration import WindsurfIntegration
from trae_integration import TraeIntegration
from vscode_ai_integration import VSCodeAIIntegration
from ollama_integration import OllamaIntegration
from sublime_integration import SublimeIntegration


class UnifiedAIHub:
    """Unified hub for all AI platform integrations"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
        # Initialize all AI platform integrations
        self.platforms = {
            'cursor': CursorIntegration(self.workspace_path),
            'windsurf': WindsurfIntegration(self.workspace_path),
            'trae': TraeIntegration(self.workspace_path),
            'vscode': VSCodeAIIntegration(self.workspace_path),
            'ollama': OllamaIntegration(self.workspace_path),
            'sublime': SublimeIntegration(self.workspace_path)
        }
        
        self.status = {
            'initialized': False,
            'connected_platforms': [],
            'failed_platforms': [],
            'total_items': 242,
            'integrated_items': 0,
            'last_sync': None
        }
        
        self.executor = ThreadPoolExecutor(max_workers=6)
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('unified_ai_hub.log'),
                logging.StreamHandler()
            ]
        )
        
    async def initialize_all_platforms(self):
        """Initialize all AI platforms concurrently"""
        try:
            self.logger.info("🚀 Initializing Unified AI Hub")
            self.logger.info("Connecting to all 6 AI platforms...")
            
            # Connect to all platforms concurrently
            tasks = []
            for name, platform in self.platforms.items():
                task = asyncio.create_task(
                    self._connect_platform(name, platform)
                )
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for i, (name, result) in enumerate(zip(self.platforms.keys(), results)):
                if isinstance(result, Exception):
                    self.status['failed_platforms'].append(name)
                    self.logger.error(f"❌ {name.upper()} failed: {str(result)}")
                else:
                    self.status['connected_platforms'].append(name)
                    self.logger.info(f"✅ {name.upper()} connected successfully")
            
            self.status['initialized'] = True
            self.status['last_sync'] = datetime.now().isoformat()
            
            return {
                'status': 'success',
                'connected': len(self.status['connected_platforms']),
                'failed': len(self.status['failed_platforms']),
                'platforms': self.status,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Hub initialization failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _connect_platform(self, name: str, platform):
        """Connect to individual platform"""
        try:
            if hasattr(platform, 'connect'):
                result = platform.connect()
                # Handle both async and sync methods
                if asyncio.iscoroutine(result):
                    result = await result
            else:
                # For synchronous platforms
                result = platform.get_status()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Platform {name} connection failed: {str(e)}")
            raise e
    
    async def sync_all_platforms(self):
        """Synchronize all platforms"""
        try:
            self.logger.info("🔄 Synchronizing all AI platforms...")
            
            sync_tasks = []
            for name, platform in self.platforms.items():
                if name in self.status['connected_platforms']:
                    task = asyncio.create_task(
                        self._sync_platform(name, platform)
                    )
                    sync_tasks.append(task)
            
            results = await asyncio.gather(*sync_tasks, return_exceptions=True)
            
            sync_status = {}
            for i, (name, result) in enumerate(
                zip(self.status['connected_platforms'], results)
            ):
                if isinstance(result, Exception):
                    sync_status[name] = {'status': 'error', 'error': str(result)}
                else:
                    sync_status[name] = result
            
            self.status['last_sync'] = datetime.now().isoformat()
            
            return {
                'status': 'success',
                'sync_results': sync_status,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Platform sync failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _sync_platform(self, name: str, platform):
        """Sync individual platform"""
        try:
            if hasattr(platform, 'sync'):
                return await platform.sync()
            elif hasattr(platform, 'get_status'):
                return platform.get_status()
            else:
                return {'status': 'no_sync_method', 'platform': name}
                
        except Exception as e:
            self.logger.error(f"Platform {name} sync failed: {str(e)}")
            raise e
    
    def get_unified_status(self):
        """Get unified status of all platforms"""
        platform_statuses = {}
        
        for name, platform in self.platforms.items():
            try:
                if hasattr(platform, 'get_status'):
                    platform_statuses[name] = platform.get_status()
                else:
                    platform_statuses[name] = {'status': 'unknown'}
            except Exception as e:
                platform_statuses[name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return {
            'hub_status': self.status,
            'platform_statuses': platform_statuses,
            'summary': {
                'total_platforms': len(self.platforms),
                'connected': len(self.status['connected_platforms']),
                'failed': len(self.status['failed_platforms']),
                'success_rate': (
                    len(self.status['connected_platforms']) / 
                    len(self.platforms) * 100
                ) if self.platforms else 0
            },
            'timestamp': datetime.now().isoformat()
        }
    
    async def execute_unified_command(self, command: str, **kwargs):
        """Execute command across all connected platforms"""
        try:
            self.logger.info(f"🎯 Executing unified command: {command}")
            
            results = {}
            tasks = []
            
            for name, platform in self.platforms.items():
                if name in self.status['connected_platforms']:
                    if hasattr(platform, command):
                        task = asyncio.create_task(
                            self._execute_platform_command(
                                name, platform, command, **kwargs
                            )
                        )
                        tasks.append((name, task))
            
            # Execute all commands concurrently
            for name, task in tasks:
                try:
                    result = await task
                    results[name] = result
                except Exception as e:
                    results[name] = {
                        'status': 'error',
                        'error': str(e)
                    }
            
            return {
                'status': 'success',
                'command': command,
                'results': results,
                'executed_on': len(results),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Unified command execution failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _execute_platform_command(self, name: str, platform, 
                                       command: str, **kwargs):
        """Execute command on individual platform"""
        try:
            method = getattr(platform, command)
            if asyncio.iscoroutinefunction(method):
                return await method(**kwargs)
            else:
                return method(**kwargs)
        except Exception as e:
            self.logger.error(f"Command {command} failed on {name}: {str(e)}")
            raise e
    
    def create_unified_config(self):
        """Create unified configuration file"""
        try:
            config = {
                'unified_ai_hub': {
                    'version': '1.0.0',
                    'workspace_path': self.workspace_path,
                    'platforms': {
                        'cursor': {
                            'enabled': True,
                            'priority': 1,
                            'features': [
                                'IDE integration',
                                'AI code completion',
                                'Continue extension',
                                'Workspace configuration'
                            ]
                        },
                        'windsurf': {
                            'enabled': True,
                            'priority': 2,
                            'features': [
                                'GitHub Actions',
                                'CI/CD automation',
                                'DaVinci Resolve integration',
                                'Unified workflows'
                            ]
                        },
                        'trae': {
                            'enabled': True,
                            'priority': 3,
                            'features': [
                                'SOLO agents',
                                'Autonomous development',
                                'Self-healing systems',
                                'AI collaboration'
                            ]
                        },
                        'vscode': {
                            'enabled': True,
                            'priority': 4,
                            'features': [
                                'Debug Agent System',
                                'LangGraph integration',
                                'IntelliSense enhancement',
                                'Extension management'
                            ]
                        },
                        'ollama': {
                            'enabled': True,
                            'priority': 5,
                            'features': [
                                '12+ local AI models',
                                'Server monitoring',
                                'Performance metrics',
                                'Continue integration'
                            ]
                        },
                        'sublime': {
                            'enabled': True,
                            'priority': 6,
                            'features': [
                                'Build 4200 support',
                                'Automation reports',
                                'Project configurations',
                                'Package Control'
                            ]
                        }
                    },
                    'integration_settings': {
                        'auto_sync': True,
                        'sync_interval': 300,
                        'error_retry_count': 3,
                        'concurrent_operations': True,
                        'logging_level': 'INFO',
                        'backup_configs': True
                    }
                }
            }
            
            config_file = Path(self.workspace_path) / 'unified_ai_config.json'
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.logger.info(f"Unified config created: {config_file}")
            
            return {
                'status': 'success',
                'config_file': str(config_file),
                'platforms_configured': len(config['unified_ai_hub']['platforms']),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Config creation failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def run_integration_tests(self):
        """Run comprehensive integration tests"""
        try:
            self.logger.info("🧪 Running integration tests...")
            
            test_results = {
                'platform_connections': {},
                'feature_tests': {},
                'performance_tests': {},
                'compatibility_tests': {}
            }
            
            # Test platform connections
            for name, platform in self.platforms.items():
                try:
                    if hasattr(platform, 'get_status'):
                        status = platform.get_status()
                        test_results['platform_connections'][name] = {
                            'status': 'pass' if status.get('status') == 'online' 
                                     else 'fail',
                            'details': status
                        }
                    else:
                        test_results['platform_connections'][name] = {
                            'status': 'skip',
                            'reason': 'No status method'
                        }
                except Exception as e:
                    test_results['platform_connections'][name] = {
                        'status': 'fail',
                        'error': str(e)
                    }
            
            # Test unified commands
            test_commands = ['get_status']
            for command in test_commands:
                try:
                    result = await self.execute_unified_command(command)
                    test_results['feature_tests'][command] = {
                        'status': 'pass' if result['status'] == 'success' 
                                 else 'fail',
                        'executed_on': result.get('executed_on', 0)
                    }
                except Exception as e:
                    test_results['feature_tests'][command] = {
                        'status': 'fail',
                        'error': str(e)
                    }
            
            # Calculate overall test results
            total_tests = (
                len(test_results['platform_connections']) +
                len(test_results['feature_tests'])
            )
            
            passed_tests = sum(
                1 for result in test_results['platform_connections'].values()
                if result['status'] == 'pass'
            ) + sum(
                1 for result in test_results['feature_tests'].values()
                if result['status'] == 'pass'
            )
            
            return {
                'status': 'success',
                'test_results': test_results,
                'summary': {
                    'total_tests': total_tests,
                    'passed': passed_tests,
                    'failed': total_tests - passed_tests,
                    'success_rate': (passed_tests / total_tests * 100) 
                                   if total_tests > 0 else 0
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Integration tests failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def shutdown(self):
        """Gracefully shutdown all platforms"""
        try:
            self.logger.info("🔄 Shutting down Unified AI Hub...")
            
            shutdown_tasks = []
            for name, platform in self.platforms.items():
                if hasattr(platform, 'shutdown'):
                    task = asyncio.create_task(platform.shutdown())
                    shutdown_tasks.append(task)
            
            if shutdown_tasks:
                await asyncio.gather(*shutdown_tasks, return_exceptions=True)
            
            self.executor.shutdown(wait=True)
            
            self.logger.info("✅ Unified AI Hub shutdown complete")
            
            return {
                'status': 'success',
                'message': 'Hub shutdown complete',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Shutdown failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }


async def main():
    """Main function for testing Unified AI Hub"""
    hub = UnifiedAIHub()
    
    print("🌟 Unified AI Hub - Connecting All 6 Platforms")
    print("=" * 60)
    
    try:
        # Initialize all platforms
        init_result = await hub.initialize_all_platforms()
        print(f"Initialization: {init_result['status']}")
        print(f"Connected: {init_result['connected']}/6 platforms")
        
        if init_result['connected'] > 0:
            # Create unified config
            config_result = hub.create_unified_config()
            print(f"Config Creation: {config_result['status']}")
            
            # Get unified status
            status = hub.get_unified_status()
            print(f"Success Rate: {status['summary']['success_rate']:.1f}%")
            
            # Run integration tests
            test_result = await hub.run_integration_tests()
            print(f"Integration Tests: {test_result['status']}")
            if 'summary' in test_result:
                print(f"Test Success Rate: "
                      f"{test_result['summary']['success_rate']:.1f}%")
            
            # Sync all platforms
            sync_result = await hub.sync_all_platforms()
            print(f"Platform Sync: {sync_result['status']}")
        
        # Shutdown
        await hub.shutdown()
        
    except Exception as e:
        print(f"❌ Hub execution failed: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())