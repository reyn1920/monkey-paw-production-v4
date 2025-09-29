#!/usr/bin/env python3
import os, sys, json, importlib, traceback
APP_SPEC = os.environ.get("MP_APP_SPEC", "app.main:app")
def load_app(spec: str):
    mod_name, app_attr = spec.split(":")
    mod = importlib.import_module(mod_name)
    return getattr(mod, app_attr)
res = {"app_spec": APP_SPEC, "ok": False, "error": None, "routes": []}
try:
    app = load_app(APP_SPEC)
    for r in getattr(app, "routes", []):
        methods = list(getattr(r, "methods", []) or [])
        path = getattr(r, "path", None) or getattr(r, "path_format", None)
        name = getattr(r, "name", "")
        endpoint = getattr(r, "endpoint", None)
        handler = getattr(endpoint, "__name__", "") if endpoint else ""
        res["routes"].append({"path": path, "methods": methods, "name": name, "handler": handler})
    res["ok"] = True
except Exception as e:
    import traceback
    res["error"] = "".join(traceback.format_exception_only(type(e), e)).strip()
print(json.dumps(res, indent=2))
