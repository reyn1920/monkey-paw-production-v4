import pathlib, json
root = pathlib.Path(".")
diags = sorted((root / "reports").glob("diagnostic_*"))
if not diags:
    raise SystemExit("No diagnostics found.")
latest = diags[-1]
routes = json.loads((latest / "routes_static.json").read_text())
baseline = {
  "intended": {
    "routes": ["/api/health","/api/status","/api/research","/api/draft","/api/repurpose","/api/publish","/api/admin/approve_publish/{value}"]
  }
}
out = "# Intended vs Actual\n\n"
out += "## Intended routes\n```json\n" + json.dumps(baseline, indent=2) + "\n```\n"
out += "## Actual (static scan)\n```json\n" + json.dumps(routes, indent=2) + "\n```\n"
(root / "reports/COMPARISON.md").write_text(out, encoding="utf-8")
print("Written ./reports/COMPARISON.md")
