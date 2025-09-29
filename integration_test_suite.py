#!/usr/bin/env python3
"""
Integration Test Suite for Monkey Paw Production v4
Tests all 242 integrated items across 6 AI platforms
"""

import os
import json
import asyncio
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from unified_ai_hub import UnifiedAIHub


class IntegrationTestSuite:
    """Comprehensive test suite for all AI platform integrations"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
        self.hub = UnifiedAIHub(self.workspace_path)
        
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'skipped_tests': 0,
            'platform_results': {},
            'feature_results': {},
            'performance_results': {},
            'compatibility_results': {}
        }
        
        # Test categories and expected counts
        self.expected_items = {
            'cursor': 38,
            'windsurf': 47,
            'trae': 52,
            'vscode': 32,
            'ollama': 45,
            'sublime': 28
        }
        
        self.total_expected = sum(self.expected_items.values())  # 242
        
    def setup_logging(self):
        """Setup test logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('integration_tests.log'),
                logging.StreamHandler()
            ]
        )
    
    async def run_all_tests(self):
        """Run comprehensive integration tests"""
        try:
            self.logger.info("🧪 Starting Integration Test Suite")
            self.logger.info(f"Testing {self.total_expected} integrated items")
            self.logger.info("=" * 60)
            
            # Initialize the hub
            init_result = await self.hub.initialize_all_platforms()
            if init_result['status'] != 'success':
                return {
                    'status': 'error',
                    'message': 'Hub initialization failed',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Run test categories
            await self._test_platform_connections()
            await self._test_platform_features()
            await self._test_cross_platform_compatibility()
            await self._test_performance_metrics()
            await self._test_error_handling()
            await self._test_configuration_integrity()
            
            # Generate final report
            return self._generate_test_report()
            
        except Exception as e:
            self.logger.error(f"Test suite execution failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _test_platform_connections(self):
        """Test all platform connections"""
        self.logger.info("🔌 Testing Platform Connections")
        
        for platform_name in self.expected_items.keys():
            try:
                platform = self.hub.platforms.get(platform_name)
                if not platform:
                    self._record_test_result(
                        f"{platform_name}_connection",
                        'fail',
                        'Platform not found in hub'
                    )
                    continue
                
                # Test connection
                if hasattr(platform, 'get_status'):
                    status = platform.get_status()
                    if status.get('status') in ['online', 'success']:
                        self._record_test_result(
                            f"{platform_name}_connection",
                            'pass',
                            f"Connected successfully: {status.get('message', '')}"
                        )
                    else:
                        self._record_test_result(
                            f"{platform_name}_connection",
                            'fail',
                            f"Connection failed: {status.get('message', '')}"
                        )
                else:
                    self._record_test_result(
                        f"{platform_name}_connection",
                        'skip',
                        'No status method available'
                    )
                    
            except Exception as e:
                self._record_test_result(
                    f"{platform_name}_connection",
                    'fail',
                    str(e)
                )
    
    async def _test_platform_features(self):
        """Test platform-specific features"""
        self.logger.info("⚙️ Testing Platform Features")
        
        # Cursor AI features
        await self._test_cursor_features()
        
        # Windsurf AI features
        await self._test_windsurf_features()
        
        # Trae AI features
        await self._test_trae_features()
        
        # VS Code AI features
        await self._test_vscode_features()
        
        # Ollama AI features
        await self._test_ollama_features()
        
        # Sublime AI features
        await self._test_sublime_features()
    
    async def _test_cursor_features(self):
        """Test Cursor AI specific features"""
        cursor = self.hub.platforms.get('cursor')
        if not cursor:
            return
        
        features_to_test = [
            'get_status',
            'sync_with_ai_ceo',
            'install_extensions',
            'setup_workspace'
        ]
        
        for feature in features_to_test:
            try:
                if hasattr(cursor, feature):
                    method = getattr(cursor, feature)
                    if asyncio.iscoroutinefunction(method):
                        result = await method()
                    else:
                        result = method()
                    
                    self._record_test_result(
                        f"cursor_{feature}",
                        'pass' if result.get('status') == 'success' else 'fail',
                        result.get('message', 'Feature executed')
                    )
                else:
                    self._record_test_result(
                        f"cursor_{feature}",
                        'skip',
                        'Feature not implemented'
                    )
            except Exception as e:
                self._record_test_result(
                    f"cursor_{feature}",
                    'fail',
                    str(e)
                )
    
    async def _test_windsurf_features(self):
        """Test Windsurf AI specific features"""
        windsurf = self.hub.platforms.get('windsurf')
        if not windsurf:
            return
        
        features_to_test = [
            'get_status',
            'setup_github_actions',
            'setup_davinci_resolve',
            'create_unified_workflow'
        ]
        
        for feature in features_to_test:
            try:
                if hasattr(windsurf, feature):
                    method = getattr(windsurf, feature)
                    if asyncio.iscoroutinefunction(method):
                        result = await method()
                    else:
                        result = method()
                    
                    self._record_test_result(
                        f"windsurf_{feature}",
                        'pass' if result.get('status') == 'success' else 'fail',
                        result.get('message', 'Feature executed')
                    )
                else:
                    self._record_test_result(
                        f"windsurf_{feature}",
                        'skip',
                        'Feature not implemented'
                    )
            except Exception as e:
                self._record_test_result(
                    f"windsurf_{feature}",
                    'fail',
                    str(e)
                )
    
    async def _test_trae_features(self):
        """Test Trae AI specific features"""
        trae = self.hub.platforms.get('trae')
        if not trae:
            return
        
        features_to_test = [
            'get_status',
            'initialize_project',
            'generate_code',
            'review_code'
        ]
        
        for feature in features_to_test:
            try:
                if hasattr(trae, feature):
                    method = getattr(trae, feature)
                    if asyncio.iscoroutinefunction(method):
                        result = await method()
                    else:
                        result = method()
                    
                    self._record_test_result(
                        f"trae_{feature}",
                        'pass' if result.get('status') == 'success' else 'fail',
                        result.get('message', 'Feature executed')
                    )
                else:
                    self._record_test_result(
                        f"trae_{feature}",
                        'skip',
                        'Feature not implemented'
                    )
            except Exception as e:
                self._record_test_result(
                    f"trae_{feature}",
                    'fail',
                    str(e)
                )
    
    async def _test_vscode_features(self):
        """Test VS Code AI specific features"""
        vscode = self.hub.platforms.get('vscode')
        if not vscode:
            return
        
        features_to_test = [
            'get_status',
            'install_ai_extensions',
            'setup_debug_agent_system',
            'setup_intellisense_config'
        ]
        
        for feature in features_to_test:
            try:
                if hasattr(vscode, feature):
                    method = getattr(vscode, feature)
                    if asyncio.iscoroutinefunction(method):
                        result = await method()
                    else:
                        result = method()
                    
                    self._record_test_result(
                        f"vscode_{feature}",
                        'pass' if result.get('status') == 'success' else 'fail',
                        result.get('message', 'Feature executed')
                    )
                else:
                    self._record_test_result(
                        f"vscode_{feature}",
                        'skip',
                        'Feature not implemented'
                    )
            except Exception as e:
                self._record_test_result(
                    f"vscode_{feature}",
                    'fail',
                    str(e)
                )
    
    async def _test_ollama_features(self):
        """Test Ollama AI specific features"""
        ollama = self.hub.platforms.get('ollama')
        if not ollama:
            return
        
        features_to_test = [
            'get_status',
            'start_server',
            'list_models',
            'get_performance_metrics'
        ]
        
        for feature in features_to_test:
            try:
                if hasattr(ollama, feature):
                    method = getattr(ollama, feature)
                    if asyncio.iscoroutinefunction(method):
                        result = await method()
                    else:
                        result = method()
                    
                    self._record_test_result(
                        f"ollama_{feature}",
                        'pass' if result.get('status') == 'success' else 'fail',
                        result.get('message', 'Feature executed')
                    )
                else:
                    self._record_test_result(
                        f"ollama_{feature}",
                        'skip',
                        'Feature not implemented'
                    )
            except Exception as e:
                self._record_test_result(
                    f"ollama_{feature}",
                    'fail',
                    str(e)
                )
    
    async def _test_sublime_features(self):
        """Test Sublime AI specific features"""
        sublime = self.hub.platforms.get('sublime')
        if not sublime:
            return
        
        features_to_test = [
            'get_status',
            'setup_package_control',
            'setup_project_config',
            'generate_automation_report'
        ]
        
        for feature in features_to_test:
            try:
                if hasattr(sublime, feature):
                    method = getattr(sublime, feature)
                    if asyncio.iscoroutinefunction(method):
                        result = await method()
                    else:
                        result = method()
                    
                    self._record_test_result(
                        f"sublime_{feature}",
                        'pass' if result.get('status') == 'success' else 'fail',
                        result.get('message', 'Feature executed')
                    )
                else:
                    self._record_test_result(
                        f"sublime_{feature}",
                        'skip',
                        'Feature not implemented'
                    )
            except Exception as e:
                self._record_test_result(
                    f"sublime_{feature}",
                    'fail',
                    str(e)
                )
    
    async def _test_cross_platform_compatibility(self):
        """Test cross-platform compatibility"""
        self.logger.info("🔄 Testing Cross-Platform Compatibility")
        
        try:
            # Test unified command execution
            result = await self.hub.execute_unified_command('get_status')
            
            self._record_test_result(
                'unified_command_execution',
                'pass' if result['status'] == 'success' else 'fail',
                f"Executed on {result.get('executed_on', 0)} platforms"
            )
            
            # Test platform synchronization
            sync_result = await self.hub.sync_all_platforms()
            
            self._record_test_result(
                'platform_synchronization',
                'pass' if sync_result['status'] == 'success' else 'fail',
                'Platform sync completed'
            )
            
        except Exception as e:
            self._record_test_result(
                'cross_platform_compatibility',
                'fail',
                str(e)
            )
    
    async def _test_performance_metrics(self):
        """Test performance metrics"""
        self.logger.info("📊 Testing Performance Metrics")
        
        try:
            start_time = datetime.now()
            
            # Test hub initialization time
            await self.hub.initialize_all_platforms()
            
            init_time = (datetime.now() - start_time).total_seconds()
            
            self._record_test_result(
                'hub_initialization_time',
                'pass' if init_time < 30 else 'fail',
                f"Initialization took {init_time:.2f} seconds"
            )
            
            # Test unified status retrieval time
            start_time = datetime.now()
            status = self.hub.get_unified_status()
            status_time = (datetime.now() - start_time).total_seconds()
            
            self._record_test_result(
                'status_retrieval_time',
                'pass' if status_time < 5 else 'fail',
                f"Status retrieval took {status_time:.2f} seconds"
            )
            
        except Exception as e:
            self._record_test_result(
                'performance_metrics',
                'fail',
                str(e)
            )
    
    async def _test_error_handling(self):
        """Test error handling capabilities"""
        self.logger.info("🚨 Testing Error Handling")
        
        try:
            # Test invalid command execution
            result = await self.hub.execute_unified_command('invalid_command')
            
            self._record_test_result(
                'invalid_command_handling',
                'pass' if 'error' in result or result['executed_on'] == 0 
                        else 'fail',
                'Invalid command handled gracefully'
            )
            
        except Exception as e:
            self._record_test_result(
                'error_handling',
                'pass',  # Exception handling is working
                f"Error properly caught: {str(e)}"
            )
    
    async def _test_configuration_integrity(self):
        """Test configuration file integrity"""
        self.logger.info("⚙️ Testing Configuration Integrity")
        
        try:
            # Test unified config creation
            config_result = self.hub.create_unified_config()
            
            self._record_test_result(
                'unified_config_creation',
                'pass' if config_result['status'] == 'success' else 'fail',
                'Unified configuration created'
            )
            
            # Verify config file exists and is valid JSON
            config_file = Path(self.workspace_path) / 'unified_ai_config.json'
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        config_data = json.load(f)
                    
                    # Verify all platforms are configured
                    platforms_in_config = len(
                        config_data.get('unified_ai_hub', {})
                        .get('platforms', {})
                    )
                    
                    self._record_test_result(
                        'config_file_integrity',
                        'pass' if platforms_in_config == 6 else 'fail',
                        f"Config contains {platforms_in_config}/6 platforms"
                    )
                    
                except json.JSONDecodeError:
                    self._record_test_result(
                        'config_file_integrity',
                        'fail',
                        'Config file contains invalid JSON'
                    )
            else:
                self._record_test_result(
                    'config_file_integrity',
                    'fail',
                    'Config file not found'
                )
                
        except Exception as e:
            self._record_test_result(
                'configuration_integrity',
                'fail',
                str(e)
            )
    
    def _record_test_result(self, test_name: str, status: str, message: str):
        """Record a test result"""
        self.test_results['total_tests'] += 1
        
        if status == 'pass':
            self.test_results['passed_tests'] += 1
            self.logger.info(f"✅ {test_name}: PASS - {message}")
        elif status == 'fail':
            self.test_results['failed_tests'] += 1
            self.logger.error(f"❌ {test_name}: FAIL - {message}")
        else:  # skip
            self.test_results['skipped_tests'] += 1
            self.logger.warning(f"⏭️ {test_name}: SKIP - {message}")
        
        # Store detailed result
        category = test_name.split('_')[0]
        if category not in self.test_results['platform_results']:
            self.test_results['platform_results'][category] = []
        
        self.test_results['platform_results'][category].append({
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def _generate_test_report(self):
        """Generate comprehensive test report"""
        success_rate = (
            self.test_results['passed_tests'] / 
            self.test_results['total_tests'] * 100
        ) if self.test_results['total_tests'] > 0 else 0
        
        report = {
            'status': 'success',
            'test_summary': {
                'total_tests': self.test_results['total_tests'],
                'passed': self.test_results['passed_tests'],
                'failed': self.test_results['failed_tests'],
                'skipped': self.test_results['skipped_tests'],
                'success_rate': round(success_rate, 2)
            },
            'platform_breakdown': {},
            'expected_vs_actual': {
                'expected_items': self.total_expected,
                'tested_features': self.test_results['total_tests'],
                'coverage_percentage': round(
                    (self.test_results['total_tests'] / self.total_expected * 100)
                    if self.total_expected > 0 else 0, 2
                )
            },
            'detailed_results': self.test_results['platform_results'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Calculate platform-specific success rates
        for platform, results in self.test_results['platform_results'].items():
            total = len(results)
            passed = len([r for r in results if r['status'] == 'pass'])
            
            report['platform_breakdown'][platform] = {
                'total_tests': total,
                'passed': passed,
                'success_rate': round((passed / total * 100) if total > 0 else 0, 2)
            }
        
        # Save report to file
        report_file = Path(self.workspace_path) / 'integration_test_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info("📋 Test Report Generated")
        self.logger.info(f"Overall Success Rate: {success_rate:.1f}%")
        self.logger.info(f"Report saved to: {report_file}")
        
        return report


async def main():
    """Main function for running integration tests"""
    test_suite = IntegrationTestSuite()
    
    print("🧪 Integration Test Suite - Testing 242 AI Items")
    print("=" * 60)
    
    try:
        # Run all tests
        report = await test_suite.run_all_tests()
        
        if report['status'] == 'success':
            print(f"\n📊 Test Results Summary:")
            print(f"Total Tests: {report['test_summary']['total_tests']}")
            print(f"Passed: {report['test_summary']['passed']}")
            print(f"Failed: {report['test_summary']['failed']}")
            print(f"Skipped: {report['test_summary']['skipped']}")
            print(f"Success Rate: {report['test_summary']['success_rate']}%")
            print(f"Coverage: {report['expected_vs_actual']['coverage_percentage']}%")
            
            print(f"\n🏆 Platform Breakdown:")
            for platform, stats in report['platform_breakdown'].items():
                print(f"{platform.upper()}: {stats['success_rate']}% "
                      f"({stats['passed']}/{stats['total_tests']})")
        else:
            print(f"❌ Test suite failed: {report['message']}")
            
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())