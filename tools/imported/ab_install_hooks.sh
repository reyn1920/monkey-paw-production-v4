#!/bin/bash

# Git Hooks Installation Script
# Installs pre-commit and pre-push hooks for code quality and security
# Usage: ./install_hooks.sh [--force] [--uninstall]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
TOOLS_HOOKS_DIR="$PROJECT_ROOT/tools/hooks"

# Parse command line arguments
FORCE=false
UNINSTALL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --force)
            FORCE=true
            shift
            ;;
        --uninstall)
            UNINSTALL=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--force] [--uninstall]"
            echo "  --force      Overwrite existing hooks"
            echo "  --uninstall  Remove installed hooks"
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
    echo -e "${BLUE}[HOOKS]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[HOOKS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[HOOKS]${NC} $1"
}

log_error() {
    echo -e "${RED}[HOOKS]${NC} $1"
}

# Check if we're in a Git repository
check_git_repo() {
    if [ ! -d "$PROJECT_ROOT/.git" ]; then
        log_error "Not a Git repository. Please run 'git init' first."
        exit 1
    fi
}

# Create hooks directory if it doesn't exist
ensure_hooks_dir() {
    if [ ! -d "$HOOKS_DIR" ]; then
        mkdir -p "$HOOKS_DIR"
        log_info "Created hooks directory: $HOOKS_DIR"
    fi
}

# Install a single hook
install_hook() {
    local hook_name="$1"
    local source_file="$TOOLS_HOOKS_DIR/${hook_name}_guard.sh"
    local target_file="$HOOKS_DIR/$hook_name"

    if [ ! -f "$source_file" ]; then
        log_error "Source hook file not found: $source_file"
        return 1
    fi

    # Check if hook already exists
    if [ -f "$target_file" ] && [ "$FORCE" = false ]; then
        log_warning "Hook already exists: $hook_name (use --force to overwrite)"
        return 0
    fi

    # Copy and make executable
    cp "$source_file" "$target_file"
    chmod +x "$target_file"

    log_success "Installed hook: $hook_name"
}

# Uninstall a single hook
uninstall_hook() {
    local hook_name="$1"
    local target_file="$HOOKS_DIR/$hook_name"

    if [ -f "$target_file" ]; then
        rm "$target_file"
        log_success "Uninstalled hook: $hook_name"
    else
        log_info "Hook not found: $hook_name"
    fi
}

# Install all hooks
install_all_hooks() {
    log_info "Installing Git hooks..."

    # List of hooks to install
    local hooks=("pre-commit" "pre-push")

    for hook in "${hooks[@]}"; do
        install_hook "$hook"
    done

    log_success "All hooks installed successfully!"
    log_info "Hooks will now run automatically on git commit and git push"
    log_info "To bypass hooks temporarily, use: git commit --no-verify"
}

# Uninstall all hooks
uninstall_all_hooks() {
    log_info "Uninstalling Git hooks..."

    local hooks=("pre-commit" "pre-push")

    for hook in "${hooks[@]}"; do
        uninstall_hook "$hook"
    done

    log_success "All hooks uninstalled successfully!"
}

# Verify hook installation
verify_installation() {
    log_info "Verifying hook installation..."

    local hooks=("pre-commit" "pre-push")
    local all_installed=true

    for hook in "${hooks[@]}"; do
        local target_file="$HOOKS_DIR/$hook"
        if [ -f "$target_file" ] && [ -x "$target_file" ]; then
            log_success "✓ $hook hook is installed and executable"
        else
            log_error "✗ $hook hook is missing or not executable"
            all_installed=false
        fi
    done

    if [ "$all_installed" = true ]; then
        log_success "All hooks are properly installed!"
        return 0
    else
        log_error "Some hooks are not properly installed"
        return 1
    fi
}

# Show hook status
show_status() {
    log_info "Git Hooks Status:"
    echo

    local hooks=("pre-commit" "pre-push")

    for hook in "${hooks[@]}"; do
        local target_file="$HOOKS_DIR/$hook"
        local source_file="$TOOLS_HOOKS_DIR/${hook}_guard.sh"

        echo -n "  $hook: "

        if [ -f "$target_file" ]; then
            if [ -x "$target_file" ]; then
                echo -e "${GREEN}Installed${NC}"
            else
                echo -e "${YELLOW}Installed (not executable)${NC}"
            fi
        else
            echo -e "${RED}Not installed${NC}"
        fi

        # Check if source exists
        if [ ! -f "$source_file" ]; then
            echo -e "    ${RED}Warning: Source file missing: $source_file${NC}"
        fi
    done

    echo
}

# Test hooks
test_hooks() {
    log_info "Testing installed hooks..."

    # Test pre-commit hook
    if [ -f "$HOOKS_DIR/pre-commit" ]; then
        log_info "Testing pre-commit hook..."
        if "$HOOKS_DIR/pre-commit" --test 2>/dev/null; then
            log_success "Pre-commit hook test passed"
        else
            log_warning "Pre-commit hook test failed or not supported"
        fi
    fi

    # Test pre-push hook
    if [ -f "$HOOKS_DIR/pre-push" ]; then
        log_info "Testing pre-push hook..."
        if "$HOOKS_DIR/pre-push" --test 2>/dev/null; then
            log_success "Pre-push hook test passed"
        else
            log_warning "Pre-push hook test failed or not supported"
        fi
    fi
}

# Main execution
check_git_repo
ensure_hooks_dir

if [ "$UNINSTALL" = true ]; then
    uninstall_all_hooks
else
    install_all_hooks
    echo
    verify_installation
    echo
    show_status
    echo
    test_hooks
fi

log_info "Done!"
