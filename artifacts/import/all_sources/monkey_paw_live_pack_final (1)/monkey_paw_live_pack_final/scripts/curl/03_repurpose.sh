#!/bin/zsh
curl -s -X POST "http://127.0.0.1:8000/api/repurpose?seed_id=${1:-1}" | python3 -m json.tool
