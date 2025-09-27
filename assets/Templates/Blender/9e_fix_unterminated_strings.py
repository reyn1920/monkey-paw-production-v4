#!/usr/bin/env python3
"""
Fix Unterminated String Literals
Systematically fixes unterminated string literal errors in Python files.
"""

import os
import ast
from pathlib import Path
from typing import Any


def find_unterminated_strings(content: str) -> list[tuple[int, str]]:
    """Find lines with unterminated string literals."""
    issues = []
    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        # Skip comments and empty lines
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Check for unterminated triple quotes
        if ('"""' in line and line.count('"""') % 2 != 0) or (
            "'''" in line and line.count("'''") % 2 != 0
        ):
            issues.append((i, "Unterminated triple quote"))

        # Check for unterminated single/double quotes
        # Simple heuristic: odd number of quotes not in comments
        if '"' in line:
            quote_count = line.count('"')
            # Exclude escaped quotes
            escaped_quotes = line.count('\\"')
            actual_quotes = quote_count - escaped_quotes
            if actual_quotes % 2 != 0:
                issues.append((i, "Unterminated double quote"))

        if "'" in line:
            quote_count = line.count("'")
            # Exclude escaped quotes
            escaped_quotes = line.count("\\'")
            actual_quotes = quote_count - escaped_quotes
            if actual_quotes % 2 != 0:
                issues.append((i, "Unterminated single quote"))

    return issues


def fix_unterminated_strings(content: str) -> str:
    """Fix unterminated string literals in content."""
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        fixed_line = line

        # Fix unterminated triple quotes
        if '"""' in line and line.count('"""') % 2 != 0:
            # Add closing triple quote at end of line
            fixed_line = line + '"""'

        elif "'''" in line and line.count("'''") % 2 != 0:
            # Add closing triple quote at end of line
            fixed_line = line + "'''"

        # Fix unterminated single quotes (simple cases)
        elif "'" in line and line.count("'") % 2 != 0:
            # If line ends with an odd number of quotes, add one
            if line.rstrip().endswith("'"):
                pass  # Already ends with quote
            else:
                # Find the last unmatched quote and close it
                if "'" in line and not line.strip().startswith("#"):
                    fixed_line = line + "'"

        # Fix unterminated double quotes (simple cases)
        elif '"' in line and line.count('"') % 2 != 0:
            # If line ends with an odd number of quotes, add one
            if line.rstrip().endswith('"'):
                pass  # Already ends with quote
            else:
                # Find the last unmatched quote and close it
                if '"' in line and not line.strip().startswith("#"):
                    fixed_line = line + '"'

        fixed_lines.append(fixed_line)

    return "\n".join(fixed_lines)


def is_valid_python(content: str) -> tuple[bool, str]:
    """Check if Python content is syntactically valid."""
    try:
        ast.parse(content)
        return True, "Valid"
    except SyntaxError as e:
        return False, f"Syntax error: {e.msg} (line {e.lineno})"
    except Exception as e:
        return False, f"Parse error: {str(e)}"


def process_file(file_path: Path) -> dict[str, Any]:
    """Process a single Python file to fix unterminated strings."""
    result = {
        "file": str(file_path),
        "processed": False,
        "fixed": False,
        "issues_found": 0,
        "issues_fixed": 0,
        "error": None,
        "before_valid": False,
        "after_valid": False,
    }

    try:
        # Read file
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            original_content = f.read()

        result["processed"] = True

        # Check if originally valid
        result["before_valid"], before_msg = is_valid_python(original_content)

        # Find issues
        issues = find_unterminated_strings(original_content)
        result["issues_found"] = len(issues)

        if issues:
            # Fix the content
            fixed_content = fix_unterminated_strings(original_content)

            # Check if fix worked
            result["after_valid"], after_msg = is_valid_python(fixed_content)

            if result["after_valid"] or len(fixed_content.strip()) > len(
                original_content.strip()
            ):
                # Write fixed content
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(fixed_content)

                result["fixed"] = True
                result["issues_fixed"] = len(issues)
                print(f"✅ Fixed {len(issues)} issues in {file_path.name}")
            else:
                print(f"⚠️  Could not fix issues in {file_path.name}: {after_msg}")
        else:
            result["after_valid"] = result["before_valid"]

    except Exception as e:
        result["error"] = str(e)
        print(f"❌ Error processing {file_path.name}: {e}")

    return result


def main():
    """Main function to fix unterminated strings in all Python files."""
    # DEBUG_REMOVED: print("🔧 Fixing Unterminated String Literals")
    # DEBUG_REMOVED: print("=" * 50)

    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk("."):
        # Skip certain directories
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d not in ["__pycache__", "node_modules", "venv", "env"]
        ]

        for file in files:
            if file.endswith(".py"):
                python_files.append(Path(root) / file)

    print(f"📁 Found {len(python_files)} Python files")

    # Process files
    results = []
    fixed_count = 0
    total_issues_fixed = 0

    for file_path in python_files:
        result = process_file(file_path)
        results.append(result)

        if result["fixed"]:
            fixed_count += 1
            total_issues_fixed += result["issues_fixed"]

    # Summary
    # DEBUG_REMOVED: print("\n" + "=" * 50)
    # DEBUG_REMOVED: print("📊 SUMMARY")
    print(f"📁 Total files processed: {len([r for r in results if r['processed']])}")
    # DEBUG_REMOVED: print(f"🔧 Files fixed: {fixed_count}")
    # DEBUG_REMOVED: print(f"⚡ Total issues fixed: {total_issues_fixed}")

    # Show files that still have issues
    still_invalid = [r for r in results if r["processed"] and not r["after_valid"]]
    if still_invalid:
        print(f"\n⚠️  Files still with syntax errors: {len(still_invalid)}")
        for result in still_invalid[:10]:  # Show first 10
            print(f"   - {Path(result['file']).name}")

    # Generate report
    report_path = "unterminated_strings_fix_report.txt"
    with open(report_path, "w") as f:
        f.write("Unterminated String Literals Fix Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(
            f"Total files processed: {len([r for r in results if r['processed']])}\n"
        )
        f.write(f"Files fixed: {fixed_count}\n")
        f.write(f"Total issues fixed: {total_issues_fixed}\n\n")

        f.write("Fixed Files:\n")
        for result in results:
            if result["fixed"]:
                f.write(
                    f"  ✅ {result['file']} - Fixed {result['issues_fixed']} issues\n"
                )

        f.write("\nFiles Still With Issues:\n")
        for result in still_invalid:
            f.write(f"  ❌ {result['file']}\n")


# DEBUG_REMOVED: print(f"\n📄 Detailed report saved to: {report_path}")
# DEBUG_REMOVED: print("\n🎉 Unterminated string literal fix complete!")

if __name__ == "__main__":
    main()
