#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
python3 tools/cannot_fail.py --root "$ROOT" --passes 6 || true
python3 tools/debug_sweep.py --root "$ROOT" --full --fix
python3 tools/debug_sweep.py --root "$ROOT" --full --fix
echo "[preflight] cannot-fail + clean x2 done"
