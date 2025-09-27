#!/bin/zsh
curl -s http://127.0.0.1:8000/api/health | python3 -m json.tool
