"""
Integration Workflow Test Suite
Tests the complete workflow across Cursor, Bolt.diy, Firebase, and Trae.ai
"""

import asyncio
import json
import logging
import time
from pathlib import Path

from cursor_integration import CursorIntegration
from bolt_integration import BoltDIYIntegration
from firebase_integration import FirebaseIntegration
from trae_integration import TraeIntegration
from sync_manager import initialize_sync_system


class IntegrationWorkflowTest:
    """Test suite for the complete integration workflow"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.test_results = []
        self.platforms = {}
        self.sync_manager = None
        
    def setup_logging(self):
        """Setup logging for tests"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def ai_ceo_callback(self, event):
        """Mock AI CEO callback for testing"""
        self.logger.info(f"AI CEO Event: {event}")
    
    async def setup_platforms(self):
        """Initialize all platform integrations"""
        try:
            # Initialize platforms
            self.platforms = {
                'cursor': CursorIntegration(self.ai_ceo_callback),
                'bolt': BoltDIYIntegration(self.ai_ceo_callback),
                'firebase': FirebaseIntegration(self.ai_ceo_callback),
                'trae': TraeIntegration(self.ai_ceo_callback)
            }
            
            # Initialize sync system
            self.sync_manager = initialize_sync_system(self.platforms)
            
            self.logger.info("All platforms initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"Platform setup failed: {str(e)}")
            return False
    
    async def test_platform_connections(self):
        """Test connections to all platforms"""
        test_name = "Platform Connections"
        self.logger.info(f"Testing: {test_name}")
        
        results = {}
        
        for name, platform in self.platforms.items():
            try:
                result = platform.connect()
                results[name] = result['status'] == 'success'
                self.logger.info(f"{name}: {result['status']}")
                
            except Exception as e:
                results[name] = False
                self.logger.error(f"{name} connection failed: {str(e)}")
        
        success = all(results.values())
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': results
        })
        
        return success
    
    async def test_project_initialization(self):
        """Test project initialization across platforms"""
        test_name = "Project Initialization"
        self.logger.info(f"Testing: {test_name}")
        
        test_project_path = "/tmp/test_integration_project"
        Path(test_project_path).mkdir(exist_ok=True)
        
        results = {}
        
        for name, platform in self.platforms.items():
            try:
                if hasattr(platform, 'initialize_project'):
                    result = platform.initialize_project(test_project_path)
                    results[name] = result['status'] == 'success'
                else:
                    results[name] = True  # Skip if not applicable
                    
            except Exception as e:
                results[name] = False
                self.logger.error(f"{name} initialization failed: {str(e)}")
        
        success = all(results.values())
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': results
        })
        
        return success
    
    async def test_code_generation_workflow(self):
        """Test code generation and optimization workflow"""
        test_name = "Code Generation Workflow"
        self.logger.info(f"Testing: {test_name}")
        
        try:
            # Test Trae.ai code generation
            trae = self.platforms['trae']
            gen_result = trae.generate_code(
                "Create a React component for user profile"
            )
            
            if gen_result['status'] != 'success':
                raise Exception("Code generation failed")
            
            # Test code optimization
            test_file = "/tmp/test_code.js"
            with open(test_file, 'w') as f:
                f.write(gen_result['code'])
            
            opt_result = trae.optimize_code(test_file)
            
            success = opt_result['status'] == 'success'
            
        except Exception as e:
            success = False
            self.logger.error(f"Code workflow failed: {str(e)}")
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': {'generation': gen_result, 'optimization': opt_result}
        })
        
        return success
    
    async def test_deployment_workflow(self):
        """Test deployment workflow through Bolt.diy"""
        test_name = "Deployment Workflow"
        self.logger.info(f"Testing: {test_name}")
        
        try:
            bolt = self.platforms['bolt']
            
            # Test rapid prototyping with correct parameters
            proto_result = bolt.create_rapid_prototype('react', 'test-app')
            
            success = proto_result['status'] == 'success'
            
            # Test Firebase hosting deployment
            firebase = self.platforms['firebase']
            hosting_result = firebase.deploy_hosting('/tmp/test_project')
            
            success = success and hosting_result['status'] == 'success'
            
        except Exception as e:
            success = False
            proto_result = {'error': str(e)}
            self.logger.error(f"Deployment workflow failed: {str(e)}")
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': proto_result
        })
        
        return success
    
    async def test_firebase_integration(self):
        """Test Firebase backend integration"""
        test_name = "Firebase Integration"
        self.logger.info(f"Testing: {test_name}")
        
        try:
            firebase = self.platforms['firebase']
            
            # Test Firestore setup
            firestore_result = firebase.setup_firestore()
            
            success = firestore_result['status'] == 'success'
            
        except Exception as e:
            success = False
            firestore_result = {'error': str(e)}
            self.logger.error(f"Firebase integration failed: {str(e)}")
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': firestore_result
        })
        
        return success
    
    async def test_sync_system(self):
        """Test real-time sync system"""
        test_name = "Sync System"
        self.logger.info(f"Testing: {test_name}")
        
        try:
            # Test sync manager status
            status = self.sync_manager.get_sync_status()
            
            # Test sync event
            test_event = {
                'type': 'file_changed',
                'source_platform': 'cursor',
                'data': {'file': 'test.js', 'action': 'modified'}
            }
            
            self.sync_manager.trigger_sync(test_event)
            
            # Wait a moment for processing
            await asyncio.sleep(1)
            
            success = status['service_running']
            
        except Exception as e:
            success = False
            status = {'error': str(e)}
            self.logger.error(f"Sync system test failed: {str(e)}")
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': status
        })
        
        return success
    
    async def test_ai_ceo_communication(self):
        """Test AI CEO communication across platforms"""
        test_name = "AI CEO Communication"
        self.logger.info(f"Testing: {test_name}")
        
        try:
            # Test AI CEO sync from each platform
            results = {}
            
            for name, platform in self.platforms.items():
                if hasattr(platform, 'sync_with_ai_ceo'):
                    if name in ['firebase', 'trae']:
                        # Firebase and Trae require data parameter
                        test_data = {'event': 'test', 'timestamp': time.time()}
                        result = platform.sync_with_ai_ceo(test_data)
                    else:
                        # Other platforms don't require parameters
                        result = platform.sync_with_ai_ceo()
                    results[name] = result['status'] == 'success'
                else:
                    results[name] = True  # Skip if not applicable
            
            success = all(results.values())
            
        except Exception as e:
            success = False
            results = {'error': str(e)}
            self.logger.error(f"AI CEO communication failed: {str(e)}")
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': results
        })
        
        return success
    
    async def run_all_tests(self):
        """Run the complete test suite"""
        self.setup_logging()
        self.logger.info("Starting Integration Workflow Tests")
        
        # Setup
        if not await self.setup_platforms():
            self.logger.error("Platform setup failed - aborting tests")
            return False
        
        # Run tests
        tests = [
            self.test_platform_connections,
            self.test_project_initialization,
            self.test_code_generation_workflow,
            self.test_deployment_workflow,
            self.test_firebase_integration,
            self.test_sync_system,
            self.test_ai_ceo_communication
        ]
        
        for test in tests:
            try:
                await test()
                await asyncio.sleep(0.5)  # Brief pause between tests
            except Exception as e:
                self.logger.error(f"Test {test.__name__} failed: {str(e)}")
        
        # Generate report
        self.generate_test_report()
        
        # Return overall success
        return all(result['success'] for result in self.test_results)
    
    def generate_test_report(self):
        """Generate and save test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['success'])
        
        report = {
            'timestamp': time.time(),
            'summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': total_tests - passed_tests,
                'success_rate': f"{(passed_tests/total_tests)*100:.1f}%"
            },
            'results': self.test_results
        }
        
        # Save report
        report_file = Path("integration_test_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        self.logger.info("=" * 50)
        self.logger.info("INTEGRATION TEST REPORT")
        self.logger.info("=" * 50)
        self.logger.info(f"Total Tests: {total_tests}")
        self.logger.info(f"Passed: {passed_tests}")
        self.logger.info(f"Failed: {total_tests - passed_tests}")
        self.logger.info(f"Success Rate: {report['summary']['success_rate']}")
        self.logger.info(f"Report saved to: {report_file}")
        self.logger.info("=" * 50)


async def main():
    """Main test runner"""
    test_suite = IntegrationWorkflowTest()
    success = await test_suite.run_all_tests()
    
    if success:
        print("✅ All integration tests passed!")
        return 0
    else:
        print("❌ Some integration tests failed!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)