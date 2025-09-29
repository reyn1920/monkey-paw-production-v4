#!/bin/bash
# Production Rollback Script
# Usage: ./scripts/rollback.sh [commit_hash]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    error "Not in a git repository"
fi

# Get current commit
CURRENT_COMMIT=$(git rev-parse HEAD)
log "Current commit: $CURRENT_COMMIT"

# Determine target commit
if [ $# -eq 0 ]; then
    # No argument provided, rollback to previous commit
    TARGET_COMMIT=$(git rev-parse HEAD~1)
    log "No commit specified, rolling back to previous commit: $TARGET_COMMIT"
else
    TARGET_COMMIT="$1"
    # Validate the commit exists
    if ! git cat-file -e "$TARGET_COMMIT" 2>/dev/null; then
        error "Commit $TARGET_COMMIT does not exist"
    fi
    log "Rolling back to specified commit: $TARGET_COMMIT"
fi

# Safety check - don't rollback to the same commit
if [ "$CURRENT_COMMIT" = "$TARGET_COMMIT" ]; then
    warn "Already at target commit $TARGET_COMMIT, nothing to do"
    exit 0
fi

# Show what we're about to do
log "Rollback plan:"
echo "  From: $CURRENT_COMMIT"
echo "  To:   $TARGET_COMMIT"
echo
log "Changes that will be reverted:"
git log --oneline "$TARGET_COMMIT..$CURRENT_COMMIT" || true
echo

# Confirmation prompt
read -p "Proceed with rollback? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log "Rollback cancelled"
    exit 0
fi

# Create a backup branch
BACKUP_BRANCH="backup-$(date +%Y%m%d-%H%M%S)-$CURRENT_COMMIT"
log "Creating backup branch: $BACKUP_BRANCH"
git branch "$BACKUP_BRANCH" "$CURRENT_COMMIT"

# Perform the rollback
log "Performing rollback..."
git reset --hard "$TARGET_COMMIT"

# Verify the rollback
NEW_COMMIT=$(git rev-parse HEAD)
if [ "$NEW_COMMIT" = "$TARGET_COMMIT" ]; then
    log "✅ Rollback successful!"
    log "Current commit: $NEW_COMMIT"
    log "Backup branch created: $BACKUP_BRANCH"
    echo
    log "To restore the previous state, run:"
    echo "  git reset --hard $BACKUP_BRANCH"
else
    error "Rollback failed - unexpected state"
fi

# Check if there are any uncommitted changes
if ! git diff-index --quiet HEAD --; then
    warn "There are uncommitted changes in the working directory"
    git status --short
fi

log "Rollback complete. Remember to:"
echo "  1. Restart any running services"
echo "  2. Run tests to verify functionality"
echo "  3. Update deployment if necessary"
