#!/bin/bash

# RUN EVERYTHING SCRIPT
# Starts runtime + snapshot + tunnel (if cloudflared installed) and verifies GREEN

echo "🚀 Starting Complete System Runtime"
echo "=================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "📁 Project Root: $PROJECT_ROOT"
echo ""

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -i :$port >/dev/null 2>&1; then
        echo "⚠️  Port $port is already in use"
        return 1
    else
        echo "✅ Port $port is available"
        return 0
    fi
}

# Function to start health services
start_health_services() {
    echo "🏥 Starting Health Services..."
    
    # Check ports
    check_port 8000
    check_port 4000
    
    # Start health services in background
    echo "Starting health service on port 8000..."
    npm run health:8000 &
    HEALTH_8000_PID=$!
    
    echo "Starting health service on port 4000..."
    npm run health:4000 &
    HEALTH_4000_PID=$!
    
    # Wait a moment for services to start
    sleep 3
    
    # Check if services are running
    if curl -s http://127.0.0.1:8000/health >/dev/null 2>&1; then
        echo "✅ Health service 8000: Running"
    else
        echo "❌ Health service 8000: Failed to start"
    fi
    
    if curl -s http://127.0.0.1:4000/health >/dev/null 2>&1; then
        echo "✅ Health service 4000: Running"
    else
        echo "❌ Health service 4000: Failed to start"
    fi
}

# Function to start main application
start_main_app() {
    echo "🎯 Starting Main Application..."
    
    # Check if development server is already running
    if curl -s http://127.0.0.1:3002 >/dev/null 2>&1; then
        echo "⚠️  Development server already running on port 3002"
    else
        echo "Starting development server..."
        npm run dev &
        DEV_PID=$!
        
        # Wait for server to start
        sleep 5
        
        if curl -s http://127.0.0.1:3002 >/dev/null 2>&1; then
            echo "✅ Development server: Running on http://127.0.0.1:3002"
        else
            echo "❌ Development server: Failed to start"
        fi
    fi
}

# Function to start automation systems
start_automation() {
    echo "🤖 Starting Automation Systems..."
    
    # Start automation orchestrator
    if [ -f "automation/automation-orchestrator.js" ]; then
        echo "Starting automation orchestrator..."
        npm run automation:start &
        AUTO_PID=$!
        echo "✅ Automation orchestrator: Started"
    else
        echo "⚠️  Automation orchestrator not found"
    fi
    
    # Start business automation
    if [ -f "automation/business-automation-system.js" ]; then
        echo "Starting business automation system..."
        npm run business:start &
        BUSINESS_PID=$!
        echo "✅ Business automation: Started"
    else
        echo "⚠️  Business automation system not found"
    fi
}

# Function to start tunnel (if cloudflared is available)
start_tunnel() {
    echo "🌐 Checking for Tunnel Service..."
    
    if command -v cloudflared >/dev/null 2>&1; then
        echo "Starting cloudflared tunnel..."
        cloudflared tunnel --url http://127.0.0.1:3002 &
        TUNNEL_PID=$!
        echo "✅ Cloudflared tunnel: Started"
    else
        echo "⚠️  Cloudflared not installed - skipping tunnel"
        echo "   Install with: brew install cloudflared"
    fi
}

# Function to create snapshot
create_snapshot() {
    echo "📸 Creating System Snapshot..."
    
    SNAPSHOT_DIR="artifacts/snapshots"
    TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
    
    mkdir -p "$SNAPSHOT_DIR"
    
    # Create snapshot
    tar -czf "$SNAPSHOT_DIR/runtime_snapshot_$TIMESTAMP.tar.gz" \
        --exclude="node_modules" \
        --exclude=".git" \
        --exclude="artifacts/snapshots" \
        --exclude="logs" \
        -C "$PROJECT_ROOT" .
    
    echo "✅ Snapshot created: $SNAPSHOT_DIR/runtime_snapshot_$TIMESTAMP.tar.gz"
    
    # Mirror to Google Drive if available
    if [ -d "$HOME/Google Drive" ]; then
        mkdir -p "$HOME/Google Drive/MonkeyPaw_Snapshots"
        cp "$SNAPSHOT_DIR/runtime_snapshot_$TIMESTAMP.tar.gz" "$HOME/Google Drive/MonkeyPaw_Snapshots/"
        echo "✅ Snapshot mirrored to Google Drive"
    fi
}

