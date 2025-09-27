#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate
python tools/rule1_guard.py .
python tools/py_audit.py .
python utils/seed_sqlite.py
./scripts/run_api.sh
