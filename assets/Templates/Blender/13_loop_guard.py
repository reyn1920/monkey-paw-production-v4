import sqlite3
import json
import time
import hashlib
import os
import threading
from dataclasses import dataclass
from typing import Any, Dict, Optional

DEFAULT_DB = os.environ.get(
    "ANTI_LOOP_DB", os.path.expanduser("~/ONLINPRDUCTION/var/runtime/agent_state.db")
)
os.makedirs(os.path.dirname(DEFAULT_DB), exist_ok=True)

_INIT_SQL = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS actions(
  job_id TEXT,
  step INTEGER,
  at REAL,
  action_sig TEXT,
  tool_name TEXT,
  result_sig TEXT
);
CREATE INDEX IF NOT EXISTS idx_actions_job ON actions(job_id, step);
CREATE TABLE IF NOT EXISTS budgets(
  job_id TEXT PRIMARY KEY,
  started_at REAL,
  max_steps INTEGER,
  max_seconds INTEGER
);
"""


def _conn():
    db = sqlite3.connect(DEFAULT_DB, timeout=30)
    db.execute("PRAGMA busy_timeout=30000;")
    return db


def _init():
    with _conn() as c:
        for stmt in _INIT_SQL.strip().split(";"):
            s = stmt.strip()
            if s:
                c.execute(s)


_init_lock = threading.Lock()
with _init_lock:
    _init()


def _sig(obj: Any) -> str:
    try:
        s = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        s = str(obj)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


@dataclass
class GuardDecision:
    allow: bool
    reason: str = ""
    cool_down: float = 0.0
    step: int = 0


class LoopGuard:
    def __init__(
        self,
        job_id: str,
        max_steps: int = int(os.environ.get("ANTI_LOOP_MAX_STEPS", "40")),
        max_seconds: int = int(os.environ.get("ANTI_LOOP_MAX_SECONDS", "900")),
        dup_window: int = int(os.environ.get("ANTI_LOOP_DUP_WINDOW", "6")),
        dup_threshold: int = int(os.environ.get("ANTI_LOOP_DUP_THRESHOLD", "3")),
        tool_rate_limit: int = int(os.environ.get("ANTI_LOOP_TOOL_RATE", "8")),
        tool_window_sec: int = int(os.environ.get("ANTI_LOOP_TOOL_WINDOW", "60")),
    ):
        self.job_id = job_id
        self.max_steps = max_steps
        self.max_seconds = max_seconds
        self.dup_window = dup_window
        self.dup_threshold = dup_threshold
        self.tool_rate_limit = tool_rate_limit
        self.tool_window_sec = tool_window_sec
        self._start = time.time()
        self._ensure_budget_row()

    def _ensure_budget_row(self):
        with _conn() as c:
            c.execute(
                "INSERT OR IGNORE INTO budgets(job_id, started_at, max_steps, max_seconds) VALUES(?,?,?,?)",
                (self.job_id, self._start, self.max_steps, self.max_seconds),
            )

    def _now(self) -> float:
        return time.time()

    def _current_step(self) -> int:
        with _conn() as c:
            cur = c.execute(
                "SELECT COALESCE(MAX(step),0) FROM actions WHERE job_id=?",
                (self.job_id,),
            )
            row = cur.fetchone()
            return int(row[0] or 0)

    def _recent_actions(self, limit: int = None):
        limit = limit or self.dup_window
        with _conn() as c:
            cur = c.execute(
                "SELECT step, action_sig, tool_name, at FROM actions WHERE job_id=? ORDER BY step DESC LIMIT ?",
                (self.job_id, limit),
            )
            return cur.fetchall()

    def _tool_count_in_window(self, tool_name: str) -> int:
        since = self._now() - self.tool_window_sec
        with _conn() as c:
            cur = c.execute(
                "SELECT COUNT(1) FROM actions WHERE job_id=? AND tool_name=? AND at>=?",
                (self.job_id, tool_name, since),
            )
            return int(cur.fetchone()[0])

    def check(
        self, action: Dict[str, Any], tool_name: str, result: Optional[Any] = None
    ) -> GuardDecision:
        step = self._current_step() + 1
        elapsed = self._now() - self._start
        if step > self.max_steps:
            return GuardDecision(
                False,
                reason=f"step_budget_exceeded({step}>{self.max_steps})",
                step=step,
            )
        if elapsed > self.max_seconds:
            return GuardDecision(
                False,
                reason=f"time_budget_exceeded({int(elapsed)}s>{self.max_seconds}s)",
                step=step,
            )

        action_sig = _sig({"tool": tool_name, "action": action})
        recent = self._recent_actions(self.dup_window)
        dup_hits = sum(1 for _, a_sig, _, _ in recent if a_sig == action_sig)
        if dup_hits >= self.dup_threshold:
            return GuardDecision(
                False,
                reason=f"duplicate_action_loop(sig={action_sig[:8]}*, hits={dup_hits})",
                cool_down=10.0,
                step=step,
            )

        used = self._tool_count_in_window(tool_name)
        if used >= self.tool_rate_limit:
            return GuardDecision(
                False,
                reason=f"tool_rate_limited({tool_name}, {used}/{self.tool_rate_limit}@{self.tool_window_sec}s)",
                cool_down=5.0,
                step=step,
            )

        result_sig = ""
        if result is not None:
            try:
                result_sig = _sig(result)
            except Exception:
                result_sig = ""

        with _conn() as c:
            c.execute(
                "INSERT INTO actions(job_id, step, at, action_sig, tool_name, result_sig) VALUES(?,?,?,?,?,?)",
                (self.job_id, step, self._now(), action_sig, tool_name, result_sig),
            )
        return GuardDecision(True, reason="ok", step=step)


def idempotency_key(user_id: str, job_payload: Dict[str, Any]) -> str:
    return _sig({"u": user_id, "p": job_payload})
