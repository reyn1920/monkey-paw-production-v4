#!/bin/bash

# patch_package_json.sh - Package.json Patching Script
# Part of the Trae AI Cleanup Framework
#
# This script handles package.json modifications, dependency updates,
# security patches, and package optimization.

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_FILE="$SCRIPT_DIR/package_patcher.log"
BACKUP_DIR="$SCRIPT_DIR/backups"
PACKAGE_JSON="$PROJECT_ROOT/package.json"
PACKAGE_LOCK="$PROJECT_ROOT/package-lock.json"
YARN_LOCK="$PROJECT_ROOT/yarn.lock"
PNPM_LOCK="$PROJECT_ROOT/pnpm-lock.yaml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default options
DRY_RUN=false
VERBOSE=false
BACKUP=true
AUTO_FIX=false
UPDATE_DEPS=false
SECURITY_AUDIT=false
CLEAN_INSTALL=false
OPTIMIZE=false
FIX_VULNERABILITIES=false

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"

    case "$level" in
        "ERROR")
            echo -e "${RED}[ERROR]${NC} $message" >&2
            ;;
        "WARN")
            echo -e "${YELLOW}[WARN]${NC} $message"
            ;;
        "INFO")
            echo -e "${GREEN}[INFO]${NC} $message"
            ;;
        "DEBUG")
            if [[ "$VERBOSE" == "true" ]]; then
                echo -e "${BLUE}[DEBUG]${NC} $message"
            fi
            ;;
    esac
}

# Error handling
error_exit() {
    log "ERROR" "$1"
    exit 1
}

# Usage information
show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Package.json Patching and Optimization Tool

OPTIONS:
    -d, --dry-run           Show what would be done without making changes
    -v, --verbose           Enable verbose output
    -b, --no-backup         Skip creating backups
    -a, --auto-fix          Automatically fix common issues
    -u, --update-deps       Update dependencies to latest versions
    -s, --security-audit    Run security audit and fix vulnerabilities
    -c, --clean-install     Clean install dependencies
    -o, --optimize          Optimize package.json structure
    -f, --fix-vulns         Fix security vulnerabilities
    -h, --help              Show this help message

EXAMPLES:
    $0 --dry-run --verbose          # Preview changes with detailed output
    $0 --auto-fix --optimize        # Fix issues and optimize package.json
    $0 --security-audit --fix-vulns # Security-focused cleanup
    $0 --update-deps --clean-install # Update and reinstall dependencies

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -b|--no-backup)
                BACKUP=false
                shift
                ;;
            -a|--auto-fix)
                AUTO_FIX=true
                shift
                ;;
            -u|--update-deps)
                UPDATE_DEPS=true
                shift
                ;;
            -s|--security-audit)
                SECURITY_AUDIT=true
                shift
                ;;
            -c|--clean-install)
                CLEAN_INSTALL=true
                shift
                ;;
            -o|--optimize)
                OPTIMIZE=true
                shift
                ;;
            -f|--fix-vulns)
                FIX_VULNERABILITIES=true
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                error_exit "Unknown option: $1"
                ;;
        esac
    done
}

# Check prerequisites
check_prerequisites() {
    log "INFO" "Checking prerequisites..."

    # Check if package.json exists
    if [[ ! -f "$PACKAGE_JSON" ]]; then
        error_exit "package.json not found at $PACKAGE_JSON"
    fi

    # Check for package managers
    local package_manager=""
    if command -v npm >/dev/null 2>&1; then
        package_manager="npm"
    elif command -v yarn >/dev/null 2>&1; then
        package_manager="yarn"
    elif command -v pnpm >/dev/null 2>&1; then
        package_manager="pnpm"
    else
        error_exit "No package manager found (npm, yarn, or pnpm required)"
    fi

    log "INFO" "Using package manager: $package_manager"

    # Check for jq (JSON processor)
    if ! command -v jq >/dev/null 2>&1; then
        log "WARN" "jq not found. Some features may be limited."
    fi

    # Create backup directory
    if [[ "$BACKUP" == "true" ]]; then
        mkdir -p "$BACKUP_DIR"
    fi
}

