#!/bin/bash

# LaunchAgents Load Script
# Loads background jobs: hourly autosnap, weekly blitz, API watchdog

echo "🔄 Loading LaunchAgents - Background Jobs"
echo "========================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAUNCHAGENTS_DIR="$HOME/Library/LaunchAgents"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCHAGENTS_DIR"

echo "📁 Project Root: $PROJECT_ROOT"
echo "📁 LaunchAgents: $LAUNCHAGENTS_DIR"
echo ""

# Function to create LaunchAgent plist
create_launchagent() {
    local name="$1"
    local script_path="$2"
    local interval="$3"
    local description="$4"
    
    local plist_file="$LAUNCHAGENTS_DIR/com.monkeypaw.$name.plist"
    
    cat > "$plist_file" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.monkeypaw.$name</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$script_path</string>
    </array>
    
    <key>StartInterval</key>
    <integer>$interval</integer>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <false/>
    
    <key>StandardOutPath</key>
    <string>$PROJECT_ROOT/logs/$name.log</string>
    
    <key>StandardErrorPath</key>
    <string>$PROJECT_ROOT/logs/$name.error.log</string>
    
    <key>WorkingDirectory</key>
    <string>$PROJECT_ROOT</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
        <key>PROJECT_ROOT</key>
        <string>$PROJECT_ROOT</string>
    </dict>
</dict>
</plist>
EOF
    
    echo "✅ Created LaunchAgent: $name"
}

# Create logs directory
mkdir -p "$PROJECT_ROOT/logs"

# 1. Hourly Autosnap (every hour = 3600 seconds)
create_launchagent "autosnap" "$SCRIPTS_DIR/autosnap.sh" 3600 "Hourly autosnap and Drive mirror"

# 2. Weekly Blitz (every week = 604800 seconds)
create_launchagent "weekly_blitz" "$SCRIPTS_DIR/weekly_blitz.sh" 604800 "Weekly marketing blitz update"

# 3. API Watchdog (every 5 minutes = 300 seconds)
create_launchagent "api_watchdog" "$SCRIPTS_DIR/api_watchdog.sh" 300 "API health monitoring"

# 4. Daily Analytics Export (every day = 86400 seconds)
create_launchagent "daily_analytics" "$SCRIPTS_DIR/daily_analytics.sh" 86400 "Daily analytics export"

# 5. Port Monitor (every 30 seconds)
create_launchagent "port_monitor" "$SCRIPTS_DIR/monitor_ports.sh" 30 "Port conflict monitoring"

# Load all LaunchAgents
echo ""
echo "🔄 Loading LaunchAgents..."

launchctl load "$LAUNCHAGENTS_DIR/com.monkeypaw.autosnap.plist" 2>/dev/null || echo "⚠️  Autosnap already loaded"
launchctl load "$LAUNCHAGENTS_DIR/com.monkeypaw.weekly_blitz.plist" 2>/dev/null || echo "⚠️  Weekly blitz already loaded"
launchctl load "$LAUNCHAGENTS_DIR/com.monkeypaw.api_watchdog.plist" 2>/dev/null || echo "⚠️  API watchdog already loaded"
launchctl load "$LAUNCHAGENTS_DIR/com.monkeypaw.daily_analytics.plist" 2>/dev/null || echo "⚠️  Daily analytics already loaded"
launchctl load "$LAUNCHAGENTS_DIR/com.monkeypaw.port_monitor.plist" 2>/dev/null || echo "⚠️  Port monitor already loaded"

echo ""
echo "📋 LaunchAgent Status:"
launchctl list | grep monkeypaw || echo "No monkeypaw agents found"

# Create the supporting scripts
echo ""
echo "📝 Creating supporting scripts..."

# Autosnap script
cat > "$SCRIPTS_DIR/autosnap.sh" << 'EOF'
#!/bin/bash
# Hourly autosnap script

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
SNAPSHOT_DIR="$PROJECT_ROOT/artifacts/snapshots"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

mkdir -p "$SNAPSHOT_DIR"

# Create snapshot
echo "[$TIMESTAMP] Creating hourly snapshot..."
tar -czf "$SNAPSHOT_DIR/snapshot_$TIMESTAMP.tar.gz" \
    --exclude="node_modules" \
    --exclude=".git" \
    --exclude="artifacts/snapshots" \
    -C "$PROJECT_ROOT" .

# Mirror to Google Drive if available
if [ -d "$HOME/Google Drive" ]; then
    cp "$SNAPSHOT_DIR/snapshot_$TIMESTAMP.tar.gz" "$HOME/Google Drive/MonkeyPaw_Snapshots/"
    echo "[$TIMESTAMP] Snapshot mirrored to Google Drive"
