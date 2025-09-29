#!/usr/bin/env bash
set -euo pipefail
DB=${ANTI_LOOP_DB:-"$HOME/ONLINPRDUCTION/var/runtime/agent_state.db"}
python3 - <<'PY'
import sqlite3, time, os
db = os.environ.get("ANTI_LOOP_DB", os.path.expanduser("~/ONLINPRDUCTION/var/runtime/agent_state.db"))
con = sqlite3.connect(db, timeout=10)
cur = con.execute("SELECT job_id, MAX(step), MAX(at) FROM actions GROUP BY job_id")
now = time.time()
alerts = []
for job_id, step, at in cur.fetchall():
    if at is None: 
        continue
    if now - float(at or 0) > 180:
        alerts.append((job_id, step, int(now - at)))
if alerts:
    print("Anti-Loop Watchdog alerts:")
    for j,s,age in alerts:
        print(f"- job={j} last_step={s} idle={age}s → consider stop/cooldown")
else:
    print("Anti-Loop Watchdog: all clear")
PY
