#!/bin/zsh
set -e
echo "== Monkey Paw Productions — Live Start =="
if ! command -v uvicorn >/dev/null 2>&1; then
  echo "uvicorn not found; installing deps locally (no venv)"
  pip install -r requirements.txt
fi
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
