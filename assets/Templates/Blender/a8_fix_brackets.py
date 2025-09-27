import re


def fix_commented_brackets(file_path):
    with open(file_path) as f:
        content = f.read()

    # Fix commented closing brackets/parentheses/braces
    # Pattern matches: # followed by optional whitespace, then closing bracket/paren/brace
    patterns = [
        (r"#\s*\}", "}"),
        (r"#\s*\)", ")"),
        (r"#\s*\]", "]"),
        (r"#\s*\),", "),"),
        (r"#\s*\},", "},"),
        (r"#\s*\],", "],"),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    with open(file_path, "w") as f:
        f.write(content)


# DEBUG_REMOVED: print(f"Fixed commented brackets in {file_path}")

if __name__ == "__main__":
    fix_commented_brackets("app/dashboard.py")
