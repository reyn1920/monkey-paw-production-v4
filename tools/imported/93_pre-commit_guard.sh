#!/bin/bash

# Pre-commit Guard - Code Quality and Security Gate
# Runs before each commit to ensure code quality and security standards
# This script is designed to be used as a Git pre-commit hook

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_FILE="$PROJECT_ROOT/.trae/precommit.log"
TEST_MODE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --test)
            TEST_MODE=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Logging functions
log_info() {
    echo -e "${BLUE}[PRE-COMMIT]${NC} $1"
    echo "$(date): [INFO] $1" >> "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[PRE-COMMIT]${NC} $1"
    echo "$(date): [SUCCESS] $1" >> "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[PRE-COMMIT]${NC} $1"
    echo "$(date): [WARNING] $1" >> "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[PRE-COMMIT]${NC} $1"
    echo "$(date): [ERROR] $1" >> "$LOG_FILE"
}

# Initialize
init_precommit() {
    mkdir -p "$PROJECT_ROOT/.trae"
    touch "$LOG_FILE"

    if [ "$TEST_MODE" = true ]; then
        log_info "Running in test mode"
        return 0
    fi

    log_info "Starting pre-commit checks..."
}

# Get list of staged files
get_staged_files() {
    if [ "$TEST_MODE" = true ]; then
        # In test mode, check all files
        find "$PROJECT_ROOT" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" -o -name "*.json" -o -name "*.md" \) | head -10
    else
        # Get staged files from git
        git diff --cached --name-only --diff-filter=ACM
    fi
}

# Check for secrets and sensitive data
check_secrets() {
    log_info "Checking for secrets and sensitive data..."
    local violations=0

    # Patterns to check for
    local secret_patterns=(
        "password\s*=\s*['\"][^'\"]+['\"]"  # password = "value"
        "api[_-]?key\s*=\s*['\"][^'\"]+['\"]"  # api_key = "value"
        "secret\s*=\s*['\"][^'\"]+['\"]"  # secret = "value"
        "token\s*=\s*['\"][^'\"]+['\"]"  # token = "value"
        "['\"][A-Za-z0-9]{32,}['\"]"  # Long strings that might be keys
        "sk-[A-Za-z0-9]{32,}"  # OpenAI API keys
        "ghp_[A-Za-z0-9]{36}"  # GitHub personal access tokens
        "gho_[A-Za-z0-9]{36}"  # GitHub OAuth tokens
    )

    while IFS= read -r file; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            for pattern in "${secret_patterns[@]}"; do
                if grep -iE "$pattern" "$PROJECT_ROOT/$file" >/dev/null 2>&1; then
                    log_error "Potential secret found in $file"
                    grep -inE "$pattern" "$PROJECT_ROOT/$file" | head -3
                    ((violations++))
                fi
            done
        fi
    done < <(get_staged_files)

    if [ $violations -gt 0 ]; then
        log_error "$violations potential secrets found!"
        log_error "Please remove secrets and use environment variables instead"
        return 1
    else
        log_success "No secrets detected"
        return 0
    fi
}

# Check for TODO/FIXME comments
check_todos() {
    log_info "Checking for TODO/FIXME comments..."
    local todo_count=0

    while IFS= read -r file; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            local todos=$(grep -inE "(TODO|FIXME|XXX|HACK)" "$PROJECT_ROOT/$file" | wc -l)
            if [ $todos -gt 0 ]; then
                log_warning "$todos TODO/FIXME found in $file"
                ((todo_count += todos))
            fi
        fi
    done < <(get_staged_files)

    if [ $todo_count -gt 0 ]; then
        log_warning "Total: $todo_count TODO/FIXME comments found"
        log_info "Consider addressing these before committing"
    else
        log_success "No TODO/FIXME comments found"
    fi

    return 0  # Don't fail on TODOs, just warn
}

# Check Python code quality
check_python_quality() {
    local python_files
    python_files=$(get_staged_files | grep -E "\.py$" || true)

    if [ -z "$python_files" ]; then
        return 0
    fi

    log_info "Checking Python code quality..."

    # Check if flake8 is available
    if command -v flake8 >/dev/null 2>&1; then
        log_info "Running flake8..."
        if echo "$python_files" | xargs flake8 --max-line-length=88 --extend-ignore=E203,W503; then
            log_success "Python linting passed"
        else
            log_error "Python linting failed"
            return 1
        fi
    else
        log_warning "flake8 not available, skipping Python linting"
    fi

    # Check for basic Python syntax
    while IFS= read -r file; do
        if [ -f "$PROJECT_ROOT/$file" ] && [[ "$file" == *.py ]]; then
            if ! python3 -m py_compile "$PROJECT_ROOT/$file" 2>/dev/null; then
                log_error "Python syntax error in $file"
                return 1
            fi
        fi
    done < <(get_staged_files)

    log_success "Python syntax check passed"
    return 0
}

