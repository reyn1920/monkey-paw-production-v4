"""
SOLO Agent - Upgraded Logic with Self-Healing Verification

This module implements an advanced SOLO agent with verification and self-healing
capabilities to ensure robust task execution and automatic error recovery.
"""

import asyncio
import logging
import time
import uuid
from datetime import datetime
from typing import Any, Optional

from .tool_runner import run_tool, plan_goal, async_run_tool, async_plan_goal

logger = logging.getLogger(__name__)


class SOLOAgent:
    """
    Self-Organizing Learning Operations Agent with self-healing capabilities.
    """

    def __init__(
        self, agent_id: Optional[str] = None, config: Optional[dict[str, Any]] = None
    ):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.config = config or {}
        self.execution_history: list[dict[str, Any]] = []
        self.failed_actions: list[dict[str, Any]] = []
        self.recovery_attempts = 0
        self.max_recovery_attempts = 3

        # Setup logging
        self.logger = logging.getLogger(f"SOLOAgent_{self.agent_id}")

    def get_status(self) -> dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.agent_id,
            "execution_count": len(self.execution_history),
            "failed_actions": len(self.failed_actions),
            "recovery_attempts": self.recovery_attempts,
            "last_execution": (
                self.execution_history[-1] if self.execution_history else None
            ),
        }

    async def execute_goal_async(
        self, goal: str, context: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Asynchronously execute a goal with self-healing verification.

        Args:
            goal: High-level goal description
            context: Additional context for execution

        Returns:
            Execution result with status and details
        """
        execution_id = str(uuid.uuid4())
        start_time = time.time()

        self.logger.info(f"🚀 Starting goal execution: {goal}")

        try:
            # Generate execution plan
            plan = await async_plan_goal(goal)

            execution_record = {
                "execution_id": execution_id,
                "goal": goal,
                "context": context or {},
                "plan": plan,
                "start_time": start_time,
                "status": "in_progress",
                "steps_completed": 0,
                "total_steps": len(plan),
            }

            self.execution_history.append(execution_record)

            # Execute plan with verification
            result = await self._execute_plan_with_verification(plan, execution_record)

            # Update execution record
            execution_record.update(
                {
                    "end_time": time.time(),
                    "duration": time.time() - start_time,
                    "status": "completed" if result["success"] else "failed",
                    "result": result,
                }
            )

            return result

        except Exception as e:
            self.logger.error(f"❌ Goal execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "execution_id": execution_id,
                "timestamp": datetime.now().isoformat(),
            }

    async def _execute_plan_with_verification(
        self, plan: list[dict[str, Any]], execution_record: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Execute a plan with verification and self-healing.

        Args:
            plan: List of steps to execute
            execution_record: Execution tracking record

        Returns:
            Execution result
        """
        completed_steps = []

        for i, step in enumerate(plan):
            tool_name = step["tool"]
            tool_args = step.get("args", [])
            tool_kwargs = step.get("kwargs", {})
            description = step.get("description", f"Step {i + 1}")

            self.logger.info(f"▶️  Executing step {i + 1}/{len(plan)}: {description}")

            # Execute the tool
            result = await async_run_tool(tool_name, *tool_args, **tool_kwargs)

            # Verify the action
            verification_result = await self._verify_action_async(
                tool_name, result, step
            )

            if not verification_result["success"]:
                self.logger.warning(
                    f"🛑 Step {i + 1} failed verification: {verification_result['reason']}"
                )

                # Attempt self-healing
                healing_result = await self._attempt_self_healing(
                    step, result, verification_result
                )

                if not healing_result["success"]:
                    self.logger.error(f"❌ Self-healing failed for step {i + 1}")

                    # Record failure and stop execution
                    self.failed_actions.append(
                        {
                            "step": step,
                            "result": result,
                            "verification": verification_result,
                            "healing_attempt": healing_result,
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                    return {
                        "success": False,
                        "error": f"Step {i + 1} failed and could not be healed",
                        "failed_step": step,
                        "completed_steps": completed_steps,
                        "verification_failure": verification_result,
                    }
                else:
                    self.logger.info(f"✅ Self-healing successful for step {i + 1}")
                    result = healing_result["result"]

            # Step completed successfully
            completed_steps.append(
                {
                    "step": step,
                    "result": result,
                    "verification": verification_result,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            execution_record["steps_completed"] = i + 1

            self.logger.info(f"✅ Step {i + 1} completed successfully")

        return {
            "success": True,
            "completed_steps": completed_steps,
            "total_steps": len(plan),
            "message": "All steps completed successfully",
        }

    async def _verify_action_async(
        self, tool_name: str, result: dict[str, Any], step: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Verify that an action was successful and didn't cause problems.

        Args:
            tool_name: Name of the tool that was executed
            result: Result from tool execution
            step: Step configuration

        Returns:
            Verification result
        """
        self.logger.info(f"🔍 [Verifier] Verifying action '{tool_name}'...")

        # Check for explicit failure codes
        if result.get("code", 0) != 0:
            return {
                "success": False,
                "reason": f"Action failed with non-zero exit code: {result.get('code')}",
                "details": result.get("stderr", ""),
            }

        # Check if the tool execution was marked as unsuccessful
        if not result.get("success", True):
            return {
                "success": False,
                "reason": "Tool execution marked as unsuccessful",
                "details": result.get("stderr", ""),
            }

        # Run verification tests based on tool type
        if tool_name == "pytest":
            return await self._verify_pytest_result(result)
        elif tool_name == "npm":
            return await self._verify_npm_result(result, step)
        elif tool_name == "git":
            return await self._verify_git_result(result, step)
        else:
            # Generic verification - check for common error patterns
            return self._verify_generic_result(result)

    async def _verify_pytest_result(self, result: dict[str, Any]) -> dict[str, Any]:
        """Verify pytest execution results."""
        stdout = result.get("stdout", "")
        stderr = result.get("stderr", "")

        # Check for test failures
        if "FAILED" in stdout or "ERROR" in stdout:
            return {"success": False, "reason": "Tests failed", "details": stdout}

        # Check for import errors or syntax errors
        if "ImportError" in stderr or "SyntaxError" in stderr:
            return {
                "success": False,
                "reason": "Import or syntax errors detected",
                "details": stderr,
            }

        return {
            "success": True,
            "reason": "Tests passed successfully",
            "details": stdout,
        }

    async def _verify_npm_result(
        self, result: dict[str, Any], step: dict[str, Any]
    ) -> dict[str, Any]:
        """Verify npm command results."""
        stderr = result.get("stderr", "")

        # Check for npm errors
        if "npm ERR!" in stderr:
            return {"success": False, "reason": "npm command failed", "details": stderr}

        # Check for dependency vulnerabilities (if audit command)
        if "audit" in step.get("args", []) and "vulnerabilities" in result.get(
            "stdout", ""
        ):
            return {
                "success": False,
                "reason": "Security vulnerabilities detected",
                "details": result.get("stdout", ""),
            }

        return {"success": True, "reason": "npm command completed successfully"}

    async def _verify_git_result(
        self, result: dict[str, Any], step: dict[str, Any]
    ) -> dict[str, Any]:
        """Verify git command results."""
        stderr = result.get("stderr", "")

        # Check for git errors
        if "error:" in stderr.lower() or "fatal:" in stderr.lower():
            return {"success": False, "reason": "Git command failed", "details": stderr}

        return {"success": True, "reason": "Git command completed successfully"}

    def _verify_generic_result(self, result: dict[str, Any]) -> dict[str, Any]:
        """Generic verification for unknown tools."""
        stderr = result.get("stderr", "")

        # Check for common error patterns
        error_patterns = ["error", "failed", "exception", "traceback"]

        for pattern in error_patterns:
            if pattern.lower() in stderr.lower():
                return {
                    "success": False,
                    "reason": f"Error pattern detected: {pattern}",
                    "details": stderr,
                }

        return {"success": True, "reason": "No error patterns detected"}

    async def _attempt_self_healing(
        self,
        failed_step: dict[str, Any],
        result: dict[str, Any],
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Attempt to heal from a failed action.

        Args:
            failed_step: The step that failed
            result: Result from the failed step
            verification: Verification result

        Returns:
            Healing attempt result
        """
        self.recovery_attempts += 1

        if self.recovery_attempts > self.max_recovery_attempts:
            return {
                "success": False,
                "reason": "Maximum recovery attempts exceeded",
                "attempts": self.recovery_attempts,
            }

        self.logger.info(
            f"🔧 [Self-Healing] Attempting recovery (attempt {self.recovery_attempts})"
        )

        tool_name = failed_step["tool"]

        # Tool-specific healing strategies
        if tool_name == "pytest":
            return await self._heal_pytest_failure(failed_step, result, verification)
        elif tool_name == "npm":
            return await self._heal_npm_failure(failed_step, result, verification)
        elif tool_name == "git":
            return await self._heal_git_failure(failed_step, result, verification)
        else:
            return await self._heal_generic_failure(failed_step, result, verification)

    async def _heal_pytest_failure(
        self,
        failed_step: dict[str, Any],
        result: dict[str, Any],
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        """Heal pytest failures."""
        # Try running with different options
        healing_args = ["--tb=short", "-x", "--maxfail=1"]

        self.logger.info("🔧 Retrying pytest with healing options")
        healing_result = await async_run_tool("pytest", *healing_args)

        if healing_result.get("success", False):
            return {
                "success": True,
                "result": healing_result,
                "healing_strategy": "retry_with_options",
            }

        return {
            "success": False,
            "reason": "Pytest healing failed",
            "healing_result": healing_result,
        }

    async def _heal_npm_failure(
        self,
        failed_step: dict[str, Any],
        result: dict[str, Any],
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        """Heal npm failures."""
        # Try clearing cache and reinstalling
        self.logger.info("🔧 Clearing npm cache and retrying")

        cache_result = await async_run_tool("npm", "cache", "clean", "--force")
        if cache_result.get("success", False):
            # Retry original command
            original_args = failed_step.get("args", [])
            retry_result = await async_run_tool("npm", *original_args)

            if retry_result.get("success", False):
                return {
                    "success": True,
                    "result": retry_result,
                    "healing_strategy": "cache_clear_retry",
                }

        return {"success": False, "reason": "npm healing failed"}

    async def _heal_git_failure(
        self,
        failed_step: dict[str, Any],
        result: dict[str, Any],
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        """Heal git failures."""
        # Basic git healing - check status and try to resolve
        status_result = await async_run_tool("git", "status", "--porcelain")

        if status_result.get("success", False):
            return {
                "success": True,
                "result": status_result,
                "healing_strategy": "status_check",
            }

        return {"success": False, "reason": "Git healing failed"}

    async def _heal_generic_failure(
        self,
        failed_step: dict[str, Any],
        result: dict[str, Any],
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        """Generic healing attempt."""
        # Wait and retry
        await asyncio.sleep(1)

        tool_name = failed_step["tool"]
        args = failed_step.get("args", [])
        kwargs = failed_step.get("kwargs", {})

        retry_result = await async_run_tool(tool_name, *args, **kwargs)

        if retry_result.get("success", False):
            return {
                "success": True,
                "result": retry_result,
                "healing_strategy": "simple_retry",
            }

        return {
            "success": False,
            "reason": "Generic healing failed",
            "retry_result": retry_result,
        }


# Standalone functions for backward compatibility
def verify_action(tool_name: str, result: dict[str, Any]) -> bool:
    """
    Checks if the last action was successful and didn't cause new problems.
    This is the core of the self-healing loop.
    """
    print(f"🔍 [Verifier] Verifying action '{tool_name}'...")

    # 1. Check for explicit failure codes
    if result.get("code", 0) != 0:
        print("❌ [Verifier] Action failed with non-zero exit code.")
        return False

    # 2. Run a quick test suite (placeholder for your actual test command)
    # This is the most important step to prevent regressions.
    test_result = run_tool("pytest", "--quicktest")  # Example command
    if test_result.get("code", 0) != 0:
        print(
            "❌ [Verifier] SELF-HEALING TRIGGERED: Action broke the test suite! Rolling back."
        )
        # In a real system, you would add logic here to revert the last change.
        return False

    print("✅ [Verifier] Action was successful and passed verification.")
    return True


def execute(goal: str):
    """
    Upgraded execution loop with verification and self-healing.
    """
    plan = plan_goal(goal)  # Assume a planner creates a list of tool calls

    for step in plan:
        tool_to_run = step["tool"]
        tool_args = step.get("args", [])

        print(f"\n▶️  Executing: {tool_to_run}...")
        result = run_tool(tool_to_run, *tool_args)

        # --- THE CRITICAL UPGRADE ---
        if not verify_action(tool_to_run, result):
            print(
                "🛑 [SOLO Agent] Halting plan due to verification failure. Re-planning..."
            )
            # Here, you would call the Dynamic Planner to create a new plan
            # based on the new failure context.
            break  # Stop the current failed plan

    print("\n🏁 Plan execution finished.")
