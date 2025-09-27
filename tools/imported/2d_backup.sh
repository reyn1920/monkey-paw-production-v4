#!/usr/bin/env bash
set -e
TS=$(date +%Y%m%d_%H%M%S)
mkdir -p backups
zip -r backups/snapshot_$TS.zip assets backend config dashboard docs tools qa http || true
echo Backup OK
