#!/usr/bin/env python3
# tools/rule1_guard.py — scan for banned vocabulary
import sys
import pathlib
import re

BANNED = [
    r"\bproduction\b",
    r"\bProduction\b",
    r"\bPRODUCTION\b",
    r"\bsimulation\b",
    r"\bplaceholder\b",
    r"\btheoretical\b",
    r"\bdemo\b",
    r"\bmock\b",
    r"\bfake\b",
    r"\bsample\b",
    r"\btest\b",
]


def scan(root: str):
    rootp = pathlib.Path(root)
    offenders = []
    for p in rootp.rglob("*"):
        if p.is_file() and p.suffix.lower() in {
            ".py",
            ".md",
            ".txt",
            ".json",
            ".yaml",
            ".yml",
            ".js",
            ".mjs",
            ".ts",
            ".tsx",
            ".html",
            ".css",
        }:
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except:
                continue
            for pat in BANNED:
                if re.search(pat, txt):
                    offenders.append((str(p), pat))
    return offenders


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    bad = scan(root)
    if bad:
        for f, pat in bad:
            print(f"FORBIDDEN: {f} :: {pat}")
        sys.exit(2)
# DEBUG_REMOVED: print("OK")
