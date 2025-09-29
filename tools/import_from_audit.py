#!/usr/bin/env python3
import os, sys, json, shutil, time
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / 'out'
ASSETS = PROJECT / 'assets'
TOOLS = PROJECT / 'tools'
REPORTS = PROJECT / 'reports'
BACKUP_DIR = PROJECT / 'artifacts' / 'backup_pre_overwrite'

MAPS = {
    'avatars': 'assets/Avatars/import/',
    'tts_voices': 'assets/Voices/import/',
    'resolve': 'assets/Templates/Resolve/',
    'blender': 'assets/Templates/Blender/',
    'luts': 'assets/LUTs/',
    'overlays': 'assets/Overlays/',
    'fonts': 'assets/Fonts/',
    'sfx': 'assets/SFX/',
    'music': 'assets/Music/',
    'broll': 'assets/Broll/',
    'scripts_configs': 'tools/imported/',
    'marketing': 'reports/marketing/',
}

SKIP_EXTS = {'.tmp', '.ds_store', '.crdownload'}


def safe_copy(src: Path, dest: Path, audit_lines: list):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        # Do not overwrite – add-only policy
        audit_lines.append(f"SKIP EXISTS: {dest}")
        return False
    shutil.copy2(src, dest)
    audit_lines.append(f"COPIED: {src} -> {dest}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: import_from_audit.py <audit_dir>")
        sys.exit(1)

    audit_dir = Path(sys.argv[1]).resolve()
    inv = audit_dir / 'downloads_inventory.json'
    if not inv.exists():
        print(f"Inventory not found: {inv}")
        sys.exit(2)

    with inv.open('r', encoding='utf-8') as f:
        items = json.load(f)

    ts = time.strftime('%Y%m%d-%H%M%S')
    log_path = OUT / f'import_audit_{ts}.txt'
    log_lines = [f"Import started: {ts}"]

    imported_count = 0

    for r in items:
        group = r.get('group')
        src = Path(r['path'])
        if not group or group not in MAPS:
            continue
        if not src.exists() or not src.is_file():
            continue
        if src.suffix.lower() in SKIP_EXTS:
            continue

        rel_name = src.name
        # Flatten small risk of name collisions by prefixing with 2-char hash
        prefix = hex(abs(hash(str(src))) % 256)[2:].zfill(2)
        dest_dir = PROJECT / MAPS[group]
        dest = dest_dir / f"{prefix}_{rel_name}"

        try:
            if safe_copy(src, dest, log_lines):
                imported_count += 1
        except Exception as e:
            log_lines.append(f"ERROR: copy failed {src} -> {dest}: {e}")

    log_lines.append(f"Imported files: {imported_count}")
    log_path.write_text('\n'.join(log_lines))
    print(f"DONE: {log_path}")

if __name__ == '__main__':
    main()
