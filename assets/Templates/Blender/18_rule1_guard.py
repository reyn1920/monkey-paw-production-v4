from __future__ import annotations

import re
from pathlib import Path

RULE1: re.Pattern[str] = re.compile(r"do\-not\-delete", re.IGNORECASE)


def scan_paths(paths: list[Path]) -> list[str]:
    violations: list[str] = []
    for p in paths:
        if not p.is_file():
            continue
        with p.open("r", encoding="utf-8", errors="ignore") as f:
            text: str = f.read()
        if RULE1.search(text):
            violations.append(str(p))
    return violations


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    paths: list[Path] = [
        p for p in root.rglob("*") if p.suffix in {".md", ".txt", ".py", ".json"}
    ]
    bad: list[str] = scan_paths(paths)
    if bad:
        print("Rule1 guard violations (do-not-delete markers found):")
        for b in bad:
            print(" -", b)
        return 1
    print("rule1_guard: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
