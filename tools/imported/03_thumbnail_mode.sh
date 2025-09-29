#!/bin/bash

# Thumbnail Mode Control Script
# Manages THUMBNAIL_MODE setting in app_settings.yaml

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SETTINGS_FILE="$SCRIPT_DIR/app_settings.yaml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if settings file exists
check_settings_file() {
    if [[ ! -f "$SETTINGS_FILE" ]]; then
        print_error "Settings file not found: $SETTINGS_FILE"
        print_status "Creating default settings file..."
        create_default_settings
    fi
}

# Function to create default settings file
create_default_settings() {
    cat > "$SETTINGS_FILE" << 'EOF'
# Application Settings Configuration
# Thumbnail Generation Pipeline Control

# THUMBNAIL_MODE: Controls thumbnail generation behavior
# Values: 'enabled', 'disabled', 'auto'
# - enabled: Force thumbnail generation for all supported content
# - disabled: Skip all thumbnail generation
# - auto: Generate thumbnails based on content type and size heuristics
THUMBNAIL_MODE: 'auto'

# Thumbnail Configuration
thumbnail:
  max_width: 800
  max_height: 600
  quality: 85
  format: 'webp'
  fallback_format: 'jpeg'
  
# Content Processing
content:
  supported_formats:
    - 'jpg'
    - 'jpeg'
    - 'png'
    - 'gif'
    - 'webp'
    - 'pdf'
    - 'mp4'
    - 'mov'
  max_file_size: 50MB
  
# Performance Settings
performance:
  concurrent_jobs: 4
  timeout_seconds: 30
  retry_attempts: 3
EOF
    print_success "Default settings file created"
}

# Function to get current thumbnail mode
get_current_mode() {
    if [[ -f "$SETTINGS_FILE" ]]; then
        grep "^THUMBNAIL_MODE:" "$SETTINGS_FILE" | sed "s/THUMBNAIL_MODE: *'\([^']*\)'.*/\1/" | tr -d "'\""
    else
        echo "unknown"
    fi
}

# Function to set thumbnail mode
set_thumbnail_mode() {
    local new_mode="$1"
    
    # Validate mode
    case "$new_mode" in
        enabled|disabled|auto)
            ;;
        *)
            print_error "Invalid mode: $new_mode"
            print_status "Valid modes: enabled, disabled, auto"
            exit 1
            ;;
    esac
    
    check_settings_file
    
    # Create backup
    if [[ -f "$SETTINGS_FILE" ]]; then
        cp "$SETTINGS_FILE" "${SETTINGS_FILE}.backup.$(date +%s)"
        print_status "Created backup of settings file"
    fi
    
    # Update the mode using sed
    if grep -q "^THUMBNAIL_MODE:" "$SETTINGS_FILE"; then
        # Replace existing line
        sed -i.tmp "s/^THUMBNAIL_MODE: *.*/THUMBNAIL_MODE: '$new_mode'/" "$SETTINGS_FILE"
        rm -f "${SETTINGS_FILE}.tmp"
    else
        # Add new line after the comment block
        sed -i.tmp "/^# - auto:/a\\
THUMBNAIL_MODE: '$new_mode'\\
" "$SETTINGS_FILE"
        rm -f "${SETTINGS_FILE}.tmp"
    fi
    
    print_success "Thumbnail mode set to: $new_mode"
}

# Function to show current status
show_status() {
    check_settings_file
    
    local current_mode
    current_mode=$(get_current_mode)
    
    echo
    print_status "=== Thumbnail System Status ==="
    echo "Current mode: $current_mode"
    echo "Settings file: $SETTINGS_FILE"
    
    case "$current_mode" in
        enabled)
            echo "Status: ✅ Thumbnails will be generated for all supported content"
            ;;
        disabled)
            echo "Status: ❌ Thumbnail generation is disabled"
            ;;
        auto)
            echo "Status: 🔄 Thumbnails generated based on content heuristics"
            ;;
        *)
            echo "Status: ❓ Unknown or invalid mode"
            ;;
    esac
    echo
}

# Function to test thumbnail generation
test_thumbnails() {
    print_status "Testing thumbnail generation..."
    
    if command -v python3 &> /dev/null; then
        if [[ -f "$SCRIPT_DIR/thumbnailer.py" ]]; then
            python3 "$SCRIPT_DIR/thumbnailer.py" 2>/dev/null || true
            print_success "Thumbnail system test completed"
        else
            print_warning "thumbnailer.py not found, skipping test"
        fi
    else
        print_warning "Python3 not found, skipping test"
    fi
}

# Function to clear thumbnail cache
clear_cache() {
    local cache_dir="$SCRIPT_DIR/cache/thumbnails"
    
    if [[ -d "$cache_dir" ]]; then
        print_status "Clearing thumbnail cache..."
        rm -rf "$cache_dir"/*
        print_success "Thumbnail cache cleared"
    else
        print_warning "Thumbnail cache directory not found: $cache_dir"
    fi
}

# Function to show help
show_help() {
    echo "Thumbnail Mode Control Script"
    echo
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo
    echo "Commands:"
    echo "  status                 Show current thumbnail mode and status"
    echo "  enable                 Enable thumbnail generation for all content"
    echo "  disable                Disable thumbnail generation"
    echo "  auto                   Enable automatic thumbnail generation"
    echo "  set <mode>             Set thumbnail mode (enabled|disabled|auto)"
    echo "  test                   Test thumbnail generation system"
    echo "  clear-cache            Clear thumbnail cache"
    echo "  help                   Show this help message"
    echo
    echo "Examples:"
    echo "  $0 status              # Show current status"
    echo "  $0 enable              # Enable thumbnails"
    echo "  $0 set auto            # Set to auto mode"
    echo "  $0 clear-cache         # Clear cache"
    echo
}

# Main script logic
main() {
    case "${1:-status}" in
        status)
            show_status
            ;;
        enable)
            set_thumbnail_mode "enabled"
            show_status
            ;;
        disable)
            set_thumbnail_mode "disabled"
            show_status
            ;;
        auto)
            set_thumbnail_mode "auto"
            show_status
            ;;
        set)
            if [[ -z "$2" ]]; then
                print_error "Mode argument required for 'set' command"
                show_help
                exit 1
            fi
            set_thumbnail_mode "$2"
            show_status
            ;;
        test)
            test_thumbnails
            ;;
        clear-cache)
            clear_cache
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"