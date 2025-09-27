#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate
python -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8099
