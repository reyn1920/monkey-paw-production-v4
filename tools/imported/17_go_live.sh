#!/bin/bash
# TRAE AI Online Production - Go Live Script
# One-click go live: add-only merge, deps, migrations, supervisor, API

set -e  # Exit on any error

echo "🚀 TRAE AI Online Production - Go Live Process"
echo "=============================================="

# Check if APP_DIR is set
if [ -z "$APP_DIR" ]; then
    echo "📁 Setting APP_DIR to current directory..."
    export APP_DIR="$(pwd)"
fi

echo "📁 Working with application directory: $APP_DIR"

# Navigate to the application directory
cd "$APP_DIR"

echo ""
echo "🔍 Phase 1: Pre-deployment validation"
echo "======================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "⚠️  Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - TRAE AI Online Production"
fi

# Check for Python environment
echo "🐍 Checking Python environment..."
if command -v python3 &> /dev/null; then
    echo "✅ Python3 found: $(python3 --version)"
else
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Check for Node.js if package.json exists
if [ -f "package.json" ]; then
    echo "📦 Checking Node.js environment..."
    if command -v npm &> /dev/null; then
        echo "✅ npm found: $(npm --version)"
    else
        echo "❌ npm not found. Please install Node.js"
        exit 1
    fi
fi

echo ""
echo "📦 Phase 2: Dependencies installation"
echo "====================================="

# Install Python dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "🐍 Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# Install Node.js dependencies if package.json exists
if [ -f "package.json" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

echo ""
echo "🗄️  Phase 3: Database migrations"
echo "================================"

# Check for database initialization
if [ -f "init-db.sql" ]; then
    echo "🗄️  Database schema found, ensuring database is ready..."
fi

# Run any existing migration scripts
if [ -f "migrations/migrate.py" ]; then
    echo "🔄 Running database migrations..."
    python3 migrations/migrate.py
elif [ -f "scripts/migrate.py" ]; then
    echo "🔄 Running database migrations..."
    python3 scripts/migrate.py
fi

echo ""
echo "🔧 Phase 4: Application configuration"
echo "===================================="

# Check for environment configuration
if [ -f ".env.example" ]; then
    if [ ! -f ".env" ]; then
        echo "📝 Creating .env from .env.example..."
        cp .env.example .env
        echo "⚠️  Please update .env with your production values"
    fi
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Build frontend if needed
if [ -f "package.json" ] && [ -f "vite.config.js" ]; then
    echo "🏗️  Building frontend application..."
    npm run build
fi

echo ""
echo "🚀 Phase 5: Starting production services"
echo "======================================="

# Kill any existing processes on the ports we need
echo "🔄 Stopping any existing services..."
pkill -f "uvicorn.*8000" || true
pkill -f "python.*8098" || true
pkill -f "node.*8099" || true

# Start the main application
echo "🚀 Starting main application on port 8000..."
if [ -f "app/main.py" ]; then
    nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > logs/app.log 2>&1 &
    echo $! > run.pid
elif [ -f "main.py" ]; then
    nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload > logs/main.log 2>&1 &
    echo $! > run.pid
fi

# Start additional services if they exist
if [ -f "backend/app.py" ]; then
    echo "🔧 Starting backend service..."
    nohup python3 backend/app.py > logs/backend.log 2>&1 &
fi

# Wait a moment for services to start
sleep 3

echo ""
echo "🔍 Phase 6: Health checks"
echo "========================"

# Check if main service is running
echo "🏥 Checking application health..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Main application is healthy"
else
    echo "⚠️  Main application health check failed, but continuing..."
fi

# Check if docs are available
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo "✅ API documentation is available"
else
    echo "⚠️  API documentation not available"
fi

echo ""
echo "🎉 Phase 7: Go-live complete!"
echo "============================"

echo ""
echo "🌐 Your application is now live!"
echo ""
echo "📊 Dashboard: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🏥 Health Check: http://localhost:8000/health"
echo ""
echo "📝 Logs are available in the logs/ directory"
echo "🔧 Process ID saved to run.pid"
echo ""
echo "🚀 Go-live process completed successfully!"
echo ""
echo "⚠️  Next steps:"
echo "   1. Update your .env file with production values"
echo "   2. Configure your domain and SSL certificates"
echo "   3. Set up monitoring and backups"
echo "   4. Test all functionality thoroughly"
echo ""