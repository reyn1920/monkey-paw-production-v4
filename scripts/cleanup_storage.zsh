#!/bin/zsh
# Non-destructive storage cleanup helper for Monkey Paw V4
# - Default: dry-run (prints actions)
# - Use --apply to actually perform actions
# - Safe targets: generated logs/inventories in out/, cache-like imports in assets/*/import
# - Archival: compress large CSV/JSON/TXT into .gz in-place
# - Deletion: only of clearly generated, re-creatable files with explicit --apply

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

APPLY=false
RETENTION_DAYS=${RETENTION_DAYS:-14}
LARGE_MB=${LARGE_MB:-10}
CLEAR_IMPORTS=false

for arg in "$@"; do
  case "$arg" in
    --apply) APPLY=true ;;
    --days=*) RETENTION_DAYS="${arg#*=}" ;;
    --large=*) LARGE_MB="${arg#*=}" ;;
    --clear-imports) CLEAR_IMPORTS=true ;;
    --help|-h)
      cat <<EOF
Usage: zsh scripts/cleanup_storage.zsh [--apply] [--days=N] [--large=MB]

Default is dry-run. In dry-run, actions are only printed.
  --apply     Actually perform deletions and compressions
  --days=N    Retention for generated logs (default: 14)
  --large=MB  Compress text data files larger than MB (default: 10)
  --clear-imports  Also clear contents of assets/*/import (cache-like)

Targets:
  - Delete old generated logs in out/: import_audit_*.txt, *_inventory.{json,csv}
  - Gzip large CSV/JSON/TXT in out/ and reports/marketing/ over threshold
  - Optionally clear cache-like imports under assets/*/import (kept by default)
EOF
      exit 0
      ;;
  esac
done

red() { printf "\033[31m%s\033[0m\n" "$*"; }
grn() { printf "\033[32m%s\033[0m\n" "$*"; }
yel() { printf "\033[33m%s\033[0m\n" "$*"; }
inf() { printf "[info] %s\n" "$*"; }

# Helper to maybe run or echo
run() {
  if $APPLY; then
    eval "$*"
  else
    yel "DRY-RUN: $*"
  fi
}

# Summary of heavy directories
inf "Top-level sizes:"
( du -sh * 2>/dev/null | sort -h ) || true

epoch_cutoff=$(python3 - <<PY
import time,sys
print(int(time.time()) - int($RETENTION_DAYS)*24*3600)
PY
)

# 1) Delete old generated logs in out/
inf "Scanning out/ for generated audit/inventory older than ${RETENTION_DAYS} days..."
mkdir -p out
found=false
for f in $(find out -maxdepth 2 -type f \( -name 'import_audit_*.txt' -o -name '*_inventory.json' -o -name '*_inventory.csv' -o -name 'downloads_inventory.*' \) 2>/dev/null); do
  mtime=$(stat -f %m "$f" 2>/dev/null || echo 0)
  if [ "$mtime" -lt "$epoch_cutoff" ]; then
    found=true
    if $APPLY; then
      rm -f "$f" && grn "Deleted $f"
    else
      yel "Would delete: $f"
    fi
  fi
done
$found || inf "No old generated files found to delete."

# 2) Compress large text data in out/ and reports/marketing/
inf "Compressing large text data (> ${LARGE_MB} MB) in out/ and reports/marketing/..."
for dir in out reports/marketing; do
  [ -d "$dir" ] || continue
  while IFS= read -r -d '' f; do
    # skip already compressed
    case "$f" in *.gz) continue;; esac
    sz=$(stat -f %z "$f" 2>/dev/null || echo 0)
    if [ "$sz" -gt $(( $LARGE_MB * 1048576 )) ]; then
      if $APPLY; then
        gzip -9 "$f" && grn "Compressed: $f.gz"
      else
        yel "Would gzip: $f"
      fi
    fi
  done < <(find "$dir" -type f \( -name '*.csv' -o -name '*.json' -o -name '*.txt' -o -name '*.md' \) -print0 2>/dev/null)
done

# 3) Optional: Clear cache-like imports under assets (guarded by --clear-imports)
inf "Cache/import directories under assets/:"
( du -sh assets/*/import 2>/dev/null | sort -h ) || true
if $CLEAR_IMPORTS; then
  inf "Clearing contents of assets/*/import (flag enabled) ..."
  while IFS= read -r -d '' d; do
    if $APPLY; then
      rm -rf "${d}"/* 2>/dev/null || true
      grn "Cleared: $d/*"
    else
      yel "Would clear: $d/*"
    fi
  done < <(find assets -type d -name import -print0 2>/dev/null)
else
  inf "--clear-imports not set; leaving import caches intact."
fi

# 4) Report top 20 largest files after cleanup (or preview)
inf "Top 20 largest files in project (post preview):"
find . -type f -not -path './.venv*' -not -path './.venv_monkeypawv4*' -exec stat -f '%z %N' {} + \
  | sort -n -k1 | tail -n 20 | awk '{sz=$1; $1=""; gsub(/^ /,""); printf("%8.1f MB  %s\n", sz/1048576, $0)}'

echo
if $APPLY; then
  grn "Cleanup applied."
else
  yel "Dry-run only. Re-run with --apply to perform actions."
fi
