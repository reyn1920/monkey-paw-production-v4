#!/bin/bash

# Pre-push Guard - Deployment Readiness and Security Gate
# Runs before each push to ensure deployment readiness and security
# This script is designed to be used as a Git pre-push hook

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_FILE="$PROJECT_ROOT/.trae/prepush.log"
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
    echo -e "${BLUE}[PRE-PUSH]${NC} $1"
    echo "$(date): [INFO] $1" >> "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[PRE-PUSH]${NC} $1"
    echo "$(date): [SUCCESS] $1" >> "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[PRE-PUSH]${NC} $1"
    echo "$(date): [WARNING] $1" >> "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[PRE-PUSH]${NC} $1"
    echo "$(date): [ERROR] $1" >> "$LOG_FILE"
}

# Initialize
init_prepush() {
    mkdir -p "$PROJECT_ROOT/.trae"
    touch "$LOG_FILE"

    if [ "$TEST_MODE" = true ]; then
        log_info "Running in test mode"
        return 0
    fi

    log_info "Starting pre-push checks..."
}

# Check if we're pushing to main/master branch
check_target_branch() {
    if [ "$TEST_MODE" = true ]; then
        return 0
    fi

    # Read from stdin (git pre-push hook format)
    while read local_ref local_sha remote_ref remote_sha; do
        local branch_name=$(echo "$remote_ref" | sed 's|refs/heads/||')

        if [[ "$branch_name" == "main" || "$branch_name" == "master" ]]; then
            log_warning "Pushing to protected branch: $branch_name"
            log_info "Running enhanced security checks..."
            return 0
        fi
    done

    log_info "Pushing to feature branch, running standard checks..."
    return 0
}

# Deep security scan
deep_security_scan() {
    log_info "Running deep security scan..."
    local violations=0

    # Enhanced secret patterns
    local secret_patterns=(
        "password\s*[:=]\s*['\"][^'\"]{8,}['\"]"  # Longer passwords
        "api[_-]?key\s*[:=]\s*['\"][^'\"]{16,}['\"]"  # API keys
        "secret[_-]?key\s*[:=]\s*['\"][^'\"]{16,}['\"]"  # Secret keys
        "access[_-]?token\s*[:=]\s*['\"][^'\"]{20,}['\"]"  # Access tokens
        "private[_-]?key\s*[:=]\s*['\"][^'\"]{32,}['\"]"  # Private keys
        "-----BEGIN [A-Z ]+-----"  # PEM format keys
        "['\"][A-Za-z0-9+/]{40,}={0,2}['\"]"  # Base64 encoded secrets
        "sk-[A-Za-z0-9]{48,}"  # OpenAI API keys (updated pattern)
        "ghp_[A-Za-z0-9]{36}"  # GitHub personal access tokens
        "gho_[A-Za-z0-9]{36}"  # GitHub OAuth tokens
        "ghs_[A-Za-z0-9]{36}"  # GitHub app tokens
        "github_pat_[A-Za-z0-9_]{82}"  # New GitHub PAT format
        "glpat-[A-Za-z0-9\-_]{20}"  # GitLab personal access tokens
        "xoxb-[A-Za-z0-9\-]+"  # Slack bot tokens
        "xoxp-[A-Za-z0-9\-]+"  # Slack user tokens
        "AKIA[0-9A-Z]{16}"  # AWS access key IDs
        "[0-9a-zA-Z/+]{40}"  # AWS secret access keys
    )

    # Scan all files in the repository
    find "$PROJECT_ROOT" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.env*" -o -name "*.config" \) ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/.trae/*" | while read -r file; do
        for pattern in "${secret_patterns[@]}"; do
            if grep -iE "$pattern" "$file" >/dev/null 2>&1; then
                log_error "Potential secret found in $file"
                grep -inE "$pattern" "$file" | head -2
                ((violations++))
            fi
        done
    done

    if [ $violations -gt 0 ]; then
        log_error "$violations potential secrets found in deep scan!"
        return 1
    else
        log_success "Deep security scan passed"
        return 0
    fi
}

# Check environment files
check_env_files() {
    log_info "Checking environment files..."
    local issues=0

    # Check for .env files that shouldn't be committed
    local env_files=("$PROJECT_ROOT/.env" "$PROJECT_ROOT/.env.local" "$PROJECT_ROOT/.env.production")

    for env_file in "${env_files[@]}"; do
        if [ -f "$env_file" ]; then
            # Check if it's tracked by git
            if git ls-files --error-unmatch "$env_file" >/dev/null 2>&1; then
                log_error "Environment file is tracked by Git: $(basename "$env_file")"
                log_error "This file may contain secrets and should not be committed"
                ((issues++))
            else
                log_success "Environment file properly ignored: $(basename "$env_file")"
            fi
        fi
    done

    # Check for .env.example or .env.template
    if [ ! -f "$PROJECT_ROOT/.env.example" ] && [ ! -f "$PROJECT_ROOT/.env.template" ]; then
        log_warning "No .env.example or .env.template found"
        log_info "Consider creating an example environment file for documentation"
    else
        log_success "Environment template file found"
    fi

    if [ $issues -gt 0 ]; then
        return 1
    else
        return 0
    fi
}

