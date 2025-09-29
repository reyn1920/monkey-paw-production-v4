#!/bin/bash

# href_fix.sh - Fix broken href references in HTML and template files
# Part of the Trae AI Cleanup Framework

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_FILE="$PROJECT_ROOT/tools/cleanup/href_fix.log"
BACKUP_DIR="$PROJECT_ROOT/tools/cleanup/backups/href_$(date +%Y%m%d_%H%M%S)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

# Usage function
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Fix broken href references in HTML and template files.

Options:
    -h, --help          Show this help message
    -d, --dry-run       Show what would be fixed without making changes
    -b, --backup        Create backup before making changes (default: true)
    --no-backup         Skip backup creation
    -v, --verbose       Enable verbose output
    -f, --fix-all       Fix all detected issues automatically
    --target-dir DIR    Target directory to scan (default: project root)
    --extensions EXTS   File extensions to scan (default: html,htm,php,twig,vue,jsx,tsx)

Examples:
    $0 --dry-run                    # Show what would be fixed
    $0 --fix-all                    # Fix all issues automatically
    $0 --target-dir ./templates     # Scan only templates directory
    $0 --extensions "html,php"      # Scan only HTML and PHP files

EOF
}

# Default options
DRY_RUN=false
CREATE_BACKUP=true
VERBOSE=false
FIX_ALL=false
TARGET_DIR="$PROJECT_ROOT"
EXTENSIONS="html,htm,php,twig,vue,jsx,tsx"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -b|--backup)
            CREATE_BACKUP=true
            shift
            ;;
        --no-backup)
            CREATE_BACKUP=false
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--fix-all)
            FIX_ALL=true
            shift
            ;;
        --target-dir)
            TARGET_DIR="$2"
            shift 2
            ;;
        --extensions)
            EXTENSIONS="$2"
            shift 2
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Initialize
log_info "Starting href fix process..."
log_info "Target directory: $TARGET_DIR"
log_info "Extensions: $EXTENSIONS"
log_info "Dry run: $DRY_RUN"
log_info "Create backup: $CREATE_BACKUP"

# Create backup directory if needed
if [[ "$CREATE_BACKUP" == "true" && "$DRY_RUN" == "false" ]]; then
    mkdir -p "$BACKUP_DIR"
    log_info "Backup directory created: $BACKUP_DIR"
fi

# Statistics
FILES_SCANNED=0
FILES_WITH_ISSUES=0
ISSUES_FOUND=0
ISSUES_FIXED=0

