#!/usr/bin/env zsh
set -euo pipefail
ROOT="${1:-.}"
echo "Pass 1:"
zsh "$(dirname "$0")/run_audit_once.zsh" "$ROOT"
echo "Pass 2:"
zsh "$(dirname "$0")/run_audit_once.zsh" "$ROOT"
echo "GREEN: two consecutive passes complete."
