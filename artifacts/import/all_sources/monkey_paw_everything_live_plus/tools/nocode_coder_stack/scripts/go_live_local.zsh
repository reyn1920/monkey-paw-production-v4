#!/usr/bin/env zsh
set -euo pipefail
APP_DIR="$(cd "$(dirname "$0")/../../apps/monkey_paw_live" && pwd)"
HEALTH="http://127.0.0.1:8000/api/health"
cd "$APP_DIR"
zsh ./scripts/run_local.zsh > ./run_local.log 2>&1 &
PID=$!
echo "[go-live] started PID=$PID; waiting for health"
for i in {1..60}; do
  if curl -sS -m 1.5 "$HEALTH" | grep -q '"ok": true'; then
    echo "GREEN — API healthy"
    exit 0
  fi
  printf "."
  sleep 1
done
echo
echo "RED — API not healthy after 60s; tail logs:"
tail -n 80 ./run_local.log || true
exit 1