# Create backup
create_backup() {
    if [[ "$BACKUP" == "false" ]]; then
        return 0
    fi

    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local backup_file="$BACKUP_DIR/package_json_$timestamp.json"

    log "INFO" "Creating backup: $backup_file"

    if [[ "$DRY_RUN" == "false" ]]; then
        cp "$PACKAGE_JSON" "$backup_file"

        # Backup lock files if they exist
        if [[ -f "$PACKAGE_LOCK" ]]; then
            cp "$PACKAGE_LOCK" "$BACKUP_DIR/package-lock_$timestamp.json"
        fi
        if [[ -f "$YARN_LOCK" ]]; then
            cp "$YARN_LOCK" "$BACKUP_DIR/yarn_lock_$timestamp.lock"
        fi
        if [[ -f "$PNPM_LOCK" ]]; then
            cp "$PNPM_LOCK" "$BACKUP_DIR/pnpm-lock_$timestamp.yaml"
        fi
    fi
}

# Detect package manager
detect_package_manager() {
    if [[ -f "$PNPM_LOCK" ]]; then
        echo "pnpm"
    elif [[ -f "$YARN_LOCK" ]]; then
        echo "yarn"
    elif [[ -f "$PACKAGE_LOCK" ]]; then
        echo "npm"
    else
        echo "npm"  # Default to npm
    fi
}

# Validate package.json syntax
validate_package_json() {
    log "INFO" "Validating package.json syntax..."

    if ! jq empty "$PACKAGE_JSON" 2>/dev/null; then
        error_exit "Invalid JSON syntax in package.json"
    fi

    # Check required fields
    local required_fields=("name" "version")
    for field in "${required_fields[@]}"; do
        if ! jq -e ".$field" "$PACKAGE_JSON" >/dev/null 2>&1; then
            log "WARN" "Missing required field: $field"
        fi
    done

    log "INFO" "package.json syntax is valid"
}

# Fix common package.json issues
fix_common_issues() {
    if [[ "$AUTO_FIX" == "false" ]]; then
        return 0
    fi

    log "INFO" "Fixing common package.json issues..."

    local temp_file=$(mktemp)

    # Fix missing fields
    jq '. + {
        "private": (if .private == null then true else .private end),
        "license": (if .license == null then "UNLICENSED" else .license end),
        "engines": (if .engines == null then {"node": ">=14.0.0"} else .engines end)
    }' "$PACKAGE_JSON" > "$temp_file"

    # Sort dependencies alphabetically
    jq '.dependencies = (.dependencies | to_entries | sort_by(.key) | from_entries) |
        .devDependencies = (.devDependencies | to_entries | sort_by(.key) | from_entries) |
        .peerDependencies = (.peerDependencies | to_entries | sort_by(.key) | from_entries)' \
        "$temp_file" > "${temp_file}.sorted"

    if [[ "$DRY_RUN" == "false" ]]; then
        mv "${temp_file}.sorted" "$PACKAGE_JSON"
    else
        log "INFO" "[DRY RUN] Would fix common issues in package.json"
    fi

    rm -f "$temp_file" "${temp_file}.sorted"
}

# Optimize package.json structure
optimize_package_json() {
    if [[ "$OPTIMIZE" == "false" ]]; then
        return 0
    fi

    log "INFO" "Optimizing package.json structure..."

    local temp_file=$(mktemp)

    # Reorder fields in a logical structure
    jq '{
        name: .name,
        version: .version,
        description: .description,
        private: .private,
        license: .license,
        author: .author,
        contributors: .contributors,
        homepage: .homepage,
        repository: .repository,
        bugs: .bugs,
        keywords: .keywords,
        engines: .engines,
        main: .main,
        module: .module,
        types: .types,
        exports: .exports,
        files: .files,
        bin: .bin,
        scripts: .scripts,
        dependencies: .dependencies,
        devDependencies: .devDependencies,
        peerDependencies: .peerDependencies,
        optionalDependencies: .optionalDependencies,
        bundledDependencies: .bundledDependencies,
        config: .config,
        browserslist: .browserslist,
        eslintConfig: .eslintConfig,
        prettier: .prettier,
        jest: .jest
    } | with_entries(select(.value != null))' "$PACKAGE_JSON" > "$temp_file"

    if [[ "$DRY_RUN" == "false" ]]; then
        mv "$temp_file" "$PACKAGE_JSON"
        log "INFO" "package.json structure optimized"
    else
        log "INFO" "[DRY RUN] Would optimize package.json structure"
    fi

    rm -f "$temp_file"
}

