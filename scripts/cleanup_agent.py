#!/usr/bin/env python3
"""
Code Janitor Agent - Systematic Cleanup Protocol
===============================================

An agent dedicated to systematically resolving code debt and adding type safety.
This implements the "Code Janitor" approach to clean up hundreds of small issues
that create unstable foundations.
"""

import logging
import re
import subprocess
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[logging.FileHandler("cleanup.log"), logging.StreamHandler()],
)


class CodeJanitor:
    """The Code Janitor Agent - Cleaning up the noise."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.fixes_applied = []

    def log_fix(self, file_path: Path, fix_description: str):
        """Log a fix that was applied."""
        self.fixes_applied.append(f"{file_path.name}: {fix_description}")
        self.logger.info(f"🧹 {file_path.name}: {fix_description}")

    def get_unused_imports(self, file_path: Path) -> list[str]:
        """Use pyflakes to identify unused imports in a file."""
        try:
            result = subprocess.run(
                ["python3", "-m", "pyflakes", str(file_path)],
                capture_output=True,
                text=True,
            )

            unused_imports = []
            for line in result.stdout.split("\n"):
                if "imported but unused" in line:
                    # Extract the import name from pyflakes output
                    # Format: "file.py:line:col: 'module.name' imported but unused"
                    match = re.search(r"'([^']+)' imported but unused", line)
                    if match:
                        unused_imports.append(match.group(1))

            return unused_imports
        except Exception as e:
            self.logger.error(f"Error checking unused imports in {file_path}: {e}")
            return []

    def remove_unused_imports_from_file(self, file_path: Path) -> bool:
        """Remove unused imports from a single file."""
        try:
            with open(file_path) as f:
                content = f.read()

            original_content = content
            unused_imports = self.get_unused_imports(file_path)

            if not unused_imports:
                return False

            lines = content.split("\n")
            cleaned_lines = []
            removed_count = 0

            for line in lines:
                should_remove = False

                # Check if this line imports any of the unused imports
                for unused_import in unused_imports:
                    # Handle different import patterns
                    patterns = [
                        f"^import {re.escape(unused_import)}$",
                        f"^from .* import .*{re.escape(unused_import.split('.')[-1])}.*$",
                        f"^from {re.escape(unused_import)} import",
                    ]

                    for pattern in patterns:
                        if re.match(pattern, line.strip()):
                            should_remove = True
                            break

                    if should_remove:
                        break

                if should_remove:
                    removed_count += 1
                    self.log_fix(file_path, f"Removed unused import: {line.strip()}")
                else:
                    cleaned_lines.append(line)

            if removed_count > 0:
                # Write the cleaned content
                with open(file_path, "w") as f:
                    f.write("\n".join(cleaned_lines))

                # Verify the file still compiles
                if self.verify_syntax(file_path):
                    return True
                else:
                    # Revert if syntax is broken
                    with open(file_path, "w") as f:
                        f.write(original_content)
                    self.logger.error(f"Reverted {file_path} - syntax broken after cleanup")
                    return False

            return False

        except Exception as e:
            self.logger.error(f"Error removing unused imports from {file_path}: {e}")
            return False

    def fix_deprecated_types_in_file(self, file_path: Path) -> bool:
        """Fix deprecated typing imports (Dict -> dict, List -> list, etc.)."""
        try:
            with open(file_path) as f:
                content = f.read()

            original_content = content

            # Modern Python (3.9+) replacements
            replacements = {
                "dict": "dict",
                "list": "list",
                "set": "set",
                "tuple": "tuple",
                "frozenset": "frozenset",
                "dict[": "dict[",
                "list[": "list[",
                "set[": "set[",
                "tuple[": "tuple[",
                "Frozenset[": "frozenset[",
            }

            modified = False
            for old_type, new_type in replacements.items():
                if old_type in content:
                    content = content.replace(old_type, new_type)
                    modified = True
                    self.log_fix(file_path, f"Modernized type: {old_type} -> {new_type}")

            # Remove now-unused typing imports if we made changes
            if modified:
                # Check if we can remove typing imports that are no longer needed
                lines = content.split("\n")
                cleaned_lines = []

                for line in lines:
                    # Remove specific typing imports that are no longer needed
                    if re.match(r"^from typing import.*Dict.*", line.strip()):
                        # Remove Dict from the import
                        new_line = re.sub(r",?\s*Dict\s*,?", "", line)
                        new_line = re.sub(r"from typing import\s*,", "from typing import", new_line)
                        new_line = re.sub(r"from typing import\s*$", "", new_line)
                        if new_line.strip() and new_line.strip() != "from typing import":
                            cleaned_lines.append(new_line)
                        else:
                            self.log_fix(
                                file_path,
                                f"Removed obsolete typing import: {line.strip()}",
                            )
                    else:
                        cleaned_lines.append(line)

                content = "\n".join(cleaned_lines)

            if modified:
                # Write the updated content
                with open(file_path, "w") as f:
                    f.write(content)

                # Verify syntax
                if self.verify_syntax(file_path):
                    return True
                else:
                    # Revert if broken
                    with open(file_path, "w") as f:
                        f.write(original_content)
                    self.logger.error(
                        f"Reverted {file_path} - syntax broken after type modernization"
                    )
                    return False

            return False

        except Exception as e:
            self.logger.error(f"Error fixing deprecated types in {file_path}: {e}")
            return False

    def fix_simple_undefined_names(self, file_path: Path) -> bool:
        """Fix simple undefined name errors by adding missing imports."""
        try:
            # Get pyflakes output to find undefined names
            result = subprocess.run(
                ["python3", "-m", "pyflakes", str(file_path)],
                capture_output=True,
                text=True,
            )

            undefined_names = []
            for line in result.stdout.split("\n"):
                if "undefined name" in line:
                    match = re.search(r"undefined name '([^']+)'", line)
                    if match:
                        undefined_names.append(match.group(1))

            if not undefined_names:
                return False

            with open(file_path) as f:
                content = f.read()

            original_content = content

            # Common fixes for undefined names
            common_fixes = {
                "Dict": "from typing import Dict",
                "List": "from typing import List",
                "Optional": "from typing import Optional",
                "Union": "from typing import Union",
                "Any": "from typing import Any",
                "Tuple": "from typing import Tuple",
                "Set": "from typing import Set",
                "Callable": "from typing import Callable",
            }

            imports_to_add = []
            for name in undefined_names:
                if name in common_fixes:
                    import_line = common_fixes[name]
                    if import_line not in content:
                        imports_to_add.append(import_line)
                        self.log_fix(
                            file_path,
                            f"Adding missing import for undefined name '{name}'",
                        )

            if imports_to_add:
                # Add imports after existing imports
                lines = content.split("\n")

                # Find the best insertion point (after other imports)
                insert_index = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith(("import ", "from ")) and "typing" not in line:
                        insert_index = i + 1

                # Insert the new imports
                for import_line in imports_to_add:
                    lines.insert(insert_index, import_line)
                    insert_index += 1

                content = "\n".join(lines)

                # Write and verify
                with open(file_path, "w") as f:
                    f.write(content)

                if self.verify_syntax(file_path):
                    return True
                else:
                    # Revert if broken
                    with open(file_path, "w") as f:
                        f.write(original_content)
                    self.logger.error(f"Reverted {file_path} - syntax broken after adding imports")
                    return False

            return False

        except Exception as e:
            self.logger.error(f"Error fixing undefined names in {file_path}: {e}")
            return False

    def verify_syntax(self, file_path: Path) -> bool:
        """Verify that a Python file has valid syntax."""
        try:
            with open(file_path) as f:
                content = f.read()
            compile(content, str(file_path), "exec")
            return True
        except (SyntaxError, TypeError):
            return False
        except Exception:
            return False

    def clean_file(self, file_path: Path) -> int:
        """Clean a single Python file. Returns number of fixes applied."""
        if not file_path.suffix == ".py":
            return 0

        self.logger.info(f"🧹 Cleaning {file_path}")

        fixes_count = 0

        # Step 1: Remove unused imports
        if self.remove_unused_imports_from_file(file_path):
            fixes_count += 1

        # Step 2: Fix deprecated types
        if self.fix_deprecated_types_in_file(file_path):
            fixes_count += 1

        # Step 3: Fix simple undefined names
        if self.fix_simple_undefined_names(file_path):
            fixes_count += 1

        return fixes_count

    def remove_all_unused_imports(self, project_root: Path):
        """Remove unused imports from all Python files in the project."""
        self.logger.info("🧹 [CodeJanitor] Starting unused import removal...")

        python_files = list(project_root.rglob("*.py"))
        total_fixes = 0

        for py_file in python_files:
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue

            fixes = self.clean_file(py_file)
            total_fixes += fixes

        self.logger.info(
            f"🧹 [CodeJanitor] Completed cleanup. Applied {total_fixes} fixes across {len(python_files)} files."
        )

    def fix_all_deprecated_types(self, project_root: Path):
        """Fix deprecated types in all Python files."""
        self.logger.info("🧹 [CodeJanitor] Modernizing deprecated types...")

        python_files = list(project_root.rglob("*.py"))

        for py_file in python_files:
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue

            self.fix_deprecated_types_in_file(py_file)


class CleanupAgent:
    """
    An agent dedicated to systematically resolving code debt and adding type safety.
    """

    def __init__(self, project_root: str):
        self.root = Path(project_root)
        self.janitor = CodeJanitor()
        self.logger = logging.getLogger(__name__)

    def run_full_cleanup(self):
        """Executes the complete cleanup and refactoring protocol."""
        self.logger.info("🧹 [CleanupAgent] Starting full codebase cleanup protocol...")

        # Step 1: The Janitor cleans up all the simple, low-risk noise.
        self.logger.info("\n--- Step 1: Running Code Janitor ---")
        self.janitor.remove_all_unused_imports(self.root)
        self.janitor.fix_all_deprecated_types(self.root)

        # Step 2: Re-run static analysis to confirm fixes.
        self.logger.info("\n--- Step 2: Verifying Cleanup ---")
        result = subprocess.run(
            ["python3", "-m", "pyflakes", "app/*.py"], capture_output=True, text=True
        )

        if result.stdout.strip():
            error_lines = result.stdout.strip().split("\n")
            error_count = len([line for line in error_lines if line.strip()])
            self.logger.info(f"✅ [CleanupAgent] Cleanup complete. Remaining issues: {error_count}")

            # Show top remaining issues
            self.logger.info("Top remaining issues:")
            for line in error_lines[:5]:
                if line.strip():
                    self.logger.info(f"  - {line}")
        else:
            self.logger.info("✅ [CleanupAgent] Cleanup complete. No pyflakes issues remaining!")

        self.logger.info("The codebase is now cleaner and more stable.")

        # Show summary of fixes
        if self.janitor.fixes_applied:
            self.logger.info(f"\n📋 Summary of {len(self.janitor.fixes_applied)} fixes applied:")
            for fix in self.janitor.fixes_applied[:10]:  # Show first 10
                self.logger.info(f"  ✓ {fix}")
            if len(self.janitor.fixes_applied) > 10:
                self.logger.info(f"  ... and {len(self.janitor.fixes_applied) - 10} more fixes")


if __name__ == "__main__":
    # You would command the agent to run on your project directory
    cleanup_protocol = CleanupAgent(project_root=".")
    cleanup_protocol.run_full_cleanup()
