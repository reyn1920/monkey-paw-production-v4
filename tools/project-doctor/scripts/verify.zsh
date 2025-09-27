#!/usr/bin/env zsh
set -euo pipefail
ROOT="${1:-.}"
echo "Quick verify (GREEN/YELLOW):"
[[ -f "$ROOT/apps/monkey_paw_live/config/config.yaml" ]] && echo "config: present" || echo "config: missing"
[[ -d "$ROOT/apps/monkey_paw_live/app" ]] && echo "app: present" || echo "app: missing"
