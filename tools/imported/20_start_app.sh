#!/bin/bash

# TRAE.AI Application Startup Script
# This script provides a simple interface to start and manage the TRAE.AI application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$PROJECT_DIR/startup.log"
PID_FILE="$PROJECT_DIR/app.pid"

# Functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO:${NC} $1" | tee -a "$LOG_FILE"
}

# Check if app is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

# Start the application
start_app() {
    log "🚀 Starting TRAE.AI Application System..."

    # Change to project directory
    cd "$PROJECT_DIR"

    # Check if already running
    if is_running; then
        warn "Application is already running (PID: $(cat "$PID_FILE"))"
        return 0
    fi

    # Start Ollama if not running
    if ! pgrep -f "ollama serve" > /dev/null; then
        log "🤖 Starting Ollama service..."
        if command -v ollama >/dev/null 2>&1; then
            ollama serve > /dev/null 2>&1 &
            sleep 3
            log "✅ Ollama service started"
        else
            warn "⚠️  Ollama not found, attempting to install via Homebrew..."
            if command -v brew >/dev/null 2>&1; then
                brew install ollama
                ollama serve > /dev/null 2>&1 &
                sleep 3
                log "✅ Ollama installed and started"
            else
                error "❌ Homebrew not found, please install Ollama manually"
            fi
        fi
    else
        log "✅ Ollama is already running"
    fi

    # Start Chrome with essential tabs if not running
    if ! pgrep -f "Google Chrome" > /dev/null; then
        log "🌐 Starting Chrome with essential tabs..."
        open -a "Google Chrome"
        sleep 2

        # Open essential tabs
        open -u "http://localhost:8000"
        open -u "http://localhost:9000"
        open -u "https://github.com"
        open -u "https://netlify.com"
        open -u "https://openai.com"

        log "✅ Chrome started with essential tabs"
    else
        log "✅ Chrome is already running"
    fi

    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        log "Activating virtual environment..."
        source venv/bin/activate
    fi

    # Start the system manager
    log "Starting system manager..."
    python3 startup_system.py --mode production > "$LOG_FILE" 2>&1 &
    local pid=$!

    # Save PID
    echo $pid > "$PID_FILE"

    # Wait a moment and check if it started successfully
    sleep 3

    if ps -p "$pid" > /dev/null 2>&1; then
        log "✅ Application started successfully (PID: $pid)"
        log "🌐 Application should be available at: http://localhost:8000"
        log "📊 Health check: http://localhost:8000/health"
        log "📖 API docs: http://localhost:8000/docs"
        log "🌐 Dashboard: http://localhost:9000"
        log "📋 Logs: tail -f $LOG_FILE"
        return 0
    else
        error "❌ Application failed to start"
        rm -f "$PID_FILE"
        return 1
    fi
}

# Stop the application
stop_app() {
    log "🛑 Stopping TRAE.AI Application..."

    if ! is_running; then
        warn "Application is not running"
        return 0
    fi

    local pid=$(cat "$PID_FILE")

    # Send SIGTERM for graceful shutdown
    log "Sending graceful shutdown signal to PID $pid..."
    kill -TERM "$pid" 2>/dev/null || true

    # Wait for graceful shutdown
    local count=0
    while [ $count -lt 30 ] && ps -p "$pid" > /dev/null 2>&1; do
        sleep 1
        count=$((count + 1))
    done

    # Force kill if still running
    if ps -p "$pid" > /dev/null 2>&1; then
        warn "Graceful shutdown failed, force killing..."
        kill -KILL "$pid" 2>/dev/null || true
        sleep 2
    fi

    # Kill any remaining processes
    pkill -f "startup_system.py" 2>/dev/null || true
    pkill -f "uvicorn.*main:app" 2>/dev/null || true

    # Clean up PID file
    rm -f "$PID_FILE"

    # Optionally stop Ollama (commented out to keep it running for other uses)
    # log "🤖 Stopping Ollama service..."
    # pkill -f "ollama serve" 2>/dev/null || true

    log "✅ Application stopped"
    info "ℹ️  Note: Ollama and Chrome are left running for continued use"
}

