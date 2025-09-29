#!/usr/bin/env python3
import py_compile
import pathlib
import fnmatch
import sys

IGNORE = [
    p.strip()
    for p in open(".rewriteignore").read().splitlines()
    if p.strip() and not p.startswith("#")
]


def ignored(path: str) -> bool:
    norm = path.replace("\\", "/")
    return any(fnmatch.fnmatch(norm, pat) for pat in IGNORE)


errors = []
root = pathlib.Path(".").resolve()
for p in root.rglob("*.py"):
    rel = str(p.relative_to(root)).replace("\\", "/")
    if ignored(rel) or rel.endswith(".failed.py"):
        continue
    try:
        py_compile.compile(str(p), doraise=True)
    except Exception as e:
        errors.append((rel, e))

if errors:
    print("Syntax errors=")
    for rel, e in errors:
        print(f"  {rel}\n    {e.__class__.__name__}: {e}")
    sys.exit(1)
print("✅ No syntax errors (filtered by .rewriteignore).")
