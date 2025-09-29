#!/bin/bash
# TRAE AI Production Deployment Script
# Handles secure production deployments with rollback capabilities

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
PRODUCTION_SITE_ID="${NETLIFY_PRODUCTION_SITE_ID}"
NETLIFY_AUTH_TOKEN="${NETLIFY_AUTH_TOKEN}"
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
COMMIT_SHA=$(git rev-parse --short HEAD)
FULL_COMMIT_SHA=$(git rev-parse HEAD)
DEPLOYMENT_TIME=$(date +"%Y%m%d_%H%M%S")

echo -e "${MAGENTA}🚀 TRAE AI Production Deployment${NC}"
echo -e "${MAGENTA}===================================${NC}"
echo "Branch: $BRANCH_NAME"
echo "Commit: $COMMIT_SHA ($FULL_COMMIT_SHA)"
echo "Timestamp: $(date)"
echo "Deployment ID: $DEPLOYMENT_TIME"
echo ""

# Pre-deployment validation
echo -e "${BLUE}🔍 Pre-deployment validation...${NC}"

# Check if on main branch
if [ "$BRANCH_NAME" != "main" ]; then
    echo -e "${RED}❌ Error: Production deployments must be from 'main' branch${NC}"
    echo "Current branch: $BRANCH_NAME"
    exit 1
fi

# Validate environment variables
if [ -z "$NETLIFY_AUTH_TOKEN" ]; then
    echo -e "${RED}❌ Error: NETLIFY_AUTH_TOKEN not set${NC}"
    exit 1
fi

if [ -z "$PRODUCTION_SITE_ID" ]; then
    echo -e "${RED}❌ Error: NETLIFY_PRODUCTION_SITE_ID not set${NC}"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}❌ Error: Uncommitted changes detected${NC}"
    echo "Please commit or stash all changes before production deployment."
    git status --porcelain
    exit 1
fi

# Verify we're up to date with remote
echo -e "${BLUE}📡 Checking remote sync...${NC}"
git fetch origin main
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo -e "${RED}❌ Error: Local branch is not in sync with origin/main${NC}"
    echo "Please pull the latest changes: git pull origin main"
    exit 1
fi

echo -e "${GREEN}✅ Pre-deployment validation passed${NC}"
echo ""

# Security and quality checks
echo -e "${BLUE}🔒 Running security and quality checks...${NC}"

# Install dependencies if needed
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Run comprehensive tests
echo -e "${BLUE}🧪 Running test suite...${NC}"
if [ -f "pytest.ini" ] && command -v pytest &>/dev/null; then
    pytest tests/-v --tb=short --cov=. --cov-report=term-missing || {
        echo -e "${RED}❌ Tests failed! Aborting production deployment.${NC}"
        exit 1
    }
    echo -e "${GREEN}✅ All tests passed with coverage report${NC}"
else
    echo -e "${YELLOW}⚠️  No tests found or pytest not available${NC}"
fi

# Security scanning
echo -e "${BLUE}🛡️  Running security scans...${NC}"
if command -v bandit &>/dev/null; then
    bandit -r . -f json -o bandit-production-report.json || {
        echo -e "${RED}❌ Security scan failed! Please review and fix issues.${NC}"
        exit 1
    }
    echo -e "${GREEN}✅ Security scan passed${NC}"
fi

if command -v safety &>/dev/null; then
    safety check --json --output safety-production-report.json || {
        echo -e "${YELLOW}⚠️  Dependency vulnerabilities detected. Review safety-production-report.json${NC}"
    }
fi

# Check for secrets
if command -v gitleaks &>/dev/null; then
    gitleaks detect --source . --report-format json --report-path gitleaks-production-report.json || {
        echo -e "${RED}❌ Secrets detected in codebase! Aborting deployment.${NC}"
        exit 1
    }
    echo -e "${GREEN}✅ No secrets detected${NC}"
fi

echo -e "${GREEN}✅ Security and quality checks completed${NC}"
echo ""

# Backup current production deployment
echo -e "${BLUE}💾 Creating deployment backup...${NC}"
if command -v netlify &>/dev/null; then
    # Get current production deployment info
    CURRENT_DEPLOY=$(netlify api listSiteDeploys --data='{"site_id":"'$PRODUCTION_SITE_ID'"}' | jq -r '.[0].id//"unknown"')
    echo "Current production deployment: $CURRENT_DEPLOY"
    echo "$CURRENT_DEPLOY" > .last-production-deploy
fi

# Final confirmation
echo -e "${YELLOW}⚠️  PRODUCTION DEPLOYMENT CONFIRMATION${NC}"
echo -e "${YELLOW}=====================================${NC}"
echo "Site ID: $PRODUCTION_SITE_ID"
echo "Branch: $BRANCH_NAME"
echo "Commit: $FULL_COMMIT_SHA"
echo "Time: $(date)"
echo ""
read -p "Are you sure you want to deploy to PRODUCTION? (yes/no): " -r
echo ""
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo -e "${YELLOW}Deployment cancelled by user.${NC}"
    exit 0
fi

# Deploy to production
echo -e "${MAGENTA}🚀 Deploying to production...${NC}"
echo -e "${MAGENTA}=============================${NC}"

# Authenticate with Netlify
echo "$NETLIFY_AUTH_TOKEN" | netlify auth:login --auth-token

# Deploy with production flag
netlify deploy --prod --site="$PRODUCTION_SITE_ID" --dir=. --message="Production deployment: $COMMIT_SHA at $DEPLOYMENT_TIME"

# Get deployment URL
PRODUCTION_URL=$(netlify status --json | jq -r '.site.url//.site.ssl_url//"Unknown"')

echo ""
echo -e "${GREEN}🎉 Production deployment successful!${NC}"
echo -e "${GREEN}====================================${NC}"
echo "Production URL: $PRODUCTION_URL"
echo "Branch: $BRANCH_NAME"
echo "Commit: $FULL_COMMIT_SHA"
echo "Deployed at: $(date)"
echo "Deployment ID: $DEPLOYMENT_TIME"
echo ""

# Post-deployment verification
echo -e "${BLUE}🔍 Post-deployment verification...${NC}"

# Wait for deployment to propagate
echo "Waiting 30 seconds for deployment to propagate..."
sleep 30

# Run smoke tests against production
if [ -f "scripts/smoke-tests.sh" ]; then
    echo -e "${BLUE}🔥 Running production smoke tests...${NC}"
    if STAGING_URL="$PRODUCTION_URL" bash scripts/smoke-tests.sh; then
        echo -e "${GREEN}✅ Production smoke tests passed!${NC}"
    else
        echo -e "${RED}❌ Production smoke tests failed!${NC}"
        echo -e "${YELLOW}Consider rolling back if issues are critical.${NC}"
        echo "Rollback command: bash scripts/rollback-production.sh"
    fi
fi

# Log deployment
echo "$DEPLOYMENT_TIME,$FULL_COMMIT_SHA,$PRODUCTION_URL,$(date)" >> deployment-log.csv

echo ""
echo -e "${GREEN}✅ Production deployment complete!${NC}"
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Monitor application performance and error rates"
echo "2. Verify all critical user flows are working"
echo "3. Check monitoring dashboards and logs"
echo "4. If issues arise, use: bash scripts/rollback-production.sh"
echo ""
echo -e "${MAGENTA}🎊 TRAE AI is now live in production! 🎊${NC}"
