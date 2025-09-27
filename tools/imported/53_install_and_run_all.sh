#!/usr/bin/env bash
set -euo pipefail
echo "[Installer] Starting add-only setup…"
ROOT="$(pwd)"
if [ ! -d ".venv" ]; then python3 -m venv .venv; fi
source .venv/bin/activate
python -m pip install --upgrade pip wheel setuptools >/dev/null
pip install fastapi==0.115.0 uvicorn[standard]==0.30.6 pydantic==2.9.2 starlette==0.40.0 aiosqlite==0.20.0 edge-tts==6.1.12 pillow==10.4.0 httpx >/dev/null || true

# Import scraped JSON if present
if [ -f "data/scraped/scraped.json" ]; then
  echo "[Installer] Importing scraped.json"
  python utils/import_scraped.py data/scraped/scraped.json || true
fi

# Optional rescrape from local HTML dumps
if [ -d "data/scraped/html_dumps" ]; then
  echo "[Installer] Rescraping local HTML dumps…"
  python utils/rescrape_local.py data/scraped/html_dumps data/scraped/scraped.json || true
  if [ -f "data/scraped/scraped.json" ]; then python utils/import_scraped.py data/scraped/scraped.json || true; fi
fi

# Build dashboard
if command -v npm >/dev/null 2>&1; then
  (cd frontend && npm install --silent && npm run build --silent) || echo "[Installer] Frontend build warnings."
else
  echo "[Installer] npm not found. You can still use the API; build the UI later on a Node machine."
fi

# Start API
echo "[Installer] Launching API on 0.0.0.0:8099"
python -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8099 &

# Optional: kick Puppeteer research (headful)
if command -v node >/dev/null 2>&1; then
  echo "[Installer] Puppeteer scaffold available. To run: node puppeteer/runner.mjs"
fi

echo "[Installer] Done. Dashboard: http://127.0.0.1:8099/dashboard"
