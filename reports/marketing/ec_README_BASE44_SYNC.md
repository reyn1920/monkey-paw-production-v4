# Base44 Synchronization System

This system automatically synchronizes updates from the Base44 development environment to the online production environment.

## Features

- **Automatic Update Detection**: Monitors Base44 files for changes
- **Configurable Sync Rules**: Define which files to sync and exclude patterns
- **Backup System**: Creates backups before applying updates
- **Daemon Mode**: Runs continuously to check for updates at regular intervals
- **Logging**: Comprehensive logging of all sync operations

## Files

- `scripts/base44_sync.py` - Main synchronization script
- `scripts/auto_sync_daemon.py` - Daemon for automatic syncing
- `base44_sync_config.json` - Configuration file
- `.last_base44_sync` - Timestamp of last sync (auto-generated)

## Usage

### Manual Sync

```bash
# Check for updates without syncing
python scripts/base44_sync.py --check-only

# Force sync regardless of update detection
python scripts/base44_sync.py --force

# Normal sync (only if updates detected)
python scripts/base44_sync.py
```

### Automatic Sync Daemon

```bash
# Run daemon with default 5-minute interval
python scripts/auto_sync_daemon.py

# Run with custom interval (in seconds)
python scripts/auto_sync_daemon.py --interval 600

# Run as background daemon (detached)
python scripts/auto_sync_daemon.py --daemon
```

## Configuration

Edit `base44_sync_config.json` to customize:

- `sync_files`: List of files/patterns to sync from Base44
- `exclude_patterns`: Patterns to exclude from sync
- `auto_backup`: Enable/disable automatic backups
- `backup_dir`: Directory for storing backups
- `sync_interval`: Default interval for daemon mode

## Integration with Production

The sync system integrates with your production environment by:

1. **Environment Variables**: Updates `.env.example` with Base44 configuration
2. **Dependencies**: Syncs `requirements.txt` and other dependency files
3. **Application Code**: Updates backend and frontend code as configured
4. **Configuration Files**: Syncs configuration templates and examples

## Monitoring

- Check `base44_sync.log` for sync operation logs
- Check `auto_sync_daemon.log` for daemon operation logs
- Monitor backup directory for successful backup creation

## Safety Features

- **Backup Before Sync**: Automatic backups prevent data loss
- **Dry Run Mode**: Test sync operations without making changes
- **Rollback Capability**: Use backups to restore previous state
- **Selective Sync**: Only sync configured files, not entire directories

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure scripts have execute permissions
2. **Import Errors**: Run from project root directory
3. **Path Issues**: Verify Base44 directory exists and is accessible
4. **Config Errors**: Check JSON syntax in configuration file

### Logs

All operations are logged with timestamps and detailed information:
- INFO: Normal operations and status updates
- WARNING: Non-critical issues that don't stop sync
- ERROR: Critical issues that prevent sync completion

## Security Considerations

- Scripts run with current user permissions
- No network operations (local file sync only)
- Backups stored locally in configured directory
- Configuration files should not contain secrets