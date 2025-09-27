#!/bin/bash
# TRAE AI Production Rollback Script
# Emergency rollback to previous stable deployment

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
ROLLBACK_TIME=$(date +"%Y%m%d_%H%M%S")

echo -e "${RED}🚨 TRAE AI Production Rollback${NC}"
echo -e "${RED}==============================${NC}"
echo "Timestamp: $(date)"
echo "Rollback ID: $ROLLBACK_TIME"
echo ""

# Validate environment variables
if [ -z "$NETLIFY_AUTH_TOKEN" ]; then
    echo -e "${RED}❌ Error: NETLIFY_AUTH_TOKEN not set${NC}"
    exit 1
fi

if [ -z "$PRODUCTION_SITE_ID" ]; then
    echo -e "${RED}❌ Error: NETLIFY_PRODUCTION_SITE_ID not set${NC}"
    exit 1
fi

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo -e "${RED}❌ Error: Netlify CLI not found${NC}"
    echo "Please install: npm install -g netlify-cli"
    exit 1
fi

# Authenticate with Netlify
echo -e "${BLUE}🔐 Authenticating with Netlify...${NC}"
echo "$NETLIFY_AUTH_TOKEN" | netlify auth:login --auth-token

# Get deployment history
echo -e "${BLUE}📋 Fetching deployment history...${NC}"
DEPLOYMENTS=$(netlify api listSiteDeploys --data='{"site_id":"'$PRODUCTION_SITE_ID'"}' 2>/dev/null)

if [ -z "$DEPLOYMENTS" ] || [ "$DEPLOYMENTS" = "null" ]; then
    echo -e "${RED}❌ Error: Could not fetch deployment history${NC}"
    exit 1
fi

# Parse deployments and show options
echo -e "${YELLOW}Available deployments for rollback:${NC}"
echo "====================================="

# Get current deployment
CURRENT_DEPLOY=$(echo "$DEPLOYMENTS" | jq -r '.[0].id // "unknown"')
CURRENT_COMMIT=$(echo "$DEPLOYMENTS" | jq -r '.[0].commit_ref // "unknown"')
CURRENT_TIME=$(echo "$DEPLOYMENTS" | jq -r '.[0].created_at // "unknown"')

echo -e "${MAGENTA}CURRENT (Active):${NC}"
echo "  ID: $CURRENT_DEPLOY"
echo "  Commit: $CURRENT_COMMIT"
echo "  Deployed: $CURRENT_TIME"
echo ""

# Show previous deployments
echo -e "${BLUE}PREVIOUS DEPLOYMENTS:${NC}"
echo "$DEPLOYMENTS" | jq -r '.[1:6][] | "  [" + (.created_at | split("T")[0]) + "] " + .id + " (" + (.commit_ref // "unknown")[0:7] + ")"' | nl

echo ""

# Check for last known good deployment
if [ -f ".last-production-deploy" ]; then
    LAST_DEPLOY=$(cat .last-production-deploy)
    echo -e "${GREEN}Last known good deployment: $LAST_DEPLOY${NC}"
    echo ""
fi

# Rollback options
echo -e "${YELLOW}Rollback Options:${NC}"
echo "1. Rollback to previous deployment (recommended)"
echo "2. Rollback to last known good deployment"
echo "3. Rollback to specific deployment ID"
echo "4. Cancel rollback"
echo ""

read -p "Select rollback option (1-4): " -r ROLLBACK_OPTION
echo ""

