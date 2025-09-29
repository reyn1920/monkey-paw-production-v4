#!/usr/bin/env python3
"""
Guardian Agent - The Final Protocol for AI Self-Critique

The Guardian is a higher-level agent whose only job is to be skeptical.
It supervises the "worker" agent and validates its results against the ground truth
of the pytest command, creating a self-healing, self-critiquing loop.
"""

import subprocess
import re
from pathlib import Path
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TestResult:
    """Represents the result of running the test suite."""
    passed: int
    failed: int
    errors: int
    warnings: int
    skipped: int
    total_time: float
    exit_code: int
    raw_output: str
    summary_line: str


class GuardianAgent:
    """
    An agent that supervises and validates the work of other AI agents.
    
    The Guardian enforces the ground truth by running the full test suite
    and rejecting any "fixes" that don't actually resolve the issues.
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the Guardian Agent.
        
        Args:
            project_root: Path to the project root. Defaults to current working directory.
        """
        self.project_root = project_root or Path.cwd()
        self.validation_history: list[TestResult] = []
        
    def get_ground_truth(self, timeout: int = 60) -> TestResult:
        """
        Runs the full test suite to get the real number of failures and errors.
        
        This is the source of truth that cannot be argued with or hallucinated away.
        
        Args:
            timeout: Maximum time to wait for tests to complete (default: 60 seconds)
        
        Returns:
            TestResult: Complete test execution results
        """
        print("🛡️ [Guardian] Running ground truth validation...")
        
        start_time = datetime.now()
        
        try:
            # Run pytest with comprehensive output
            result = subprocess.run(
                ["python3", "-m", "pytest", "tests/", "-v", "--tb=short", "--no-header"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=timeout
            )
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            output = result.stdout + result.stderr
            
        except subprocess.TimeoutExpired as e:
            print(f"⚠️ [Guardian] Test execution timed out after {timeout} seconds")
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Create a timeout result
            output = f"TIMEOUT: Test execution exceeded {timeout} seconds\n"
            if e.stdout:
                output += e.stdout.decode() if isinstance(e.stdout, bytes) else str(e.stdout)
            if e.stderr:
                output += e.stderr.decode() if isinstance(e.stderr, bytes) else str(e.stderr)
            
            # Create a proper result object with returncode attribute
            class MockResult:
                def __init__(self, returncode: int):
                    self.returncode = returncode
                    self.stdout = ""
                    self.stderr = output
            
            result = MockResult(-1)
            
        except Exception as e:
            print(f"❌ [Guardian] Error running tests: {e}")
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            output = f"ERROR: {str(e)}"
            
            # Create a proper result object with returncode attribute
            class MockResult:
                def __init__(self, returncode: int):
                    self.returncode = returncode
                    self.stdout = ""
                    self.stderr = output
            
            result = MockResult(-1)
        
        # Parse pytest output for detailed results
        test_result = self._parse_pytest_output(output, result.returncode, execution_time)
        
        # Store in validation history
        self.validation_history.append(test_result)
        
        return test_result
    
    def _parse_pytest_output(self, output: str, exit_code: int, execution_time: float) -> TestResult:
        """
        Parse pytest output to extract detailed test results.
        
        Args:
            output: Raw pytest output
            exit_code: Process exit code
            execution_time: Test execution time in seconds
            
        Returns:
            TestResult: Parsed test results
        """
        # Initialize counters
        passed = failed = errors = warnings = skipped = 0
        summary_line = ""
        
        # Look for the final summary line
        summary_patterns = [
            r'=+ (\d+) failed.*?(\d+) passed.*?in ([\d.]+)s =+',
            r'=+ (\d+) passed.*?in ([\d.]+)s =+',
            r'=+ (\d+) error.*?in ([\d.]+)s =+',
            r'=+ FAILURES =+',
            r'=+ (\d+) passed, (\d+) warning.*?in ([\d.]+)s =+',
        ]
        
        lines = output.split('\n')
        
        # Find summary line (usually near the end)
        for line in reversed(lines):
            if 'passed' in line or 'failed' in line or 'error' in line:
                if '==' in line:  # This is likely the summary line
                    summary_line = line.strip()
                    break
        
        # Parse the summary line for counts
        if summary_line:
            # Extract numbers from summary
            numbers = re.findall(r'(\d+)', summary_line)
            
            if 'failed' in summary_line and 'passed' in summary_line:
                if len(numbers) >= 2:
                    failed = int(numbers[0])
                    passed = int(numbers[1])
            elif 'passed' in summary_line and 'failed' not in summary_line:
                if numbers:
                    passed = int(numbers[0])
            elif 'error' in summary_line:
                if numbers:
                    errors = int(numbers[0])
        
        # Count warnings
        warning_count = len(re.findall(r'warning', output, re.IGNORECASE))
        warnings = warning_count
        
        # If we couldn't parse the summary, try counting individual test results
        if passed == 0 and failed == 0 and errors == 0:
            passed = len(re.findall(r'PASSED', output))
            failed = len(re.findall(r'FAILED', output))
            errors = len(re.findall(r'ERROR', output))
            skipped = len(re.findall(r'SKIPPED', output))
        
        return TestResult(
            passed=passed,
            failed=failed,
            errors=errors,
            warnings=warnings,
            skipped=skipped,
            total_time=execution_time,
            exit_code=exit_code,
            raw_output=output,
            summary_line=summary_line or "No summary found"
        )
    
    def supervise_task(self, worker_task: Callable[[], Any], task_description: str = "Unknown task") -> bool:
        """
        Supervises a worker agent's task, demanding actual success.
        
        Args:
            worker_task: The function/task to be supervised
            task_description: Description of what the task is supposed to accomplish
            
        Returns:
            bool: True if the task actually succeeded, False otherwise
        """
        print(f"🛡️ [Guardian] Supervising worker agent: {task_description}")
        
        # Get baseline ground truth before the task
        print("🛡️ [Guardian] Establishing baseline ground truth...")
        baseline = self.get_ground_truth()
        
        print(f"📊 [Guardian] Baseline: {baseline.passed} passed, {baseline.failed} failed, {baseline.errors} errors")
        
        # Execute the worker task
        print("🔧 [Guardian] Executing worker task...")
        try:
            worker_result = worker_task()
            print(f"✅ [Guardian] Worker task completed. Worker reported: {worker_result}")
        except Exception as e:
            print(f"❌ [Guardian] Worker task failed with exception: {e}")
            return False
        
        # Get ground truth after the task
        print("🛡️ [Guardian] Verifying ground truth after task completion...")
        final_result = self.get_ground_truth()
        
        print(f"📊 [Guardian] Final result: {final_result.passed} passed, {final_result.failed} failed, {final_result.errors} errors")
        
        # Analyze the results
        success = self._analyze_results(baseline, final_result, task_description)
        
        if success:
            print("✅🎉 [Guardian] SUCCESS! Ground truth confirms the task was completed successfully.")
            print(f"📈 [Guardian] Improvement: {final_result.failed - baseline.failed} fewer failures, {final_result.errors - baseline.errors} fewer errors")
        else:
            print("❌ [Guardian] FAILURE! Task did not achieve the expected improvement.")
            print(f"📉 [Guardian] Current state: {final_result.failed} failures, {final_result.errors} errors")
            print("🚨 [Guardian] The agent may be hallucinating success. A full architectural review is required.")
        
        return success
    
    def _analyze_results(self, baseline: TestResult, final: TestResult, task_description: str) -> bool:
        """
        Analyze test results to determine if the task actually succeeded.
        
        Args:
            baseline: Test results before the task
            final: Test results after the task
            task_description: Description of the task
            
        Returns:
            bool: True if the task succeeded, False otherwise
        """
        # Perfect success: no failures or errors
        if final.failed == 0 and final.errors == 0:
            return True
        
        # Improvement: fewer failures/errors than baseline
        if final.failed < baseline.failed or final.errors < baseline.errors:
            # Partial success - some improvement but not complete
            improvement = (baseline.failed - final.failed) + (baseline.errors - final.errors)
            print(f"📈 [Guardian] Partial success: {improvement} fewer issues, but {final.failed + final.errors} remain")
            return final.failed + final.errors == 0  # Only consider complete success
        
        # No improvement or regression
        if final.failed >= baseline.failed and final.errors >= baseline.errors:
            return False
        
        return False
    
    def get_validation_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive validation report.
        
        Returns:
            Dict containing validation history and analysis
        """
        if not self.validation_history:
            return {"status": "no_validations", "message": "No validations performed yet"}
        
        latest = self.validation_history[-1]
        
        return {
            "status": "success" if latest.failed == 0 and latest.errors == 0 else "issues_detected",
            "latest_result": {
                "passed": latest.passed,
                "failed": latest.failed,
                "errors": latest.errors,
                "warnings": latest.warnings,
                "execution_time": latest.total_time,
                "summary": latest.summary_line
            },
            "total_validations": len(self.validation_history),
            "trend": self._analyze_trend() if len(self.validation_history) > 1 else "insufficient_data"
        }
    
    def _analyze_trend(self) -> str:
        """Analyze the trend in test results over time."""
        if len(self.validation_history) < 2:
            return "insufficient_data"
        
        recent = self.validation_history[-1]
        previous = self.validation_history[-2]
        
        recent_issues = recent.failed + recent.errors
        previous_issues = previous.failed + previous.errors
        
        if recent_issues < previous_issues:
            return "improving"
        elif recent_issues > previous_issues:
            return "degrading"
        else:
            return "stable"


# Example usage and integration
def example_worker_task():
    """Example worker task that claims to fix something."""
    print("🔧 [Worker] Attempting to fix the authentication service...")
    # This would be where the actual fix happens
    return "Fixed generate_token method in AuthenticationService"


if __name__ == "__main__":
    # Example of how to use the Guardian Agent
    guardian = GuardianAgent()
    
    # Supervise a worker task
    success = guardian.supervise_task(
        example_worker_task,
        "Fix missing generate_token method in AuthenticationService"
    )
    
    # Get validation report
    report = guardian.get_validation_report()
    print(f"\n📋 [Guardian] Validation Report: {report}")
    
    if not success:
        print("\n🚨 [Guardian] CRITICAL: The worker agent has failed to complete the task successfully.")
        print("🔄 [Guardian] Recommendation: Re-run the worker task or perform manual intervention.")