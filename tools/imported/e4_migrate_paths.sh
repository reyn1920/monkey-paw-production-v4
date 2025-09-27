#!/bin/bash

# Path migration script - migrates references from Google Drive to Projects directory
# This script finds and replaces all occurrences of the old path with the new path

OLD="/Users/thomasbrianreynolds/Library/CloudStorage/GoogleDrive-brianinpty@gmail.com/My Drive/online production"
NEW="$HOME/Projects/online_runtime"
DST="$HOME/Projects/online_runtime"  # Fixed: Define the destination directory

echo "Starting path migration..."
echo "OLD: $OLD"
echo "NEW: $NEW"
echo "DST: $DST"

# Check if destination directory exists
if [ ! -d "$DST" ]; then
    echo "Error: Destination directory '$DST' does not exist!"
    echo "Please create the destination directory first or copy your project there."
    exit 1
fi

# Find all files containing the old path and save to temporary file
echo "Searching for files containing old path references..."
grep -RIl --null "$OLD" "$DST" \
  --exclude-dir .git --exclude-dir node_modules --exclude-dir .venv --exclude-dir __pycache__ \
  --exclude "*.png" --exclude "*.jpg" --exclude "*.jpeg" --exclude "*.gif" --exclude "*.pdf" \
  --exclude "*.pyc" --exclude "*.log" --exclude "*.db" \
  > /tmp/path_hits.txt || true

# Count the number of files found
file_count=$(grep -c . /tmp/path_hits.txt 2>/dev/null || echo "0")
echo "Found $file_count files containing old path references"

if [ "$file_count" -eq 0 ]; then
    echo "No files found with old path references. Migration complete!"
    rm -f /tmp/path_hits.txt
    exit 0
fi

# Show which files will be modified
echo "Files that will be modified:"
while IFS= read -r -d '' f; do
    echo "  - $f"
done < /tmp/path_hits.txt

# Ask for confirmation
read -p "Do you want to proceed with the path replacement? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Migration cancelled."
    rm -f /tmp/path_hits.txt
    exit 0
fi

# Perform the replacement
echo "Performing path replacement..."
replaced_count=0
while IFS= read -r -d '' f; do
    if [ -f "$f" ]; then
        # Create backup
        cp "$f" "$f.backup"
        
        # Perform replacement
        if sed -i '' "s|${OLD}|${NEW}|g" "$f"; then
            echo "  ✓ Updated: $f"
            ((replaced_count++))
        else
            echo "  ✗ Failed to update: $f"
            # Restore backup on failure
            mv "$f.backup" "$f"
        fi
    fi
done < /tmp/path_hits.txt

echo "Migration complete!"
echo "Successfully updated $replaced_count files"
echo "Backup files created with .backup extension"

# Clean up
rm -f /tmp/path_hits.txt

echo "To remove backup files after verification, run:"
echo "find '$DST' -name '*.backup' -delete"