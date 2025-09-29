#!/usr/bin/env python3
"""
Syntax normalizer: gentle fixes for common Python source quirks.
- Ensure UTF-8 LF newlines
- Ensure trailing newline
- Replace smart quotes with ASCII
No removals or renames; writes in-place with a backup copy.
"""
import os, pathlib, shutil

SMART = {
    "\u2018": "'", "\u2019": "'",
    "\u201C": '"', "\u201D": '"'
}

def normalize_text(s: str) -> str:
    for k, v in SMART.items():
        s = s.replace(k, v)
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    if not s.endswith("\n"):
        s += "\n"
    return s

def process_file(p: pathlib.Path):
    try:
        raw = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return
    fixed = normalize_text(raw)
    if fixed != raw:
        backup = p.with_suffix(p.suffix + ".bak_keep")
        try:
            shutil.copy2(p, backup)
        except Exception:
            pass
        p.write_text(fixed, encoding="utf-8")

def main():
    root = pathlib.Path(".")
    for p in root.rglob("*.py"):
        if any(seg in {".git","node_modules",".venv","__pycache__"} for seg in p.parts):
            continue
        process_file(p)
    print("[Normalizer] done.")

if __name__ == "__main__":
    main()
