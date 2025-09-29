#!/bin/bash

# Ports Guard Script - Prevents Avatar Port Conflicts
# This script ensures proper port isolation to prevent dashboard crashes

echo "🔒 Setting up Avatar Port Isolation..."

# Define port assignments
LINLYX_PORT=9510
TALKING_HEADS_PORT=9520
DASHBOARD_PORT=9600

# Create ports configuration
mkdir -p config
cat > config/ports.yaml << EOF
# Avatar Port Configuration
# CRITICAL: Never bind dashboard to avatar ports - this causes crashes

avatar_ports:
  linlyx_talker:
    port: $LINLYX_PORT
    service: "Linlyx-Talker (Primary Avatar)"
    description: "Full-body avatar with natural expressions and movements"
    
  talking_heads:
    port: $TALKING_HEADS_PORT
    service: "Talking Heads / Picoccio (Secondary Avatar)"
    description: "Talking head avatar with facial expressions"
    
dashboard_ports:
  main_dashboard:
    port: $DASHBOARD_PORT
    service: "Automation Dashboard"
    description: "Main control dashboard - NEVER bind to avatar ports"

# Port conflict prevention
conflict_prevention:
  enabled: true
  check_interval: 30
  auto_kill_conflicts: false
  log_conflicts: true
EOF

echo "✅ Port configuration created at config/ports.yaml"

# Create port monitoring script
cat > scripts/monitor_ports.sh << 'EOF'
#!/bin/bash

# Port Monitor - Checks for port conflicts
source config/ports.yaml 2>/dev/null || {
    echo "❌ Port configuration not found. Run ports_guard.sh first."
    exit 1
}

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
EOF

chmod +x scripts/monitor_ports.sh

# Create port conflict resolver
cat > scripts/resolve_port_conflicts.sh << 'EOF'
#!/bin/bash

# Port Conflict Resolver - Safely resolves port conflicts

echo "🔧 Resolving port conflicts..."

# Function to safely kill process on port
kill_port_process() {
    local port=$1
    local service=$2
    
    if lsof -i :$port >/dev/null 2>&1; then
        local pid=$(lsof -ti :$port)
        local process=$(ps -p $pid -o comm= 2>/dev/null || echo "unknown")
        
        echo "⚠️  Found $process (PID $pid) on port $port ($service)"
        
        # Don't kill critical system processes
        if [[ "$process" =~ ^(kernel_task|WindowServer|loginwindow)$ ]]; then
            echo "❌ Cannot kill system process $process"
            return 1
        fi
        
        # Ask for confirmation before killing
        read -p "Kill $process (PID $pid) on port $port? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill -TERM $pid
            sleep 2
            if kill -0 $pid 2>/dev/null; then
                echo "Force killing $pid..."
                kill -KILL $pid
            fi
            echo "✅ Freed port $port"
        else
            echo "⏭️  Skipped port $port"
        fi
    fi
}

# Check and resolve conflicts
kill_port_process 9510 "Linlyx-Talker"
kill_port_process 9520 "Talking Heads"
kill_port_process 9600 "Dashboard"

echo "✅ Port conflict resolution complete"
EOF

chmod +x scripts/resolve_port_conflicts.sh

echo "✅ Port isolation system created:"
echo "   📁 config/ports.yaml - Port configuration"
echo "   🔍 scripts/monitor_ports.sh - Port monitoring"
echo "   🔧 scripts/resolve_port_conflicts.sh - Conflict resolution"
echo ""
echo "🚨 CRITICAL RULES:"
echo "   • Linlyx-Talker: Port 9510"
echo "   • Talking Heads: Port 9520" 
echo "   • Dashboard: Port 9600 ONLY"
echo "   • NEVER bind dashboard to avatar ports (causes crashes)"
echo ""
echo "Run 'bash scripts/monitor_ports.sh' to check port status"
