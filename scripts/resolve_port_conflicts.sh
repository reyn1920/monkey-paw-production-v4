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
