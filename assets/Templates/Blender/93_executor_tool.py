#!/usr/bin/env python3
"""
Deterministic Executor Tool for Debug Agent
Provides safe, controlled execution of code with comprehensive logging and error handling.
"""

import subprocess
import sys
import os
import tempfile
import json
import time
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import traceback
from dataclasses import dataclass
from enum import Enum


class ExecutionStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class ExecutionResult:
    status: ExecutionStatus
    stdout: str
    stderr: str
    exit_code: int
    execution_time: float
    command: str
    working_directory: str
    environment_vars: Dict[str, str]
    timestamp: str
    error_details: Optional[str] = None


class DeterministicExecutor:
    """
    A deterministic executor that provides safe, controlled execution of commands
    with comprehensive logging and error handling.
    """

    def __init__(self, timeout: int = 300, max_output_size: int = 1024 * 1024):
        self.timeout = timeout
        self.max_output_size = max_output_size
        self.execution_history: List[ExecutionResult] = []

    def execute_command(
        self,
        command: str,
        working_dir: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
        shell: bool = True,
    ) -> ExecutionResult:
        """
        Execute a command with comprehensive logging and error handling.

        Args:
            command: The command to execute
            working_dir: Working directory for execution
            env_vars: Additional environment variables
            shell: Whether to use shell execution

        Returns:
            ExecutionResult with comprehensive execution details
        """
        start_time = time.time()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Set up environment
        env = os.environ.copy()
        if env_vars:
            env.update(env_vars)

        # Set working directory
        if working_dir is None:
            working_dir = os.getcwd()
        working_dir = str(Path(working_dir).resolve())

        try:
            # Execute command
            process = subprocess.Popen(
                command,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=working_dir,
                env=env,
            )

            try:
                stdout, stderr = process.communicate(timeout=self.timeout)
                exit_code = process.returncode
                status = (
                    ExecutionStatus.SUCCESS
                    if exit_code == 0
                    else ExecutionStatus.FAILURE
                )
                error_details = None

            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                exit_code = -1
                status = ExecutionStatus.TIMEOUT
                error_details = f"Command timed out after {self.timeout} seconds"

        except Exception as e:
            stdout = ""
            stderr = str(e)
            exit_code = -1
            status = ExecutionStatus.ERROR
            error_details = f"Execution error: {str(e)}\n{traceback.format_exc()}"

        execution_time = time.time() - start_time

        # Truncate output if too large
        if len(stdout) > self.max_output_size:
            stdout = stdout[: self.max_output_size] + "\n... (output truncated)"
        if len(stderr) > self.max_output_size:
            stderr = stderr[: self.max_output_size] + "\n... (output truncated)"

        result = ExecutionResult(
            status=status,
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            execution_time=execution_time,
            command=command,
            working_directory=working_dir,
            environment_vars=env_vars or {},
            timestamp=timestamp,
            error_details=error_details,
        )

        self.execution_history.append(result)
        return result

    def execute_python_code(
        self,
        code: str,
        working_dir: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> ExecutionResult:
        """
        Execute Python code safely in a temporary file.

        Args:
            code: Python code to execute
            working_dir: Working directory for execution
            env_vars: Additional environment variables

        Returns:
            ExecutionResult with execution details
        """
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            command = f"{sys.executable} {temp_file}"
            result = self.execute_command(command, working_dir, env_vars, shell=True)
            return result
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
            except OSError:
                pass

    def run_tests(
        self,
        test_command: str = "python -m pytest tests/ -v",
        working_dir: Optional[str] = None,
    ) -> ExecutionResult:
        """
        Run tests with standardized reporting.

        Args:
            test_command: Command to run tests
            working_dir: Working directory for test execution

        Returns:
            ExecutionResult with test execution details
        """
        return self.execute_command(test_command, working_dir)

    def validate_fix(
        self,
        fix_code: str,
        test_command: str = "python -m pytest tests/ -v",
        working_dir: Optional[str] = None,
    ) -> Tuple[ExecutionResult, ExecutionResult]:
        """
        Apply a fix and validate it by running tests.

        Args:
            fix_code: Code containing the fix
            test_command: Command to run tests
            working_dir: Working directory

        Returns:
            Tuple of (fix_execution_result, test_execution_result)
        """
        # Apply the fix
        fix_result = self.execute_python_code(fix_code, working_dir)

        # Run tests to validate
        test_result = self.run_tests(test_command, working_dir)

        return fix_result, test_result

    def get_execution_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all executions.

        Returns:
            Dictionary with execution statistics and history
        """
        if not self.execution_history:
            return {"total_executions": 0, "history": []}

        total = len(self.execution_history)
        successful = sum(
            1 for r in self.execution_history if r.status == ExecutionStatus.SUCCESS
        )
        failed = sum(
            1 for r in self.execution_history if r.status == ExecutionStatus.FAILURE
        )
        errors = sum(
            1 for r in self.execution_history if r.status == ExecutionStatus.ERROR
        )
        timeouts = sum(
            1 for r in self.execution_history if r.status == ExecutionStatus.TIMEOUT
        )

        avg_execution_time = (
            sum(r.execution_time for r in self.execution_history) / total
        )

        return {
            "total_executions": total,
            "successful": successful,
            "failed": failed,
            "errors": errors,
            "timeouts": timeouts,
            "success_rate": successful / total * 100,
            "average_execution_time": avg_execution_time,
            "history": [
                {
                    "timestamp": r.timestamp,
                    "command": r.command,
                    "status": r.status.value,
                    "exit_code": r.exit_code,
                    "execution_time": r.execution_time,
                    "error_details": r.error_details,
                }
                for r in self.execution_history
            ],
        }

    def clear_history(self):
        """Clear execution history."""
        self.execution_history.clear()


# Global executor instance
executor = DeterministicExecutor()


def execute_command(command: str, **kwargs) -> ExecutionResult:
    """Convenience function for command execution."""
    return executor.execute_command(command, **kwargs)


def execute_python_code(code: str, **kwargs) -> ExecutionResult:
    """Convenience function for Python code execution."""
    return executor.execute_python_code(code, **kwargs)


def run_tests(
    test_command: str = "python -m pytest tests/ -v", **kwargs
) -> ExecutionResult:
    """Convenience function for running tests."""
    return executor.run_tests(test_command, **kwargs)


def validate_fix(fix_code: str, **kwargs) -> Tuple[ExecutionResult, ExecutionResult]:
    """Convenience function for validating fixes."""
    return executor.validate_fix(fix_code, **kwargs)


if __name__ == "__main__":
    # Example usage and testing
    print("Testing Deterministic Executor...")

    # Test basic command execution
    result = execute_command("echo 'Hello, World!'")
    print(f"Command execution: {result.status.value}")
    print(f"Output: {result.stdout.strip()}")

    # Test Python code execution
    python_code = """
print("Python code execution test")
import sys
print(f"Python version: {sys.version}")
"""
    result = execute_python_code(python_code)
    print(f"Python execution: {result.status.value}")

    # Print execution summary
    summary = executor.get_execution_summary()
    print(f"Execution summary: {json.dumps(summary, indent=2)}")
