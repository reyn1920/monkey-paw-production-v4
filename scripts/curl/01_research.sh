#!/usr/bin/env zsh
set -euo pipefail
TOPIC="${1:-sample topic}"
curl -s -X POST http://127.0.0.1:8000/api/research   -H "content-type: application/json"   -d '{"topic":"'"$TOPIC"'","source":"manual","content":"notes"}' | python3 -m json.tool
