import sys, re, json, os
root = sys.argv[1] if len(sys.argv)>1 else "."
pat = re.compile(r'@router\.(get|post|put|delete|patch)\(\s*["\']([^"\']+)["\']')
found = []
for base, _, files in os.walk(root):
    for f in files:
        if f.endswith(".py"):
            p = os.path.join(base, f)
            try:
                s = open(p, "r", encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            for m in pat.finditer(s):
                found.append({"file": p, "method": m.group(1).upper(), "path": m.group(2)})
print(json.dumps({"routes": found}, indent=2))
