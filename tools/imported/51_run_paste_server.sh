#!/usr/bin/env bash
set -euo pipefail

# Simple paste server using Python's built-in HTTP server
# This serves the paste functionality on port 5000

ROOT="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$ROOT/../.." && pwd)"

echo "🚀 Starting paste server on http://127.0.0.1:5000"
echo "📁 Serving from: $PROJECT_ROOT"

# Change to project root and start server
cd "$PROJECT_ROOT"

# Check if Python 3 is available
if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "❌ Error: Python not found"
    exit 1
fi

# Start HTTP server on port 5000
$PYTHON -m http.server 5000 --bind 127.0.0.1
