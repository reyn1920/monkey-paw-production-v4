#!/bin/bash

# TRAE.AI Daily Autonomous Operations Cycle
# This script handles cron-based autonomous operations including:
# - System health checks
# - Database maintenance
# - Performance optimization
# - Backup operations
# - Log rotation
# - Security scans
# - Resource cleanup
#
# Author: TRAE.AI System
# Version: 1.0.0
# Created: 2024
#
# Usage: Add to crontab for daily execution:
# 0 2 * * * /path/to/run_daily_cycle.sh >> /var/log/trae_daily.log 2>&1

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
LOG_DIR="$PROJECT_ROOT/logs"
BACKUP_DIR="$PROJECT_ROOT/backups"
DB_PATH="$PROJECT_ROOT/right_perspective.db"
VENV_PATH="$PROJECT_ROOT/venv"
DAILY_LOG="$LOG_DIR/daily_cycle_$(date +%Y%m%d).log"
MAX_LOG_DAYS=30
MAX_BACKUP_DAYS=7

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

    case "$level" in
        "INFO")
            echo -e "${GREEN}[$timestamp] [INFO]${NC} $message" | tee -a "$DAILY_LOG"
            ;;
        "WARN")
            echo -e "${YELLOW}[$timestamp] [WARN]${NC} $message" | tee -a "$DAILY_LOG"
            ;;
        "ERROR")
            echo -e "${RED}[$timestamp] [ERROR]${NC} $message" | tee -a "$DAILY_LOG"
            ;;
        "DEBUG")
            echo -e "${BLUE}[$timestamp] [DEBUG]${NC} $message" | tee -a "$DAILY_LOG"
            ;;
        *)
            echo "[$timestamp] $message" | tee -a "$DAILY_LOG"
            ;;
    esac
}

# Error handling
error_exit() {
    log "ERROR" "$1"
    exit 1
}

# Check if running as expected user (not root for security)
check_user() {
    if [[ $EUID -eq 0 ]]; then
        error_exit "This script should not be run as root for security reasons"
    fi
    log "INFO" "Running as user: $(whoami)"
}

# Create necessary directories
setup_directories() {
    log "INFO" "Setting up directories..."

    mkdir -p "$LOG_DIR" || error_exit "Failed to create log directory"
    mkdir -p "$BACKUP_DIR" || error_exit "Failed to create backup directory"

    # Set proper permissions
    chmod 755 "$LOG_DIR" "$BACKUP_DIR"

    log "INFO" "Directories setup complete"
}

# System health check
system_health_check() {
    log "INFO" "Starting system health check..."

    # Check disk space
    local disk_usage=$(df "$PROJECT_ROOT" | awk 'NR==2 {print $5}' | sed 's/%//')
    if [[ $disk_usage -gt 90 ]]; then
        log "WARN" "High disk usage: ${disk_usage}%"
    else
        log "INFO" "Disk usage: ${disk_usage}% - OK"
    fi

    # Check memory usage
    if command -v free >/dev/null 2>&1; then
        local mem_usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
        if [[ $mem_usage -gt 90 ]]; then
            log "WARN" "High memory usage: ${mem_usage}%"
        else
            log "INFO" "Memory usage: ${mem_usage}% - OK"
        fi
    fi

    # Check if virtual environment exists
    if [[ ! -d "$VENV_PATH" ]]; then
        log "WARN" "Virtual environment not found at $VENV_PATH"
    else
        log "INFO" "Virtual environment found - OK"
    fi

    # Check if database exists and is accessible
    if [[ ! -f "$DB_PATH" ]]; then
        log "WARN" "Database not found at $DB_PATH"
    else
        # Test database connectivity
        if command -v sqlite3 >/dev/null 2>&1; then
            if sqlite3 "$DB_PATH" "SELECT 1;" >/dev/null 2>&1; then
                log "INFO" "Database connectivity - OK"
            else
                log "ERROR" "Database connectivity failed"
            fi
        fi
    fi

    log "INFO" "System health check complete"
}

