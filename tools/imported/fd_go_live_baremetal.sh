#!/usr/bin/env bash
set -euo pipefail
if [[ -z "${APP_DIR:-}" ]]; then echo 'Set APP_DIR, e.g.: export APP_DIR="$HOME/online production"'; exit 1; fi
PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$HOME/snapshots"
tar -czf "$HOME/snapshots/online_runtime_$(date +%Y%m%d_%H%M%S).tar.gz" -C "$(dirname "$APP_DIR")" "$(basename "$APP_DIR")"
rsync -a "$PACK_DIR/" "$APP_DIR/" --exclude '.DS_Store' --exclude 'node_modules' --exclude '.venv' --exclude 'go_live_baremetal.sh'
cd "$APP_DIR"
python3 -m pip install --user --upgrade pip wheel setuptools
python3 -m pip install --user fastapi uvicorn pydantic python-multipart aiosqlite httpx rich typer pyyaml playwright ruff black isort
python3 -m playwright install chromium
if command -v npm >/dev/null 2>&1 && [[ -f "frontend/package.json" ]]; then (cd frontend && npm install && npm run build) || true; fi
python3 tools/db_migrate.py || true
bash tools/preflight_all.sh "."
bash tools/hardening/phoenix_protocol.sh >/tmp/phoenix.log 2>&1 &
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 >/tmp/uvicorn.log 2>&1 &
echo "Dashboard: http://localhost:8000"