# Check JavaScript/TypeScript code quality
check_js_quality() {
    local js_files
    js_files=$(get_staged_files | grep -E "\.(js|ts|jsx|tsx)$" || true)

    if [ -z "$js_files" ]; then
        return 0
    fi

    log_info "Checking JavaScript/TypeScript code quality..."

    # Check if eslint is available
    if command -v eslint >/dev/null 2>&1; then
        log_info "Running ESLint..."
        if echo "$js_files" | xargs eslint --quiet; then
            log_success "JavaScript linting passed"
        else
            log_error "JavaScript linting failed"
            return 1
        fi
    elif [ -f "$PROJECT_ROOT/node_modules/.bin/eslint" ]; then
        log_info "Running ESLint (local)..."
        if echo "$js_files" | xargs "$PROJECT_ROOT/node_modules/.bin/eslint" --quiet; then
            log_success "JavaScript linting passed"
        else
            log_error "JavaScript linting failed"
            return 1
        fi
    else
        log_warning "ESLint not available, skipping JavaScript linting"
    fi

    return 0
}

# Check file sizes
check_file_sizes() {
    log_info "Checking file sizes..."
    local large_files=0
    local max_size=1048576  # 1MB in bytes

    while IFS= read -r file; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            local size=$(stat -f%z "$PROJECT_ROOT/$file" 2>/dev/null || stat -c%s "$PROJECT_ROOT/$file" 2>/dev/null || echo 0)
            if [ $size -gt $max_size ]; then
                log_warning "Large file detected: $file ($(($size/1024))KB)"
                ((large_files++))
            fi
        fi
    done < <(get_staged_files)

    if [ $large_files -gt 0 ]; then
        log_warning "$large_files large files found (>1MB)"
        log_info "Consider using Git LFS for large files"
    else
        log_success "No large files detected"
    fi

    return 0  # Don't fail on large files, just warn
}

# Check for merge conflict markers
check_merge_conflicts() {
    log_info "Checking for merge conflict markers..."
    local conflicts=0

    while IFS= read -r file; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            if grep -E "^(<{7}|={7}|>{7})" "$PROJECT_ROOT/$file" >/dev/null 2>&1; then
                log_error "Merge conflict markers found in $file"
                ((conflicts++))
            fi
        fi
    done < <(get_staged_files)

    if [ $conflicts -gt 0 ]; then
        log_error "$conflicts files contain merge conflict markers!"
        return 1
    else
        log_success "No merge conflict markers found"
        return 0
    fi
}

# Run Rule-1 scanner if available
check_rule1() {
    if [ -f "$PROJECT_ROOT/tools/audits/rule1_scan.py" ]; then
        log_info "Running Rule-1 content scanner..."
        if python3 "$PROJECT_ROOT/tools/audits/rule1_scan.py" --quiet; then
            log_success "Rule-1 scan passed"
            return 0
        else
            log_error "Rule-1 scan failed"
            return 1
        fi
    else
        log_info "Rule-1 scanner not available, skipping"
        return 0
    fi
}

# Main execution
init_precommit

# Exit early if test mode
if [ "$TEST_MODE" = true ]; then
    log_success "Pre-commit hook test completed"
    exit 0
fi

# Run all checks
failed_checks=0

check_secrets || ((failed_checks++))
check_merge_conflicts || ((failed_checks++))
check_python_quality || ((failed_checks++))
check_js_quality || ((failed_checks++))
check_rule1 || ((failed_checks++))

# Non-failing checks (warnings only)
check_todos
check_file_sizes

# Final result
if [ $failed_checks -gt 0 ]; then
    log_error "Pre-commit checks failed! ($failed_checks failures)"
    log_error "Commit aborted. Please fix the issues above."
    log_info "To bypass these checks temporarily, use: git commit --no-verify"
    exit 1
else
    log_success "All pre-commit checks passed!"
    log_success "Proceeding with commit..."
    exit 0
fi
