#!/usr/bin/env bash
set -euo pipefail
APP_MODULE="app.main:app"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
bash tools/preflight_all.sh "."
backoff=1
while true; do
  nohup python3 -m uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT" >/tmp/uvicorn.log 2>&1 &
  PID=$!
  # wait for health gate
  if bash tools/health_gate.sh "http://localhost:${PORT}/health"; then
    wait "$PID" || true
  else
    kill "$PID" >/dev/null 2>&1 || true
  fi
  sleep "$backoff"
  backoff=$(( backoff * 2 ))
  if [[ "$backoff" -gt 60 ]]; then backoff=60; fi
done
