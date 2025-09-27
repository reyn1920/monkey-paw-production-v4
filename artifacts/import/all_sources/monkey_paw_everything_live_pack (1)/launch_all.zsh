#!/usr/bin/env zsh
set -euo pipefail
echo "== Everything Live Pack : launcher =="
# 1) Start API
if [[ -f "./apps/monkey_paw_live/scripts/run_local.zsh" ]]; then
  echo "[1/5] Starting API..."
  zsh ./apps/monkey_paw_live/scripts/run_local.zsh &
  APIPID=$!
  sleep 3
else
  echo "App launcher missing."; exit 1
fi
# 2) Live selfcheck
echo "[2/5] Live selfcheck..."
zsh ./apps/monkey_paw_live/scripts/live_check.zsh || true
# 3) Project Doctor diagnostics
echo "[3/5] Diagnostics..."
zsh ./tools/project-doctor/scripts/diagnose_all.zsh . || true
# 4) Build Intended vs. Actual comparison
echo "[4/5] Building comparison doc..."
python3 ./tools/project-doctor/scripts/build_comparison.py || true
# 5) Two‑pass verify + optional go‑live
echo "[5/5] Two‑pass verification..."
zsh ./tools/nocode_coder_stack/scripts/run_all.zsh . || true
echo "Done. API PID=$APIPID"
