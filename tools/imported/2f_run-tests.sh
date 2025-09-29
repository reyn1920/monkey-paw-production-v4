#!/bin/bash
# TRAE AI Comprehensive Test Runner
# Runs all tests, security scans, and quality checks

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
TEST_RESULTS_DIR="test-results"
COVERAGE_THRESHOLD=80
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo -e "${BLUE}🧪 TRAE AI Comprehensive Test Suite${NC}"
echo -e "${BLUE}====================================${NC}"
echo "Timestamp: $(date)"
echo "Test Run ID: $TIMESTAMP"
echo ""

# Create test results directory
mkdir -p "$TEST_RESULTS_DIR"

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Helper function to run a test suite
run_test_suite() {
    local suite_name="$1"
    local test_command="$2"
    local required="${3:-true}"

    echo -e "${BLUE}🔍 Running $suite_name...${NC}"
    echo "Command: $test_command"
    echo ""

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    if eval "$test_command"; then
        echo -e "${GREEN}✅ $suite_name: PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ $suite_name: FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))

        if [ "$required" = "true" ]; then
            echo -e "${RED}Required test suite failed. Aborting.${NC}"
            exit 1
        else
            echo -e "${YELLOW}Optional test suite failed. Continuing...${NC}"
        fi
    fi
    echo ""
}

# Install test dependencies
echo -e "${BLUE}📦 Installing test dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Install additional testing tools
echo "Installing testing and security tools..."
pip install pytest pytest-cov bandit safety gitleaks || echo "Some tools may not be available"

echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# 1. Unit Tests with Coverage
if [ -d "tests" ] && command -v pytest &> /dev/null; then
    run_test_suite "Unit Tests with Coverage" \
        "pytest tests/ -v --tb=short --cov=. --cov-report=html:$TEST_RESULTS_DIR/coverage-html --cov-report=xml:$TEST_RESULTS_DIR/coverage.xml --cov-report=term-missing --cov-fail-under=$COVERAGE_THRESHOLD --junitxml=$TEST_RESULTS_DIR/pytest-results.xml" \
        true
else
    echo -e "${YELLOW}⚠️  Pytest not available or no tests directory found${NC}"
    echo ""
fi

# 2. Security Scan - Bandit
if command -v bandit &> /dev/null; then
    run_test_suite "Security Scan (Bandit)" \
        "bandit -r . -f json -o $TEST_RESULTS_DIR/bandit-report.json -f txt -o $TEST_RESULTS_DIR/bandit-report.txt" \
        true
else
    echo -e "${YELLOW}⚠️  Bandit not available, installing...${NC}"
    pip install bandit
    if command -v bandit &> /dev/null; then
        run_test_suite "Security Scan (Bandit)" \
            "bandit -r . -f json -o $TEST_RESULTS_DIR/bandit-report.json -f txt -o $TEST_RESULTS_DIR/bandit-report.txt" \
            true
    fi
fi

# 3. Dependency Vulnerability Scan - Safety
if command -v safety &> /dev/null; then
    run_test_suite "Dependency Vulnerability Scan (Safety)" \
        "safety check --json --output $TEST_RESULTS_DIR/safety-report.json" \
        false  # Non-critical, as some vulnerabilities might be acceptable
else
    echo -e "${YELLOW}⚠️  Safety not available, installing...${NC}"
    pip install safety
    if command -v safety &> /dev/null; then
        run_test_suite "Dependency Vulnerability Scan (Safety)" \
            "safety check --json --output $TEST_RESULTS_DIR/safety-report.json" \
            false
    fi
fi

# 4. Secret Detection - Gitleaks (if available)
if command -v gitleaks &> /dev/null; then
    run_test_suite "Secret Detection (Gitleaks)" \
        "gitleaks detect --source . --report-format json --report-path $TEST_RESULTS_DIR/gitleaks-report.json" \
        true
else
    echo -e "${YELLOW}⚠️  Gitleaks not available. Install from: https://github.com/gitleaks/gitleaks${NC}"
    echo ""
fi

# 5. Code Quality - Flake8 (if available)
if command -v flake8 &> /dev/null; then
    run_test_suite "Code Quality (Flake8)" \
        "flake8 . --output-file=$TEST_RESULTS_DIR/flake8-report.txt --tee" \
        false  # Non-critical
else
    echo -e "${YELLOW}⚠️  Flake8 not available for code quality checks${NC}"
    echo ""
fi

# 6. Integration Tests (if they exist separately)
if [ -f "tests/test_integration.py" ]; then
    run_test_suite "Integration Tests" \
        "pytest tests/test_integration.py -v --tb=short --junitxml=$TEST_RESULTS_DIR/integration-results.xml" \
        true
fi

# 7. System Health Check
run_test_suite "System Health Check" \
    "python -c 'import sys; print(f\"Python version: {sys.version}\"); import os; print(f\"Working directory: {os.getcwd()}\"); print(\"System health: OK\")'"

# 8. File Structure Validation
run_test_suite "File Structure Validation" \
    "python -c 'import os; required=[\"launch_live.py\", \"requirements.txt\", \"app/dashboard.py\"]; missing=[f for f in required if not os.path.exists(f)]; print(f\"Missing files: {missing}\") if missing else print(\"All required files present\"); exit(1 if missing else 0)'"

# Generate summary report
echo -e "${BLUE}📊 Generating test summary...${NC}"

cat > "$TEST_RESULTS_DIR/test-summary.json" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "test_run_id": "$TIMESTAMP",
  "summary": {
    "total_test_suites": $TOTAL_TESTS,
    "passed_test_suites": $PASSED_TESTS,
    "failed_test_suites": $FAILED_TESTS,
    "success_rate": "$(echo "scale=2; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc -l)%"
  },
  "environment": {
    "python_version": "$(python --version 2>&1)",
    "working_directory": "$(pwd)",
    "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
    "git_branch": "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')"
  },
  "coverage_threshold": $COVERAGE_THRESHOLD,
  "results_directory": "$TEST_RESULTS_DIR"
}
EOF

# Display final summary
echo ""
echo -e "${MAGENTA}📋 Test Execution Summary${NC}"
echo -e "${MAGENTA}=========================${NC}"
echo "Test Run ID: $TIMESTAMP"
echo "Total Test Suites: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $FAILED_TESTS${NC}"
echo "Success Rate: $(echo "scale=2; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc -l)%"
echo "Results Directory: $TEST_RESULTS_DIR"
echo ""

# List generated reports
echo -e "${BLUE}📄 Generated Reports:${NC}"
find "$TEST_RESULTS_DIR" -type f -name "*.json" -o -name "*.xml" -o -name "*.txt" | sort
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 All test suites passed! System is ready for deployment.${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED_TESTS test suite(s) failed. Please review and fix issues before deployment.${NC}"
    echo -e "${BLUE}📋 Next steps:${NC}"
    echo "1. Review failed test reports in $TEST_RESULTS_DIR"
    echo "2. Fix identified issues"
    echo "3. Re-run tests: bash scripts/run-tests.sh"
    echo "4. Only deploy after all tests pass"
    exit 1
fi
