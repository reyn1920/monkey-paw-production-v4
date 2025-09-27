#!/usr/bin/env python3
"""
Comprehensive bracket fixing script for dashboard.py
This script systematically fixes bracket mismatches and syntax errors.
"""

import re
import ast
import sys
from pathlib import Path


def fix_bracket_mismatches(content):
    """Fix common bracket mismatch patterns in the content."""

    # Pattern 1: Fix commented closing brackets
    # Replace patterns like:
    # #                             ),
    # with:
    #                             ),
    content = re.sub(r"^(\s*)#(\s*[)\]}],?\s*)$", r"\1\2", content, flags=re.MULTILINE)

    # Pattern 2: Fix jsonify calls with missing closing braces
    # Look for patterns like:
    # return jsonify(
    #     {
    #         "key": "value",
    # )
    # )
    # And fix to:
    # return jsonify(
    #     {
    #         "key": "value",
    #     }
    # )

    lines = content.split("\n")
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is a jsonify call
        if "return jsonify(" in line and "{" in line:
            # Start collecting the jsonify block
            jsonify_lines = [line]
            brace_count = line.count("{") - line.count("}")
            paren_count = line.count("(") - line.count(")")
            i += 1

            # Collect lines until we balance braces and parentheses
            while i < len(lines) and (brace_count > 0 or paren_count > 0):
                current_line = lines[i]
                jsonify_lines.append(current_line)

                brace_count += current_line.count("{") - current_line.count("}")
                paren_count += current_line.count("(") - current_line.count(")")

                # If we see a line with just ) or }) that doesn't balance, fix it
                stripped = current_line.strip()
                if stripped in [")", "}", "),", "},"] and (
                    brace_count < 0 or paren_count < 0
                ):
                    # This line is causing imbalance, fix it
                    if brace_count < 0 and paren_count >= 0:
                        # Need to add closing brace before parenthesis
                        indent = len(current_line) - len(current_line.lstrip())
                        if stripped == ")":
                            jsonify_lines[-1] = " " * (indent + 4) + "}"
                            jsonify_lines.append(" " * indent + ")")
                        elif stripped == "},":
                            # Already correct
                            pass
                        elif stripped == "),":
                            jsonify_lines[-1] = " " * (indent + 4) + "}"
                            jsonify_lines.append(" " * indent + ")")
                        brace_count = 0
                        paren_count = 0

                i += 1

            fixed_lines.extend(jsonify_lines)
        else:
            fixed_lines.append(line)
            i += 1

    return "\n".join(fixed_lines)


def fix_logger_calls(content):
    """Fix logger calls with missing closing parentheses."""

    # Pattern: Fix logger calls like:
    # self.logger.error(
    #     f"message"
    # )
    # where the closing ) is missing proper indentation

    lines = content.split("\n")
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is a logger call
        if "self.logger." in line and "(" in line and line.strip().endswith("("):
            # This is the start of a logger call
            logger_lines = [line]
            paren_count = line.count("(") - line.count(")")
            i += 1

            # Collect lines until we balance parentheses
            while i < len(lines) and paren_count > 0:
                current_line = lines[i]
                logger_lines.append(current_line)
                paren_count += current_line.count("(") - current_line.count(")")

                # If we see a line with just ) that's not properly indented
                if current_line.strip() == ")" and paren_count == 0:
                    # Fix the indentation
                    base_indent = len(logger_lines[0]) - len(logger_lines[0].lstrip())
                    logger_lines[-1] = " " * base_indent + ")"

                i += 1

            fixed_lines.extend(logger_lines)
        else:
            fixed_lines.append(line)
            i += 1

    return "\n".join(fixed_lines)


def validate_syntax(content):
    """Validate Python syntax and return error details if any."""
    try:
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, {
            "line": e.lineno,
            "message": e.msg,
            "text": e.text.strip() if e.text else "N/A",
        }


def main():
    """Main function to fix bracket issues in dashboard.py."""

    dashboard_path = Path("app/dashboard.py")

    if not dashboard_path.exists():
        # DEBUG_REMOVED: print(f"❌ File not found: {dashboard_path}")
        sys.exit(1)

    # Create backup
    backup_path = dashboard_path.with_suffix(".py.backup_comprehensive_final")
    # DEBUG_REMOVED: print(f"📁 Creating backup: {backup_path}")

    with open(dashboard_path, encoding="utf-8") as f:
        original_content = f.read()

    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(original_content)

    # DEBUG_REMOVED: print("🔧 Starting comprehensive bracket fixes...")

    # Apply fixes
    content = original_content

    # DEBUG_REMOVED: print("  - Fixing commented brackets...")
    content = fix_bracket_mismatches(content)

    # DEBUG_REMOVED: print("  - Fixing logger calls...")
    content = fix_logger_calls(content)

    # Additional specific fixes for common patterns
    # DEBUG_REMOVED: print("  - Applying specific pattern fixes...")

    # Fix specific patterns we've seen
    fixes = [
        # Fix source parameter calls
        (
            r'source="manual_trigger",\s*\)',
            'source="manual_trigger"\n                )',
        ),
        # Fix dictionary comprehensions with missing brackets
        (
            r"}\s*for\s+\w+\s+in\s+\w+\s*$",
            r"}\n                        for api in apis\n                    ],",
        ),
    ]

    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    # Write the fixed content
    # DEBUG_REMOVED: print("💾 Writing fixed content...")
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Validate syntax
    # DEBUG_REMOVED: print("✅ Validating syntax...")
    is_valid, error = validate_syntax(content)

    if is_valid:
        # DEBUG_REMOVED: print("🎉 ✅ dashboard.py syntax is now completely valid!")
        return True
    else:
        # DEBUG_REMOVED: print(f"❌ Syntax error still exists on line {error['line']}: {error['message']}")
        # DEBUG_REMOVED: print(f"   Text: {error['text']}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