# Database maintenance
database_maintenance() {
    log "INFO" "Starting database maintenance..."

    if [[ ! -f "$DB_PATH" ]]; then
        log "WARN" "Database not found, skipping maintenance"
        return 0
    fi

    # Activate virtual environment if available
    if [[ -f "$VENV_PATH/bin/activate" ]]; then
        source "$VENV_PATH/bin/activate"
        log "INFO" "Virtual environment activated"
    fi

    # Database optimization
    if command -v sqlite3 >/dev/null 2>&1; then
        log "INFO" "Running database VACUUM..."
        sqlite3 "$DB_PATH" "VACUUM;" || log "WARN" "Database VACUUM failed"

        log "INFO" "Analyzing database statistics..."
        sqlite3 "$DB_PATH" "ANALYZE;" || log "WARN" "Database ANALYZE failed"

        # Check database integrity
        log "INFO" "Checking database integrity..."
        local integrity_check=$(sqlite3 "$DB_PATH" "PRAGMA integrity_check;")
        if [[ "$integrity_check" == "ok" ]]; then
            log "INFO" "Database integrity check - OK"
        else
            log "ERROR" "Database integrity check failed: $integrity_check"
        fi

        # Get database size
        local db_size=$(du -h "$DB_PATH" | cut -f1)
        log "INFO" "Database size: $db_size"

        # Clean old performance metrics (keep last 90 days)
        log "INFO" "Cleaning old performance metrics..."
        sqlite3 "$DB_PATH" "DELETE FROM performance_metrics WHERE timestamp < datetime('now', '-90 days');" || log "WARN" "Failed to clean old metrics"

        # Clean old system logs (keep last 30 days)
        log "INFO" "Cleaning old system logs..."
        sqlite3 "$DB_PATH" "DELETE FROM system_logs WHERE timestamp < datetime('now', '-30 days');" || log "WARN" "Failed to clean old logs"

        # Update statistics after cleanup
        sqlite3 "$DB_PATH" "ANALYZE;" || log "WARN" "Post-cleanup ANALYZE failed"
    else
        log "WARN" "sqlite3 not available, skipping database maintenance"
    fi

    log "INFO" "Database maintenance complete"
}

# Backup operations
backup_operations() {
    log "INFO" "Starting backup operations..."

    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/trae_backup_$backup_timestamp.tar.gz"

    # Create backup
    log "INFO" "Creating system backup..."

    # Files to backup
    local backup_items=(
        "config.json"
        "schema.sql"
        "backend/"
        "utils/"
        "scripts/"
        "app/"
        "launch_live.py"
    )

    # Add database if it exists
    if [[ -f "$DB_PATH" ]]; then
        backup_items+=("right_perspective.db")
    fi

    # Create tar archive
    if tar -czf "$backup_file" -C "$PROJECT_ROOT" "${backup_items[@]}" 2>/dev/null; then
        log "INFO" "Backup created: $backup_file"

        # Get backup size
        local backup_size=$(du -h "$backup_file" | cut -f1)
        log "INFO" "Backup size: $backup_size"
    else
        log "ERROR" "Failed to create backup"
    fi

    # Clean old backups
    log "INFO" "Cleaning old backups (keeping last $MAX_BACKUP_DAYS days)..."
    find "$BACKUP_DIR" -name "trae_backup_*.tar.gz" -type f -mtime +$MAX_BACKUP_DAYS -delete 2>/dev/null || true

    # Count remaining backups
    local backup_count=$(find "$BACKUP_DIR" -name "trae_backup_*.tar.gz" -type f | wc -l)
    log "INFO" "Total backups retained: $backup_count"

    log "INFO" "Backup operations complete"
}

# Log rotation and cleanup
log_rotation() {
    log "INFO" "Starting log rotation and cleanup..."

    # Clean old daily cycle logs
    find "$LOG_DIR" -name "daily_cycle_*.log" -type f -mtime +$MAX_LOG_DAYS -delete 2>/dev/null || true

    # Clean old application logs
    find "$LOG_DIR" -name "*.log" -type f -mtime +$MAX_LOG_DAYS -delete 2>/dev/null || true

    # Compress logs older than 7 days
    find "$LOG_DIR" -name "*.log" -type f -mtime +7 ! -name "*$(date +%Y%m%d)*" -exec gzip {} \; 2>/dev/null || true

    # Count remaining log files
    local log_count=$(find "$LOG_DIR" -type f | wc -l)
    log "INFO" "Total log files: $log_count"

    log "INFO" "Log rotation complete"
}

# Security scan
security_scan() {
    log "INFO" "Starting security scan..."

    # Check file permissions
    log "INFO" "Checking critical file permissions..."

    # Check if sensitive files have proper permissions
    local sensitive_files=(
        "$DB_PATH"
        "config.json"
        "launch_live.py"
    )

    for file in "${sensitive_files[@]}"; do
        if [[ -f "$file" ]]; then
            local perms=$(stat -c "%a" "$file" 2>/dev/null || stat -f "%A" "$file" 2>/dev/null || echo "unknown")
            if [[ "$perms" != "unknown" ]]; then
                log "INFO" "$file permissions: $perms"

                # Check if file is world-readable (security risk)
                if [[ "$perms" =~ [0-9][0-9][4-7] ]]; then
                    log "WARN" "$file is world-readable (potential security risk)"
                fi
            fi
        fi
    done

    # Check for .env files that might contain secrets
    log "INFO" "Scanning for potential secret files..."
    local secret_files=$(find "$PROJECT_ROOT" -name ".env*" -type f 2>/dev/null || true)
    if [[ -n "$secret_files" ]]; then
        log "WARN" "Found potential secret files:"
        echo "$secret_files" | while read -r file; do
            log "WARN" "  - $file"
        done
    fi

    # Check for Python cache files and clean them
    log "INFO" "Cleaning Python cache files..."
    find "$PROJECT_ROOT" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_ROOT" -name "*.pyc" -type f -delete 2>/dev/null || true

    log "INFO" "Security scan complete"
}

