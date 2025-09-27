#!/usr/bin/env zsh
set -euo pipefail
ROOT="${1:-.}"
echo "Pass 1"
python3 ./tools/nocode_coder_stack/scripts/rule1_guard.py "$ROOT" || true
echo "Pass 2"
python3 ./tools/nocode_coder_stack/scripts/rule1_guard.py "$ROOT" || true
echo "Two-pass audit complete."
