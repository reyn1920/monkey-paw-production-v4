#!/usr/bin/env zsh
set -euo pipefail
APP_DIR="$(cd "$(dirname "$0")/../../apps/monkey_paw_live" && pwd)"
cd "$APP_DIR"
zsh ./scripts/run_local.zsh > ./run_local.log 2>&1 &
APIPID=$!
echo "Started PID=$APIPID, waiting for health..."
for i in {1..30}; do
  if curl -s http://127.0.0.1:8000/api/health | grep -q ok; then
    echo "GREEN — API healthy"; exit 0
  fi
  sleep 1
done
echo "RED — API not healthy after 30s"; exit 1
