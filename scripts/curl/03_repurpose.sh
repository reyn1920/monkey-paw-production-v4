#!/usr/bin/env zsh
set -euo pipefail
DID="${1:-1}"
curl -s -X POST http://127.0.0.1:8000/api/repurpose   -H "content-type: application/json"   -d '{"draft_id":'"$DID"',"variants":["youtube_script","blog_post","social_post"]}' | python3 -m json.tool
