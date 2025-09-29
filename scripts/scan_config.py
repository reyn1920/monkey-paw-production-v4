#!/usr/bin/env python3
import os, sys, json, pathlib
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
res = {"yaml": [], "json": [], "toml": [], "env": [], "feature_flags": []}
for ext, key in [("*.yml","yaml"), ("*.yaml","yaml"), ("*.json","json"), ("*.toml","toml"), (".env","env")]:
    if ext == ".env":
        for p in ROOT.rglob(".env"):
            res["env"].append(str(p.relative_to(ROOT)))
    else:
        for p in ROOT.rglob(ext):
            res[key].append(str(p.relative_to(ROOT)))
flags = []
for y in res["yaml"]:
    if any(k in y.lower() for k in ["feature", "toggle", "config"]):
        flags.append(y)
res["feature_flags"] = flags
print(json.dumps({"root": str(ROOT), "config": res}, indent=2))