# Function to check if file exists
check_file_exists() {
    local file_path="$1"
    local base_dir="$2"

    # Handle different types of paths
    if [[ "$file_path" =~ ^https?://]]; then
        # External URL - skip for now
        return 1
    elif [[ "$file_path" =~ ^mailto: ]]; then
        # Email link - skip
        return 1
    elif [[ "$file_path" =~ ^tel: ]]; then
        # Phone link - skip
        return 1
    elif [[ "$file_path" =~ ^# ]]; then
        # Anchor link - skip
        return 1
    elif [[ "$file_path" =~ ^/]]; then
        # Absolute path from root
        local full_path="$PROJECT_ROOT$file_path"
    else
        # Relative path
        local full_path="$base_dir/$file_path"
    fi

    [[ -f "$full_path" ]]
}

# Function to suggest fix for broken href
suggest_href_fix() {
    local broken_href="$1"
    local file_dir="$2"

    # Try to find similar files
    local basename=$(basename "$broken_href")
    local dirname=$(dirname "$broken_href")

    # Search for files with similar names
    local suggestions=()
    while IFS= read -r -d '' file; do
        local rel_path=$(realpath --relative-to="$file_dir" "$file")
        suggestions+=("$rel_path")
    done < <(find "$PROJECT_ROOT" -name "*$basename*" -type f -print0 2>/dev/null | head -5)

    if [[ ${#suggestions[@]} -gt 0 ]]; then
        echo "Possible fixes:"
        for i in "${!suggestions[@]}"; do
            echo "  $((i+1)). ${suggestions[$i]}"
        done
        echo "${suggestions[0]}"  # Return first suggestion
    else
        echo "No suggestions found"
        echo ""
    fi
}

# Function to fix href in file
fix_href_in_file() {
    local file="$1"
    local old_href="$2"
    local new_href="$3"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would fix: $old_href -> $new_href in $file"
        return 0
    fi

    # Create backup if requested
    if [[ "$CREATE_BACKUP" == "true" ]]; then
        local backup_file="$BACKUP_DIR/$(basename "$file").backup"
        cp "$file" "$backup_file"
    fi

    # Use sed to replace the href
    if sed -i.tmp "s|href=\"$old_href\"|href=\"$new_href\"|g" "$file" && rm "$file.tmp"; then
        log_success "Fixed: $old_href -> $new_href in $file"
        ((ISSUES_FIXED++))
        return 0
    else
        log_error "Failed to fix: $old_href in $file"
        return 1
    fi
}

# Function to scan file for broken hrefs
scan_file_for_hrefs() {
    local file="$1"
    local file_dir=$(dirname "$file")
    local file_has_issues=false

    ((FILES_SCANNED++))

    if [[ "$VERBOSE" == "true" ]]; then
        log_info "Scanning: $file"
    fi

    # Extract all href attributes
    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            local href=$(echo "$line" | sed -n 's/.*href="\([^"]*\)".*/\1/p')
            if [[ -n "$href" ]]; then
                if ! check_file_exists "$href" "$file_dir"; then
                    ((ISSUES_FOUND++))
                    file_has_issues=true

                    log_warning "Broken href found in $file: $href"

                    if [[ "$FIX_ALL" == "true" ]]; then
                        local suggestion=$(suggest_href_fix "$href" "$file_dir" | tail -1)
                        if [[ -n "$suggestion" && "$suggestion" != "No suggestions found" ]]; then
                            fix_href_in_file "$file" "$href" "$suggestion"
                        fi
                    else
                        suggest_href_fix "$href" "$file_dir" >/dev/null
                    fi
                fi
            fi
        fi
    done < <(grep -n 'href="[^"]*"' "$file" 2>/dev/null || true)

    if [[ "$file_has_issues" == "true" ]]; then
        ((FILES_WITH_ISSUES++))
    fi
}

# Main scanning function
scan_for_broken_hrefs() {
    log_info "Scanning for broken href references..."

    # Convert extensions to find pattern
    local find_pattern=""
    IFS=',' read -ra EXT_ARRAY <<< "$EXTENSIONS"
    for ext in "${EXT_ARRAY[@]}"; do
        if [[ -n "$find_pattern" ]]; then
            find_pattern="$find_pattern -o"
        fi
        find_pattern="$find_pattern -name \"*.$ext\""
    done

    # Find and scan files
    local find_cmd="find \"$TARGET_DIR\" -type f \( $find_pattern \) -not -path '*/node_modules/*' -not -path '*/venv/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/build/*'"

    while IFS= read -r -d '' file; do
        scan_file_for_hrefs "$file"
    done < <(eval "$find_cmd -print0")
}

# Function to generate report
generate_report() {
    log_info "=== HREF FIX REPORT ==="
    log_info "Files scanned: $FILES_SCANNED"
    log_info "Files with issues: $FILES_WITH_ISSUES"
    log_info "Issues found: $ISSUES_FOUND"
    log_info "Issues fixed: $ISSUES_FIXED"

    if [[ $ISSUES_FOUND -gt 0 && $ISSUES_FIXED -eq 0 && "$DRY_RUN" == "false" ]]; then
        log_warning "Issues found but not fixed. Run with --fix-all to auto-fix or manually review."
    elif [[ $ISSUES_FOUND -eq 0 ]]; then
        log_success "No broken href references found!"
    elif [[ "$DRY_RUN" == "true" ]]; then
        log_info "Dry run completed. Run without --dry-run to apply fixes."
    fi
}

# Main execution
main() {
    # Validate target directory
    if [[ ! -d "$TARGET_DIR" ]]; then
        log_error "Target directory does not exist: $TARGET_DIR"
        exit 1
    fi

    # Run the scan
    scan_for_broken_hrefs

    # Generate report
    generate_report

    # Exit with appropriate code
    if [[ $ISSUES_FOUND -gt 0 && $ISSUES_FIXED -lt $ISSUES_FOUND ]]; then
        exit 1
    else
        exit 0
    fi
}

# Run main function
main "$@"
