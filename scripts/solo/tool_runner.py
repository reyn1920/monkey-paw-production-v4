"""Tool Runner for SOLO Agent

This module provides functions to execute various tools and generate execution plans
for the SOLO agent system.
"""

import asyncio
import logging
import subprocess
import sys
from typing import Any, Optional

logger = logging.getLogger(__name__)


def run_tool(tool_name: str, *args, **kwargs) -> dict[str, Any]:
    """
    Execute a tool with the given arguments.

    Args:
        tool_name: Name of the tool to execute
        *args: Positional arguments for the tool
        **kwargs: Keyword arguments for the tool

    Returns:
        Dictionary containing execution result
    """
    logger.info(f"🔧 Executing tool: {tool_name} with args: {args}")

    try:
        if tool_name == "pytest":
            return _run_pytest(*args, **kwargs)
        elif tool_name == "npm":
            return _run_npm(*args, **kwargs)
        elif tool_name == "git":
            return _run_git(*args, **kwargs)
        elif tool_name == "python":
            return _run_python(*args, **kwargs)
        elif tool_name == "shell":
            return _run_shell(*args, **kwargs)
        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}", "code": 1}
    except Exception as e:
        logger.error(f"❌ Tool execution failed: {e}")
        return {"success": False, "error": str(e), "code": 1}


def _run_pytest(*args, **kwargs) -> dict[str, Any]:
    """Run pytest with specified arguments."""
    cmd = ["python", "-m", "pytest"] + list(args)

    # Handle common pytest options
    if kwargs.get("quicktest"):
        cmd.extend(["-x", "--tb=short", "-q"])
    if kwargs.get("verbose"):
        cmd.append("-v")
    if kwargs.get("coverage"):
        cmd.extend(["--cov=.", "--cov-report=term-missing"])

    return _execute_command(cmd)


def _run_npm(*args, **kwargs) -> dict[str, Any]:
    """Run npm commands."""
    cmd = ["npm"] + list(args)
    return _execute_command(cmd)


def _run_git(*args, **kwargs) -> dict[str, Any]:
    """Run git commands."""
    cmd = ["git"] + list(args)
    return _execute_command(cmd)


def _run_python(*args, **kwargs) -> dict[str, Any]:
    """Run Python scripts or commands."""
    cmd = [sys.executable] + list(args)
    return _execute_command(cmd)


def _run_shell(*args, **kwargs) -> dict[str, Any]:
    """Run shell commands."""
    if len(args) == 1 and isinstance(args[0], str):
        # Single string command
        return _execute_command(args[0], shell=True)
    else:
        # List of command parts
        return _execute_command(list(args))


def _run_generic_command(tool_name: str, *args, **kwargs) -> dict[str, Any]:
    """Run a generic command."""
    cmd = [tool_name] + list(args)
    return _execute_command(cmd)


def _execute_command(
    cmd: list[str] | str, shell: bool = False, cwd: Optional[str] = None
) -> dict[str, Any]:
    """
    Execute a command and return structured result.

    Args:
        cmd: Command to execute (list or string)
        shell: Whether to use shell execution
        cwd: Working directory for command execution

    Returns:
        Dictionary with execution results
    """
    try:
        logger.info(f"Executing command: {cmd}")

        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=300,  # 5 minute timeout
        )

        return {
            "code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
        }

    except subprocess.TimeoutExpired:
        return {
            "code": 124,  # Timeout exit code
            "stdout": "",
            "stderr": "Command timed out after 5 minutes",
            "success": False,
        }
    except Exception as e:
        return {"code": 1, "stdout": "", "stderr": str(e), "success": False}


