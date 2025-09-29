#!/usr/bin/env python3
# tools/py_audit.py — quick syntax audit
import sys
import subprocess
import pathlib


def pyfiles(root="."):
    for p in pathlib.Path(root).rglob("*.py"):
        s = str(p)
        if "/.venv/" in s or "/venv/" in s:
            continue
        yield s


def audit(root="."):
    ok = True
    for f in pyfiles(root):
        try:
            subprocess.check_call(
                [sys.executable, "-m", "py_compile", f],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError:
            print(f"SYNTAX_FAIL: {f}")
            ok = False
    return ok


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(0 if audit(root) else 1)
