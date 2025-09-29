#!/usr/bin/env python3

with open("/Users/thomasbrianreynolds/online production/app/dashboard.py") as f:
    lines = f.readlines()

count = 0
for i, line in enumerate(lines, 1):
    if '"""' in line:
        count += line.count('"""')
        print(f"Line {i}: {count} total quotes so far - {line.strip()}")
        if count % 2 == 1:
            print("  -> ODD NUMBER - String started")
        else:
            print("  -> EVEN NUMBER - String closed")

print(f"\nFinal count: {count}")
if count % 2 == 1:
    print("ERROR: Odd number of triple quotes - unterminated string!")
else:
    print("OK: Even number of triple quotes")
