#!/bin/zsh
set -euo pipefail

# 1) Create venv (optional) and install deps quietly
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python3 is required. Install Xcode CLT or Python from python.org"; exit 1
fi

python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
python3 -m pip install -r requirements.txt >/dev/null 2>&1 || true

# 2) Quick audits (non-blocking)
zsh tools/audit/run_two_pass_audit.zsh || true
zsh scripts/first_run/fill_missing_info.zsh || true

# 3) Start server
lsof -ti:8000 | xargs -I{} kill -9 {} 2>/dev/null || true
( uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload ) >/tmp/monkey_paw_v3_uvicorn.log 2>&1 &

# 4) Open dashboard
if [[ "$OSTYPE" == "darwin"* ]]; then
  open "http://127.0.0.1:8000/"
else
  echo "Open http://127.0.0.1:8000/ in your browser."
fi

echo "Monkey Paw V3 is live. Logs: /tmp/monkey_paw_v3_uvicorn.log"
