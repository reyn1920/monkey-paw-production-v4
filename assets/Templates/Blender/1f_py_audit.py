from __future__ import annotations

from pathlib import Path
from collections.abc import Iterable

ROOT = Path(__file__).resolve().parents[2]


def discover_py(root: Path) -> Iterable[Path]:
    for p in root.rglob("*.py"):
        # assign to `_` to avoid unused-call warnings if you had something like str(p).strip()
        _ = str(p)
        yield p


def main() -> int:
    files: list[Path] = list(discover_py(ROOT))
    messages: list[str] = []

    for path in files:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            content: str = f.read()
        # very light check example; keep logic as you like
        if "\ttab" in content:
            msg: str = f"{path}: contains literal '\\ttab'"
            messages.append(msg)

    if messages:
        print("\n".join(messages))
        return 1
    # DEBUG_REMOVED: print("py_audit: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
