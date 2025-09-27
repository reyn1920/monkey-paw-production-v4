#!/bin/zsh
SEED_ID=${1:-1}
CONTENT=${2:-"Write a clear outline and a 500-word script."}
curl -s -X POST http://127.0.0.1:8000/api/draft -H "Content-Type: application/json" -d "{"seed_id":$SEED_ID,"content":"${CONTENT//"/\"}"}" | python3 -m json.tool
