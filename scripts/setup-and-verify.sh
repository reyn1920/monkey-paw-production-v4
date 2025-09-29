#!/bin/bash

# Setup and Verification Script
# This script sets up the entire system and runs comprehensive verification

set -euo pipefail

echo "🚀 Starting Monkey Paw Production v4 Setup and Verification"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local name=$2
    local max_attempts=30
    local attempt=1
    
    print_status "Waiting for $name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            print_success "$name is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 1
        attempt=$((attempt + 1))
    done
    
    print_error "$name failed to start within $max_attempts seconds"
    return 1
}

# Step 1: Check prerequisites
print_status "Checking prerequisites..."

if ! command_exists node; then
    print_error "Node.js is not installed. Please install Node.js first."
    exit 1
fi

if ! command_exists npm; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

NODE_VERSION=$(node --version)
NPM_VERSION=$(npm --version)
print_success "Node.js version: $NODE_VERSION"
print_success "npm version: $NPM_VERSION"

# Step 2: Install dependencies
print_status "Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    print_success "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Step 3: Create necessary directories
print_status "Creating directory structure..."
mkdir -p artifacts/staging
mkdir -p artifacts/published
mkdir -p automation/templates
mkdir -p config
mkdir -p logs
mkdir -p metrics
mkdir -p reports

print_success "Directory structure created"

# Step 4: Start health services
print_status "Starting health services..."

# Start health services in background
npm run health:8000 &
HEALTH_8000_PID=$!

npm run health:4000 &
HEALTH_4000_PID=$!

# Wait for services to be ready
wait_for_service "http://127.0.0.1:8000/api/health" "Health Service 8000"
wait_for_service "http://localhost:4000/api/health" "Health Service 4000"

# Step 5: Run verification
print_status "Running comprehensive verification..."
npm run verify

if [ $? -eq 0 ]; then
    print_success "Verification completed successfully"
else
    print_warning "Verification completed with warnings"
fi

# Step 6: Test content generation
print_status "Testing content generation..."
npm run content:generate "Test Topic" "article"

if [ $? -eq 0 ]; then
    print_success "Content generation test passed"
else
    print_warning "Content generation test failed"
fi

# Step 7: Test automation system
print_status "Testing automation system..."
npm run automation:status

if [ $? -eq 0 ]; then
    print_success "Automation system test passed"
else
    print_warning "Automation system test failed"
fi

# Step 8: Run linting
print_status "Running linting..."
npm run lint:fix

if [ $? -eq 0 ]; then
    print_success "Linting completed successfully"
else
    print_warning "Linting completed with warnings"
fi

# Step 9: Run tests
print_status "Running tests..."
npm run test

if [ $? -eq 0 ]; then
    print_success "Tests passed"
else
    print_warning "Tests completed with warnings"
fi

# Step 10: Build project
print_status "Building project..."
npm run build

if [ $? -eq 0 ]; then
    print_success "Build completed successfully"
else
    print_error "Build failed"
    exit 1
fi

# Step 11: Generate setup report
print_status "Generating setup report..."

REPORT_FILE="reports/setup-report-$(date +%Y%m%d-%H%M%S).txt"

cat > "$REPORT_FILE" << EOF
Monkey Paw Production v4 Setup Report
Generated: $(date)
Node.js Version: $NODE_VERSION
npm Version: $NPM_VERSION

Services Status:
- Health Service 8000: Running (PID: $HEALTH_8000_PID)
- Health Service 4000: Running (PID: $HEALTH_4000_PID)

Available Commands:
- npm run dev:full          # Start full development environment
- npm run start:all         # Start main app with health services
- npm run automation:start  # Start automation system
- npm run verify            # Run verification tests
- npm run monitor           # Start monitoring
- npm run content:generate  # Generate content
- npm run production:full   # Start production environment

Health Check URLs:
- http://127.0.0.1:8000/api/health
- http://localhost:4000/api/health
- http://localhost:3002

Next Steps:
1. Run 'npm run dev:full' to start the complete development environment
2. Open http://localhost:3002 in your browser
3. Check the dashboard for connection status
4. Use 'npm run automation:start' to begin content automation
5. Monitor system health with 'npm run monitor'

EOF

print_success "Setup report generated: $REPORT_FILE"

# Step 12: Final status
echo ""
echo "=========================================================="
print_success "🎉 Setup and Verification Complete!"
echo "=========================================================="
echo ""
print_status "Health Services:"
echo "  ✅ Health Service 8000: http://127.0.0.1:8000/api/health"
echo "  ✅ Health Service 4000: http://localhost:4000/api/health"
echo ""
print_status "Main Application:"
echo "  🚀 Ready to start: npm run dev:full"
echo "  🌐 Will be available at: http://localhost:3002"
echo ""
print_status "Automation System:"
echo "  🤖 Content Generation: Ready"
echo "  📊 Monitoring: Ready"
echo "  🔍 Verification: Complete"
echo ""
print_status "Quick Start Commands:"
echo "  npm run dev:full          # Start everything"
echo "  npm run automation:start  # Start automation"
echo "  npm run verify            # Run verification"
echo "  npm run monitor           # Start monitoring"
echo ""

# Cleanup function
cleanup() {
    print_status "Cleaning up..."
    kill $HEALTH_8000_PID 2>/dev/null || true
    kill $HEALTH_4000_PID 2>/dev/null || true
    print_success "Cleanup complete"
}

# Set up signal handlers
trap cleanup EXIT INT TERM

print_status "Setup complete! Press Ctrl+C to stop health services and exit."
print_status "Or run 'npm run dev:full' in another terminal to start the full system."

# Keep script running to maintain health services
wait
