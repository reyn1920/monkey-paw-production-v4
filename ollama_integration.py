#!/usr/bin/env python3
"""
Ollama AI Integration for Monkey Paw Production v4
Handles 12+ local AI models, server monitoring, performance metrics,
and Continue integration
"""

import os
import json
import logging
import requests
import subprocess
import time
from datetime import datetime
from pathlib import Path


class OllamaIntegration:
    """Integration with Ollama for local AI models and monitoring"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.logger = logging.getLogger(__name__)
        self.is_connected = False
        self.ollama_url = "http://localhost:11434"
        self.available_models = []
        self.running_models = []
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    def connect(self) -> dict:
        """Connect to Ollama server"""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            
            if response.status_code == 200:
                self.is_connected = True
                models_data = response.json()
                self.available_models = [
                    model['name'] for model in models_data.get('models', [])
                ]
                
                self.logger.info("Connected to Ollama successfully")
                
                return {
                    'status': 'success',
                    'message': 'Connected to Ollama',
                    'available_models': self.available_models,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Ollama server not responding',
                    'timestamp': datetime.now().isoformat()
                }
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ollama connection failed: {str(e)}")
            return {
                'status': 'error',
                'message': f'Connection failed: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def install_models(self) -> dict:
        """Install recommended AI models"""
        try:
            recommended_models = [
                'llama2',
                'codellama',
                'mistral',
                'neural-chat',
                'starcode',
                'vicuna',
                'orca-mini',
                'dolphin-phi',
                'tinyllama',
                'deepseek-coder',
                'magicoder',
                'phind-codellama'
            ]
            
            installed_models = []
            failed_models = []
            
            for model in recommended_models:
                try:
                    self.logger.info(f"Installing model: {model}")
                    result = subprocess.run(
                        ['ollama', 'pull', model],
                        capture_output=True,
                        text=True,
                        timeout=300  # 5 minute timeout per model
                    )
                    
                    if result.returncode == 0:
                        installed_models.append(model)
                        self.logger.info(f"Successfully installed: {model}")
                    else:
                        failed_models.append(model)
                        self.logger.error(f"Failed to install: {model}")
                        
                except subprocess.TimeoutExpired:
                    failed_models.append(model)
                    self.logger.error(f"Timeout installing: {model}")
                except Exception as e:
                    failed_models.append(model)
                    self.logger.error(f"Error installing {model}: {e}")
            
            # Update available models
            self.connect()
            
            return {
                'status': 'success',
                'message': f'Installed {len(installed_models)} models',
                'installed': installed_models,
                'failed': failed_models,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Model installation failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def setup_continue_integration(self) -> dict:
        """Setup Continue extension integration with Ollama"""
        try:
            continue_dir = Path.home() / ".continue"
            continue_dir.mkdir(exist_ok=True)
            
            # Continue configuration for Ollama
            continue_config = {
                "models": [
                    {
                        "title": "Llama 2",
                        "provider": "ollama",
                        "model": "llama2",
                        "apiBase": "http://localhost:11434"
                    },
                    {
                        "title": "Code Llama",
                        "provider": "ollama",
                        "model": "codellama",
                        "apiBase": "http://localhost:11434"
                    },
                    {
                        "title": "Mistral",
                        "provider": "ollama",
                        "model": "mistral",
                        "apiBase": "http://localhost:11434"
                    },
                    {
                        "title": "DeepSeek Coder",
                        "provider": "ollama",
                        "model": "deepseek-coder",
                        "apiBase": "http://localhost:11434"
                    }
                ],
                "tabAutocompleteModel": {
                    "title": "StarCode",
                    "provider": "ollama",
                    "model": "starcode",
                    "apiBase": "http://localhost:11434"
                },
                "embeddingsProvider": {
                    "provider": "ollama",
                    "model": "nomic-embed-text",
                    "apiBase": "http://localhost:11434"
                },
                "contextProviders": [
                    {
                        "name": "code",
                        "params": {}
                    },
                    {
                        "name": "docs",
                        "params": {}
                    },
                    {
                        "name": "diff",
                        "params": {}
                    },
                    {
                        "name": "terminal",
                        "params": {}
                    },
                    {
                        "name": "problems",
                        "params": {}
                    },
                    {
                        "name": "folder",
                        "params": {}
                    },
                    {
                        "name": "codebase",
                        "params": {}
                    }
                ],
                "slashCommands": [
                    {
                        "name": "edit",
                        "description": "Edit code in the current file"
                    },
                    {
                        "name": "comment",
                        "description": "Write comments for the code"
                    },
                    {
                        "name": "share",
                        "description": "Export the current chat session"
                    },
                    {
                        "name": "cmd",
                        "description": "Generate a shell command"
                    },
                    {
                        "name": "commit",
                        "description": "Generate a git commit message"
                    }
                ]
            }
            
            with open(continue_dir / "config.json", 'w') as f:
                json.dump(continue_config, f, indent=2)
            
            self.logger.info("Continue integration configured")
            
            return {
                'status': 'success',
                'message': 'Continue integration configured',
                'config_path': str(continue_dir / "config.json"),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Continue integration failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def setup_monitoring(self) -> dict:
        """Setup Ollama server monitoring"""
        try:
            monitoring_dir = Path(self.workspace_path) / "monitoring" / "ollama"
            monitoring_dir.mkdir(parents=True, exist_ok=True)
            
            # Monitoring script
            monitor_script = '''#!/usr/bin/env python3
"""
Ollama Server Monitor
Monitors Ollama server performance and model usage
"""

import json
import time
import requests
import logging
from datetime import datetime
from pathlib import Path

class OllamaMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ollama_url = "http://localhost:11434"
        self.metrics = {
            'server_status': [],
            'model_usage': {},
            'performance_metrics': [],
            'error_log': []
        }
        
    def start_monitoring(self, interval: int = 30):
        """Start continuous monitoring"""
        self.logger.info("Starting Ollama monitoring")
        
        while True:
            try:
                self.check_server_status()
                self.collect_performance_metrics()
                self.save_metrics()
                time.sleep(interval)
                
            except KeyboardInterrupt:
                self.logger.info("Monitoring stopped")
                break
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                self.metrics['error_log'].append({
                    'timestamp': datetime.now().isoformat(),
                    'error': str(e)
                })
    
    def check_server_status(self):
        """Check Ollama server status"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            status = {
                'timestamp': datetime.now().isoformat(),
                'status': 'online' if response.status_code == 200 else 'offline',
                'response_time': response.elapsed.total_seconds(),
                'models_count': len(response.json().get('models', []))
            }
            self.metrics['server_status'].append(status)
            
            # Keep only last 100 status checks
            if len(self.metrics['server_status']) > 100:
                self.metrics['server_status'] = self.metrics['server_status'][-100:]
                
        except Exception as e:
            status = {
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
            self.metrics['server_status'].append(status)
    
    def collect_performance_metrics(self):
        """Collect performance metrics"""
        try:
            # Get system metrics (simplified)
            import psutil
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu_usage': psutil.cpu_percent(),
                'memory_usage': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent
            }
            
            self.metrics['performance_metrics'].append(metrics)
            
            # Keep only last 100 metrics
            if len(self.metrics['performance_metrics']) > 100:
                self.metrics['performance_metrics'] = self.metrics['performance_metrics'][-100:]
                
        except ImportError:
            self.logger.warning("psutil not available for system metrics")
        except Exception as e:
            self.logger.error(f"Performance metrics error: {e}")
    
    def save_metrics(self):
        """Save metrics to file"""
        try:
            metrics_file = Path("ollama_metrics.json")
            with open(metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save metrics: {e}")
    
    def get_status_report(self):
        """Generate status report"""
        if not self.metrics['server_status']:
            return "No monitoring data available"
        
        latest_status = self.metrics['server_status'][-1]
        online_count = sum(1 for s in self.metrics['server_status'][-10:] 
                          if s.get('status') == 'online')
        
        report = f"""
Ollama Server Status Report
==========================
Current Status: {latest_status.get('status', 'unknown')}
Uptime (last 10 checks): {online_count}/10
Available Models: {latest_status.get('models_count', 0)}
Last Check: {latest_status.get('timestamp', 'unknown')}
"""
        
        if self.metrics['performance_metrics']:
            latest_perf = self.metrics['performance_metrics'][-1]
            report += f"""
Performance Metrics:
- CPU Usage: {latest_perf.get('cpu_usage', 0):.1f}%
- Memory Usage: {latest_perf.get('memory_usage', 0):.1f}%
- Disk Usage: {latest_perf.get('disk_usage', 0):.1f}%
"""
        
        return report

if __name__ == "__main__":
    monitor = OllamaMonitor()
    print(monitor.get_status_report())
    # monitor.start_monitoring()
'''
            
            with open(monitoring_dir / "monitor.py", 'w') as f:
                f.write(monitor_script)
            
            # Monitoring configuration
            monitor_config = {
                "enabled": True,
                "check_interval": 30,
                "metrics_retention": 100,
                "alerts": {
                    "server_down": True,
                    "high_cpu": 80,
                    "high_memory": 90,
                    "response_time": 5.0
                }
            }
            
            with open(monitoring_dir / "config.json", 'w') as f:
                json.dump(monitor_config, f, indent=2)
            
            self.logger.info("Ollama monitoring configured")
            
            return {
                'status': 'success',
                'message': 'Ollama monitoring configured',
                'components': ['monitor.py', 'config.json'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Monitoring setup failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def test_models(self) -> dict:
        """Test available models"""
        try:
            test_results = {}
            test_prompt = "Write a simple Python function to add two numbers."
            
            for model in self.available_models[:5]:  # Test first 5 models
                try:
                    self.logger.info(f"Testing model: {model}")
                    
                    response = requests.post(
                        f"{self.ollama_url}/api/generate",
                        json={
                            "model": model,
                            "prompt": test_prompt,
                            "stream": False
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        test_results[model] = {
                            'status': 'success',
                            'response_length': len(result.get('response', '')),
                            'eval_count': result.get('eval_count', 0),
                            'eval_duration': result.get('eval_duration', 0)
                        }
                    else:
                        test_results[model] = {
                            'status': 'error',
                            'error': f'HTTP {response.status_code}'
                        }
                        
                except Exception as e:
                    test_results[model] = {
                        'status': 'error',
                        'error': str(e)
                    }
            
            return {
                'status': 'success',
                'message': f'Tested {len(test_results)} models',
                'results': test_results,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Model testing failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_status(self) -> dict:
        """Get Ollama integration status"""
        return {
            'status': 'online' if self.is_connected else 'offline',
            'connected': self.is_connected,
            'server_url': self.ollama_url,
            'available_models': len(self.available_models),
            'models': self.available_models,
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Main function for testing Ollama integration"""
    ollama = OllamaIntegration()
    
    print("🦙 Ollama AI Integration Test")
    print("=" * 50)
    
    # Test connection
    result = ollama.connect()
    print(f"Connection: {result['status']}")
    
    if result['status'] == 'success':
        print(f"Available models: {len(result['available_models'])}")
        
        # Setup Continue integration
        continue_result = ollama.setup_continue_integration()
        print(f"Continue Integration: {continue_result['status']}")
        
        # Setup monitoring
        monitor_result = ollama.setup_monitoring()
        print(f"Monitoring: {monitor_result['status']}")
        
        # Test models (if any available)
        if ollama.available_models:
            test_result = ollama.test_models()
            print(f"Model Testing: {test_result['status']}")
        
        # Get status
        status = ollama.get_status()
        print(f"Final Status: {status['status']}")
    else:
        print("Installing recommended models...")
        install_result = ollama.install_models()
        print(f"Model Installation: {install_result['status']}")


if __name__ == "__main__":
    main()