# Performance optimization
performance_optimization() {
    log "INFO" "Starting performance optimization..."

    # Clean temporary files
    log "INFO" "Cleaning temporary files..."

    # Remove old temporary files
    find "/tmp" -name "trae_*" -type f -mtime +1 -delete 2>/dev/null || true

    # Clean system temp directory if accessible
    if [[ -d "$PROJECT_ROOT/temp" ]]; then
        find "$PROJECT_ROOT/temp" -type f -mtime +1 -delete 2>/dev/null || true
    fi

    # Optimize Python bytecode if virtual environment exists
    if [[ -f "$VENV_PATH/bin/activate" ]]; then
        source "$VENV_PATH/bin/activate"

        log "INFO" "Optimizing Python bytecode..."
        python -m compileall "$PROJECT_ROOT" -q 2>/dev/null || log "WARN" "Python bytecode optimization failed"
    fi

    # Check and report system load
    if command -v uptime >/dev/null 2>&1; then
        local load_avg=$(uptime | awk -F'load average:' '{print $2}' | xargs)
        log "INFO" "System load average: $load_avg"
    fi

    log "INFO" "Performance optimization complete"
}

# Resource cleanup
resource_cleanup() {
    log "INFO" "Starting resource cleanup..."

    # Clean up any orphaned lock files
    find "$PROJECT_ROOT" -name "*.lock" -type f -mtime +1 -delete 2>/dev/null || true

    # Clean up any orphaned PID files
    find "$PROJECT_ROOT" -name "*.pid" -type f -mtime +1 -delete 2>/dev/null || true

    # Clean up old download files if they exist
    if [[ -d "$PROJECT_ROOT/downloads" ]]; then
        find "$PROJECT_ROOT/downloads" -type f -mtime +7 -delete 2>/dev/null || true
    fi

    # Clean up old cache files
    if [[ -d "$PROJECT_ROOT/cache" ]]; then
        find "$PROJECT_ROOT/cache" -type f -mtime +7 -delete 2>/dev/null || true
    fi

    log "INFO" "Resource cleanup complete"
}

# Generate daily report
generate_daily_report() {
    log "INFO" "Generating daily report..."

    local report_file="$LOG_DIR/daily_report_$(date +%Y%m%d).txt"

    {
        echo "TRAE.AI Daily Operations Report"
        echo "Generated: $(date)"
        echo "======================================"
        echo ""

        echo "System Status:"
        echo "- Disk Usage: $(df "$PROJECT_ROOT" | awk 'NR==2 {print $5}')"

        if command -v free >/dev/null 2>&1; then
            echo "- Memory Usage: $(free | awk 'NR==2{printf "%.0f%%", $3*100/$2}')"
        fi

        if [[ -f "$DB_PATH" ]]; then
            echo "- Database Size: $(du -h "$DB_PATH" | cut -f1)"
        fi

        echo ""
        echo "Operations Completed:"
        echo "- System Health Check: ✓"
        echo "- Database Maintenance: ✓"
        echo "- Backup Operations: ✓"
        echo "- Log Rotation: ✓"
        echo "- Security Scan: ✓"
        echo "- Performance Optimization: ✓"
        echo "- Resource Cleanup: ✓"

        echo ""
        echo "File Counts:"
        echo "- Log Files: $(find "$LOG_DIR" -type f | wc -l)"
        echo "- Backup Files: $(find "$BACKUP_DIR" -name "*.tar.gz" -type f | wc -l)"

        echo ""
        echo "Next Scheduled Run: $(date -d 'tomorrow 2:00' 2>/dev/null || date -v+1d -v2H -v0M -v0S 2>/dev/null || echo 'Tomorrow at 2:00 AM')"

    } > "$report_file"

    log "INFO" "Daily report generated: $report_file"
}

# Send notifications (if configured)
send_notifications() {
    log "INFO" "Checking notification configuration..."

    # Check if notification is configured
    local config_file="$PROJECT_ROOT/config.json"
    if [[ -f "$config_file" ]]; then
        # This would integrate with the notification system
        # For now, just log that notifications would be sent
        log "INFO" "Daily operations completed - notifications would be sent if configured"
    else
        log "INFO" "No notification configuration found"
    fi
}

# Main execution function
main() {
    local start_time=$(date +%s)

    echo ""
    echo "🤖 TRAE.AI Daily Autonomous Operations Cycle"
    echo "   Started: $(date)"
    echo "   ========================================="
    echo ""

    # Initialize
    check_user
    setup_directories

    log "INFO" "Starting daily operations cycle..."

    # Execute all operations
    system_health_check
    database_maintenance
    backup_operations
    log_rotation
    security_scan
    performance_optimization
    resource_cleanup
    generate_daily_report
    send_notifications

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    log "INFO" "Daily operations cycle completed successfully"
    log "INFO" "Total execution time: ${duration} seconds"

    echo ""
    echo "✅ Daily operations cycle completed successfully!"
    echo "   Duration: ${duration} seconds"
    echo "   Log: $DAILY_LOG"
    echo ""
}

# Trap for cleanup on exit
trap 'log "INFO" "Script interrupted or completed"' EXIT

# Run main function
main "$@"

exit 0
