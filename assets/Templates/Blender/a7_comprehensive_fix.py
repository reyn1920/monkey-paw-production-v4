import re


def fix_dashboard_syntax(file_path):
    with open(file_path) as f:
        content = f.read()

    # Fix 1: Incomplete f-strings (missing closing braces)
    # Pattern: f"...{something" without closing }
    content = re.sub(r'f"([^"]*\{[^}]*)"', r'f"\1}"', content)
    content = re.sub(r"f'([^']*\{[^}]*)'", r"f'\1}'", content)

    # Fix 2: Multi-line f-strings that got broken
    # Look for patterns like: f"text_{
    #                         more_text"
    lines = content.split("\n")
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check for broken f-string
        if re.search(r'f["\'].*\{[^}]*$', line.strip()):
            # This line has an incomplete f-string, look for continuation
            j = i + 1
            while j < len(lines) and not re.search(r'[}]["\']', lines[j]):
                j += 1

            if j < len(lines):
                # Found the closing part, merge the lines
                merged_line = line.strip()
                for k in range(i + 1, j + 1):
                    merged_line += lines[k].strip()

                # Clean up the merged line
                merged_line = re.sub(r"\s+", " ", merged_line)
                fixed_lines.append(merged_line)
                i = j + 1
                continue

        # Fix 3: Dictionary/function call bracket mismatches
        # Pattern: jsonify({ ... ) ) should be jsonify({ ... })
        if "jsonify(" in line and "{" in line:
            # Look ahead for closing pattern
            bracket_count = line.count("{") - line.count("}")
            paren_count = line.count("(") - line.count(")")

            j = i + 1
            temp_lines = [line]

            while j < len(lines) and (bracket_count > 0 or paren_count > 0):
                next_line = lines[j]
                temp_lines.append(next_line)

                bracket_count += next_line.count("{") - next_line.count("}")
                paren_count += next_line.count("(") - next_line.count(")")

                # Check for the problematic pattern: ) followed by )
                if (
                    next_line.strip() == ")"
                    and j + 1 < len(lines)
                    and lines[j + 1].strip() == ")"
                    and bracket_count > 0
                ):
                    # Fix: change first ) to }
                    temp_lines[-1] = next_line.replace(")", "}")
                    bracket_count -= 1

                j += 1

            fixed_lines.extend(temp_lines)
            i = j
            continue

        fixed_lines.append(line)
        i += 1

    # Rejoin the content
    content = "\n".join(fixed_lines)

    # Fix 4: Clean up any remaining issues
    # Remove extra quotes that might have been introduced
    content = re.sub(r'",\'', '",', content)
    content = re.sub(r"\',\"", '",', content)

    # Fix spacing issues in strftime patterns
    content = re.sub(r'"%Y % m%d_ % H%M % S"', '"%Y%m%d_%H%M%S"', content)

    with open(file_path, "w") as f:
        f.write(content)


# DEBUG_REMOVED: print(f"Applied comprehensive fixes to {file_path}")

if __name__ == "__main__":
    fix_dashboard_syntax("app/dashboard.py")
