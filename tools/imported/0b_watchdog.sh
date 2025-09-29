#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"


echo "[watchdog] starting at $(date)" >> "$LOG_DIR/watchdog.log"
# Simple health check: Python audits + backend ping
python3 "$ROOT/scripts/rule1_guard.py"
python3 "$ROOT/scripts/py_audit.py"
python3 - <<'PY'
import socket
s=socket.socket();
try:
    s.connect(("127.0.0.1", 7860))
    print("backend: up")
except Exception as e:
    print("backend: down", e)
PY
