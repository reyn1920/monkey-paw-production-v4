#!/bin/zsh
set -e
python3 -m pip install -r requirements.txt >/dev/null 2>&1 || true
zsh tools/audit/run_two_pass_audit.zsh || true
zsh scripts/first_run/fill_missing_info.zsh || true
zsh scripts/run_server.zsh