case $ROLLBACK_OPTION in
    1)
        # Rollback to previous deployment
        TARGET_DEPLOY=$(echo "$DEPLOYMENTS" | jq -r '.[1].id // ""')
        TARGET_COMMIT=$(echo "$DEPLOYMENTS" | jq -r '.[1].commit_ref // "unknown"')
        TARGET_TIME=$(echo "$DEPLOYMENTS" | jq -r '.[1].created_at // "unknown"')
        ROLLBACK_TYPE="previous"
        ;;
    2)
        # Rollback to last known good
        if [ -f ".last-production-deploy" ]; then
            TARGET_DEPLOY=$(cat .last-production-deploy)
            TARGET_COMMIT="unknown"
            TARGET_TIME="unknown"
            ROLLBACK_TYPE="last-known-good"
        else
            echo -e "${RED}❌ Error: No last known good deployment found${NC}"
            exit 1
        fi
        ;;
    3)
        # Rollback to specific deployment
        read -p "Enter deployment ID: " -r TARGET_DEPLOY
        TARGET_COMMIT="unknown"
        TARGET_TIME="unknown"
        ROLLBACK_TYPE="specific"
        ;;
    4)
        echo -e "${YELLOW}Rollback cancelled by user.${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Invalid option selected${NC}"
        exit 1
        ;;
esac

if [ -z "$TARGET_DEPLOY" ] || [ "$TARGET_DEPLOY" = "null" ]; then
    echo -e "${RED}❌ Error: No valid deployment found for rollback${NC}"
    exit 1
fi

# Final confirmation
echo -e "${RED}⚠️  PRODUCTION ROLLBACK CONFIRMATION${NC}"
echo -e "${RED}====================================${NC}"
echo "Site ID: $PRODUCTION_SITE_ID"
echo "Rollback Type: $ROLLBACK_TYPE"
echo "Target Deployment: $TARGET_DEPLOY"
echo "Target Commit: $TARGET_COMMIT"
echo "Target Time: $TARGET_TIME"
echo "Current Time: $(date)"
echo ""
echo -e "${RED}This will immediately replace the current production deployment!${NC}"
read -p "Are you absolutely sure you want to rollback PRODUCTION? (yes/no): " -r
echo ""
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo -e "${YELLOW}Rollback cancelled by user.${NC}"
    exit 0
fi

# Perform rollback
echo -e "${RED}🔄 Performing production rollback...${NC}"
echo -e "${RED}====================================${NC}"

# Restore the deployment
if netlify api restoreSiteDeploy --data='{"site_id":"'$PRODUCTION_SITE_ID'","deploy_id":"'$TARGET_DEPLOY'"}' >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Rollback successful!${NC}"
else
    echo -e "${RED}❌ Rollback failed!${NC}"
    echo "Please check Netlify dashboard or contact support."
    exit 1
fi

# Get current production URL
PRODUCTION_URL=$(netlify status --json | jq -r '.site.url // .site.ssl_url // "Unknown"')

echo ""
echo -e "${GREEN}🎉 Production rollback completed!${NC}"
echo -e "${GREEN}==================================${NC}"
echo "Production URL: $PRODUCTION_URL"
echo "Rolled back to: $TARGET_DEPLOY"
echo "Rollback time: $(date)"
echo "Rollback ID: $ROLLBACK_TIME"
echo ""

# Post-rollback verification
echo -e "${BLUE}🔍 Post-rollback verification...${NC}"

# Wait for rollback to propagate
echo "Waiting 30 seconds for rollback to propagate..."
sleep 30

# Run smoke tests
if [ -f "scripts/smoke-tests.sh" ]; then
    echo -e "${BLUE}🔥 Running post-rollback smoke tests...${NC}"
    if STAGING_URL="$PRODUCTION_URL" bash scripts/smoke-tests.sh; then
        echo -e "${GREEN}✅ Post-rollback smoke tests passed!${NC}"
    else
        echo -e "${RED}❌ Post-rollback smoke tests failed!${NC}"
        echo -e "${RED}The rollback may not have resolved the issue.${NC}"
    fi
fi

# Log rollback
echo "$ROLLBACK_TIME,ROLLBACK,$TARGET_DEPLOY,$PRODUCTION_URL,$(date)" >> deployment-log.csv

echo ""
echo -e "${GREEN}✅ Production rollback complete!${NC}"
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Monitor application to ensure stability"
echo "2. Investigate the root cause of the issue"
echo "3. Fix the issue in development"
echo "4. Test thoroughly before next deployment"
echo "5. Update incident documentation"
echo ""
echo -e "${YELLOW}⚠️  Remember to address the underlying issue before the next deployment!${NC}"
