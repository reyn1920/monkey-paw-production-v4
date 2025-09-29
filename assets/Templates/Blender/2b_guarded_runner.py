from typing import Any, Dict, Callable
from backend.utils.loop_guard import LoopGuard


def GuardedAgentRunner(
    run_step_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
    job_id_fn: Callable[[Dict[str, Any]], str],
    tool_name_resolver: Callable[[Dict[str, Any]], str],
):
    """
    Wrap an agent's single-step function with anti-loop checks.
    No identifier renames required. Add-only.
    """

    def _wrapped(ctx: Dict[str, Any]) -> Dict[str, Any]:
        job_id = job_id_fn(ctx)
        guard = LoopGuard(job_id)
        tool_name = tool_name_resolver(ctx)
        planned_action = ctx.get("planned_action", {"type": "unknown", "args": {}})
        decision = guard.check(planned_action, tool_name)
        if not decision.allow:
            return {
                "status": "stopped",
                "reason": decision.reason,
                "cool_down": decision.cool_down,
                "step": decision.step,
            }
        result = run_step_fn(ctx)
        # Record with result signature continuity
        guard.check(planned_action, tool_name, result=result)
        return result

    return _wrapped
