import pathlib, json
root = pathlib.Path(".")
diags = sorted((root / "reports").glob("diagnostic_*"))
if not diags:
    print("No diagnostics found."); exit()
latest = diags[-1]
baseline = "# Intended vs Actual\n- Core pipeline should run research→draft→repurpose→publish\n"
routes = (latest / "routes_static.json").read_text()
out = baseline + "\n## Routes (static)\n```json\n" + routes + "\n```\n"
(root / "reports/COMPARISON.md").write_text(out)
print("Written ./reports/COMPARISON.md")
