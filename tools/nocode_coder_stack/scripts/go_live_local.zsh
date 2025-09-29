#!/usr/bin/env zsh
set -euo pipefail
cd "$(dirname "$0")/../../apps/monkey_paw_live"
zsh ./scripts/run_local.zsh &
PID=$!
sleep 2
zsh ./scripts/live_check.zsh
echo "Server PID: $PID (leave running or Ctrl+C in its terminal)"
