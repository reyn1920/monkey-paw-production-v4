#!/bin/bash
# Enhanced Sanity Check Script for Production API
# Tests all critical endpoints with proper error handling

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BASE_URL="${BASE_URL:-http://localhost:8000}"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%H:%M:%S')] ERROR: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')] $1${NC}"
}

# Test function with error handling
test_endpoint() {
    local method="$1"
    local endpoint="$2"
    local expected_status="${3:-200}"
    local description="$4"

    TEST_COUNT=$((TEST_COUNT + 1))
    info "Testing $description ($method $endpoint)"

    local response
    local status_code

    if response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint" 2>/dev/null); then
        status_code=$(echo "$response" | tail -n1)
        response_body=$(echo "$response" | head -n -1)

        if [ "$status_code" = "$expected_status" ]; then
            log "✅ PASS: $description (HTTP $status_code)"
            PASS_COUNT=$((PASS_COUNT + 1))

            # Try to parse JSON if it looks like JSON
            if echo "$response_body" | jq . >/dev/null 2>&1; then
                echo "$response_body" | jq -C . | head -3
            else
                echo "$response_body" | head -3
            fi
        else
            error "❌ FAIL: $description - Expected HTTP $expected_status, got $status_code"
            FAIL_COUNT=$((FAIL_COUNT + 1))
            echo "Response: $response_body" | head -3
        fi
    else
        error "❌ FAIL: $description - Connection failed"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
    echo
}

# Test redirect with proper handling
test_redirect() {
    local endpoint="$1"
    local expected_location="$2"
    local description="$3"

    TEST_COUNT=$((TEST_COUNT + 1))
    info "Testing $description (GET $endpoint)"

    local headers
    if headers=$(curl -s -I "$BASE_URL$endpoint" 2>/dev/null); then
        local status_line=$(echo "$headers" | head -n1)
        local location=$(echo "$headers" | grep -i "^location:" | cut -d' ' -f2- | tr -d '\r')

        if echo "$status_line" | grep -q "30[1-8]"; then
            if [ "$location" = "$expected_location" ]; then
                log "✅ PASS: $description (redirects to $location)"
                PASS_COUNT=$((PASS_COUNT + 1))
            else
                error "❌ FAIL: $description - Expected redirect to $expected_location, got $location"
                FAIL_COUNT=$((FAIL_COUNT + 1))
            fi
        else
            error "❌ FAIL: $description - Expected redirect, got: $status_line"
            FAIL_COUNT=$((FAIL_COUNT + 1))
        fi
    else
        error "❌ FAIL: $description - Connection failed"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
    echo
}

log "🔍 Starting comprehensive sanity checks for $BASE_URL"
log "Timestamp: $(date)"
echo

# Core API endpoints
test_endpoint "GET" "/api/version" "200" "API Version"
test_endpoint "GET" "/health" "200" "Basic Health Check"
test_endpoint "GET" "/health/detailed" "200" "Detailed Health Check"
test_endpoint "GET" "/health/ready" "200" "Readiness Probe"
test_endpoint "GET" "/metrics" "200" "Metrics Endpoint"

# System endpoints
test_endpoint "GET" "/api/system/status" "200" "System Status"
test_endpoint "GET" "/api/services" "200" "Services List"

# New production endpoints
test_endpoint "GET" "/api/software/status" "200" "Software Status"
test_endpoint "GET" "/api/blender/validate" "200" "Blender Validation"
test_endpoint "GET" "/api/resolve/validate" "200" "Resolve Validation"
test_endpoint "GET" "/api/davinci/status" "200" "DaVinci Status"
test_endpoint "GET" "/api/creative/toolchain" "200" "Creative Toolchain"
test_endpoint "GET" "/api/rss/watch" "200" "RSS Watcher"

# Dashboard endpoints (should never fail)
test_endpoint "GET" "/dashboard/analytics" "200" "Dashboard Analytics"
test_endpoint "GET" "/dashboard/api/health" "200" "Dashboard Health"
test_endpoint "GET" "/dashboard/api/status" "200" "Dashboard Status"
test_endpoint "GET" "/dashboard/api/system-info" "200" "Dashboard System Info"
test_endpoint "GET" "/dashboard/settings" "200" "Dashboard Settings"

# Test redirects
test_redirect "/version" "/api/version" "Version Redirect"

# OpenAPI documentation
test_endpoint "GET" "/openapi.json" "200" "OpenAPI Schema"
test_endpoint "GET" "/docs" "200" "Swagger UI"

# Summary
echo
log "📊 Test Summary:"
echo "  Total tests: $TEST_COUNT"
echo -e "  Passed: ${GREEN}$PASS_COUNT${NC}"
echo -e "  Failed: ${RED}$FAIL_COUNT${NC}"
echo

if [ $FAIL_COUNT -eq 0 ]; then
    log "🎉 All sanity checks passed! System is healthy."
    exit 0
else
    error "💥 $FAIL_COUNT test(s) failed. System may have issues."
    exit 1
fi
