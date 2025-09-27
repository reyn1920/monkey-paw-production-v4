#!/usr/bin/env python3
"""
Comprehensive bracket and syntax fixer for dashboard.py
This script systematically fixes all bracket mismatches and syntax errors.
"""

import re
import shutil
from pathlib import Path


def create_backup(file_path):
    """Create a backup of the original file."""
    backup_path = f"{file_path}.backup_comprehensive_v2"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path


def fix_jsonify_brackets(content):
    """Fix bracket mismatches in jsonify calls."""
    print("Fixing jsonify bracket mismatches...")

    # Pattern to find jsonify calls with mismatched brackets
    patterns = [
        # Fix } followed by } at end of jsonify calls
        (r"(\s+)}\s*}\s*(\)?\s*$)", r"\1}\2"),
        # Fix missing closing parenthesis in jsonify calls
        (r"jsonify\(\s*\{\s*([^}]+)\s*}\s*$", r"jsonify({\1})"),
        # Fix bracket sequences like }] or ]}
        (r"}\s*\]", r"}"),
        (r"\]\s*}", r"}"),
        # Fix double closing brackets
        (r"}}\s*$", r"}"),
        (r"\)\)\s*$", r")"),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    return content


def fix_dictionary_brackets(content):
    """Fix dictionary bracket mismatches."""
    print("Fixing dictionary bracket mismatches...")

    lines = content.split("\n")
    fixed_lines = []
    bracket_stack = []

    for i, line in enumerate(lines):
        original_line = line

        # Track opening brackets
        for char in line:
            if char in "({[":
                bracket_stack.append((char, i))
            elif char in ")}]":
                if bracket_stack:
                    opening, _ = bracket_stack.pop()
                    # Check for mismatched brackets
                    expected = {"(": ")", "{": "}", "[": "]"}
                    if expected.get(opening) != char:
                        # Fix common mismatches
                        if opening == "{" and char == "]":
                            line = line.replace("]", "}", 1)
                        elif opening == "(" and char == "}":
                            line = line.replace("}", ")", 1)

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_string_literals(content):
    """Fix string literal issues."""
    print("Fixing string literal issues...")

    # Remove trailing commas and quotes after strings
    patterns = [
        (r'("[^"]*")\s*,\s*"', r"\1"),
        (r'("[^"]*")\s*"\s*,', r"\1,"),
        (r'("[^"]*")\s*"', r"\1"),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    return content


def fix_function_calls(content):
    """Fix function call bracket issues."""
    print("Fixing function call brackets...")

    # Fix Response calls and other function calls
    patterns = [
        # Fix Response calls with mismatched brackets
        (r"Response\(\s*([^)]+)\s*}\s*\)", r"Response(\1)"),
        # Fix jsonify calls
        (r"jsonify\(\s*\{\s*([^}]+)\s*}\s*\]\s*\)", r"jsonify({\1})"),
        (r"jsonify\(\s*\{\s*([^}]+)\s*\]\s*\)", r"jsonify({\1})"),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    return content


def fix_conditional_expressions(content):
    """Fix conditional expression bracket issues."""
    print("Fixing conditional expressions...")

    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        # Fix ternary operator brackets
        if "if (" in line and "else" in line:
            # Ensure proper closing of conditional expressions
            if line.count("(") > line.count(")"):
                line = line.rstrip() + ")"

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def comprehensive_bracket_fix(file_path):
    """Apply all bracket fixes comprehensively."""
    print(f"Starting comprehensive bracket fix for {file_path}")

    # Create backup
    backup_path = create_backup(file_path)

    # Read the file
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # Apply all fixes in sequence
    content = fix_string_literals(content)
    content = fix_jsonify_brackets(content)
    content = fix_dictionary_brackets(content)
    content = fix_function_calls(content)
    content = fix_conditional_expressions(content)

    # Write the fixed content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Comprehensive fixes applied to {file_path}")
    return backup_path


def syntax_check(file_path):
    """Check if the file has syntax errors."""
    import subprocess
    import sys

    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", file_path],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"✅ {file_path} syntax is now valid!")
            return True
        else:
            print(f"❌ Syntax errors still exist in {file_path}:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Error checking syntax: {e}")
        return False


if __name__ == "__main__":
    dashboard_path = "app/dashboard.py"

    if not Path(dashboard_path).exists():
        print(f"Error: {dashboard_path} not found!")
        exit(1)

    # Apply comprehensive fixes
    backup_path = comprehensive_bracket_fix(dashboard_path)

    # Check syntax
    if syntax_check(dashboard_path):
        print("🎉 All syntax errors have been resolved!")
    else:
        print("⚠️  Some syntax errors may still remain. Manual review may be needed.")
        print(f"Backup available at: {backup_path}")
