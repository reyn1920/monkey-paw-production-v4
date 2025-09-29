#!/usr/bin/env python3
"""
Final Verification Script - Confirm 100% Success Rate
Verifies that all Python files have valid syntax after nuclear fixing.
"""

import ast
import sys
from pathlib import Path


def verify_syntax(filepath: Path) -> tuple[bool, str]:
    """Verify syntax of a single Python file"""
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if not content.strip():
            return True, "Empty file"

        ast.parse(content)
        return True, "Valid syntax"

    except SyntaxError as e:
        return False, f"SyntaxError: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def run_final_verification():
    """Run final verification on all Python files"""
    base_dir = Path("/Users/thomasbrianreynolds/online production")

    print("Final Verification - Confirming 100% Success Rate")
    print("=" * 60)

    # Find all Python files
    all_py_files = list(base_dir.rglob("*.py"))
    total_files = len(all_py_files)

    print(f"Verifying {total_files} Python files...")

    valid_files = 0
    invalid_files = []

    # Verify each file
    for i, py_file in enumerate(all_py_files, 1):
        is_valid, message = verify_syntax(py_file)

        if is_valid:
            valid_files += 1
        else:
            invalid_files.append((str(py_file), message))

        # Progress indicator
        if i % 1000 == 0 or i == total_files:
            success_rate = (valid_files / i) * 100
            print(f"Verified {i}/{total_files} files: {success_rate:.2f}% valid")

    # Final results
    print("\n" + "=" * 60)
    print("FINAL VERIFICATION RESULTS")
    print("=" * 60)

    success_rate = (valid_files / total_files) * 100
    print(f"Total files verified: {total_files}")
    print(f"Valid files: {valid_files}")
    print(f"Invalid files: {len(invalid_files)}")
    print(f"Success rate: {success_rate:.2f}%")

    if success_rate == 100.0:
        print("\n🎉 VERIFICATION COMPLETE: 100% SUCCESS CONFIRMED! 🎉")
        print("All Python files have valid syntax.")
        success = True
    else:
        print(
            f"\n❌ VERIFICATION FAILED: {len(invalid_files)} files still have syntax errors"
        )
        print("\nInvalid files:")
        for filepath, error in invalid_files[:10]:  # Show first 10 errors
            print(f"  {filepath}: {error}")
        if len(invalid_files) > 10:
            print(f"  ... and {len(invalid_files) - 10} more files")
        success = False

    # Write detailed report
    with open("final_verification_report.txt", "w") as f:
        f.write("Final Verification Report\n")
        f.write("========================\n\n")
        f.write(f"Total files: {total_files}\n")
        f.write(f"Valid files: {valid_files}\n")
        f.write(f"Invalid files: {len(invalid_files)}\n")
        f.write(f"Success rate: {success_rate:.2f}%\n\n")

        if invalid_files:
            f.write("Invalid files:\n")
            for filepath, error in invalid_files:
                f.write(f"{filepath}: {error}\n")

    print("\nDetailed report written to final_verification_report.txt")

    return success


if __name__ == "__main__":
    success = run_final_verification()
    sys.exit(0 if success else 1)
