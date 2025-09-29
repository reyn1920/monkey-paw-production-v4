#!/bin/bash

# Go-Live Disable Script
# Disables real publishing behavior (turns on dry_run mode)

echo "🛑 Disabling Go-Live Mode - Safe Testing Mode"
echo "============================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_DIR="$PROJECT_ROOT/config"

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Disable go-live mode in features.yaml
cat > "$CONFIG_DIR/features.yaml" << 'EOF'
# Safe Testing Configuration
# This file controls production behavior

# Publishing behavior
publishing:
  dry_run: true  # Set to true for testing, false for real publishing
  auto_publish: false
  require_approval: true
  
# API usage
apis:
  use_paid_apis: false  # Set to true when you can afford paid APIs
  fallback_to_free: true
  
# Safety features
safety:
  backup_before_publish: true
  max_daily_posts: 10  # Reduced for testing
  rate_limiting: true
  
# Analytics
analytics:
  track_all_events: true
  export_daily: true
  
# Avatar settings
avatars:
  linlyx_talker:
    enabled: true
    port: 9510
    auto_start: false  # Manual start for testing
    
  talking_heads:
    enabled: true
    port: 9520
    auto_start: false  # Manual start for testing
    
# Video pipeline
video_pipeline:
  auto_render: false  # Manual render for testing
  quality: "medium"
  background_removal: true
  
# Business automation
business_automation:
  income_streams: 9
  auto_optimize: false  # Manual optimization for testing
  revenue_tracking: true
EOF

echo "✅ Go-Live mode disabled in config/features.yaml"

# Create testing environment file
cat > "$PROJECT_ROOT/.env.testing" << 'EOF'
# Testing Environment Variables
NODE_ENV=development
GO_LIVE_MODE=false
DRY_RUN=true

# API Keys (use test keys or leave empty)
# OPENAI_API_KEY=test_key
# ANTHROPIC_API_KEY=test_key
# GOOGLE_GENERATIVE_AI_API_KEY=test_key

# Database
DATABASE_URL=sqlite:./db/monkey_paw_test.db

# Ports
DASHBOARD_PORT=9600
LINLYX_PORT=9510
TALKING_HEADS_PORT=9520

# Analytics
ANALYTICS_ENABLED=true
TELEMETRY_DB=./analytics/telemetry_test.sqlite
EOF

echo "✅ Testing environment file created"

# Log the go-live disable event
if [ -f "$PROJECT_ROOT/analytics/log_event.py" ]; then
    python3 "$PROJECT_ROOT/analytics/log_event.py" event 'go_live_disabled' '{"mode": "testing", "dry_run": true}' 'system'
fi

echo ""
echo "🛑 GO-LIVE MODE DISABLED!"
echo "========================="
echo "✅ Safe testing mode is now active"
echo "✅ Dry-run mode is enabled"
echo "✅ Auto-publishing is disabled"
echo "✅ Manual approval required"
echo "✅ Reduced rate limits for testing"
echo ""
echo "✅ SAFE: No real content will be published"
echo "   Perfect for testing and development"
echo ""
echo "To re-enable go-live mode:"
echo "  bash scripts/go_live_enable.sh"
echo ""
echo "Your system is now in safe testing mode! 🧪"
