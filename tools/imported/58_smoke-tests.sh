#!/bin/bash
# TRAE AI Smoke Tests for Staging Environment
# Basic health checks to validate staging deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
STAGING_URL="${STAGING_URL:-http://localhost:8080}"
TIMEOUT=30
RETRIES=3

echo -e "${BLUE}🔥 TRAE AI Smoke Tests${NC}"
echo -e "${BLUE}=====================${NC}"
echo "Target URL: $STAGING_URL"
echo "Timeout: ${TIMEOUT}s"
echo "Retries: $RETRIES"
echo ""

# Test counter
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# Helper function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"

    TEST_COUNT=$((TEST_COUNT + 1))
    echo -e "${BLUE}Test $TEST_COUNT: $test_name${NC}"

    if eval "$test_command"; then
        echo -e "${GREEN}✅ PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}❌ FAIL${NC}"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
    echo ""
}

# Helper function to check HTTP response
check_http() {
    local url="$1"
    local expected_status="${2:-200}"
    local description="$3"

    for i in $(seq 1 $RETRIES); do
        if response=$(curl -s -w "HTTPSTATUS:%{http_code}" --max-time $TIMEOUT "$url" 2>/dev/null); then
            http_code=$(echo "$response" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
            body=$(echo "$response" | sed -e 's/HTTPSTATUS:.*//g')

            if [ "$http_code" = "$expected_status" ]; then
                if [ -n "$description" ]; then
                    echo "  Response: $description check passed"
                fi
                return 0
            else
                echo "  Expected status $expected_status, got $http_code"
            fi
        else
            echo "  Attempt $i/$RETRIES failed"
        fi

        if [ $i -lt $RETRIES ]; then
            sleep 2
        fi
    done

    return 1
}

# Test 1: Basic connectivity
run_test "Basic Connectivity" "check_http '$STAGING_URL' 200 'Homepage accessible'"

# Test 2: Health check endpoint
run_test "Health Check Endpoint" "check_http '$STAGING_URL/.netlify/functions/health-check' 200 'Health check returns OK'"

# Test 3: Static assets
run_test "Static Assets" "check_http '$STAGING_URL/app/static/index.html' 200 'Static files served'"

# Test 4: Dashboard accessibility (if running)
if curl -s --max-time 5 "$STAGING_URL:5000" >/dev/null 2>&1; then
    run_test "Dashboard Accessibility" "check_http '$STAGING_URL:5000' 200 'Dashboard accessible'"
else
    echo -e "${YELLOW}⚠️  Dashboard not running, skipping dashboard tests${NC}"
    echo ""
fi

# Test 5: Security headers
run_test "Security Headers" "
    response_headers=\$(curl -s -I --max-time $TIMEOUT '$STAGING_URL' 2>/dev/null)
    echo \"\$response_headers\" | grep -i 'x-frame-options\|x-content-type-options\|x-xss-protection' >/dev/null
"

# Test 6: No sensitive data exposure
run_test "No Sensitive Data Exposure" "
    response_body=\$(curl -s --max-time $TIMEOUT '$STAGING_URL' 2>/dev/null)
    ! echo \"\$response_body\" | grep -i 'api[_-]key\|secret\|password\|token' >/dev/null
"

# Test 7: Performance check (response time < 5 seconds)
run_test "Performance Check" "
    response_time=\$(curl -s -w '%{time_total}' -o /dev/null --max-time $TIMEOUT '$STAGING_URL' 2>/dev/null)
    awk 'BEGIN { exit (\"'\$response_time'\" < 5.0) ? 0 : 1 }'
"

# Test 8: Content validation
run_test "Content Validation" "
    response_body=\$(curl -s --max-time $TIMEOUT '$STAGING_URL' 2>/dev/null)
    echo \"\$response_body\" | grep -i 'trae\|ai' >/dev/null
"

# Summary
echo -e "${BLUE}📊 Test Summary${NC}"
echo -e "${BLUE}===============${NC}"
echo "Total Tests: $TEST_COUNT"
echo -e "${GREEN}Passed: $PASS_COUNT${NC}"
echo -e "${RED}Failed: $FAIL_COUNT${NC}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}🎉 All smoke tests passed! Staging deployment is healthy.${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAIL_COUNT test(s) failed. Please investigate before promoting to production.${NC}"
    exit 1
fi
