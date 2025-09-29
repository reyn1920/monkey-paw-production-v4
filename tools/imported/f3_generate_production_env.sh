#!/bin/bash

# Production Environment Generator Script
# This script generates secure environment variables for production deployment

echo "Generating production environment configuration..."

# Create backup of existing .env if it exists
if [ -f ".env" ]; then
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    echo "Backed up existing .env file"
fi

# Generate secure random values
TRAE_MASTER_KEY="trae_prod_master_key_2025_$(openssl rand -hex 16)"
SECRET_KEY="prod_secret_key_2025_$(openssl rand -hex 16)"
JWT_SECRET="prod_jwt_secret_2025_$(openssl rand -hex 16)"
DASHBOARD_SECRET_KEY="dashboard_secret_2025_$(openssl rand -hex 12)"
MONITORING_SECRET_KEY="monitoring_secret_2025_$(openssl rand -hex 12)"
ROUTELLM_SECRET_KEY="routellm_secret_2025_$(openssl rand -hex 12)"
TOTAL_ACCESS_SECRET_KEY="total_access_secret_2025_$(openssl rand -hex 12)"
SYSTEM_MONITOR_SECRET_KEY="system_monitor_secret_2025_$(openssl rand -hex 12)"
SCANNER_TOKEN="scanner_token_2025_$(openssl rand -hex 12)"
EDGE_TTS_TOKEN="edge_tts_token_2025_$(openssl rand -hex 12)"
SECURITY_SCANNER_SECRET="security_scanner_secret_2025_$(openssl rand -hex 12)"
TEST_CLIENT_SECRET="test_client_secret_2025_$(openssl rand -hex 12)"
TRAE_API_TOKEN="trae_api_token_2025_$(openssl rand -hex 12)"

# Create production .env file
cat > .env << EOF
# Production Environment Configuration
# Generated: $(date)
# WARNING: This file contains sensitive information - do not commit to version control

# Environment Settings
ENVIRONMENT=production
NODE_ENV=production
USE_MOCK=false
LOG_LEVEL=INFO
DEBUG=false

# Core Application Configuration
HOST=0.0.0.0
PORT=8080

# Security Keys (Generated)
TRAE_MASTER_KEY=${TRAE_MASTER_KEY}
SECRET_KEY=${SECRET_KEY}
JWT_SECRET=${JWT_SECRET}
DASHBOARD_SECRET_KEY=${DASHBOARD_SECRET_KEY}
MONITORING_SECRET_KEY=${MONITORING_SECRET_KEY}
ROUTELLM_SECRET_KEY=${ROUTELLM_SECRET_KEY}
TOTAL_ACCESS_SECRET_KEY=${TOTAL_ACCESS_SECRET_KEY}
SYSTEM_MONITOR_SECRET_KEY=${SYSTEM_MONITOR_SECRET_KEY}
SCANNER_TOKEN=${SCANNER_TOKEN}
EDGE_TTS_TOKEN=${EDGE_TTS_TOKEN}
SECURITY_SCANNER_SECRET=${SECURITY_SCANNER_SECRET}
TEST_CLIENT_SECRET=${TEST_CLIENT_SECRET}
TRAE_API_TOKEN=${TRAE_API_TOKEN}

# Database Configuration
DATABASE_URL=sqlite:///./data/app.db

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080","https://yourdomain.com"]
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,https://yourdomain.com
TRUSTED_HOSTS=localhost,yourdomain.com

# Rate Limiting
RATE_LIMIT_RPM=120

# Geocoding Configuration
NOMINATIM_USER_AGENT="TraeApp/1.0 (production)"

# Feature Flags
ENABLE_FULL_API=1
ENABLE_DASHBOARD=1
REQUIRE_PETFINDER=false

# Social Media Configuration (Disabled for security)
SOCIAL_ENABLED=false
FACEBOOK_ACCESS_TOKEN=
LINKEDIN_ACCESS_TOKEN=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
PINTEREST_ACCESS_TOKEN=
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
INSTAGRAM_ACCESS_TOKEN=
YOUTUBE_API_KEY=

# External API Keys (Set to empty - replace with real values when available)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
COQUI_API_KEY=
GROK_API_KEY=

# Deployment Configuration (Set to empty - replace with real values when available)
NETLIFY_AUTH_TOKEN=
NETLIFY_SITE_ID=

# Payment Configuration (Set to empty - replace with real values when available)
STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
EOF

echo "Production environment configuration generated successfully!"
echo "File: .env"
echo ""
echo "IMPORTANT SECURITY NOTES:"
echo "1. This file contains sensitive information - do not commit to version control"
echo "2. Replace placeholder API keys with real values before deployment"
echo "3. Ensure proper file permissions: chmod 600 .env"
echo "4. Backup this file securely"
echo ""
echo "Generated keys:"
echo "TRAE_MASTER_KEY: ${TRAE_MASTER_KEY}"
echo "SECRET_KEY: ${SECRET_KEY}"
echo "JWT_SECRET: ${JWT_SECRET}"

# Set secure file permissions
chmod 600 .env
echo "Set secure file permissions (600) on .env file"

echo "Environment generation complete!"