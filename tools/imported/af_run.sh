#!/bin/bash
set -euo pipefail

echo "🚀 Starting TRAE Production Ready App..."

# Activate virtual environment
source .venv/bin/activate

# Start Redis if not running
echo "🔄 Starting Redis..."
docker compose -f infra/docker-compose.yml up -d

# Wait for Redis to be ready
echo "⏳ Waiting for Redis..."
until docker compose -f infra/docker-compose.yml exec redis redis-cli ping > /dev/null 2>&1; do
    sleep 1
done

# Run the application
echo "🌐 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
