#!/bin/bash

# TRAE.AI Cron Management Script
# Handles automated tasks, monitoring, and maintenance
# Version: 1.0
# Author: TRAE.AI System

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_ROOT/logs"
CRON_LOG="$LOG_DIR/cron.log"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" | tee -a "$CRON_LOG"
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

# Health monitoring task
health_monitor() {
    log_info "Starting health monitoring task"

    cd "$PROJECT_ROOT"

    # Check if dashboard is running
    local dashboard_port=${DASHBOARD_PORT:-8083}
    if curl -s "http://127.0.0.1:$dashboard_port/api/status" >/dev/null 2>&1; then
        log_success "Dashboard health check passed"
    else
        log_error "Dashboard health check failed"
        # Attempt to restart dashboard
        log_info "Attempting to restart dashboard"
        if [[ -f "$PROJECT_ROOT/scripts/phoenix_protocol.sh" ]]; then
            bash "$PROJECT_ROOT/scripts/phoenix_protocol.sh" deploy >> "$CRON_LOG" 2>&1
            log_info "Dashboard restart attempted"
        fi
    fi

    # Check disk space
    local disk_usage
    disk_usage=$(df "$PROJECT_ROOT" | awk 'NR==2 {print $5}' | sed 's/%//')

    if [[ $disk_usage -lt 80 ]]; then
        log_success "Disk usage OK: ${disk_usage}%"
    elif [[ $disk_usage -lt 90 ]]; then
        log_warn "Disk usage warning: ${disk_usage}%"
    else
        log_error "Disk usage critical: ${disk_usage}%"
        # Trigger cleanup
        cleanup_logs
        cleanup_backups
    fi

    # Check memory usage
    if command_exists "free"; then
        local memory_usage
        memory_usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2 }')

        if [[ $memory_usage -lt 80 ]]; then
            log_success "Memory usage OK: ${memory_usage}%"
        elif [[ $memory_usage -lt 90 ]]; then
            log_warn "Memory usage warning: ${memory_usage}%"
        else
            log_error "Memory usage critical: ${memory_usage}%"
        fi
    fi

    log_info "Health monitoring task completed"
}

