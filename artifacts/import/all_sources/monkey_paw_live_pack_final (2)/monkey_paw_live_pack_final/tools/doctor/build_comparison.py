from pathlib import Path
import datetime

BASE = Path(__file__).resolve().parents[2]
REPORTS = BASE / "reports"
REPORTS.mkdir(exist_ok=True, parents=True)

def list_tree(root: Path) -> str:
    out = []
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out.append(str(p.relative_to(BASE)))
    return "\n".join(out)

now = datetime.datetime.now().isoformat()
content = f"""# Build Comparison
Time: {now}

## Staging files
{list_tree(BASE/'artifacts'/'staging')}

## Published files
{list_tree(BASE/'artifacts'/'published')}
"""
(REPORTS / "COMPARISON.md").write_text(content)
print("Wrote reports/COMPARISON.md")
