#!/bin/bash

# LaunchAgents Unload Script
# Unloads background jobs: hourly autosnap, weekly blitz, API watchdog

echo "🛑 Unloading LaunchAgents - Stopping Background Jobs"
echo "==================================================="

LAUNCHAGENTS_DIR="$HOME/Library/LaunchAgents"

echo "📁 LaunchAgents: $LAUNCHAGENTS_DIR"
echo ""

# Unload all LaunchAgents
echo "🔄 Unloading LaunchAgents..."

launchctl unload "$LAUNCHAGENTS_DIR/com.monkeypaw.autosnap.plist" 2>/dev/null || echo "⚠️  Autosnap not loaded"
launchctl unload "$LAUNCHAGENTS_DIR/com.monkeypaw.weekly_blitz.plist" 2>/dev/null || echo "⚠️  Weekly blitz not loaded"
launchctl unload "$LAUNCHAGENTS_DIR/com.monkeypaw.api_watchdog.plist" 2>/dev/null || echo "⚠️  API watchdog not loaded"
launchctl unload "$LAUNCHAGENTS_DIR/com.monkeypaw.daily_analytics.plist" 2>/dev/null || echo "⚠️  Daily analytics not loaded"
launchctl unload "$LAUNCHAGENTS_DIR/com.monkeypaw.port_monitor.plist" 2>/dev/null || echo "⚠️  Port monitor not loaded"

echo ""
echo "📋 LaunchAgent Status:"
launchctl list | grep monkeypaw || echo "✅ No monkeypaw agents running"

# Optionally remove plist files
read -p "Remove LaunchAgent plist files? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f "$LAUNCHAGENTS_DIR/com.monkeypaw.autosnap.plist"
    rm -f "$LAUNCHAGENTS_DIR/com.monkeypaw.weekly_blitz.plist"
    rm -f "$LAUNCHAGENTS_DIR/com.monkeypaw.api_watchdog.plist"
    rm -f "$LAUNCHAGENTS_DIR/com.monkeypaw.daily_analytics.plist"
    rm -f "$LAUNCHAGENTS_DIR/com.monkeypaw.port_monitor.plist"
    echo "✅ LaunchAgent plist files removed"
fi

echo ""
echo "🛑 LAUNCHAGENTS UNLOADED!"
echo "========================="
echo "✅ Hourly autosnap: Stopped"
echo "✅ Weekly blitz: Stopped"
echo "✅ API watchdog: Stopped"
echo "✅ Daily analytics: Stopped"
echo "✅ Port monitor: Stopped"
echo ""
echo "Background jobs are now stopped."
echo "Your system is in manual mode."
echo ""
echo "To reload LaunchAgents:"
echo "  bash scripts/launchagents_load.sh"
echo ""
echo "Background automation paused! ⏸️"
