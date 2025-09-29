#!/bin/bash

# 0) Pick the live port (tries 5000 then 8080)
for p in 5000 8080; do
  if curl -sf "http://127.0.0.1:$p/api/routes" >/dev/null; then PORT=$p; break; fi
done
echo "Using PORT=${PORT:-none}"

# 1) List key routes
echo "=== Key Routes ==="
curl -s "http://127.0.0.1:$PORT/api/routes" | jq '.routes[] | select(.rule|test("/api/(audit|metrics|health|routes)"))'

# 2) One-shot verdict JSON
echo "=== One-shot Verdict ==="
curl -s "http://127.0.0.1:$PORT/api/audit/verdict" | jq '{verdict, system_health, uptime}'

# 3) Stream a few SSE lines (note -N to unbuffer)
echo "=== SSE Stream (5 lines) ==="
curl -sN "http://127.0.0.1:$PORT/api/audit/verdict/stream" | head -n 5

# 4) Health
echo "=== Health Endpoints ==="
echo "Liveness:"
curl -s "http://127.0.0.1:$PORT/health/liveness" | jq .
echo "Readiness:"
curl -s "http://127.0.0.1:$PORT/health/readiness" | jq .

# 5) Prometheus metrics (first 20 lines)
echo "=== Prometheus Metrics (first 20 lines) ==="
curl -s "http://127.0.0.1:$PORT/api/metrics" | sed -n '1,20p'

# 6) Run review + archive and show latest verdict
echo "=== Run and Archive ==="
curl -s -X POST "http://127.0.0.1:$PORT/api/audit/run-and-archive" -H "Content-Type: application/json" -d '{}' | jq '{ok, saved: .saved.name, verdict: .saved.verdict}'
