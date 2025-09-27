#!/bin/zsh
curl -s -X POST http://127.0.0.1:8000/api/publish | python3 -m json.tool
