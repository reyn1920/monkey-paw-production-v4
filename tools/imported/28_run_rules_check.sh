#!/bin/bash

# TRAE AI Project Rules Checker
# Comprehensive validation script for project compliance
# Usage: ./run_rules_check.sh [--fix] [--verbose] [--component <name>]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$PROJECT_ROOT/.trae/rules_check.log"
FIX_MODE=false
VERBOSE=false
COMPONENT="all"
ERROR_COUNT=0
WARNING_COUNT=0

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --fix)
            FIX_MODE=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --component)
            COMPONENT="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [--fix] [--verbose] [--component <name>]"
            echo "  --fix       Attempt to automatically fix issues"
            echo "  --verbose   Show detailed output"
            echo "  --component Specific component to check (security|quality|structure|all)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    [ "$VERBOSE" = true ] && echo "$(date): [INFO] $1" >> "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
    [ "$VERBOSE" = true ] && echo "$(date): [PASS] $1" >> "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    echo "$(date): [WARN] $1" >> "$LOG_FILE"
    ((WARNING_COUNT++))
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
    echo "$(date): [FAIL] $1" >> "$LOG_FILE"
    ((ERROR_COUNT++))
}

# Initialize log directory
mkdir -p "$PROJECT_ROOT/.trae"

# Header
echo "==========================================="
echo "    TRAE AI Project Rules Checker"
echo "==========================================="
echo "Project Root: $PROJECT_ROOT"
echo "Component: $COMPONENT"
echo "Fix Mode: $FIX_MODE"
echo "Verbose: $VERBOSE"
echo "==========================================="
echo ""

# Security Checks
check_security() {
    log_info "Running security compliance checks..."

    # Check for hardcoded secrets
    log_info "Scanning for hardcoded secrets..."
    if command -v grep >/dev/null 2>&1; then
        # Common secret patterns
        SECRET_PATTERNS=(
            "api_key\s*=\s*['\"][^'\"]+['\"]"
            "password\s*=\s*['\"][^'\"]+['\"]"
            "secret\s*=\s*['\"][^'\"]+['\"]"
            "token\s*=\s*['\"][^'\"]+['\"]"
            "sk-[a-zA-Z0-9]{32,}"
            "ghp_[a-zA-Z0-9]{36}"
        )

        for pattern in "${SECRET_PATTERNS[@]}"; do
            if grep -r -i -E "$pattern" --exclude-dir=.git --exclude-dir=venv --exclude-dir=node_modules --exclude="*.log" "$PROJECT_ROOT" >/dev/null 2>&1; then
                log_error "Potential hardcoded secret found (pattern: $pattern)"
                if [ "$VERBOSE" = true ]; then
                    grep -r -i -E "$pattern" --exclude-dir=.git --exclude-dir=venv --exclude-dir=node_modules --exclude="*.log" "$PROJECT_ROOT" || true
                fi
            fi
        done
    else
        log_warning "grep not available, skipping secret scan"
    fi

    # Check .env files are in .gitignore
    log_info "Checking .env file protection..."
    if [ -f "$PROJECT_ROOT/.gitignore" ]; then
        if grep -q "\.env" "$PROJECT_ROOT/.gitignore"; then
            log_success ".env files are properly ignored"
        else
            log_error ".env files not found in .gitignore"
            if [ "$FIX_MODE" = true ]; then
                echo ".env" >> "$PROJECT_ROOT/.gitignore"
                echo ".env.local" >> "$PROJECT_ROOT/.gitignore"
                log_info "Added .env files to .gitignore"
            fi
        fi
    else
        log_error ".gitignore file not found"
    fi

    # Run Rule-1 scanner if available
    log_info "Running Rule-1 content scanner..."
    if [ -f "$PROJECT_ROOT/tools/audits/rule1_scan.py" ]; then
        if python3 "$PROJECT_ROOT/tools/audits/rule1_scan.py" "$PROJECT_ROOT" >/dev/null 2>&1; then
            log_success "Rule-1 scanner passed"
        else
            log_error "Rule-1 scanner found violations"
        fi
    else
        log_warning "Rule-1 scanner not found"
    fi

    # Check for HTTPS in production configs
    log_info "Checking HTTPS configuration..."
    if grep -r "http://" --include="*.py" --include="*.js" --include="*.json" "$PROJECT_ROOT" | grep -v "localhost" | grep -v "127.0.0.1" >/dev/null 2>&1; then
        log_warning "Found HTTP URLs in production code (should use HTTPS)"
    else
        log_success "No insecure HTTP URLs found"
    fi
}

