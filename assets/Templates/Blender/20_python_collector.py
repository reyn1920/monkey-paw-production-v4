# trae_ai/collectors/python_collector.py (Updated)
from functools import wraps
import traceback
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.orchestrator import TaskOrchestrator
from trae_ai.agents.preflight_agent import PreflightAgent  # Import the new agent

_orch = TaskOrchestrator()
_preflight = PreflightAgent()


def monitor(func):
    """Wrap any function for automatic error capture and autonomous correction."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"--- [trae.ai] Error Detected in '{func.__name__}'! ---")

            # --- PRE-FLIGHT CHECK ---
            is_healthy, reason = _preflight.check_environment()
            if not is_healthy:
                print(
                    "--- [trae.ai] Halting autonomous response due to critical infrastructure failure. ---"
                )
                print(f"--- Reason: {reason} ---")
                return  # Stop here to prevent the orchestrator from crashing

            # If healthy, proceed as normal
            error_context = {
                "function_name": func.__name__,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "stack_trace": traceback.format_exc(),
                "inputs": {"args": args, "kwargs": kwargs},
            }
            print("[trae.ai] Engaging Autonomous Correction Protocol...")
            # Create a task for error handling instead of calling handle_error directly
            task_id = _orch.add_task(
                name=f"error_correction_{func.__name__}",
                handler=lambda: print(
                    f"[trae.ai] Error correction task for {error_context['function_name']}: {error_context['error_message']}"
                ),
                metadata=error_context,
            )

    return wrapper
