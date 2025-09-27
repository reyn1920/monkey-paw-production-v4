#!/usr/bin/env zsh
set -euo pipefail
RID="${1:-1}"
TEXT="${2:-first pass draft}"
curl -s -X POST http://127.0.0.1:8000/api/draft   -H "content-type: application/json"   -d '{"research_id":'"$RID"',"content":"'"$TEXT"'"}' | python3 -m json.tool
