#!/usr/bin/env bash
# Comprehensive TRAE.AI System Diagnostics Bundle
# Tests all endpoints and provides clean status output

set -euo pipefail

echo "🔍 TRAE.AI System Diagnostics"
echo "============================="
echo

# VERSION Check
echo "📋 VERSION:"
curl -s http://127.0.0.1:8083/api/version \
| jq -r 'if has("service") then "✅ \(.service) • commit \(.commit[0:7]) • pid \(.pid)"
         else "✅ \(.name) v\(.version) • ts \(.ts)" end' 2>/dev/null || echo "❌ Version endpoint failed"
echo

# ACTIONS Check
echo "⚡ ACTIONS:"
curl -s http://127.0.0.1:8083/api/actions \
| jq -r '"✅ Actions: \(.count // (.actions|length)) available",
         (.actions[] | "  - " + .name)' 2>/dev/null || echo "❌ Actions endpoint failed"
echo

# HEALTH Check
echo "💚 HEALTH:"
curl -s http://127.0.0.1:8083/api/health \
| jq -r 'if .status=="healthy" then "✅ Health: healthy" else "❌ Health: \(.status)" end' 2>/dev/null || echo "❌ Health endpoint failed"
echo

# Socket.IO Check
echo "🔌 SOCKET.IO:"
echo -n "✅ Socket.IO: "
curl -s 'http://127.0.0.1:8083/socket.io/?EIO=4&transport=polling' | head -c 20 2>/dev/null || echo "❌ Failed"
echo " ..."
echo

# METRICS Check
echo "📊 METRICS (sample):"
curl -s http://127.0.0.1:8083/api/metrics | head -n 5 2>/dev/null || echo "❌ Metrics endpoint failed"
echo "  ..."
echo

# Action Invocation Test
echo "🎯 ACTION TEST:"
curl -s -X POST "http://127.0.0.1:8083/api/action/get_system_status/Get%20system%20status" \
     -H 'Content-Type: application/json' -d '{}' \
| jq -r 'if type=="object" then "✅ Action responded successfully" else "❌ Unexpected response" end' 2>/dev/null || echo "❌ Action invocation failed"
echo

# FastAPI Backend Check (if running on 8080)
echo "🚀 FASTAPI BACKEND:"
for endpoint in "/api/health" "/api/actions" "/api/system/status" "/api/metrics"; do
    status=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:8080$endpoint" 2>/dev/null || echo "000")
    if [ "$status" = "200" ]; then
        echo "  ✅ $endpoint (200 OK)"
    else
        echo "  ❌ $endpoint ($status)"
    fi
done
echo

# System Summary
echo "📈 SYSTEM SUMMARY:"
echo "  Dashboard: http://127.0.0.1:8083/"
echo "  FastAPI:   http://127.0.0.1:8080/"
echo "  Status:    $(date)"
echo
echo "✨ Diagnostics complete!"
