#!/bin/bash
# TRAE AI Staging Deployment Script
# This script handles staging deployments to Netlify for testing

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
STAGING_SITE_ID="${NETLIFY_STAGING_SITE_ID}"
PRODUCTION_SITE_ID="${NETLIFY_PRODUCTION_SITE_ID}"
NETLIFY_AUTH_TOKEN="${NETLIFY_AUTH_TOKEN}"
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
COMMIT_SHA=$(git rev-parse --short HEAD)

echo -e "${BLUE}🚀 TRAE AI Staging Deployment${NC}"
echo -e "${BLUE}================================${NC}"
echo "Branch: $BRANCH_NAME"
echo "Commit: $COMMIT_SHA"
echo "Timestamp: $(date)"
echo ""

# Validate environment
if [ -z "$NETLIFY_AUTH_TOKEN" ]; then
    echo -e "${RED}❌ Error: NETLIFY_AUTH_TOKEN not set${NC}"
    echo "Please set your Netlify authentication token."
    exit 1
fi

if [ -z "$STAGING_SITE_ID" ]; then
    echo -e "${YELLOW}⚠️  Warning: NETLIFY_STAGING_SITE_ID not set${NC}"
    echo "Will create a new site or use default configuration."
fi

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo -e "${YELLOW}📦 Installing Netlify CLI...${NC}"
    npm install -g netlify-cli
fi

# Authenticate with Netlify
echo -e "${BLUE}🔐 Authenticating with Netlify...${NC}"
echo "$NETLIFY_AUTH_TOKEN" | netlify auth:login --auth-token

# Build preparation
echo -e "${BLUE}🔨 Preparing build...${NC}"

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Run tests before deployment
echo -e "${BLUE}🧪 Running tests...${NC}"
if [ -f "pytest.ini" ] && command -v pytest &> /dev/null; then
    pytest tests/ -v --tb=short || {
        echo -e "${RED}❌ Tests failed! Aborting deployment.${NC}"
        exit 1
    }
    echo -e "${GREEN}✅ All tests passed!${NC}"
else
    echo -e "${YELLOW}⚠️  No tests found or pytest not available${NC}"
fi

# Security scan
echo -e "${BLUE}🔒 Running security scan...${NC}"
if command -v bandit &> /dev/null; then
    bandit -r . -f json -o bandit-staging-report.json || true
    echo -e "${GREEN}✅ Security scan completed${NC}"
else
    echo -e "${YELLOW}⚠️  Bandit not available, skipping security scan${NC}"
fi

# Deploy to staging
echo -e "${BLUE}🚀 Deploying to staging...${NC}"

if [ "$BRANCH_NAME" = "main" ]; then
    # Deploy to staging site
    if [ -n "$STAGING_SITE_ID" ]; then
        netlify deploy --site="$STAGING_SITE_ID" --dir=. --message="Staging deployment: $COMMIT_SHA"
    else
        netlify deploy --dir=. --message="Staging deployment: $COMMIT_SHA"
    fi
else
    # Deploy as branch preview
    netlify deploy --dir=. --alias="$BRANCH_NAME" --message="Branch preview: $BRANCH_NAME ($COMMIT_SHA)"
fi

# Get deployment URL
DEPLOY_URL=$(netlify status --json | jq -r '.site.url // .site.ssl_url // "Unknown"')

echo ""
echo -e "${GREEN}🎉 Staging deployment successful!${NC}"
echo -e "${GREEN}================================${NC}"
echo "Deployment URL: $DEPLOY_URL"
echo "Branch: $BRANCH_NAME"
echo "Commit: $COMMIT_SHA"
echo "Deployed at: $(date)"
echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Test the staging deployment at: $DEPLOY_URL"
echo "2. Run end-to-end tests"
echo "3. If all tests pass, promote to production"
echo ""

# Optional: Run smoke tests against staging
if [ -f "scripts/smoke-tests.sh" ]; then
    echo -e "${BLUE}🔥 Running smoke tests...${NC}"
    STAGING_URL="$DEPLOY_URL" bash scripts/smoke-tests.sh
fi

echo -e "${GREEN}✅ Staging deployment complete!${NC}"
