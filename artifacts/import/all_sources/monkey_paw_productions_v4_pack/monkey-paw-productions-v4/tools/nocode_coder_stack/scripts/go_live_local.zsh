#!/bin/zsh
set -e
HOST="${HOST:-127.0.0.1}"; PORT="${PORT:-8000}"
if command -v uvicorn >/dev/null 2>&1; then
  uvicorn app.main:app --host "$HOST" --port "$PORT" --reload &
  PID=$!; sleep 2
  python3 "$(dirname "$0")/ping_health.py" "http://$HOST:$PORT/api/health" || true
  echo "uvicorn PID: $PID"
else
  echo "uvicorn not installed (skipping start)"
fi
