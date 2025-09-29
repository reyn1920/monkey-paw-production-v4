#!/bin/bash

# Persistence Guard - Critical File Protection System
# Protects essential project files from accidental deletion or modification
# Usage: ./persist_guard.sh [--check] [--restore] [--backup]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKUP_DIR="$PROJECT_ROOT/.trae/backups"
LOG_FILE="$PROJECT_ROOT/.trae/persist_guard.log"
CHECKSUM_FILE="$PROJECT_ROOT/.trae/checksums.txt"

# Protected files and directories
PROTECTED_ITEMS=(
    "TRAE_RULES.md"
    "CHECKPOINT_TRAE_RULES_2025-08-28.md"
    ".base44rc.json"
    "run_rules_check.sh"
    "tools/dnd/"
    "tools/audits/rule1_scan.py"
    "tools/audits/persist_guard.sh"
    "tools/start_local.py"
    ".trae/"
    ".gitignore"
    "requirements.txt"
)

# Critical system files that should never be modified
CRITICAL_FILES=(
    "tools/dnd/DO_NOT_DELETE.txt"
    ".trae/rules/"
)

# Parse command line arguments
MODE="check"
while [[ $# -gt 0 ]]; do
    case $1 in
        --check)
            MODE="check"
            shift
            ;;
        --restore)
            MODE="restore"
            shift
            ;;
        --backup)
            MODE="backup"
            shift
            ;;
        --install)
            MODE="install"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--check] [--restore] [--backup] [--install]"
            echo "  --check    Verify integrity of protected files (default)"
            echo "  --restore  Restore files from backup"
            echo "  --backup   Create backup of protected files"
            echo "  --install  Install file system watchers"
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
    echo -e "${BLUE}[GUARD]${NC} $1"
    echo "$(date): [INFO] $1" >> "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[GUARD]${NC} $1"
    echo "$(date): [SUCCESS] $1" >> "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[GUARD]${NC} $1"
    echo "$(date): [WARNING] $1" >> "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[GUARD]${NC} $1"
    echo "$(date): [ERROR] $1" >> "$LOG_FILE"
}

# Initialize directories
init_directories() {
    mkdir -p "$BACKUP_DIR"
    mkdir -p "$PROJECT_ROOT/.trae/rules"
    mkdir -p "$PROJECT_ROOT/tools/dnd"
    touch "$LOG_FILE"
}

# Generate checksums for protected files
generate_checksums() {
    log_info "Generating checksums for protected files..."
    > "$CHECKSUM_FILE"

    for item in "${PROTECTED_ITEMS[@]}"; do
        local full_path="$PROJECT_ROOT/$item"
        if [ -f "$full_path" ]; then
            local checksum=$(shasum -a 256 "$full_path" | cut -d' ' -f1)
            echo "$checksum  $item" >> "$CHECKSUM_FILE"
            log_info "Checksum generated for: $item"
        elif [ -d "$full_path" ]; then
            # For directories, checksum all files recursively
            find "$full_path" -type f -exec shasum -a 256 {} \; | while read checksum file; do
                local rel_path=$(echo "$file" | sed "s|$PROJECT_ROOT/||")
                echo "$checksum  $rel_path" >> "$CHECKSUM_FILE"
            done
            log_info "Directory checksums generated for: $item"
        else
            log_warning "Protected item not found: $item"
        fi
    done
}

# Verify file integrity
verify_integrity() {
    log_info "Verifying integrity of protected files..."
    local violations=0

    if [ ! -f "$CHECKSUM_FILE" ]; then
        log_warning "Checksum file not found, generating new checksums..."
        generate_checksums
        return 0
    fi

    while IFS= read -r line; do
        if [ -z "$line" ]; then continue; fi

        local expected_checksum=$(echo "$line" | cut -d' ' -f1)
        local file_path=$(echo "$line" | cut -d' ' -f3-)
        local full_path="$PROJECT_ROOT/$file_path"

        if [ -f "$full_path" ]; then
            local current_checksum=$(shasum -a 256 "$full_path" | cut -d' ' -f1)
            if [ "$expected_checksum" != "$current_checksum" ]; then
                log_error "Integrity violation detected: $file_path"
                log_error "Expected: $expected_checksum"
                log_error "Current:  $current_checksum"
                ((violations++))
            else
                log_success "Integrity verified: $file_path"
            fi
        else
            log_error "Protected file missing: $file_path"
            ((violations++))
        fi
    done < "$CHECKSUM_FILE"

    if [ $violations -gt 0 ]; then
        log_error "$violations integrity violations detected!"
        return 1
    else
        log_success "All protected files verified successfully"
        return 0
    fi
}

