import os, json, glob, pathlib, datetime
root = pathlib.Path(".")
diags = sorted((root / "reports").glob("diagnostic_*"))
if not diags:
    print("No diagnostics found.")
    raise SystemExit(0)
latest = diags[-1]
baseline = (root / "tools/project-doctor/templates/COMPARISON_BASELINE.md").read_text(encoding="utf-8")
parts = {
    "routes_static": json.loads((latest / "routes_static.json").read_text(encoding="utf-8")) if (latest / "routes_static.json").exists() else {},
    "routes_runtime": json.loads((latest / "routes_runtime.json").read_text(encoding="utf-8")) if (latest / "routes_runtime.json").exists() else {},
    "jobs": json.loads((latest / "jobs.json").read_text(encoding="utf-8")) if (latest / "jobs.json").exists() else {},
    "db": json.loads((latest / "db.json").read_text(encoding="utf-8")) if (latest / "db.json").exists() else {},
    "faiss": json.loads((latest / "faiss.json").read_text(encoding="utf-8")) if (latest / "faiss.json").exists() else {},
    "config": json.loads((latest / "config.json").read_text(encoding="utf-8")) if (latest / "config.json").exists() else {},
    "addon": json.loads((latest / "addon_matches.json").read_text(encoding="utf-8")) if (latest / "addon_matches.json").exists() else {},
}
def sec(title, obj):
    return f"\n### {title}\n\n```json\n{json.dumps(obj, indent=2)}\n```\n"

out = baseline
out += sec("Routes (static scan)", parts["routes_static"])
out += sec("Routes (runtime scan)", parts["routes_runtime"])
out += sec("Jobs", parts["jobs"])
out += sec("DB", parts["db"])
out += sec("FAISS", parts["faiss"])
out += sec("Config Files", parts["config"])
out += sec("Addon‑like Files", parts["addon"])

path = root / "reports" / "COMPARISON.md"
path.write_text(out, encoding="utf-8")
print(str(path))
