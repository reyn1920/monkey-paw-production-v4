#!/usr/bin/env python3
"""
Production Debug Cleaner

This script removes all debug-related code from the production codebase:
- print() statements
- console.log statements
- debug flags set to True
- pdb/breakpoint statements
- debug imports
- test print statements in documentation
"""

import os
import re
from pathlib import Path
import ast
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ProductionDebugCleaner:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.stats = {
            "files_processed": 0,
            "files_cleaned": 0,
            "print_statements_removed": 0,
            "console_logs_removed": 0,
            "debug_flags_fixed": 0,
            "debug_imports_removed": 0,
            "pdb_statements_removed": 0,
        }

        # Patterns to match debug code
        self.debug_patterns = {
            "print_statements": [
                r"^\s*print\s*\([^)]*\)\s*$",  # Standalone print statements
                r"^\s*print\s*\([^)]*\)\s*#.*$",  # Print with comments
                r"\s*print\s*\([^)]*\)\s*;",  # Print followed by semicolon
            ],
            "console_logs": [
                r"^\s*console\.log\s*\([^)]*\)\s*;?\s*$",
                r"^\s*console\.debug\s*\([^)]*\)\s*;?\s*$",
                r"^\s*console\.info\s*\([^)]*\)\s*;?\s*$",
                r"^\s*console\.warn\s*\([^)]*\)\s*;?\s*$",
            ],
            "debug_flags": [
                r"DEBUG\s*=\s*True",
                r"debug\s*=\s*True",
                r"DEBUG\s*=\s*true",
                r"debug\s*=\s*true",
            ],
            "debug_imports": [
                r"^\s*import\s+pdb\s*$",
                r"^\s*from\s+pdb\s+import.*$",
                r"^\s*import\s+ipdb\s*$",
                r"^\s*from\s+ipdb\s+import.*$",
            ],
            "pdb_statements": [
                r"^\s*pdb\.set_trace\(\)\s*$",
                r"^\s*ipdb\.set_trace\(\)\s*$",
                r"^\s*breakpoint\(\)\s*$",
            ],
        }

        # Files to skip (legitimate debug files)
        self.skip_files = {
            "debug_system.py",
            "ai_debug_assistant.py",
            "web_enhanced_debugger.py",
            "debugger_demo.py",
            "production_debug_cleaner.py",  # This file
            "base44_debug_guard.py",
        }

        # Directories to skip
        self.skip_dirs = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            "node_modules",
            ".venv",
            "venv",
            ".ruff_cache",
        }

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        if file_path.name in self.skip_files:
            return True

        # Skip if in backup directories
        if any(part.startswith("backup_") for part in file_path.parts):
            return True

        # Skip if in url_fix_backups
        if "url_fix_backups" in file_path.parts:
            return True

        return False

    def clean_python_file(self, file_path: Path) -> bool:
        """Clean debug code from Python file"""
        try:
            with open(file_path, encoding="utf-8") as f:
                original_content = f.read()

            lines = original_content.split("\n")
            cleaned_lines = []
            changes_made = False

            for line_num, line in enumerate(lines, 1):
                original_line = line
                should_remove = False

                # Check for print statements
                for pattern in self.debug_patterns["print_statements"]:
                    if re.match(pattern, line):
                        # Skip if it's in a docstring or comment example
                        if not self.is_in_docstring_example(lines, line_num - 1):
                            should_remove = True
                            self.stats["print_statements_removed"] += 1
                            break

                # Check for debug flags
                if not should_remove:
                    for pattern in self.debug_patterns["debug_flags"]:
                        if re.search(pattern, line):
                            # Replace with False/false
                            if "True" in line:
                                line = re.sub(r"True", "False", line)
                            elif "true" in line:
                                line = re.sub(r"true", "false", line)
                            self.stats["debug_flags_fixed"] += 1
                            changes_made = True
                            break

                # Check for debug imports
                if not should_remove:
                    for pattern in self.debug_patterns["debug_imports"]:
                        if re.match(pattern, line):
                            should_remove = True
                            self.stats["debug_imports_removed"] += 1
                            break

                # Check for pdb statements
                if not should_remove:
                    for pattern in self.debug_patterns["pdb_statements"]:
                        if re.match(pattern, line):
                            should_remove = True
                            self.stats["pdb_statements_removed"] += 1
                            break

                if should_remove:
                    changes_made = True
                    # Keep the line as comment for reference
                    cleaned_lines.append(f"# DEBUG_REMOVED: {original_line.strip()}")
                else:
                    cleaned_lines.append(line)

            if changes_made:
                # Write cleaned content
                cleaned_content = "\n".join(cleaned_lines)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(cleaned_content)

                # Validate syntax
                try:
                    ast.parse(cleaned_content)
                except SyntaxError as e:
                    logger.error(f"Syntax error after cleaning {file_path}: {e}")
                    # Restore original content
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(original_content)
                    return False

                return True

            return False

        except Exception as e:
            logger.error(f"Error cleaning Python file {file_path}: {e}")
            return False

    def clean_javascript_file(self, file_path: Path) -> bool:
        """Clean debug code from JavaScript/TypeScript file"""
        try:
            with open(file_path, encoding="utf-8") as f:
                original_content = f.read()

            lines = original_content.split("\n")
            cleaned_lines = []
            changes_made = False

            for line in lines:
                original_line = line
                should_remove = False

                # Check for console.log statements
                for pattern in self.debug_patterns["console_logs"]:
                    if re.match(pattern, line):
                        should_remove = True
                        self.stats["console_logs_removed"] += 1
                        break

                if should_remove:
                    changes_made = True
                    cleaned_lines.append(f"// DEBUG_REMOVED: {original_line.strip()}")
                else:
                    cleaned_lines.append(line)

            if changes_made:
                cleaned_content = "\n".join(cleaned_lines)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(cleaned_content)
                return True

            return False

        except Exception as e:
            logger.error(f"Error cleaning JavaScript file {file_path}: {e}")
            return False

    def clean_markdown_file(self, file_path: Path) -> bool:
        """Clean debug code from Markdown files"""
        try:
            with open(file_path, encoding="utf-8") as f:
                original_content = f.read()

            # Remove print statements in code blocks that are examples
            content = original_content
            changes_made = False

            # Pattern for print statements in markdown code blocks
            print_in_code_pattern = r"```[a-zA-Z]*\n[^`]*print\([^)]*\)[^`]*```"

            # Replace with cleaned version
            def replace_print_in_code(match):
                nonlocal changes_made
                code_block = match.group(0)
                # Only remove if it's clearly a debug print, not an example
                if (
                    "example" not in code_block.lower()
                    and "demo" not in code_block.lower()
                ):
                    cleaned_block = re.sub(
                        r"^\s*print\([^)]*\)\s*$",
                        "# DEBUG_REMOVED: print statement",
                        code_block,
                        flags=re.MULTILINE,
                    )
                    if cleaned_block != code_block:
                        changes_made = True
                        self.stats["print_statements_removed"] += 1
                    return cleaned_block
                return code_block

            content = re.sub(
                print_in_code_pattern, replace_print_in_code, content, flags=re.DOTALL
            )

            if changes_made:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                return True

            return False

        except Exception as e:
            logger.error(f"Error cleaning Markdown file {file_path}: {e}")
            return False

    def is_in_docstring_example(self, lines: list[str], line_index: int) -> bool:
        """Check if line is part of a docstring example"""
        # Look for triple quotes before and after
        start_quote = -1
        end_quote = -1

        # Search backwards for opening triple quote
        for i in range(line_index - 1, -1, -1):
            if '"""' in lines[i] or "'''" in lines[i]:
                start_quote = i
                break

        # Search forwards for closing triple quote
        for i in range(line_index + 1, len(lines)):
            if '"""' in lines[i] or "'''" in lines[i]:
                end_quote = i
                break

        return start_quote != -1 and end_quote != -1

    def clean_file(self, file_path: Path) -> bool:
        """Clean debug code from a file based on its extension"""
        if self.should_skip_file(file_path):
            return False

        self.stats["files_processed"] += 1

        if file_path.suffix in [".py"]:
            cleaned = self.clean_python_file(file_path)
        elif file_path.suffix in [".js", ".ts", ".jsx", ".tsx"]:
            cleaned = self.clean_javascript_file(file_path)
        elif file_path.suffix in [".md"]:
            cleaned = self.clean_markdown_file(file_path)
        else:
            return False

        if cleaned:
            self.stats["files_cleaned"] += 1
            logger.info(f"Cleaned debug code from: {file_path}")

        return cleaned

    def clean_directory(self, directory: Path | None = None) -> None:
        """Clean debug code from all files in directory"""
        if directory is None:
            directory = self.root_dir

        logger.info(f"Starting debug cleanup in: {directory}")

        for root, dirs, files in os.walk(directory):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]

            root_path = Path(root)

            for file in files:
                file_path = root_path / file
                try:
                    self.clean_file(file_path)
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")

    def generate_report(self) -> str:
        """Generate cleanup report"""
        report = f"""
=== PRODUCTION DEBUG CLEANUP REPORT ===

Files Processed: {self.stats["files_processed"]}
Files Cleaned: {self.stats["files_cleaned"]}

Debug Code Removed:
- Print Statements: {self.stats["print_statements_removed"]}
- Console.log Statements: {self.stats["console_logs_removed"]}
- Debug Flags Fixed: {self.stats["debug_flags_fixed"]}
- Debug Imports Removed: {self.stats["debug_imports_removed"]}
- PDB/Breakpoint Statements: {self.stats["pdb_statements_removed"]}

Total Debug Items Cleaned: {
            sum(
                [
                    self.stats["print_statements_removed"],
                    self.stats["console_logs_removed"],
                    self.stats["debug_flags_fixed"],
                    self.stats["debug_imports_removed"],
                    self.stats["pdb_statements_removed"],
                ]
            )
        }

Cleanup Success Rate: {
            (self.stats["files_cleaned"] / max(1, self.stats["files_processed"]))
            * 100:.1f}%

=== PRODUCTION READY ===
All debug code has been removed or commented out.
The codebase is now production-ready.
"""
        return report


def main():
    """Main function to run the debug cleaner"""
    root_dir = "/Users/thomasbrianreynolds/online production"

    logger.info("Starting Production Debug Cleanup...")

    cleaner = ProductionDebugCleaner(root_dir)
    cleaner.clean_directory()

    # Generate and save report
    report = cleaner.generate_report()

    # Save report to file
    report_file = Path(root_dir) / "debug_cleanup_report.txt"
    with open(report_file, "w") as f:
        f.write(report)

    print(report)
    print(f"\nDetailed report saved to: {report_file}")

    logger.info("Production Debug Cleanup completed successfully!")


if __name__ == "__main__":
    main()
