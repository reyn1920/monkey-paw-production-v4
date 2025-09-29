#!/usr/bin/env zsh
set -euo pipefail
curl -s -X POST http://127.0.0.1:8000/api/admin/approve_publish/true | python3 -m json.tool
curl -s -X POST http://127.0.0.1:8000/api/publish | python3 -m json.tool
