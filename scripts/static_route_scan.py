#!/usr/bin/env python3
import os, re, sys, json, pathlib
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
routes = []
decor_pat = re.compile(r'@(.*?)(?:\.(get|post|put|delete|patch|options|head)|\.api_route)\(\s*["\']([^"\']+)["\']', re.I)
def_pat = re.compile(r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', re.M)
for py in ROOT.rglob("*.py"):
    try: text = py.read_text(errors="ignore")
    except Exception: continue
    for m in decor_pat.finditer(text):
        deco_prefix = m.group(1)
        method = (m.group(2) or "ANY").upper()
        path = m.group(3)
        idx = m.end()
        sub = text[idx:idx+1000]
        mdef = def_pat.search(sub)
        func = mdef.group(1) if mdef else "<unknown>"
        line = text[:m.start()].count("\n") + 1
        routes.append({"file": str(py.relative_to(ROOT)), "line": line, "deco": deco_prefix, "method": method, "path": path, "function": func})
print(json.dumps({"root": str(ROOT), "routes": routes}, indent=2))
