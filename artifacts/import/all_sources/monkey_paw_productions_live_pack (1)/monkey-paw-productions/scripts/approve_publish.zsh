#!/bin/zsh
set -e
echo "== Approve Publish =="
curl -s -X POST http://127.0.0.1:8000/api/admin/approve_publish/true | tee /dev/stderr