# Restart the application
restart_app() {
    log "🔄 Restarting TRAE.AI Application..."
    stop_app
    sleep 2
    start_app
}

# Show application status
status_app() {
    echo -e "\n${BLUE}=== TRAE.AI Application Status ===${NC}"

    if is_running; then
        local pid=$(cat "$PID_FILE")
        log "✅ Application is running (PID: $pid)"

        # Show process info
        echo -e "\n${BLUE}Process Information:${NC}"
        ps -p "$pid" -o pid,ppid,pcpu,pmem,etime,command || true

        # Check if web server is responding
        echo -e "\n${BLUE}Service Health:${NC}"
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health | grep -q "200"; then
            log "✅ Web server is responding"
        else
            warn "⚠️ Web server is not responding"
        fi

        # Show recent logs
        echo -e "\n${BLUE}Recent Logs (last 10 lines):${NC}"
        tail -n 10 "$LOG_FILE" 2>/dev/null || echo "No logs available"

    else
        warn "❌ Application is not running"
    fi

    # Show system resources
    echo -e "\n${BLUE}System Resources:${NC}"
    echo "CPU Usage: $(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')%"
    echo "Memory Usage: $(top -l 1 | grep "PhysMem" | awk '{print $2}' | sed 's/M/MB/')"
    echo "Disk Usage: $(df -h . | tail -1 | awk '{print $5}') of $(df -h . | tail -1 | awk '{print $2}')"
}

# Show logs
show_logs() {
    if [ -f "$LOG_FILE" ]; then
        if [ "$1" = "-f" ] || [ "$1" = "--follow" ]; then
            log "Following logs (Ctrl+C to stop)..."
            tail -f "$LOG_FILE"
        else
            log "Showing recent logs..."
            tail -n 50 "$LOG_FILE"
        fi
    else
        warn "No log file found at $LOG_FILE"
    fi
}

# Install as system service (macOS LaunchAgent)
install_service() {
    log "📦 Installing TRAE.AI as system service..."

    local plist_file="$HOME/Library/LaunchAgents/com.traeai.app.plist"

    cat > "$plist_file" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.traeai.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PROJECT_DIR/start_app.sh</string>
        <string>start</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$PROJECT_DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$PROJECT_DIR/service.log</string>
    <key>StandardErrorPath</key>
    <string>$PROJECT_DIR/service.error.log</string>
</dict>
</plist>
EOF

    # Load the service
    launchctl load "$plist_file"

    log "✅ Service installed and loaded"
    log "   Service will start automatically on login"
    log "   Control with: launchctl start/stop com.traeai.app"
}

# Uninstall system service
uninstall_service() {
    log "🗑️ Uninstalling TRAE.AI system service..."

    local plist_file="$HOME/Library/LaunchAgents/com.traeai.app.plist"

    # Unload and remove
    launchctl unload "$plist_file" 2>/dev/null || true
    rm -f "$plist_file"

    log "✅ Service uninstalled"
}

# Show help
show_help() {
    echo -e "\n${BLUE}TRAE.AI Application Manager${NC}"
    echo -e "Usage: $0 {start|stop|restart|status|logs|install-service|uninstall-service|help}"
    echo ""
    echo "Commands:"
    echo "  start              Start the application"
    echo "  stop               Stop the application"
    echo "  restart            Restart the application"
    echo "  status             Show application status"
    echo "  logs [-f]          Show logs (use -f to follow)"
    echo "  install-service    Install as system service (auto-start)"
    echo "  uninstall-service  Remove system service"
    echo "  help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start           # Start the application"
    echo "  $0 logs -f         # Follow logs in real-time"
    echo "  $0 install-service # Install to start automatically"
    echo ""
}

# Main script logic
case "${1:-}" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    restart)
        restart_app
        ;;
    status)
        status_app
        ;;
    logs)
        show_logs "$2"
        ;;
    install-service)
        install_service
        ;;
    uninstall-service)
        uninstall_service
        ;;
    help|--help|-h)
        show_help
        ;;
    "")
        warn "No command specified"
        show_help
        exit 1
        ;;
    *)
        error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
