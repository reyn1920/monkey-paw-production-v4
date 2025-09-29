#!/bin/bash
# Merge the latest staged folder into the current project under integrated_pack/<timestamp>
set -e
MERGE_DIR="$(dirname "$0")"
CONFIG="$MERGE_DIR/merge_config.json"

CURRENT_ROOT=$(jq -r .current_project_root "$CONFIG")
STAGING_ROOT="$MERGE_DIR/../staging"
INTEGRATED_ROOT="$MERGE_DIR/../integrated_pack"

LATEST_STAGE=$(ls -td "$STAGING_ROOT"/*/ | head -1)
TIMESTAMP=$(basename "$LATEST_STAGE")
DEST="$INTEGRATED_ROOT/$TIMESTAMP"

mkdir -p "$DEST"
cp -R "$LATEST_STAGE"/* "$DEST"/

# Copy into current project (additive, no overwrite outside integrated_pack)
cp -Rn "$DEST"/* "$CURRENT_ROOT"/

# Backup
mkdir -p "$MERGE_DIR/../backups"
cp -R "$CURRENT_ROOT" "$MERGE_DIR/../backups/backup_$TIMESTAMP"

echo "Merged $LATEST_STAGE into $CURRENT_ROOT (integrated_pack/$TIMESTAMP) and backed up."
