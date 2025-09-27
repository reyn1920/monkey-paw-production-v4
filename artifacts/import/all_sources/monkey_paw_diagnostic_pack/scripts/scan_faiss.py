#!/usr/bin/env python3
import os, sys, json, pathlib
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
hits = {"files": [], "index_files": []}
for py in ROOT.rglob("*.py"):
    try: t = py.read_text(errors="ignore")
    except Exception: continue
    if "import faiss" in t or "faiss." in t:
        hits["files"].append(str(py.relative_to(ROOT)))
for idx in ROOT.rglob("*.index"):
    hits["index_files"].append(str(idx.relative_to(ROOT)))
print(json.dumps({"root": str(ROOT), "faiss": hits}, indent=2))