def plan_goal(goal: str) -> list[dict[str, Any]]:
    """
    Create an execution plan for achieving a given goal.

    Args:
        goal: High-level goal description

    Returns:
        List of steps/tasks to execute
    """
    logger.info(f"Planning goal: {goal}")

    # Basic goal parsing and planning logic
    goal_lower = goal.lower()
    plan = []

    # Web development goals
    if "web" in goal_lower or "frontend" in goal_lower or "ui" in goal_lower:
        plan.extend(
            [
                {
                    "tool": "npm",
                    "args": ["install"],
                    "description": "Install dependencies",
                },
                {
                    "tool": "npm",
                    "args": ["run", "build"],
                    "description": "Build application",
                },
                {"tool": "npm", "args": ["run", "test"], "description": "Run tests"},
            ]
        )

    # Testing goals
    elif "test" in goal_lower:
        plan.extend(
            [
                {
                    "tool": "pytest",
                    "args": ["--quicktest"],
                    "description": "Run quick tests",
                },
                {"tool": "pytest", "args": ["-v"], "description": "Run verbose tests"},
            ]
        )

    # Deployment goals
    elif "deploy" in goal_lower or "production" in goal_lower:
        plan.extend(
            [
                {
                    "tool": "pytest",
                    "args": ["--quicktest"],
                    "description": "Pre-deployment tests",
                },
                {
                    "tool": "shell",
                    "args": ["./scripts/deploy-production.sh"],
                    "description": "Deploy to production",
                },
                {
                    "tool": "shell",
                    "args": ["./scripts/smoke-tests.sh"],
                    "description": "Post-deployment smoke tests",
                },
            ]
        )

    # Code quality goals
    elif "lint" in goal_lower or "quality" in goal_lower:
        plan.extend(
            [
                {
                    "tool": "python",
                    "args": ["-m", "flake8", "."],
                    "description": "Run linting",
                },
                {
                    "tool": "python",
                    "args": ["-m", "black", "--check", "."],
                    "description": "Check code formatting",
                },
                {
                    "tool": "python",
                    "args": ["-m", "mypy", "."],
                    "description": "Run type checking",
                },
            ]
        )

    # Security goals
    elif "security" in goal_lower or "audit" in goal_lower:
        plan.extend(
            [
                {
                    "tool": "python",
                    "args": ["-m", "safety", "check"],
                    "description": "Security audit",
                },
                {
                    "tool": "python",
                    "args": ["-m", "bandit", "-r", "."],
                    "description": "Security linting",
                },
            ]
        )

    # Generic goals - create a basic plan
    else:
        plan.extend(
            [
                {
                    "tool": "pytest",
                    "args": ["--quicktest"],
                    "description": f"Test current state for: {goal}",
                },
                {
                    "tool": "shell",
                    "args": ["echo", f"Processing goal: {goal}"],
                    "description": "Process goal",
                },
            ]
        )

    logger.info(f"Generated plan with {len(plan)} steps")
    return plan


async def async_run_tool(tool_name: str, *args, **kwargs) -> dict[str, Any]:
    """
    Asynchronously execute a tool with the given arguments.

    Args:
        tool_name: Name of the tool to execute
        *args: Positional arguments for the tool
        **kwargs: Keyword arguments for the tool

    Returns:
        Dictionary containing execution result
    """
    logger.info(f"🔧 Async executing tool: {tool_name} with args: {args}")

    try:
        if tool_name == "pytest":
            return await _async_run_pytest(*args, **kwargs)
        elif tool_name == "npm":
            return await _async_run_npm(*args, **kwargs)
        elif tool_name == "git":
            return await _async_run_git(*args, **kwargs)
        elif tool_name == "python":
            return await _async_run_python(*args, **kwargs)
        elif tool_name == "shell":
            return await _async_run_shell(*args, **kwargs)
        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}", "code": 1}
    except Exception as e:
        logger.error(f"❌ Async tool execution failed: {e}")
        return {"success": False, "error": str(e), "code": 1}


async def _async_run_pytest(*args, **kwargs) -> dict[str, Any]:
    """Async pytest execution."""
    return await _async_run_command("pytest", *args, **kwargs)


async def _async_run_npm(*args, **kwargs) -> dict[str, Any]:
    """Async npm execution."""
    return await _async_run_command("npm", *args, **kwargs)


async def _async_run_git(*args, **kwargs) -> dict[str, Any]:
    """Async git execution."""
    return await _async_run_command("git", *args, **kwargs)


async def _async_run_python(*args, **kwargs) -> dict[str, Any]:
    """Async python execution."""
    return await _async_run_command("python", *args, **kwargs)


async def _async_run_shell(*args, **kwargs) -> dict[str, Any]:
    """Async shell command execution."""
    if args:
        return await _async_run_command(args[0], *args[1:], **kwargs)
    return {"success": False, "error": "No shell command provided", "code": 1}


async def _async_run_command(command: str, *args, **kwargs) -> dict[str, Any]:
    """
    Async command execution using subprocess.

    Args:
        command: Command to execute
        *args: Command arguments
        **kwargs: Additional options

    Returns:
        Execution result dictionary
    """
    try:
        cmd_list = [command] + list(args)

        # Create subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd_list,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=kwargs.get("cwd"),
            env=kwargs.get("env"),
        )

        # Wait for completion
        stdout, stderr = await process.communicate()

        return {
            "success": process.returncode == 0,
            "code": process.returncode,
            "stdout": stdout.decode("utf-8") if stdout else "",
            "stderr": stderr.decode("utf-8") if stderr else "",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "code": 1,
            "stdout": "",
            "stderr": str(e),
        }


async def async_plan_goal(goal: str) -> list[dict[str, Any]]:
    """
    Async wrapper for plan_goal function.

    Args:
        goal: High-level goal description

    Returns:
        List of execution steps
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, plan_goal, goal)
