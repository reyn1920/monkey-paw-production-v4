import os, sys, json
spec = os.environ.get("PD_APP_SPEC", "apps.monkey_paw_live.app.main:app")
try:
    mod, obj = spec.split(":")
    m = __import__(mod, fromlist=[obj])
    app = getattr(m, obj)
    routes = []
    for r in getattr(app, "routes", []):
        methods = sorted(getattr(r, "methods", []) or [])
        path = getattr(r, "path", "")
        routes.append({"methods": methods, "path": path})
    print(json.dumps({"spec": spec, "routes": routes}, indent=2))
except Exception as e:
    print(json.dumps({"spec": spec, "error": str(e)}))
