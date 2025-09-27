#!/bin/zsh
set -e
ROOT="${1:-.}"
if command -v ruff >/dev/null 2>&1; then ruff check "$ROOT" || true; else echo "ruff not installed (skipping)"; fi
if command -v flake8 >/dev/null 2>&1; then flake8 "$ROOT" || true; else echo "flake8 not installed (skipping)"; fi
if command -v mypy >/dev/null 2>&1; then mypy "$ROOT" || true; else echo "mypy not installed (skipping)"; fi
python3 "$(dirname "$0")/rule1_guard.py" "$ROOT" || true
