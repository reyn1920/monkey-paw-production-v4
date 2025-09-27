"""
Auto anti-loop patcher.
Placed at repo root. Python will import sitecustomize automatically (unless -S is used).
It scans loaded modules and safely wraps common agent step functions without editing code.
"""

import os, sys, threading, time, inspect, types, traceback
from pathlib import Path

# Allow opt-out
if os.environ.get("ANTI_LOOP_AUTO_WRAP", "1") != "1":
    pass  # disabled
else:
    LOG_DIR = Path(os.path.expanduser("~/ONLINPRDUCTION/var/runtime"))
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE = LOG_DIR / "anti_loop.log"

    def log(msg: str):
        try:
            with LOG_FILE.open("a", encoding="utf-8") as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S") + " " + msg + "\n")
        except Exception:
            pass

    try:
        from backend.agents.middleware.guarded_runner import GuardedAgentRunner
        from backend.utils.loop_guard import LoopGuard  # ensure DB path exists
    except Exception as e:
        log(f"[sitecustomize] missing anti-loop modules: {e}")
        GuardedAgentRunner = None

    _wrapped = set()

    def _job_id_of(ctx: dict) -> str:
        return (
            ctx.get("job_id")
            or ctx.get("trace_id")
            or ctx.get("request_id")
            or "default-job"
        )

    def _tool_name_of(ctx: dict) -> str:
        a = ctx.get("planned_action") or {}
        return a.get("tool") or a.get("type") or "agent-core"

    def _maybe_wrap_module(mod: types.ModuleType):
        if not GuardedAgentRunner:
            return
        try:
            for name, obj in vars(mod).items():
                # Free function pattern: run_agent_step(ctx) -> dict
                if name == "run_agent_step" and callable(obj) and obj not in _wrapped:
                    try:
                        wrapped = GuardedAgentRunner(obj, _job_id_of, _tool_name_of)
                        setattr(mod, name, wrapped)
                        _wrapped.add(wrapped)
                        log(f"wrapped {mod.__name__}.{name}")
                    except Exception as e:
                        log(f"wrap failed for {mod.__name__}.{name}: {e}")
                # Class method pattern: class SomethingAgent: def step(self, ctx)
                if inspect.isclass(obj) and "Agent" in obj.__name__:
                    if hasattr(obj, "step") and callable(getattr(obj, "step")):
                        meth = getattr(obj, "step")
                        if meth not in _wrapped:

                            def _make_wrapped(meth):
                                def _w(self, ctx):
                                    # Build a pseudo ctx if not provided
                                    local_ctx = ctx or {}
                                    job_id = _job_id_of(local_ctx)
                                    guard = LoopGuard(job_id)
                                    decision = guard.check(
                                        local_ctx.get(
                                            "planned_action",
                                            {"type": "unknown", "args": {}},
                                        ),
                                        getattr(self, "__class__", type(self)).__name__,
                                    )
                                    if not decision.allow:
                                        return {
                                            "status": "stopped",
                                            "reason": decision.reason,
                                            "cool_down": decision.cool_down,
                                            "step": decision.step,
                                        }
                                    res = meth(self, ctx)
                                    guard.check(
                                        local_ctx.get(
                                            "planned_action",
                                            {"type": "unknown", "args": {}},
                                        ),
                                        getattr(self, "__class__", type(self)).__name__,
                                        result=res,
                                    )
                                    return res

                                return _w

                            try:
                                setattr(obj, "step", _make_wrapped(meth))
                                _wrapped.add(meth)
                                log(
                                    f"wrapped method {mod.__name__}.{obj.__name__}.step"
                                )
                            except Exception as e:
                                log(
                                    f"wrap failed for class {mod.__name__}.{obj.__name__}.step: {e}"
                                )
        except Exception as e:
            log(f"scan failed for {mod}: {e}")

    def _monitor():
        # Try for a while at start-up
        for _ in range(60):
            for m in list(sys.modules.values()):
                if not isinstance(m, types.ModuleType):
                    continue
                mn = getattr(m, "__name__", "")
                # Only scan project modules (heuristic)
                if mn and (
                    mn.startswith("agents")
                    or mn.startswith("orchestrator")
                    or "agent" in mn
                ):
                    _maybe_wrap_module(m)
            time.sleep(1.0)

    t = threading.Thread(target=_monitor, name="anti_loop_autowrap", daemon=True)
    t.start()
