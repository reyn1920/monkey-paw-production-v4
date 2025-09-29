#!/usr/bin/env python3
import os, re, sys, json, pathlib
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
db = {"models": [], "sqlite_paths": [], "sql_statements": [], "db_files": []}
model_pat = re.compile(r'class\s+([A-Za-z_][A-Za-z0-9_]*)\((SQLModel|Base)\)\s*:', re.M)
sqlite_pat = re.compile(r'(sqlite3\.connect\(|sqlite://|sqlite:////)', re.I)
sql_pat = re.compile(r'\b(SELECT|INSERT|UPDATE|DELETE)\b', re.I)
for py in ROOT.rglob("*.py"):
    try: t = py.read_text(errors="ignore")
    except Exception: continue
    for m in model_pat.finditer(t):
        db["models"].append({"file": str(py.relative_to(ROOT)), "model": m.group(1)})
    if sqlite_pat.search(t) or "sqlmodel" in t.lower() or "sqlalchemy" in t.lower():
        db["sqlite_paths"].append(str(py.relative_to(ROOT)))
    if sql_pat.search(t):
        db["sql_statements"].append(str(py.relative_to(ROOT)))
for p in ROOT.rglob("*.db"):
    db["db_files"].append(str(p.relative_to(ROOT)))
print(json.dumps({"root": str(ROOT), "db": db}, indent=2))
