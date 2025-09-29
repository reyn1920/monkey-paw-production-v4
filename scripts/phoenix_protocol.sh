#!/bin/bash

# Phoenix Protocol - TRAE.AI System Deployment and Recovery Script
# Handles deployment, rollback, health checks, and system recovery
# Version: 3.0
# Author: TRAE.AI System

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_ROOT/logs"
BACKUP_DIR="$PROJECT_ROOT/backups"
ASSETS_DIR="$PROJECT_ROOT/assets"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/phoenix_protocol_$TIMESTAMP.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Ensure required directories exist
mkdir -p "$LOG_DIR" "$BACKUP_DIR"

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }
log_success() { log "SUCCESS" "$@"; }

# Print colored output
print_status() {
    local color="$1"
    local message="$2"
    echo -e "${color}${message}${NC}"
}

print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

print_success() { print_status "$GREEN" "✓ $1"; }
print_error() { print_status "$RED" "✗ $1"; }
print_warning() { print_status "$YELLOW" "⚠ $1"; }
print_info() { print_status "$BLUE" "ℹ $1"; }

# Error handling
error_exit() {
    log_error "$1"
    print_error "$1"
    exit 1
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
check_requirements() {
    print_header "Checking System Requirements"

    local missing_commands=()
    local required_commands=("python3" "pip3" "git")

    for cmd in "${required_commands[@]}"; do
        if command_exists "$cmd"; then
            print_success "$cmd is available"
            log_info "Command available: $cmd"
        else
            missing_commands+=("$cmd")
            print_error "$cmd is not available"
            log_error "Missing command: $cmd"
        fi
    done

    if [ ${#missing_commands[@]} -gt 0 ]; then
        error_exit "Missing required commands: ${missing_commands[*]}"
    fi

    # Check Python version
    local python_version
    python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_info "Python version: $python_version"
    log_info "Python version: $python_version"

    # Check if we're in a virtual environment
    if [[ -n "${VIRTUAL_ENV:-}" ]]; then
        print_success "Running in virtual environment: $VIRTUAL_ENV"
        log_info "Virtual environment: $VIRTUAL_ENV"
    else
        print_warning "Not running in a virtual environment"
        log_warn "No virtual environment detected"
    fi
}

# Create backup
create_backup() {
    print_header "Creating System Backup"

    local backup_name="backup_$TIMESTAMP"
    local backup_path="$BACKUP_DIR/$backup_name"

    log_info "Creating backup: $backup_name"

    # Create backup directory
    mkdir -p "$backup_path"

    # Backup critical files and directories
    local backup_items=(
        "app"
        "backend"
        "scripts"
        "requirements.txt"
        "README.md"
        ".env.example"
    )

    for item in "${backup_items[@]}"; do
        local source_path="$PROJECT_ROOT/$item"
        if [[ -e "$source_path" ]]; then
            cp -r "$source_path" "$backup_path/"
            print_success "Backed up: $item"
            log_info "Backed up: $item"
        else
            print_warning "Skipped missing item: $item"
            log_warn "Missing backup item: $item"
        fi
    done

    # Create backup manifest
    cat > "$backup_path/manifest.json" << EOF
{
    "backup_id": "$backup_name",
    "timestamp": "$TIMESTAMP",
    "created_by": "phoenix_protocol.sh",
    "project_root": "$PROJECT_ROOT",
    "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
    "git_branch": "$(git branch --show-current 2>/dev/null || echo 'unknown')",
    "backup_items": $(printf '%s\n' "${backup_items[@]}" | jq -R . | jq -s . 2>/dev/null || echo '[]')
}
EOF

    print_success "Backup created: $backup_path"
    log_success "Backup created: $backup_path"

    # Keep only last 10 backups
    local backup_count
    backup_count=$(find "$BACKUP_DIR" -maxdepth 1 -type d -name "backup_*" | wc -l)

    if [[ $backup_count -gt 10 ]]; then
        print_info "Cleaning up old backups (keeping 10 most recent)"
        find "$BACKUP_DIR" -maxdepth 1 -type d -name "backup_*" -printf '%T@ %p\n' 2>/dev/null | \
            sort -n | head -n -10 | cut -d' ' -f2- | xargs rm -rf 2>/dev/null || true
        log_info "Cleaned up old backups"
    fi
}

# Install dependencies
install_dependencies() {
    print_header "Installing Dependencies"

    cd "$PROJECT_ROOT"

    # Install Python dependencies
    if [[ -f "requirements.txt" ]]; then
        print_info "Installing Python dependencies..."
        log_info "Installing Python dependencies from requirements.txt"

        pip3 install -r requirements.txt --upgrade

        print_success "Python dependencies installed"
        log_success "Python dependencies installed"
    else
        print_warning "No requirements.txt found"
        log_warn "No requirements.txt file found"
    fi

    # Install Node.js dependencies if package.json exists
    if [[ -f "package.json" ]]; then
        if command_exists "npm"; then
            print_info "Installing Node.js dependencies..."
            log_info "Installing Node.js dependencies from package.json"

            npm install

            print_success "Node.js dependencies installed"
            log_success "Node.js dependencies installed"
        else
            print_warning "package.json found but npm not available"
            log_warn "npm not available for package.json"
        fi
    fi
}

# Run security scan
run_security_scan() {
    print_header "Running Security Scan"

    cd "$PROJECT_ROOT"

    # Run compliance validator if available
    if [[ -f "backend/security/compliance_validator.py" ]]; then
        print_info "Running compliance validation..."
        log_info "Running compliance validation"

        if python3 backend/security/compliance_validator.py --base-dir . --output "$LOG_DIR/compliance_$TIMESTAMP.json"; then
            print_success "Compliance validation passed"
            log_success "Compliance validation passed"
        else
            print_error "Compliance validation failed"
            log_error "Compliance validation failed"
            return 1
        fi
    else
        print_warning "Compliance validator not found"
        log_warn "Compliance validator not available"
    fi

    # Run security scanner if available
    if [[ -f "backend/security/security_scanner.py" ]]; then
        print_info "Running security scan..."
        log_info "Running security scan"

        if python3 backend/security/security_scanner.py --target . --output "$LOG_DIR/security_scan_$TIMESTAMP.json"; then
            print_success "Security scan completed"
            log_success "Security scan completed"
        else
            print_warning "Security scan completed with warnings"
            log_warn "Security scan completed with warnings"
        fi
    else
        print_warning "Security scanner not found"
        log_warn "Security scanner not available"
    fi
}

# Run tests
run_tests() {
    print_header "Running Tests"

    cd "$PROJECT_ROOT"

    local test_files=()

    # Find test files
    if [[ -d "tests" ]]; then
        mapfile -t test_files < <(find tests -name "test_*.py" -o -name "*_test.py")
    fi

    if [[ ${#test_files[@]} -eq 0 ]]; then
        print_warning "No test files found"
        log_warn "No test files found"
        return 0
    fi

    print_info "Found ${#test_files[@]} test file(s)"
    log_info "Found ${#test_files[@]} test files"

    local failed_tests=()

    for test_file in "${test_files[@]}"; do
        print_info "Running: $test_file"
        log_info "Running test: $test_file"

        if python3 "$test_file"; then
            print_success "Passed: $test_file"
            log_success "Test passed: $test_file"
        else
            print_error "Failed: $test_file"
            log_error "Test failed: $test_file"
            failed_tests+=("$test_file")
        fi
    done

    if [[ ${#failed_tests[@]} -gt 0 ]]; then
        print_error "${#failed_tests[@]} test(s) failed: ${failed_tests[*]}"
        log_error "Failed tests: ${failed_tests[*]}"
        return 1
    else
        print_success "All tests passed"
        log_success "All tests passed"
        return 0
    fi
}

# Health check
health_check() {
    print_header "System Health Check"

    cd "$PROJECT_ROOT"

    local health_issues=()

    # Check critical files
    local critical_files=(
        "app/dashboard.py"
        "backend/core/secret_store_bridge.py"
        "requirements.txt"
    )

    for file in "${critical_files[@]}"; do
        if [[ -f "$file" ]]; then
            print_success "Critical file exists: $file"
            log_info "Critical file OK: $file"
        else
            print_error "Missing critical file: $file"
            log_error "Missing critical file: $file"
            health_issues+=("Missing file: $file")
        fi
    done

    # Check directory structure
    local critical_dirs=(
        "app"
        "backend/core"
        "backend/runner"
        "backend/security"
        "scripts"
        "assets/incoming"
        "assets/releases"
        "tests"
    )

    for dir in "${critical_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            print_success "Directory exists: $dir"
            log_info "Directory OK: $dir"
        else
            print_error "Missing directory: $dir"
            log_error "Missing directory: $dir"
            health_issues+=("Missing directory: $dir")
        fi
    done

    # Check Python imports
    print_info "Checking Python imports..."
    log_info "Checking Python imports"

    local import_test="
import sys
sys.path.insert(0, '.')
try:
    from app.dashboard import DashboardApp
    from backend.core.secret_store_bridge import SecretStoreBridge
    print('All critical imports successful')
except ImportError as e:
    print(f'Import error: {e}')
    sys.exit(1)
"

    if python3 -c "$import_test"; then
        print_success "Python imports OK"
        log_success "Python imports OK"
    else
        print_error "Python import issues detected"
        log_error "Python import issues detected"
        health_issues+=("Python import issues")
    fi

    # Check disk space
    local disk_usage
    disk_usage=$(df "$PROJECT_ROOT" | awk 'NR==2 {print $5}' | sed 's/%//')

    if [[ $disk_usage -lt 90 ]]; then
        print_success "Disk usage OK: ${disk_usage}%"
        log_info "Disk usage: ${disk_usage}%"
    else
        print_warning "High disk usage: ${disk_usage}%"
        log_warn "High disk usage: ${disk_usage}%"
        health_issues+=("High disk usage: ${disk_usage}%")
    fi

    # Summary
    if [[ ${#health_issues[@]} -eq 0 ]]; then
        print_success "System health check passed"
        log_success "System health check passed"
        return 0
    else
        print_error "Health check found ${#health_issues[@]} issue(s):"
        for issue in "${health_issues[@]}"; do
            print_error "  - $issue"
        done
        log_error "Health check issues: ${health_issues[*]}"
        return 1
    fi
}

# Deploy system
deploy() {
    print_header "Deploying TRAE.AI System"

    log_info "Starting deployment process"

    # Pre-deployment checks
    check_requirements || error_exit "Requirements check failed"

    # Create backup
    create_backup || error_exit "Backup creation failed"

    # Install dependencies
    install_dependencies || error_exit "Dependency installation failed"

    # Run security scan
    if ! run_security_scan; then
        print_warning "Security scan had issues, but continuing deployment"
        log_warn "Security scan had issues, continuing deployment"
    fi

    # Run tests
    if ! run_tests; then
        print_error "Tests failed, aborting deployment"
        log_error "Tests failed, aborting deployment"
        return 1
    fi

    # Health check
    health_check || error_exit "Health check failed"

    # Create deployment marker
    cat > "$PROJECT_ROOT/.deployment_info" << EOF
{
    "deployment_id": "deploy_$TIMESTAMP",
    "timestamp": "$TIMESTAMP",
    "script_version": "3.0",
    "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
    "git_branch": "$(git branch --show-current 2>/dev/null || echo 'unknown')",
    "status": "deployed"
}
EOF

    print_success "Deployment completed successfully"
    log_success "Deployment completed successfully"

    print_info "Deployment info saved to .deployment_info"
    print_info "Logs available at: $LOG_FILE"
}

# Show usage
usage() {
    cat << EOF
Phoenix Protocol - TRAE.AI System Management

Usage: $0 <command> [options]

Commands:
  deploy              Deploy the system (full deployment process)
  health              Run system health check
  status              Show system status
  backup              Create system backup
  security-scan       Run security scan only
  test                Run tests only
  requirements        Check system requirements

Examples:
  $0 deploy                    # Full deployment
  $0 health                    # Health check only
  $0 status                    # Show system status

Logs are saved to: $LOG_DIR
Backups are saved to: $BACKUP_DIR

EOF
}

# Main execution
main() {
    local command="${1:-}"

    # Create log entry for script execution
    log_info "Phoenix Protocol started with command: ${command:-'none'}"
    log_info "Script version: 3.0"
    log_info "Project root: $PROJECT_ROOT"
    log_info "Log file: $LOG_FILE"

    case "$command" in
        "deploy")
            deploy
            ;;
        "health")
            health_check
            ;;
        "status")
            print_header "TRAE.AI System Status"
            cd "$PROJECT_ROOT"
            if [[ -f ".deployment_info" ]]; then
                print_info "Reading deployment info..."
                cat .deployment_info 2>/dev/null || print_warning "Could not read deployment info"
            else
                print_warning "No deployment info found"
            fi
            echo
            health_check
            ;;
        "backup")
            create_backup
            ;;
        "security-scan")
            run_security_scan
            ;;
        "test")
            run_tests
            ;;
        "requirements")
            check_requirements
            ;;
        "help"|"--help"|"")
            usage
            ;;
        *)
            print_error "Unknown command: $command"
            echo
            usage
            exit 1
            ;;
    esac

    log_info "Phoenix Protocol completed for command: $command"
}

# Execute main function with all arguments
main "$@"