# Check build and deployment readiness
check_build_readiness() {
    log_info "Checking build and deployment readiness..."

    # Check for package.json and dependencies
    if [ -f "$PROJECT_ROOT/package.json" ]; then
        log_info "Found package.json, checking Node.js project..."

        # Check if node_modules exists
        if [ ! -d "$PROJECT_ROOT/node_modules" ]; then
            log_warning "node_modules not found, dependencies may not be installed"
        fi

        # Check for build script
        if grep -q '"build"' "$PROJECT_ROOT/package.json"; then
            log_success "Build script found in package.json"

            # Try to run build if npm is available
            if command -v npm >/dev/null 2>&1; then
                log_info "Testing build process..."
                cd "$PROJECT_ROOT"
                if npm run build >/dev/null 2>&1; then
                    log_success "Build test passed"
                else
                    log_error "Build test failed"
                    return 1
                fi
            fi
        else
            log_warning "No build script found in package.json"
        fi
    fi

    # Check for Python requirements
    if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
        log_info "Found requirements.txt, checking Python project..."

        # Check if virtual environment is recommended
        if [ -z "$VIRTUAL_ENV" ] && [ ! -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
            log_warning "No virtual environment detected"
            log_info "Consider using a virtual environment for Python projects"
        fi
    fi

    return 0
}

# Check for critical files
check_critical_files() {
    log_info "Checking for critical project files..."
    local missing_files=0

    # List of critical files
    local critical_files=(
        "README.md"
        ".gitignore"
        "TRAE_RULES.md"
    )

    for file in "${critical_files[@]}"; do
        if [ ! -f "$PROJECT_ROOT/$file" ]; then
            log_warning "Critical file missing: $file"
            ((missing_files++))
        else
            log_success "Critical file found: $file"
        fi
    done

    if [ $missing_files -gt 0 ]; then
        log_warning "$missing_files critical files are missing"
        log_info "Consider creating these files before deployment"
    fi

    return 0  # Don't fail on missing files, just warn
}

# Run comprehensive tests
run_tests() {
    log_info "Running comprehensive tests..."

    # Run Python tests if available
    if [ -f "$PROJECT_ROOT/pytest.ini" ] || [ -d "$PROJECT_ROOT/tests" ]; then
        if command -v pytest >/dev/null 2>&1; then
            log_info "Running Python tests..."
            cd "$PROJECT_ROOT"
            if pytest --quiet >/dev/null 2>&1; then
                log_success "Python tests passed"
            else
                log_error "Python tests failed"
                return 1
            fi
        fi
    fi

    # Run JavaScript tests if available
    if [ -f "$PROJECT_ROOT/package.json" ] && grep -q '"test"' "$PROJECT_ROOT/package.json"; then
        if command -v npm >/dev/null 2>&1; then
            log_info "Running JavaScript tests..."
            cd "$PROJECT_ROOT"
            if npm test >/dev/null 2>&1; then
                log_success "JavaScript tests passed"
            else
                log_error "JavaScript tests failed"
                return 1
            fi
        fi
    fi

    return 0
}

# Check deployment configuration
check_deployment_config() {
    log_info "Checking deployment configuration..."

    # Check for Netlify configuration
    if [ -f "$PROJECT_ROOT/netlify.toml" ]; then
        log_success "Netlify configuration found"

        # Validate basic structure
        if grep -q "\[build\]" "$PROJECT_ROOT/netlify.toml"; then
            log_success "Build configuration found in netlify.toml"
        else
            log_warning "No build configuration in netlify.toml"
        fi
    fi

    # Check for GitHub Actions
    if [ -d "$PROJECT_ROOT/.github/workflows" ]; then
        log_success "GitHub Actions workflows found"

        # Count workflow files
        local workflow_count=$(find "$PROJECT_ROOT/.github/workflows" -name "*.yml" -o -name "*.yaml" | wc -l)
        log_info "Found $workflow_count workflow files"
    fi

    return 0
}

# Run persistence guard check
run_persistence_check() {
    if [ -f "$PROJECT_ROOT/tools/audits/persist_guard.sh" ]; then
        log_info "Running persistence guard check..."
        if "$PROJECT_ROOT/tools/audits/persist_guard.sh" --check >/dev/null 2>&1; then
            log_success "Persistence guard check passed"
            return 0
        else
            log_error "Persistence guard check failed"
            return 1
        fi
    else
        log_info "Persistence guard not available, skipping"
        return 0
    fi
}

# Main execution
init_prepush

# Exit early if test mode
if [ "$TEST_MODE" = true ]; then
    log_success "Pre-push hook test completed"
    exit 0
fi

# Check target branch
check_target_branch

# Run all checks
failed_checks=0

deep_security_scan || ((failed_checks++))
check_env_files || ((failed_checks++))
check_build_readiness || ((failed_checks++))
run_tests || ((failed_checks++))
run_persistence_check || ((failed_checks++))

# Non-failing checks (warnings only)
check_critical_files
check_deployment_config

# Final result
if [ $failed_checks -gt 0 ]; then
    log_error "Pre-push checks failed! ($failed_checks failures)"
    log_error "Push aborted. Please fix the issues above."
    log_info "To bypass these checks temporarily, use: git push --no-verify"
    exit 1
else
    log_success "All pre-push checks passed!"
    log_success "Proceeding with push..."
    exit 0
fi