# Log cleanup task
cleanup_logs() {
    log_info "Starting log cleanup task"

    # Remove logs older than 30 days
    find "$LOG_DIR" -name "*.log" -type f -mtime +30 -delete 2>/dev/null || true

    # Keep only last 100 lines of main log files
    for log_file in "$LOG_DIR"/*.log; do
        if [[ -f "$log_file" && $(wc -l < "$log_file") -gt 1000 ]]; then
            tail -n 1000 "$log_file" > "${log_file}.tmp"
            mv "${log_file}.tmp" "$log_file"
            log_info "Truncated log file: $(basename "$log_file")"
        fi
    done

    log_success "Log cleanup completed"
}

# Backup cleanup task
cleanup_backups() {
    log_info "Starting backup cleanup task"

    local backup_dir="$PROJECT_ROOT/backups"

    if [[ -d "$backup_dir" ]]; then
        # Keep only last 10 backups
        local backup_count
        backup_count=$(find "$backup_dir" -maxdepth 1 -type d -name "backup_*" | wc -l)

        if [[ $backup_count -gt 10 ]]; then
            log_info "Cleaning up old backups (keeping 10 most recent)"
            find "$backup_dir" -maxdepth 1 -type d -name "backup_*" -printf '%T@ %p\n' 2>/dev/null | \
                sort -n | head -n -10 | cut -d' ' -f2- | xargs rm -rf 2>/dev/null || true
            log_success "Backup cleanup completed"
        else
            log_info "No backup cleanup needed ($backup_count backups)"
        fi
    else
        log_info "No backup directory found"
    fi
}

# Security scan task
security_scan() {
    log_info "Starting security scan task"

    cd "$PROJECT_ROOT"

    # Run security scanner if available
    if [[ -f "backend/security/security_scanner.py" ]]; then
        log_info "Running security scanner"

        local scan_output="$LOG_DIR/security_scan_cron_$TIMESTAMP.json"

        if python3 backend/security/security_scanner.py --target . --output "$scan_output" >> "$CRON_LOG" 2>&1; then
            log_success "Security scan completed successfully"
        else
            log_warn "Security scan completed with warnings"
        fi
    else
        log_warn "Security scanner not available"
    fi

    # Run compliance validator if available
    if [[ -f "backend/security/compliance_validator.py" ]]; then
        log_info "Running compliance validation"

        local compliance_output="$LOG_DIR/compliance_cron_$TIMESTAMP.json"

        if python3 backend/security/compliance_validator.py --base-dir . --output "$compliance_output" >> "$CRON_LOG" 2>&1; then
            log_success "Compliance validation passed"
        else
            log_error "Compliance validation failed"
        fi
    else
        log_warn "Compliance validator not available"
    fi

    log_info "Security scan task completed"
}

# Database maintenance task
database_maintenance() {
    log_info "Starting database maintenance task"

    cd "$PROJECT_ROOT"

    # Check main database
    if [[ -f "trae_ai.db" ]]; then
        local db_size
        db_size=$(du -h "trae_ai.db" | cut -f1)
        log_info "Main database size: $db_size"

        # Run VACUUM if database is large
        if command_exists "sqlite3"; then
            log_info "Running database VACUUM"
            sqlite3 "trae_ai.db" "VACUUM;" 2>/dev/null || log_warn "Database VACUUM failed"
            log_success "Database maintenance completed"
        fi
    else
        log_warn "Main database not found"
    fi

    # Check intelligence database
    if [[ -f "right_perspective.db" ]]; then
        local db_size
        db_size=$(du -h "right_perspective.db" | cut -f1)
        log_info "Intelligence database size: $db_size"

        if command_exists "sqlite3"; then
            log_info "Running intelligence database VACUUM"
            sqlite3 "right_perspective.db" "VACUUM;" 2>/dev/null || log_warn "Intelligence database VACUUM failed"
        fi
    fi

    log_info "Database maintenance task completed"
}

# Asset processing task
asset_processing() {
    log_info "Starting asset processing task"

    cd "$PROJECT_ROOT"

    local incoming_dir="assets/incoming"
    local releases_dir="assets/releases"

    if [[ -d "$incoming_dir" ]]; then
        local file_count
        file_count=$(find "$incoming_dir" -type f | wc -l)

        if [[ $file_count -gt 0 ]]; then
            log_info "Found $file_count files in incoming directory"

            # Run synthesizer if available
            if [[ -f "scripts/synthesize_release_v3.py" ]]; then
                log_info "Running release synthesizer"

                if python3 scripts/synthesize_release_v3.py --input-dir "$incoming_dir" --output-dir "$releases_dir" >> "$CRON_LOG" 2>&1; then
                    log_success "Asset processing completed"
                else
                    log_error "Asset processing failed"
                fi
            else
                log_warn "Release synthesizer not available"
            fi
        else
            log_info "No files to process in incoming directory"
        fi
    else
        log_warn "Incoming assets directory not found"
    fi

    log_info "Asset processing task completed"
}

# System metrics collection
collect_metrics() {
    log_info "Starting metrics collection task"

    cd "$PROJECT_ROOT"

    local metrics_file="$LOG_DIR/metrics_$TIMESTAMP.json"

    # Collect system metrics
    cat > "$metrics_file" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "system": {
        "uptime": "$(uptime | awk '{print $3,$4}' | sed 's/,//')",
        "load_average": "$(uptime | awk -F'load average:' '{print $2}' | xargs)",
        "disk_usage": "$(df "$PROJECT_ROOT" | awk 'NR==2 {print $5}' | sed 's/%//')%",
        "memory_usage": "$(free 2>/dev/null | awk 'NR==2{printf "%.0f%%", $3*100/$2 }' || echo 'N/A')"
    },
    "project": {
        "root": "$PROJECT_ROOT",
        "log_files": $(find "$LOG_DIR" -name "*.log" | wc -l),
        "backup_count": $(find "$PROJECT_ROOT/backups" -maxdepth 1 -type d -name "backup_*" 2>/dev/null | wc -l || echo 0),
        "database_exists": $([ -f "trae_ai.db" ] && echo true || echo false),
        "dashboard_responsive": $(curl -s "http://127.0.0.1:${DASHBOARD_PORT:-8083}/api/status" >/dev/null 2>&1 && echo true || echo false)
    }
}
EOF

    log_success "Metrics collected: $metrics_file"
    log_info "Metrics collection task completed"
}

# Install cron jobs
install_cron() {
    print_info "Installing TRAE.AI cron jobs"

    local cron_script="$SCRIPT_DIR/cron.sh"
    local temp_cron="/tmp/trae_cron_$$"

    # Get current crontab (if any)
    crontab -l 2>/dev/null > "$temp_cron" || touch "$temp_cron"

    # Remove existing TRAE.AI cron jobs
    grep -v "# TRAE.AI" "$temp_cron" > "${temp_cron}.clean" || touch "${temp_cron}.clean"
    mv "${temp_cron}.clean" "$temp_cron"

    # Add new cron jobs
    cat >> "$temp_cron" << EOF

# TRAE.AI System Maintenance Jobs
# Health monitoring every 5 minutes
*/5 * * * * $cron_script health-monitor >> $CRON_LOG 2>&1 # TRAE.AI

# Log cleanup daily at 2 AM
0 2 * * * $cron_script cleanup-logs >> $CRON_LOG 2>&1 # TRAE.AI

# Backup cleanup weekly on Sunday at 3 AM
0 3 * * 0 $cron_script cleanup-backups >> $CRON_LOG 2>&1 # TRAE.AI

# Security scan daily at 1 AM
0 1 * * * $cron_script security-scan >> $CRON_LOG 2>&1 # TRAE.AI

# Database maintenance weekly on Monday at 4 AM
0 4 * * 1 $cron_script database-maintenance >> $CRON_LOG 2>&1 # TRAE.AI

# Asset processing every 15 minutes
*/15 * * * * $cron_script asset-processing >> $CRON_LOG 2>&1 # TRAE.AI

# Metrics collection hourly
0 * * * * $cron_script collect-metrics >> $CRON_LOG 2>&1 # TRAE.AI
EOF

    # Install the new crontab
    if crontab "$temp_cron"; then
        print_success "Cron jobs installed successfully"
        log_success "Cron jobs installed"
    else
        print_error "Failed to install cron jobs"
        log_error "Failed to install cron jobs"
        rm -f "$temp_cron"
        return 1
    fi

    rm -f "$temp_cron"

    # Show installed cron jobs
    print_info "Installed cron jobs:"
    crontab -l | grep "# TRAE.AI" | while read -r line; do
        echo "  $line"
    done
}