# Update dependencies
update_dependencies() {
    if [[ "$UPDATE_DEPS" == "false" ]]; then
        return 0
    fi

    log "INFO" "Updating dependencies..."

    local package_manager=$(detect_package_manager)

    if [[ "$DRY_RUN" == "false" ]]; then
        case "$package_manager" in
            "npm")
                npm update
                ;;
            "yarn")
                yarn upgrade
                ;;
            "pnpm")
                pnpm update
                ;;
        esac
        log "INFO" "Dependencies updated"
    else
        log "INFO" "[DRY RUN] Would update dependencies using $package_manager"
    fi
}

# Run security audit
run_security_audit() {
    if [[ "$SECURITY_AUDIT" == "false" ]]; then
        return 0
    fi

    log "INFO" "Running security audit..."

    local package_manager=$(detect_package_manager)
    local audit_output

    case "$package_manager" in
        "npm")
            if audit_output=$(npm audit --json 2>/dev/null); then
                local vulnerabilities=$(echo "$audit_output" | jq -r '.metadata.vulnerabilities.total//0')
                if [[ "$vulnerabilities" -gt 0 ]]; then
                    log "WARN" "Found $vulnerabilities security vulnerabilities"
                    if [[ "$FIX_VULNERABILITIES" == "true" ]]; then
                        fix_vulnerabilities
                    fi
                else
                    log "INFO" "No security vulnerabilities found"
                fi
            else
                log "WARN" "Security audit failed or not available"
            fi
            ;;
        "yarn")
            if yarn audit --json >/dev/null 2>&1; then
                log "INFO" "Yarn audit completed"
            else
                log "WARN" "Yarn audit found issues or failed"
            fi
            ;;
        "pnpm")
            if pnpm audit >/dev/null 2>&1; then
                log "INFO" "PNPM audit completed"
            else
                log "WARN" "PNPM audit found issues or failed"
            fi
            ;;
    esac
}

# Fix security vulnerabilities
fix_vulnerabilities() {
    if [[ "$FIX_VULNERABILITIES" == "false" ]]; then
        return 0
    fi

    log "INFO" "Fixing security vulnerabilities..."

    local package_manager=$(detect_package_manager)

    if [[ "$DRY_RUN" == "false" ]]; then
        case "$package_manager" in
            "npm")
                npm audit fix --force
                ;;
            "yarn")
                yarn audit fix
                ;;
            "pnpm")
                pnpm audit --fix
                ;;
        esac
        log "INFO" "Security vulnerabilities fixed"
    else
        log "INFO" "[DRY RUN] Would fix security vulnerabilities using $package_manager"
    fi
}

# Clean install dependencies
clean_install() {
    if [[ "$CLEAN_INSTALL" == "false" ]]; then
        return 0
    fi

    log "INFO" "Performing clean install..."

    local package_manager=$(detect_package_manager)

    if [[ "$DRY_RUN" == "false" ]]; then
        # Remove node_modules and lock files
        rm -rf "$PROJECT_ROOT/node_modules"

        case "$package_manager" in
            "npm")
                rm -f "$PACKAGE_LOCK"
                npm install
                ;;
            "yarn")
                rm -f "$YARN_LOCK"
                yarn install
                ;;
            "pnpm")
                rm -f "$PNPM_LOCK"
                pnpm install
                ;;
        esac
        log "INFO" "Clean install completed"
    else
        log "INFO" "[DRY RUN] Would perform clean install using $package_manager"
    fi
}

# Remove unused dependencies
remove_unused_dependencies() {
    log "INFO" "Checking for unused dependencies..."

    # This would integrate with the unused_scan.py script
    local unused_scan_script="$SCRIPT_DIR/unused_scan.py"

    if [[ -f "$unused_scan_script" ]]; then
        local unused_deps
        unused_deps=$(python3 "$unused_scan_script" --target-dir "$PROJECT_ROOT" --output-format json | jq -r '.unused_items[] | select(.item_type == "dependency") | .name')

        if [[ -n "$unused_deps" ]]; then
            log "INFO" "Found unused dependencies: $unused_deps"

            if [[ "$AUTO_FIX" == "true" ]]; then
                local package_manager=$(detect_package_manager)

                for dep in $unused_deps; do
                    if [[ "$DRY_RUN" == "false" ]]; then
                        case "$package_manager" in
                            "npm")
                                npm uninstall "$dep"
                                ;;
                            "yarn")
                                yarn remove "$dep"
                                ;;
                            "pnpm")
                                pnpm remove "$dep"
                                ;;
                        esac
                        log "INFO" "Removed unused dependency: $dep"
                    else
                        log "INFO" "[DRY RUN] Would remove unused dependency: $dep"
                    fi
                done
            fi
        else
            log "INFO" "No unused dependencies found"
        fi
    else
        log "WARN" "unused_scan.py not found, skipping unused dependency check"
    fi
}

