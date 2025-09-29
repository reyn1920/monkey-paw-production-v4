#!/bin/bash

# Go-Live Enable Script
# Enables real publishing behavior (turns off dry_run mode)

echo "🚀 Enabling Go-Live Mode - Real Publishing Behavior"
echo "=================================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_DIR="$PROJECT_ROOT/config"

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Enable go-live mode in features.yaml
cat > "$CONFIG_DIR/features.yaml" << 'EOF'
# Go-Live Configuration
# This file controls production behavior

# Publishing behavior
publishing:
  dry_run: false  # Set to true for testing, false for real publishing
  auto_publish: true
  require_approval: false
  
# API usage
apis:
  use_paid_apis: false  # Set to true when you can afford paid APIs
  fallback_to_free: true
  
# Safety features
safety:
  backup_before_publish: true
  max_daily_posts: 50
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
    auto_start: true
    
  talking_heads:
    enabled: true
    port: 9520
    auto_start: true
    
# Video pipeline
video_pipeline:
  auto_render: true
  quality: "high"
  background_removal: true
  
# Business automation
business_automation:
  income_streams: 9
  auto_optimize: true
  revenue_tracking: true
EOF

echo "✅ Go-Live mode enabled in config/features.yaml"

# Update package.json scripts to use production settings
if [ -f "$PROJECT_ROOT/package.json" ]; then
    echo "📦 Updating package.json for production..."
    
    # Add production scripts if they don't exist
    if ! grep -q '"production:start"' "$PROJECT_ROOT/package.json"; then
        # This would require more complex JSON manipulation
        echo "⚠️  Manual update needed: Add production scripts to package.json"
    fi
fi

# Create production environment file
cat > "$PROJECT_ROOT/.env.production" << 'EOF'
# Production Environment Variables
NODE_ENV=production
GO_LIVE_MODE=true
DRY_RUN=false

# API Keys (add your actual keys here)
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
# GOOGLE_GENERATIVE_AI_API_KEY=your_key_here

# Database
DATABASE_URL=sqlite:./db/monkey_paw.db

# Ports
DASHBOARD_PORT=9600
LINLYX_PORT=9510
TALKING_HEADS_PORT=9520

# Analytics
ANALYTICS_ENABLED=true
TELEMETRY_DB=./analytics/telemetry.sqlite
EOF

echo "✅ Production environment file created"

# Log the go-live event
if [ -f "$PROJECT_ROOT/analytics/log_event.py" ]; then
    python3 "$PROJECT_ROOT/analytics/log_event.py" event 'go_live_enabled' '{"mode": "production", "dry_run": false}' 'system'
fi

echo ""
echo "🎉 GO-LIVE MODE ENABLED!"
echo "========================"
echo "✅ Real publishing behavior is now active"
echo "✅ Dry-run mode is disabled"
echo "✅ Production environment configured"
echo "✅ Analytics tracking enabled"
echo ""
echo "⚠️  WARNING: This will now publish real content!"
echo "   Make sure you're ready before proceeding."
echo ""
echo "Next steps:"
echo "1. Review config/features.yaml settings"
echo "2. Add your API keys to .env.production"
echo "3. Run: bash scripts/launchagents_load.sh"
echo "4. Monitor your content and revenue streams"
echo ""
echo "Your automated business is now LIVE! 🚀"