# Create backup of protected files
create_backup() {
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local backup_path="$BACKUP_DIR/backup_$timestamp"

    log_info "Creating backup at: $backup_path"
    mkdir -p "$backup_path"

    for item in "${PROTECTED_ITEMS[@]}"; do
        local full_path="$PROJECT_ROOT/$item"
        if [ -e "$full_path" ]; then
            local item_backup="$backup_path/$item"
            mkdir -p "$(dirname "$item_backup")"
            cp -r "$full_path" "$item_backup"
            log_success "Backed up: $item"
        else
            log_warning "Item not found for backup: $item"
        fi
    done

    # Copy checksums
    if [ -f "$CHECKSUM_FILE" ]; then
        cp "$CHECKSUM_FILE" "$backup_path/checksums.txt"
    fi

    log_success "Backup completed: $backup_path"

    # Clean old backups (keep last 10)
    local backup_count=$(ls -1 "$BACKUP_DIR" | grep "^backup_" | wc -l)
    if [ $backup_count -gt 10 ]; then
        log_info "Cleaning old backups..."
        ls -1t "$BACKUP_DIR" | grep "^backup_" | tail -n +11 | while read old_backup; do
            rm -rf "$BACKUP_DIR/$old_backup"
            log_info "Removed old backup: $old_backup"
        done
    fi
}

# Restore files from backup
restore_backup() {
    log_info "Available backups:"
    ls -1t "$BACKUP_DIR" | grep "^backup_" | head -5

    echo "Enter backup name to restore (or 'latest' for most recent):"
    read -r backup_name

    if [ "$backup_name" = "latest" ]; then
        backup_name=$(ls -1t "$BACKUP_DIR" | grep "^backup_" | head -1)
    fi

    local backup_path="$BACKUP_DIR/$backup_name"

    if [ ! -d "$backup_path" ]; then
        log_error "Backup not found: $backup_name"
        return 1
    fi

    log_warning "This will overwrite current files. Continue? (y/N)"
    read -r confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        log_info "Restore cancelled"
        return 0
    fi

    log_info "Restoring from backup: $backup_name"

    for item in "${PROTECTED_ITEMS[@]}"; do
        local backup_item="$backup_path/$item"
        local target_item="$PROJECT_ROOT/$item"

        if [ -e "$backup_item" ]; then
            mkdir -p "$(dirname "$target_item")"
            cp -r "$backup_item" "$target_item"
            log_success "Restored: $item"
        fi
    done

    # Restore checksums
    if [ -f "$backup_path/checksums.txt" ]; then
        cp "$backup_path/checksums.txt" "$CHECKSUM_FILE"
        log_success "Checksums restored"
    fi

    log_success "Restore completed from: $backup_name"
}

# Install file system watchers (if fswatch is available)
install_watchers() {
    if ! command -v fswatch >/dev/null 2>&1; then
        log_warning "fswatch not available. Install with: brew install fswatch"
        return 1
    fi

    log_info "Installing file system watchers..."

    # Create watcher script
    cat > "$PROJECT_ROOT/.trae/file_watcher.sh" << 'EOF'
#!/bin/bash
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../" && pwd)"
echo "$(date): File change detected: $1" >> "$PROJECT_ROOT/.trae/file_changes.log"
"$PROJECT_ROOT/tools/audits/persist_guard.sh" --check
EOF

    chmod +x "$PROJECT_ROOT/.trae/file_watcher.sh"

    # Start background watcher
    nohup fswatch -o "${PROTECTED_ITEMS[@]/#/$PROJECT_ROOT/}" | while read; do
        "$PROJECT_ROOT/.trae/file_watcher.sh"
    done > "$PROJECT_ROOT/.trae/watcher.log" 2>&1 &

    echo $! > "$PROJECT_ROOT/.trae/watcher.pid"
    log_success "File system watcher installed (PID: $!)"
}

# Main execution
init_directories

case $MODE in
    "check")
        verify_integrity
        ;;
    "backup")
        create_backup
        generate_checksums
        ;;
    "restore")
        restore_backup
        ;;
    "install")
        install_watchers
        ;;
    *)
        log_error "Unknown mode: $MODE"
        exit 1
        ;;
esac