# Code Quality Checks
check_quality() {
    log_info "Running code quality checks..."

    # Check Python code with flake8 if available
    if command -v flake8 >/dev/null 2>&1; then
        log_info "Running Python linting..."
        if flake8 "$PROJECT_ROOT" --exclude=venv,node_modules,.git --max-line-length=88 >/dev/null 2>&1; then
            log_success "Python linting passed"
        else
            log_warning "Python linting issues found"
            if [ "$VERBOSE" = true ]; then
                flake8 "$PROJECT_ROOT" --exclude=venv,node_modules,.git --max-line-length=88 || true
            fi
        fi
    else
        log_warning "flake8 not available, skipping Python linting"
    fi

    # Check for TODO/FIXME comments
    log_info "Scanning for TODO/FIXME comments..."
    TODO_COUNT=$(grep -r -i "TODO\|FIXME" --exclude-dir=.git --exclude-dir=venv --exclude-dir=node_modules "$PROJECT_ROOT" | wc -l || echo "0")
    if [ "$TODO_COUNT" -gt 0 ]; then
        log_warning "Found $TODO_COUNT TODO/FIXME comments"
    else
        log_success "No pending TODO/FIXME items"
    fi

    # Check for proper docstrings in Python files
    log_info "Checking Python docstring coverage..."
    PYTHON_FILES=$(find "$PROJECT_ROOT" -name "*.py" -not -path "*/venv/*" -not -path "*/.git/*" | wc -l)
    if [ "$PYTHON_FILES" -gt 0 ]; then
        UNDOCUMENTED=$(grep -L "\"\"\"" $(find "$PROJECT_ROOT" -name "*.py" -not -path "*/venv/*" -not -path "*/.git/*") | wc -l || echo "0")
        COVERAGE=$(( (PYTHON_FILES - UNDOCUMENTED) * 100 / PYTHON_FILES ))
        if [ "$COVERAGE" -ge 80 ]; then
            log_success "Docstring coverage: $COVERAGE%"
        else
            log_warning "Low docstring coverage: $COVERAGE% (target: 80%)"
        fi
    fi
}

# Project Structure Checks
check_structure() {
    log_info "Running project structure checks..."

    # Check required files exist
    REQUIRED_FILES=(
        "README.md"
        "requirements.txt"
        ".gitignore"
        "TRAE_RULES.md"
    )

    for file in "${REQUIRED_FILES[@]}"; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            log_success "Required file exists: $file"
        else
            log_error "Missing required file: $file"
        fi
    done

    # Check directory structure
    REQUIRED_DIRS=(
        "tools"
        "tools/audits"
        "backend"
        "tests"
    )

    for dir in "${REQUIRED_DIRS[@]}"; do
        if [ -d "$PROJECT_ROOT/$dir" ]; then
            log_success "Required directory exists: $dir"
        else
            log_warning "Missing directory: $dir"
            if [ "$FIX_MODE" = true ]; then
                mkdir -p "$PROJECT_ROOT/$dir"
                log_info "Created directory: $dir"
            fi
        fi
    done

    # Check for protected files
    if [ -d "$PROJECT_ROOT/tools/dnd" ]; then
        log_success "Protected directory exists: tools/dnd"
    else
        log_warning "Protected directory missing: tools/dnd"
    fi

    # Check file permissions
    EXECUTABLE_FILES=(
        "run_rules_check.sh"
        "tools/start_local.py"
    )

    for file in "${EXECUTABLE_FILES[@]}"; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            if [ -x "$PROJECT_ROOT/$file" ]; then
                log_success "File is executable: $file"
            else
                log_warning "File not executable: $file"
                if [ "$FIX_MODE" = true ]; then
                    chmod +x "$PROJECT_ROOT/$file"
                    log_info "Made file executable: $file"
                fi
            fi
        fi
    done
}

# Run checks based on component selection
case $COMPONENT in
    "security")
        check_security
        ;;
    "quality")
        check_quality
        ;;
    "structure")
        check_structure
        ;;
    "all")
        check_security
        check_quality
        check_structure
        ;;
    *)
        log_error "Unknown component: $COMPONENT"
        exit 1
        ;;
esac

# Summary
echo ""
echo "==========================================="
echo "           RULES CHECK SUMMARY"
echo "==========================================="
echo "Errors: $ERROR_COUNT"
echo "Warnings: $WARNING_COUNT"
echo "Log file: $LOG_FILE"
echo "==========================================="

# Exit with appropriate code
if [ "$ERROR_COUNT" -gt 0 ]; then
    echo -e "${RED}Rules check FAILED${NC} - $ERROR_COUNT errors found"
    exit 1
elif [ "$WARNING_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}Rules check PASSED with warnings${NC} - $WARNING_COUNT warnings"
    exit 0
else
    echo -e "${GREEN}Rules check PASSED${NC} - All checks successful"
    exit 0
fi
