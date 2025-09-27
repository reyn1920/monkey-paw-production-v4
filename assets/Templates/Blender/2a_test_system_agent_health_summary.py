import sys  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement

sys.path.append(
    "."
)  # repo root if needed  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement

from backend.agents.system_agent import (
    SystemAgent,
)  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement


def test_system_agent_has_health_summary():
    a = SystemAgent()
    assert hasattr(a, "_health_summary") or hasattr(a, "health_summary")


def test_system_agent_summary_returns_string():
    a = SystemAgent()
    report = {"healthy": 5, "unhealthy": 1, "notes": ["Test note"]}
    # resolve method defensively (mirrors your runtime strategy)
    fn = getattr(a, "_health_summary", None) or getattr(a, "health_summary", None)
    assert callable(fn)
    out = fn(report)
    assert isinstance(out, str)
    assert (
        "5" in out
    )  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement
