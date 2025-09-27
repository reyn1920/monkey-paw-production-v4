#!/bin/zsh
set -e
python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
python3 -m pip install -r requirements.txt >/dev/null 2>&1 || true
lsof -ti:8000 | xargs -I{} kill -9 {} 2>/dev/null || true
( uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload ) >/tmp/monkey_paw_v4_uvicorn.log 2>&1 &
[[ "$OSTYPE" == darwin* ]] && open "http://127.0.0.1:8000/" || true
echo "V4 launched. Logs: /tmp/monkey_paw_v4_uvicorn.log"
