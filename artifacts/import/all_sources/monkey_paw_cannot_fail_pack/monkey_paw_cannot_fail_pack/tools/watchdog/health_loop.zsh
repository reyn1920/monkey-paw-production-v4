#!/bin/zsh
# Poll a health endpoint and write colored status to reports.
URL=${1:-http://127.0.0.1:8000/api/health}
OUT=reports/WATCHDOG_HEALTH.log
PANIC=reports/PANIC_SWITCH.true
echo "Watchdog started: $URL" > $OUT
while true; do
  if [ -f "$PANIC" ]; then
    echo "$(date +%F_%T) PANIC ON — publishing disabled" >> $OUT
    sleep 3; continue
  fi
  STATUS=$(curl -s "$URL" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("status","?"))' 2>/dev/null)
  echo "$(date +%F_%T) status=$STATUS" >> $OUT
  sleep 3
done
