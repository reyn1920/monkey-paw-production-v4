#!/usr/bin/env python3

with open("/Users/thomasbrianreynolds/online production/app/dashboard.py") as f:
    lines = f.readlines()

balance = 0
first_odd_line = None

for i, line in enumerate(lines, 1):
    count = line.count('"""')
    if count > 0:
        old_balance = balance
        balance += count
        print(
            f"Line {i}: {count} quotes, balance: {old_balance} -> {balance} - {line.strip()}"
        )

        # Track when balance first becomes odd
        if balance % 2 == 1 and first_odd_line is None:
            first_odd_line = i
            print(f"  *** FIRST TIME BALANCE BECOMES ODD AT LINE {i} ***")
        elif balance % 2 == 0 and first_odd_line is not None:
            print("  -> Balance restored to even")

print(f"\nFinal balance: {balance}")
if balance % 2 == 1:
    print(
        f"ERROR: Unmatched opening triple quote! First odd balance at line {first_odd_line}"
    )
else:
    print("SUCCESS: All triple quotes are matched!")
