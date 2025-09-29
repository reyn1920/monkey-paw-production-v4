#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# 0) Fast pre-checks
command -v python3 >/dev/null || { echo "python3 not found"; exit 1; }

# 1) Minimal deps (idempotent); leave your venv as-is
pip3 install -q fastapi "uvicorn[standard]" textstat reportlab pytest >/dev/null || true

# 2) Ensure DB tables needed by the checks
python3 scripts/db_bootstrap.py

# 3) Start the health/API shim on 8081
export PORT=8081
python3 launch_live.py > .api_shim.log 2>&1 &
API_PID=$!
echo "API shim started (pid: $API_PID) on 127.0.0.1:${PORT}"

# 4) Wait briefly for the socket
for i in {1..20}; do
  if curl -s "http://127.0.0.1:${PORT}/api/health" >/dev/null; then
    echo "Health OK"
    break
  fi
  sleep 0.25
done

# 5) Run your checks file
python3 tests/test_final_verification.py
STATUS=$?

# 6) Cleanup
kill "$API_PID" >/dev/null 2>&1 || true
wait "$API_PID" >/dev/null 2>&1 || true

exit "$STATUS"
