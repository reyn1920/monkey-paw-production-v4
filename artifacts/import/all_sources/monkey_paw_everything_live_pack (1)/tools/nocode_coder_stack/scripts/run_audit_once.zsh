#!/usr/bin/env zsh
set -euo pipefail
ROOT="${1:-.}"
OUT="${ROOT}/runtime_stage"
mkdir -p "$OUT"
echo "Rule‑1 scan..."
python3 "$(dirname "$0")/rule1_guard.py" "$ROOT" || { echo "Rule‑1 violations"; exit 2; }
echo "Ruff/flake8/mypy (if present)..."
if command -v ruff >/dev/null 2>&1; then ruff check "$ROOT" || true; fi
if command -v flake8 >/dev/null 2>&1; then flake8 "$ROOT" || true; fi
if command -v mypy >/dev/null 2>&1; then mypy "$ROOT" || true; fi
echo "Audit pass complete."
