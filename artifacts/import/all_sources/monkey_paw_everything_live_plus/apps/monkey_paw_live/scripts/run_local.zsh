#!/usr/bin/env zsh
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v uvicorn >/dev/null 2>&1; then
  pip3 install "uvicorn[standard]" fastapi pydantic
fi
exec uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
