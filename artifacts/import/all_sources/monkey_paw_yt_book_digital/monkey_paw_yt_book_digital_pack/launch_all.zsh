#!/bin/zsh
set -e
python3 -m pip install -r requirements.txt >/dev/null 2>&1 || true
# health: just build reports and exporters quickly
zsh scripts/first_run/fill_missing_info.zsh || true
echo "Ready."
