#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 scripts/rule1_guard.py
python3 scripts/py_audit.py
python3 scripts/upr_monitor.py
# start api
exec uvicorn backend.app:app --host 127.0.0.1 --port 7860
