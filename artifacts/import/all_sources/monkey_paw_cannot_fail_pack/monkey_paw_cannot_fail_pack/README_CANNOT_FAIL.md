# Monkey Paw — Cannot Fail Pack (Add-Only, Zero-Cost)
This pack gives you:
- Do-Not-Delete guard (config/do_not_delete.yaml + tools/guard/do_not_delete_guard.py)
- Panic switch (scripts/panic_on.zsh / panic_off.zsh)
- Watchdog health loop (tools/watchdog/health_loop.zsh)
- Snapshots (tools/snapshots/backup_now.zsh)
- Importers for writing, thumbnails, marketing, analytics
- Viral heuristics & targets (config/heuristics.yaml)
- Databases created in db/

## Quick Start
zsh tools/guard/do_not_delete_guard.py  # track protected refs
zsh scripts/panic_on.zsh                 # disable publishing
zsh tools/snapshots/backup_now.zsh       # snapshot project
zsh tools/watchdog/health_loop.zsh &     # background health log
zsh tools/importers/import_writing.zsh ~/Documents/Writing
zsh tools/importers/import_thumbnails.zsh ~/Pictures
python3 tools/importers/import_analytics.py ~/Downloads

## Notes
- All scripts are local and free.
- Adjust config/heuristics.yaml targets to fit your channels.
- Keep your original assets in place; importers copy non-destructively.
