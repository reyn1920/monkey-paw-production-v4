#!/bin/zsh
curl -s -X POST http://127.0.0.1:8000/api/research -H "Content-Type: application/json" -d "{"topic":"${1:-default topic}"}" | python3 -m json.tool