# Generate report
generate_report() {
    log "INFO" "Generating package.json analysis report..."

    local report_file="$SCRIPT_DIR/package_analysis_$(date '+%Y%m%d_%H%M%S').txt"

    {
        echo "Package.json Analysis Report"
        echo "============================"
        echo "Generated: $(date)"
        echo "Project: $PROJECT_ROOT"
        echo ""

        # Basic info
        echo "PACKAGE INFORMATION:"
        echo "-------------------"
        if command -v jq >/dev/null 2>&1; then
            echo "Name: $(jq -r '.name//"N/A"' "$PACKAGE_JSON")"
            echo "Version: $(jq -r '.version//"N/A"' "$PACKAGE_JSON")"
            echo "Description: $(jq -r '.description//"N/A"' "$PACKAGE_JSON")"
            echo "License: $(jq -r '.license//"N/A"' "$PACKAGE_JSON")"
            echo ""

            # Dependencies count
            echo "DEPENDENCIES:"
            echo "------------"
            echo "Dependencies: $(jq '.dependencies | length' "$PACKAGE_JSON" 2>/dev/null || echo "0")"
            echo "Dev Dependencies: $(jq '.devDependencies | length' "$PACKAGE_JSON" 2>/dev/null || echo "0")"
            echo "Peer Dependencies: $(jq '.peerDependencies | length' "$PACKAGE_JSON" 2>/dev/null || echo "0")"
            echo ""
        fi

        # Package manager info
        echo "PACKAGE MANAGER:"
        echo "---------------"
        echo "Detected: $(detect_package_manager)"
        echo "Lock file exists: $([[ -f "$PACKAGE_LOCK" || -f "$YARN_LOCK" || -f "$PNPM_LOCK" ]] && echo "Yes" || echo "No")"
        echo ""

        # File sizes
        echo "FILE SIZES:"
        echo "----------"
        echo "package.json: $(du -h "$PACKAGE_JSON" | cut -f1)"
        if [[ -f "$PACKAGE_LOCK" ]]; then
            echo "package-lock.json: $(du -h "$PACKAGE_LOCK" | cut -f1)"
        fi
        if [[ -f "$YARN_LOCK" ]]; then
            echo "yarn.lock: $(du -h "$YARN_LOCK" | cut -f1)"
        fi
        if [[ -f "$PNPM_LOCK" ]]; then
            echo "pnpm-lock.yaml: $(du -h "$PNPM_LOCK" | cut -f1)"
        fi
        if [[ -d "$PROJECT_ROOT/node_modules" ]]; then
            echo "node_modules: $(du -sh "$PROJECT_ROOT/node_modules" | cut -f1)"
        fi

    } > "$report_file"

    log "INFO" "Report saved to: $report_file"

    if [[ "$VERBOSE" == "true" ]]; then
        cat "$report_file"
    fi
}

# Main execution
main() {
    log "INFO" "Starting package.json patching process..."

    # Initialize log file
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "Package.json Patcher Log - $(date)" > "$LOG_FILE"

    # Parse arguments
    parse_args "$@"

    # Check prerequisites
    check_prerequisites

    # Create backup
    create_backup

    # Validate package.json
    validate_package_json

    # Run operations
    fix_common_issues
    optimize_package_json
    remove_unused_dependencies
    update_dependencies
    run_security_audit
    clean_install

    # Generate report
    generate_report

    log "INFO" "Package.json patching completed successfully"

    if [[ "$DRY_RUN" == "true" ]]; then
        log "INFO" "This was a dry run. No changes were made."
    fi
}

# Run main function with all arguments
main "$@"
