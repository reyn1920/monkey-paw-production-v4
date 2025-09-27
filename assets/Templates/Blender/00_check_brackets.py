#!/usr/bin/env python3
#!/usr/bin/env python3
import sys

pairs = {"(": ")", "[": "]", "{": "}"}

for path in sys.argv[1:]:
    stack = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        for ln, line in enumerate(f, 1):
            # Simple approach: just check brackets without removing strings
            for ch in line:
                if ch in pairs:
                    stack.append((ch, ln))
                elif ch in pairs.values():
                    if not stack or pairs[stack[-1][0]] != ch:
                        print(f"{path}:{ln}: unexpected '{ch}'")
                    else:
                        stack.pop()

    for ch, ln in stack:
        print(f"{path}:{ln}: missing '{pairs[ch]}' for '{ch}'")
