#!/usr/bin/env python3
import os, sys, json, pathlib, fnmatch
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
patterns = [
    "*nocode*", "*no-code*", "*lowcode*",
    "*agent*builder*", "*builder*agent*",
    "*workflow*builder*", "*wind*surf*agent*",
    "*cursor*agent*", "*prompt*builder*", "*coders*",
    "agents/nocode*", "prompts/nocode*", "tools/nocode*"
]
matches = set()
for p in ROOT.rglob("*"):
    rel = str(p.relative_to(ROOT))
    for pat in patterns:
        if fnmatch.fnmatch(rel.lower(), pat.lower()):
            matches.add(rel); break
print(json.dumps({"root": str(ROOT), "patterns": patterns, "matches": sorted(matches)}, indent=2))
