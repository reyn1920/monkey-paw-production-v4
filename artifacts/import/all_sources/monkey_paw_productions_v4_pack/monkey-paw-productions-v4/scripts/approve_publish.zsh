#!/bin/zsh
set -e
curl -s -X POST http://127.0.0.1:8000/api/admin/approve_publish/true | tee /dev/stderr
