#!/bin/zsh
set -e

echo ">>> Installing Python deps (local venv recommended)"
python3 -m pip install -r requirements.txt >/dev/null 2>&1 || true

echo ">>> Starting API (background)"
# kill any uvicorn on 8000
lsof -ti:8000 | xargs -I{} kill -9 {} 2>/dev/null || true
( uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload ) >/tmp/monkey_paw_uvicorn.log 2>&1 &
sleep 2

echo ">>> Health check"
curl -s http://127.0.0.1:8000/api/health | python3 -m json.tool || true

echo ">>> Project Doctor"
zsh tools/doctor/diagnose_all.zsh || true

echo ">>> Comparison report"
python3 tools/doctor/build_comparison.py || true

echo ">>> Two-pass audit"
zsh tools/audit/run_two_pass_audit.zsh || true

echo ">>> Done. Open reports in ./reports"
