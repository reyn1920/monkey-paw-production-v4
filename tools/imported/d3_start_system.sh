#!/bin/bash
# Optimized System Startup Script

set -e

echo "🚀 Starting Right Perspective System..."

# Load environment
if [ -f ".env.development" ]; then
    export $(cat .env.development | grep -v '^#' | xargs)
    echo "✅ Environment loaded"
fi

# Run health check
echo "🏥 Running health check..."
python system_health_check.py

echo "🎯 System ready for operation!"
echo "Available services:"
echo "  - Main Application: python main.py"
echo "  - Paste Demo: python paste_integration_demo.py (port 8080)"
echo "  - Paste App: python paste_app.py (port 8081)"
echo "  - Health Check: python system_health_check.py"
