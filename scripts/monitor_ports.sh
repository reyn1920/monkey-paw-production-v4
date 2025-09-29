#!/bin/bash

# Port Monitor - Checks for port conflicts

# Default port assignments
LINLYX_PORT=9510
TALKING_HEADS_PORT=9520
DASHBOARD_PORT=9600

# Try to read from config if available
if [ -f "config/ports.yaml" ]; then
    # Extract ports from YAML (simple parsing)
    LINLYX_PORT=$(grep -A1 "linlyx_talker:" config/ports.yaml | grep "port:" | awk '{print $2}' || echo "9510")
    TALKING_HEADS_PORT=$(grep -A1 "talking_heads:" config/ports.yaml | grep "port:" | awk '{print $2}' || echo "9520")
    DASHBOARD_PORT=$(grep -A1 "main_dashboard:" config/ports.yaml | grep "port:" | awk '{print $2}' || echo "9600")
fi

check_port() {
    local port=$1
    local service=$2
    
    if lsof -i :$port >/dev/null 2>&1; then
        local pid=$(lsof -ti :$port)
        local process=$(ps -p $pid -o comm= 2>/dev/null || echo "unknown")
        echo "⚠️  Port $port ($service) is in use by PID $pid ($process)"
        return 1
    else
        echo "✅ Port $port ($service) is available"
        return 0
    fi
}

echo "🔍 Checking avatar port isolation..."

# Check avatar ports
check_port $LINLYX_PORT "Linlyx-Talker"
check_port $TALKING_HEADS_PORT "Talking Heads"

# Check dashboard port
check_port $DASHBOARD_PORT "Dashboard"

# Check for conflicts
echo ""
echo "🚨 Checking for port conflicts..."

# Check if dashboard is bound to avatar ports (CRITICAL ERROR)
if lsof -i :$LINLYX_PORT | grep -q "dashboard\|automation"; then
    echo "❌ CRITICAL: Dashboard is bound to Linlyx port $LINLYX_PORT - This will cause crashes!"
    exit 1
fi

if lsof -i :$TALKING_HEADS_PORT | grep -q "dashboard\|automation"; then
    echo "❌ CRITICAL: Dashboard is bound to Talking Heads port $TALKING_HEADS_PORT - This will cause crashes!"
    exit 1
fi

echo "✅ No port conflicts detected"