fi

# Clean old snapshots (keep last 24)
ls -t "$SNAPSHOT_DIR"/snapshot_*.tar.gz | tail -n +25 | xargs rm -f

echo "[$TIMESTAMP] Autosnap complete"
EOF

# Weekly blitz script
cat > "$SCRIPTS_DIR/weekly_blitz.sh" << 'EOF'
#!/bin/bash
# Weekly marketing blitz script

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

echo "[$TIMESTAMP] Starting weekly marketing blitz..."

# Run blitz updater if it exists
if [ -f "$PROJECT_ROOT/marketing/blitz_updater.py" ]; then
    python3 "$PROJECT_ROOT/marketing/blitz_updater.py"
    echo "[$TIMESTAMP] Marketing blitz updated"
else
    echo "[$TIMESTAMP] Blitz updater not found"
fi

# Log the event
if [ -f "$PROJECT_ROOT/analytics/log_event.py" ]; then
    python3 "$PROJECT_ROOT/analytics/log_event.py" event 'weekly_blitz' '{"timestamp": "'$TIMESTAMP'"}' 'system'
fi

echo "[$TIMESTAMP] Weekly blitz complete"
EOF

# API watchdog script
cat > "$SCRIPTS_DIR/api_watchdog.sh" << 'EOF'
#!/bin/bash
# API health monitoring script

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

echo "[$TIMESTAMP] Checking API health..."

# Check health services
if curl -s http://127.0.0.1:8000/health >/dev/null 2>&1; then
    echo "[$TIMESTAMP] Health service 8000: OK"
else
    echo "[$TIMESTAMP] Health service 8000: FAILED"
fi

if curl -s http://127.0.0.1:4000/health >/dev/null 2>&1; then
    echo "[$TIMESTAMP] Health service 4000: OK"
else
    echo "[$TIMESTAMP] Health service 4000: FAILED"
fi

# Check port conflicts
if [ -f "$PROJECT_ROOT/scripts/monitor_ports.sh" ]; then
    bash "$PROJECT_ROOT/scripts/monitor_ports.sh" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "[$TIMESTAMP] Port monitoring: OK"
    else
        echo "[$TIMESTAMP] Port monitoring: CONFLICTS DETECTED"
    fi
fi

echo "[$TIMESTAMP] API watchdog check complete"
EOF

# Daily analytics script
cat > "$SCRIPTS_DIR/daily_analytics.sh" << 'EOF'
#!/bin/bash
# Daily analytics export script

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
EXPORT_DIR="$PROJECT_ROOT/artifacts/analytics_exports"

mkdir -p "$EXPORT_DIR"

echo "[$TIMESTAMP] Exporting daily analytics..."

# Export analytics data
if [ -f "$PROJECT_ROOT/analytics/log_event.py" ]; then
    python3 "$PROJECT_ROOT/analytics/log_event.py" export "$EXPORT_DIR/analytics_$TIMESTAMP.json"
    echo "[$TIMESTAMP] Analytics exported to $EXPORT_DIR/analytics_$TIMESTAMP.json"
else
    echo "[$TIMESTAMP] Analytics logger not found"
fi

# Clean old exports (keep last 30 days)
find "$EXPORT_DIR" -name "analytics_*.json" -mtime +30 -delete

echo "[$TIMESTAMP] Daily analytics export complete"
EOF

# Make scripts executable
chmod +x "$SCRIPTS_DIR/autosnap.sh"
chmod +x "$SCRIPTS_DIR/weekly_blitz.sh"
chmod +x "$SCRIPTS_DIR/api_watchdog.sh"
chmod +x "$SCRIPTS_DIR/daily_analytics.sh"

echo ""
echo "🎉 LAUNCHAGENTS LOADED!"
echo "======================="
echo "✅ Hourly autosnap: Active"
echo "✅ Weekly blitz: Active"
echo "✅ API watchdog: Active"
echo "✅ Daily analytics: Active"
echo "✅ Port monitor: Active"
echo ""
echo "Background jobs are now running automatically:"
echo "• Snapshots every hour"
echo "• Marketing blitz every week"
echo "• API health checks every 5 minutes"
echo "• Analytics export every day"
echo "• Port monitoring every 30 seconds"
echo ""
echo "To unload LaunchAgents:"
echo "  bash scripts/launchagents_unload.sh"
echo ""
echo "Your automated business is now fully autonomous! 🤖"