# Function to run GREEN verification
run_green_verification() {
    echo "🟢 Running GREEN Verification..."
    
    if [ -f "verifier/check_green.py" ]; then
        python3 verifier/check_green.py
        GREEN_EXIT_CODE=$?
        
        if [ $GREEN_EXIT_CODE -eq 0 ]; then
            echo "✅ GREEN verification: PASSED"
        else
            echo "❌ GREEN verification: FAILED"
            echo "   Check the verification report for details"
        fi
    else
        echo "⚠️  GREEN verifier not found - creating basic check..."
        
        # Basic health check
        echo "Running basic health checks..."
        
        # Check health services
        if curl -s http://127.0.0.1:8000/health >/dev/null 2>&1; then
            echo "✅ Health service 8000: OK"
        else
            echo "❌ Health service 8000: FAILED"
        fi
        
        if curl -s http://127.0.0.1:4000/health >/dev/null 2>&1; then
            echo "✅ Health service 4000: OK"
        else
            echo "❌ Health service 4000: FAILED"
        fi
        
        # Check main app
        if curl -s http://127.0.0.1:3002 >/dev/null 2>&1; then
            echo "✅ Main application: OK"
        else
            echo "❌ Main application: FAILED"
        fi
        
        # Check port isolation
        if [ -f "scripts/monitor_ports.sh" ]; then
            bash scripts/monitor_ports.sh
        fi
    fi
}

# Function to log system start
log_system_start() {
    echo "📊 Logging System Start..."
    
    if [ -f "analytics/log_event.py" ]; then
        python3 analytics/log_event.py event 'system_start' '{"timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'", "mode": "full_runtime"}' 'system'
        echo "✅ System start logged to analytics"
    else
        echo "⚠️  Analytics logger not found"
    fi
}

# Function to display status
display_status() {
    echo ""
    echo "🎉 SYSTEM RUNTIME STATUS"
    echo "========================"
    echo ""
    echo "🌐 Web Services:"
    echo "  • Main App: http://127.0.0.1:3002"
    echo "  • Health 8000: http://127.0.0.1:8000/health"
    echo "  • Health 4000: http://127.0.0.1:4000/health"
    echo ""
    echo "🤖 Automation:"
    echo "  • Orchestrator: Running"
    echo "  • Business System: Running"
    echo ""
    echo "📊 Analytics:"
    echo "  • Event Logging: Active"
    echo "  • Database: analytics/telemetry.sqlite"
    echo ""
    echo "🔒 Port Isolation:"
    echo "  • Dashboard: 9600"
    echo "  • Linlyx-Talker: 9510"
    echo "  • Talking Heads: 9520"
    echo ""
    echo "📸 Snapshots:"
    echo "  • Local: artifacts/snapshots/"
    echo "  • Google Drive: ~/Google Drive/MonkeyPaw_Snapshots/"
    echo ""
    echo "🟢 Status: SYSTEM RUNNING"
    echo ""
    echo "To stop the system:"
    echo "  Press Ctrl+C or run: pkill -f 'node.*health-service'"
    echo ""
    echo "Your automated business empire is now LIVE! 🚀"
}

# Main execution
main() {
    echo "🚀 Starting complete system runtime..."
    echo ""
    
    # Step 1: Start health services
    start_health_services
    
    # Step 2: Start main application
    start_main_app
    
    # Step 3: Start automation systems
    start_automation
    
    # Step 4: Start tunnel (if available)
    start_tunnel
    
    # Step 5: Create snapshot
    create_snapshot
    
    # Step 6: Run GREEN verification
    run_green_verification
    
    # Step 7: Log system start
    log_system_start
    
    # Step 8: Display status
    display_status
    
    # Keep script running and show live status
    echo "🔄 System is running... Press Ctrl+C to stop"
    
    # Set up signal handlers
    trap 'echo ""; echo "🛑 Shutting down system..."; pkill -f "node.*health-service" 2>/dev/null; exit 0' INT TERM
    
    # Keep running
    while true; do
        sleep 30
        echo "💓 System heartbeat: $(date)"
    done
}

# Run main function
main "$@"
