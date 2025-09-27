#!/usr/bin/env zsh
set -euo pipefail
echo "[1/4] Start API"
zsh ./apps/monkey_paw_live/scripts/run_local.zsh &
sleep 3
echo "[2/4] Live check"
zsh ./apps/monkey_paw_live/scripts/live_check.zsh || true
echo "[3/4] Diagnostics"
zsh ./tools/project-doctor/scripts/diagnose_all.zsh . || true
python3 ./tools/project-doctor/scripts/build_comparison.py || true
echo "[4/4] Two-pass verification"
zsh ./tools/nocode_coder_stack/scripts/run_two_pass_audit.zsh . || true
echo "Done."
