#!/usr/bin/env python3
"""
Guardian Agent Integration Example

This example demonstrates how to use the Guardian Agent to supervise worker agents
and create a self-healing, self-critiquing loop that ensures code fixes actually work.

The Guardian Agent acts as a "conscience" that validates all changes against the
ground truth of the test suite, preventing hallucinations and ensuring reliability.
"""

import sys
from pathlib import Path
from typing import Callable, Any, Dict
from trae_ai.agents.guardian_agent import GuardianAgent


class WorkerAgent:
    """
    Example worker agent that performs code fixes.
    In a real implementation, this would be your main AI coding agent.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.attempts = 0
        self.max_attempts = 3
    
    def fix_authentication_service(self) -> bool:
        """
        Example worker task: Fix authentication service issues.
        This is a mock implementation - replace with your actual worker logic.
        """
        self.attempts += 1
        print(f"🔧 [{self.name}] Attempt {self.attempts}: Fixing authentication service...")
        
        # Simulate different outcomes based on attempt number
        if self.attempts == 1:
            print(f"🔧 [{self.name}] Adding missing generate_token method...")
            # In reality, this would modify actual code files
            return True
        elif self.attempts == 2:
            print(f"🔧 [{self.name}] Fixing token validation logic...")
            return True
        else:
            print(f"🔧 [{self.name}] Implementing proper error handling...")
            return True
    
    def fix_database_connection(self) -> bool:
        """Example worker task: Fix database connection issues."""
        self.attempts += 1
        print(f"🔧 [{self.name}] Attempt {self.attempts}: Fixing database connection...")
        print(f"🔧 [{self.name}] Updating connection pool settings...")
        return True
    
    def reset_attempts(self):
        """Reset attempt counter for new tasks."""
        self.attempts = 0


class GuardianSupervisor:
    """
    High-level supervisor that orchestrates the Guardian Agent and Worker Agents
    to create a self-healing development loop.
    """
    
    def __init__(self, project_root: Path | None = None):
        self.guardian = GuardianAgent()
        self.project_root = project_root if project_root is not None else Path.cwd()
        self.max_iterations = 5
    
    def supervise_worker_task(self, 
                            worker_agent: WorkerAgent, 
                            task_function: Callable[[], bool],
                            task_name: str) -> Dict[str, Any]:
        """
        Supervise a worker agent task with Guardian validation.
        
        Args:
            worker_agent: The worker agent performing the task
            task_function: The specific task function to execute
            task_name: Human-readable name of the task
            
        Returns:
            Dict containing the supervision results
        """
        print(f"\n🛡️ [Guardian Supervisor] Starting supervision of: {task_name}")
        print(f"🛡️ [Guardian Supervisor] Worker: {worker_agent.name}")
        
        # Get initial ground truth
        print("🛡️ [Guardian Supervisor] Establishing baseline ground truth...")
        initial_result = self.guardian.get_ground_truth(timeout=60)
        
        print("📊 Initial State:")
        print(f"   Passed: {initial_result.passed}")
        print(f"   Failed: {initial_result.failed}")
        print(f"   Errors: {initial_result.errors}")
        
        iteration = 0
        worker_agent.reset_attempts()
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n🔄 [Guardian Supervisor] Iteration {iteration}/{self.max_iterations}")
            
            # Worker agent attempts the fix
            try:
                success = task_function()
                if not success:
                    print(f"❌ [Guardian Supervisor] Worker reported failure on attempt {iteration}")
                    continue
                    
            except Exception as e:
                print(f"❌ [Guardian Supervisor] Worker encountered error: {e}")
                continue
            
            # Guardian validates the fix
            print("🛡️ [Guardian Supervisor] Validating worker's changes...")
            validation_result = self.guardian.get_ground_truth(timeout=60)
            
            print("📊 Post-Fix State:")
            print(f"   Passed: {validation_result.passed}")
            print(f"   Failed: {validation_result.failed}")
            print(f"   Errors: {validation_result.errors}")
            
            # Check if the fix improved the situation
            if validation_result.failed == 0 and validation_result.errors == 0:
                print("✅ [Guardian Supervisor] SUCCESS! All tests passing.")
                print(f"🎉 [Guardian Supervisor] Task '{task_name}' completed successfully in {iteration} iterations.")
                
                return {
                    "status": "success",
                    "iterations": iteration,
                    "initial_state": {
                        "passed": initial_result.passed,
                        "failed": initial_result.failed,
                        "errors": initial_result.errors
                    },
                    "final_state": {
                        "passed": validation_result.passed,
                        "failed": validation_result.failed,
                        "errors": validation_result.errors
                    },
                    "improvement": {
                        "passed_delta": validation_result.passed - initial_result.passed,
                        "failed_delta": initial_result.failed - validation_result.failed,
                        "errors_delta": initial_result.errors - validation_result.errors
                    }
                }
            
            elif validation_result.failed < initial_result.failed or validation_result.errors < initial_result.errors:
                print("📈 [Guardian Supervisor] Partial improvement detected, continuing...")
                initial_result = validation_result  # Update baseline
                
            else:
                print("❌ [Guardian Supervisor] No improvement or regression detected.")
                print("🔄 [Guardian Supervisor] Instructing worker to try again...")
        
        # Max iterations reached without success
        print(f"⚠️ [Guardian Supervisor] Maximum iterations ({self.max_iterations}) reached without full success.")
        
        final_result = self.guardian.get_ground_truth(timeout=60)
        return {
            "status": "partial" if final_result.failed < initial_result.failed else "failed",
            "iterations": self.max_iterations,
            "initial_state": {
                "passed": initial_result.passed,
                "failed": initial_result.failed,
                "errors": initial_result.errors
            },
            "final_state": {
                "passed": final_result.passed,
                "failed": final_result.failed,
                "errors": final_result.errors
            }
        }
    
    def run_full_system_validation(self) -> Dict[str, Any]:
        """
        Run a comprehensive system validation using the Guardian Agent.
        This can be used as a final check before deployment.
        """
        print("\n🛡️ [Guardian Supervisor] Running full system validation...")
        
        result = self.guardian.get_ground_truth(timeout=120)
        report = self.guardian.get_validation_report()
        
        print("📊 System Validation Results:")
        print(f"   Status: {report['status']}")
        print(f"   Passed: {result.passed}")
        print(f"   Failed: {result.failed}")
        print(f"   Errors: {result.errors}")
        print(f"   Warnings: {result.warnings}")
        print(f"   Execution Time: {result.total_time:.2f}s")
        
        if result.failed == 0 and result.errors == 0:
            print("✅ [Guardian Supervisor] System is ready for deployment!")
        else:
            print("❌ [Guardian Supervisor] System has issues that need resolution.")
        
        return {
            "ready_for_deployment": result.failed == 0 and result.errors == 0,
            "test_results": {
                "passed": result.passed,
                "failed": result.failed,
                "errors": result.errors,
                "warnings": result.warnings,
                "execution_time": result.total_time
            },
            "guardian_report": report
        }


def example_integration_workflow():
    """
    Example workflow showing how to integrate Guardian Agent supervision
    into your development process.
    """
    print("🚀 Guardian Agent Integration Example")
    print("=" * 50)
    
    # Initialize components
    supervisor = GuardianSupervisor()
    worker = WorkerAgent("TrueAI-Worker-v1")
    
    # Example 1: Supervise authentication service fix
    print("\n📋 Example 1: Supervised Authentication Service Fix")
    auth_result = supervisor.supervise_worker_task(
        worker_agent=worker,
        task_function=worker.fix_authentication_service,
        task_name="Fix Authentication Service"
    )
    
    print("\n📊 Authentication Fix Results:")
    print(f"   Status: {auth_result['status']}")
    print(f"   Iterations: {auth_result['iterations']}")
    
    # Example 2: Supervise database connection fix
    print("\n📋 Example 2: Supervised Database Connection Fix")
    db_result = supervisor.supervise_worker_task(
        worker_agent=worker,
        task_function=worker.fix_database_connection,
        task_name="Fix Database Connection"
    )
    
    print("\n📊 Database Fix Results:")
    print(f"   Status: {db_result['status']}")
    print(f"   Iterations: {db_result['iterations']}")
    
    # Example 3: Full system validation
    print("\n📋 Example 3: Full System Validation")
    validation_result = supervisor.run_full_system_validation()
    
    print("\n🎯 Final System Status:")
    print(f"   Ready for Deployment: {validation_result['ready_for_deployment']}")
    print(f"   Total Tests: {validation_result['test_results']['passed'] + validation_result['test_results']['failed']}")
    
    return {
        "auth_fix": auth_result,
        "db_fix": db_result,
        "system_validation": validation_result
    }


if __name__ == "__main__":
    """
    Run the integration example.
    
    This demonstrates the Guardian Agent protocol in action:
    1. Worker agents propose fixes
    2. Guardian validates against ground truth (pytest)
    3. Self-healing loop continues until success
    4. Final validation ensures deployment readiness
    """
    
    try:
        results = example_integration_workflow()
        
        print("\n🎉 Integration Example Completed!")
        print("=" * 50)
        
        # Summary
        all_successful = all(
            result.get('status') == 'success' 
            for result in [results['auth_fix'], results['db_fix']]
        )
        
        deployment_ready = results['system_validation']['ready_for_deployment']
        
        print("📊 Summary:")
        print(f"   All Fixes Successful: {all_successful}")
        print(f"   Deployment Ready: {deployment_ready}")
        
        if all_successful and deployment_ready:
            print("✅ System is fully validated and ready for production!")
        else:
            print("⚠️ System requires additional work before deployment.")
            
    except Exception as e:
        print(f"❌ Integration example failed: {e}")
        sys.exit(1)