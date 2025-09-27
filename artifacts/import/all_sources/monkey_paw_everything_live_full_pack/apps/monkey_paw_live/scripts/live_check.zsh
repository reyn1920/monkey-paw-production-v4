#!/usr/bin/env zsh
set -euo pipefail
URL="http://127.0.0.1:8000/api/health"
curl -s $URL | python3 -m json.tool
