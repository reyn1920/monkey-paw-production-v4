#!/bin/bash
# Monkey Paw Integration Verification Commands

echo "Testing MP Integration API endpoints..."

echo "1. Testing /api/status"
curl -X GET http://localhost:8000/api/status

echo -e "

2. Testing /api/toggle"
curl -X POST http://localhost:8000/api/toggle -H "Content-Type: application/json" -d "{\"mode\": \"public\"}"

echo -e "

3. Testing /api/chat"
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "{\"message\": \"Hello from integration test\", \"ai_system\": \"chatgpt\"}"

echo -e "

4. Testing diagnostics"
curl -X GET http://localhost:8000/api/diagnostics

echo -e "

Verification complete!"
