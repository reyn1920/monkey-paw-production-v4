#!/usr/bin/env python3
from pathlib import Path
import json
root = Path('.')
reports = root / 'reports'
base = '# Intended vs. Actual — see diagnostics.\n'
diags = sorted([p for p in reports.glob('diagnostic_*') if p.is_dir()])
out = reports / 'COMPARISON.md'
if not diags:
    out.write_text(base + "\n_No diagnostics found._\n")
else:
    out.write_text(base + f"\nUsing: {diags[-1].name}\n")
print(f"Wrote {out}")
