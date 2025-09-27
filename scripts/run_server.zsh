#!/bin/zsh
set -e
python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
python3 -m pip install -r requirements.txt >/dev/null 2>&1 || true
lsof -ti:8000 | xargs -I{} kill -9 {} 2>/dev/null || true
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
