#!/bin/zsh
set -e
DST="backups_$(date +%F_%H%M%S).tar.gz"
tar -czf "$DST" db artifacts assets config reports 2>/dev/null || true
echo "Wrote $DST"