# Remove cron jobs
remove_cron() {
    print_info "Removing TRAE.AI cron jobs"

    local temp_cron="/tmp/trae_cron_$$"

    # Get current crontab
    if crontab -l 2>/dev/null > "$temp_cron"; then
        # Remove TRAE.AI cron jobs
        grep -v "# TRAE.AI" "$temp_cron" > "${temp_cron}.clean" || touch "${temp_cron}.clean"

        # Install cleaned crontab
        if crontab "${temp_cron}.clean"; then
            print_success "TRAE.AI cron jobs removed"
            log_success "Cron jobs removed"
        else
            print_error "Failed to remove cron jobs"
            log_error "Failed to remove cron jobs"
        fi

        rm -f "$temp_cron" "${temp_cron}.clean"
    else
        print_info "No existing crontab found"
    fi
}

# Show cron status
show_cron_status() {
    print_info "TRAE.AI Cron Job Status"
    echo

    if crontab -l 2>/dev/null | grep -q "# TRAE.AI"; then
        print_success "TRAE.AI cron jobs are installed"
        echo
        print_info "Active cron jobs:"
        crontab -l | grep "# TRAE.AI" | while read -r line; do
            echo "  $line"
        done
    else
        print_warning "No TRAE.AI cron jobs found"
    fi

    echo
    print_info "Recent cron log entries:"
    if [[ -f "$CRON_LOG" ]]; then
        tail -n 10 "$CRON_LOG" | while read -r line; do
            echo "  $line"
        done
    else
        print_warning "No cron log file found"
    fi
}

# Show usage
usage() {
    cat << EOF
TRAE.AI Cron Management Script

Usage: $0 <command>

Commands:
  health-monitor        Run health monitoring task
  cleanup-logs          Run log cleanup task
  cleanup-backups       Run backup cleanup task
  security-scan         Run security scan task
  database-maintenance  Run database maintenance task
  asset-processing      Run asset processing task
  collect-metrics       Run metrics collection task

  install-cron          Install all cron jobs
  remove-cron           Remove all TRAE.AI cron jobs
  status                Show cron job status

Examples:
  $0 health-monitor     # Run health monitoring
  $0 install-cron       # Install cron jobs
  $0 status             # Show cron status

Logs are saved to: $CRON_LOG

EOF
}

# Main execution
main() {
    local command="${1:-}"

    # Create log entry for script execution
    log_info "Cron script started with command: ${command:-'none'}"
    log_info "Project root: $PROJECT_ROOT"
    log_info "Cron log: $CRON_LOG"

    case "$command" in
        "health-monitor")
            health_monitor
            ;;
        "cleanup-logs")
            cleanup_logs
            ;;
        "cleanup-backups")
            cleanup_backups
            ;;
        "security-scan")
            security_scan
            ;;
        "database-maintenance")
            database_maintenance
            ;;
        "asset-processing")
            asset_processing
            ;;
        "collect-metrics")
            collect_metrics
            ;;
        "install-cron")
            install_cron
            ;;
        "remove-cron")
            remove_cron
            ;;
        "status")
            show_cron_status
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

    log_info "Cron script completed for command: $command"
}

# Make script executable
chmod +x "$0" 2>/dev/null || true

# Execute main function with all arguments
main "$@"
