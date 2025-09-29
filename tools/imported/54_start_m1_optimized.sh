#!/bin/bash
# M1 MacBook Air Optimization Startup Script

echo "🍎 Starting M1 MacBook Air Optimizations..."

# Set M1-specific environment variables
export PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
export OMP_NUM_THREADS=8
export MKL_NUM_THREADS=8
export DOCKER_BUILDKIT=1

# Add Homebrew ARM64 to PATH
export PATH="/opt/homebrew/bin:$PATH"

echo "✅ Environment variables set for M1 optimization"

# Check if uvloop is installed
if ! python -c "import uvloop" 2>/dev/null; then
    echo "📦 Installing uvloop for better async performance..."
    pip install uvloop
fi

# Start FastAPI with M1-optimized settings
echo "🚀 Starting FastAPI with M1 optimizations..."

if [ -f "fastapi_m1_config.py" ]; then
    echo "Using M1-optimized configuration"
    gunicorn -c fastapi_m1_config.py main:app
else
    echo "Using default M1-optimized settings"
    uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
fi
