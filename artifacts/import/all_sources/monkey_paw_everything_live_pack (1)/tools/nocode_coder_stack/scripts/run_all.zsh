#!/usr/bin/env zsh
set -euo pipefail
ROOT="${1:-.}"
zsh "$(dirname "$0")/run_two_pass_audit.zsh" "$ROOT"
# Try go‑live if app present
if [[ -f "$ROOT/apps/monkey_paw_live/scripts/run_local.zsh" ]]; then
  zsh "$(dirname "$0")/go_live_local.zsh" || true
fi
echo "Report ready. See ./reports and ./runtime_stage if generated."
