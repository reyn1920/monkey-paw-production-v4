#!/usr/bin/env python3
"""
Comprehensive Folder-by-Folder Production Validator

This script performs detailed validation of every folder in the production codebase,
providing specific insights and recommendations for each directory.
"""

import re
import ast
import json
from pathlib import Path
import logging
from collections import defaultdict
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class ComprehensiveFolderValidator:
    def __init__(self):
        self.folder_results: Defaultdict[str, dict[str, Any]] = defaultdict(
            lambda: {
                "total_files": 0,
                "python_files": 0,
                "js_files": 0,
                "config_files": 0,
                "syntax_valid": 0,
                "syntax_invalid": 0,
                "debug_issues": 0,
                "security_issues": 0,
                "empty_files": 0,
                "placeholder_files": 0,
                "issues": [],
                "recommendations": [],
            }
        )

        # Directories to skip entirely
        self.skip_dirs = {
            "__pycache__",
            "node_modules",
            "venv",
            "env",
            "dist",
            "build",
            "venv_stable",
            "venv_creative",
            ".git",
            ".pytest_cache",
            ".ruff_cache",
            "backup_20250916_010932",
            "url_fix_backups",
            ".trae",
            "venv311",
        }

        # Files to skip
        self.skip_files = {
            "fix_unterminated_strings.py",
            "ultimate_syntax_fixer.py",
            "final_verification.py",
            "nuclear_syntax_fixer.py",
            "production_debug_cleaner.py",
            "production_readiness_validator.py",
            "comprehensive_folder_validator.py",
        }

    def is_placeholder_file(self, content: str) -> bool:
        """Check if file is a placeholder (empty or just pass/comments)"""
        lines = [line.strip() for line in content.split("\n") if line.strip()]

        # Empty file
        if not lines:
            return True

        # Only comments and pass statements
        code_lines = [line for line in lines if not line.startswith("#")]
        if not code_lines or (len(code_lines) == 1 and code_lines[0] == "pass"):
            return True

        # Check for nuclear syntax fixer pattern
        if any("nuclear syntax fixer" in line.lower() for line in lines):
            return True

        return False

    def validate_python_syntax(self, file_path: Path) -> tuple[bool, str]:
        """Validate Python file syntax"""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if not content.strip():
                return True, "Empty file"

            ast.parse(content)
            return True, "Valid syntax"
        except SyntaxError as e:
            return False, f"Syntax error: {e.msg} (line {e.lineno})"
        except Exception as e:
            return False, f"Parse error: {str(e)}"

    def check_file_issues(self, file_path: Path) -> dict[str, Any]:
        """Check various issues in a file"""
        issues = {
            "debug_code": [],
            "security_issues": [],
            "hardcoded_secrets": [],
            "todo_comments": [],
            "import_issues": [],
        }

        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            lines = content.split("\n")

            # Debug patterns
            debug_patterns = [
                (r"print\s*\(", "print statement"),
                (r"console\.log\s*\(", "console.log"),
                (r"DEBUG\s*=\s*True", "DEBUG flag"),
                (r"pdb\.set_trace", "debugger breakpoint"),
                (r"breakpoint\s*\(", "breakpoint call"),
            ]

            # Security patterns
            security_patterns = [
                (r'password\s*=\s*["\'][^"\'\']+["\']', "hardcoded password"),
                (r'api_key\s*=\s*["\'][^"\'\']+["\']', "hardcoded API key"),
                (r'secret\s*=\s*["\'][^"\'\']+["\']', "hardcoded secret"),
                (r'token\s*=\s*["\'][^"\'\']+["\']', "hardcoded token"),
                (r"--no-sandbox", "unsafe browser flag"),
                (r"eval\s*\(", "eval usage"),
                (r"exec\s*\(", "exec usage"),
            ]

            for i, line in enumerate(lines, 1):
                # Check debug patterns
                for pattern, desc in debug_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues["debug_code"].append(f"Line {i}: {desc}")

                # Check security patterns
                for pattern, desc in security_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues["security_issues"].append(f"Line {i}: {desc}")

                # Check for TODO comments
                if re.search(r"(TODO|FIXME|HACK|XXX)", line, re.IGNORECASE):
                    issues["todo_comments"].append(f"Line {i}: {line.strip()}")

                # Check for problematic imports
                if re.search(r"from\s+\*\s+import|import\s+\*", line):
                    issues["import_issues"].append(f"Line {i}: wildcard import")

        except Exception as e:
            issues["read_error"] = str(e)

        return issues

    def analyze_folder_structure(self, folder_path: Path) -> dict[str, Any]:
        """Analyze the structure and purpose of a folder"""
        analysis: dict[str, Any] = {
            "purpose": "Unknown",
            "file_types": defaultdict(int),
            "has_init": False,
            "has_main": False,
            "has_config": False,
            "has_tests": False,
            "structure_score": 0,
        }

        try:
            files = list(folder_path.iterdir())

            for file in files:
                if file.is_file():
                    suffix = file.suffix.lower()
                    analysis["file_types"][suffix] += 1

                    # Check for important files
                    if file.name == "__init__.py":
                        analysis["has_init"] = True
                    elif file.name in ["main.py", "app.py", "index.js", "index.html"]:
                        analysis["has_main"] = True
                    elif file.name in [
                        "config.py",
                        "settings.py",
                        ".env",
                        "package.json",
                    ]:
                        analysis["has_config"] = True
                    elif "test" in file.name.lower():
                        analysis["has_tests"] = True

            # Determine folder purpose based on name and contents
            folder_name = folder_path.name.lower()
            if "test" in folder_name:
                analysis["purpose"] = "Testing"
            elif folder_name in ["api", "routers", "endpoints"]:
                analysis["purpose"] = "API/Routing"
            elif folder_name in ["models", "schemas"]:
                analysis["purpose"] = "Data Models"
            elif folder_name in ["utils", "helpers", "common"]:
                analysis["purpose"] = "Utilities"
            elif folder_name in ["static", "assets", "public"]:
                analysis["purpose"] = "Static Assets"
            elif folder_name in ["templates", "views"]:
                analysis["purpose"] = "Templates/Views"
            elif folder_name in ["config", "settings"]:
                analysis["purpose"] = "Configuration"
            elif analysis["file_types"].get(".py", 0) > 0:
                analysis["purpose"] = "Python Module"
            elif analysis["file_types"].get(".js", 0) > 0:
                analysis["purpose"] = "JavaScript Module"

            # Calculate structure score
            score = 0
            if analysis["has_init"] and analysis["file_types"].get(".py", 0) > 1:
                score += 2  # Proper Python package
            if analysis["has_main"]:
                score += 1  # Has entry point
            if analysis["has_config"]:
                score += 1  # Has configuration
            if analysis["has_tests"]:
                score += 2  # Has tests

            analysis["structure_score"] = score

        except Exception as e:
            analysis["error"] = str(e)

        return analysis

    def process_folder(self, folder_path: Path) -> None:
        """Process a single folder"""
        try:
            folder_name = str(folder_path.relative_to(Path.cwd()))
        except ValueError:
            # Handle case where folder_path is not relative to cwd
            folder_name = folder_path.name if folder_path.name != "." else "root"

        results = self.folder_results[folder_name]

        # Analyze folder structure
        structure = self.analyze_folder_structure(folder_path)
        results["structure"] = structure

        try:
            for file_path in folder_path.rglob("*"):
                if file_path.is_file() and file_path.name not in self.skip_files:
                    results["total_files"] += 1

                    # Categorize file types
                    if file_path.suffix == ".py":
                        results["python_files"] += 1

                        # Validate Python syntax
                        is_valid, msg = self.validate_python_syntax(file_path)
                        if is_valid:
                            results["syntax_valid"] += 1
                        else:
                            results["syntax_invalid"] += 1
                            results["issues"].append(f"{file_path.name}: {msg}")

                    elif file_path.suffix in [".js", ".ts", ".jsx", ".tsx"]:
                        results["js_files"] += 1

                    elif file_path.suffix in [
                        ".json",
                        ".yaml",
                        ".yml",
                        ".toml",
                        ".ini",
                    ]:
                        results["config_files"] += 1

                    # Check file content
                    try:
                        with open(file_path, encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                        if not content.strip():
                            results["empty_files"] += 1
                        elif self.is_placeholder_file(content):
                            results["placeholder_files"] += 1
                            results["issues"].append(
                                f"{file_path.name}: Placeholder file"
                            )

                        # Check for issues
                        file_issues = self.check_file_issues(file_path)
                        if file_issues["debug_code"]:
                            results["debug_issues"] += 1
                            results["issues"].extend(
                                [
                                    f"{file_path.name}: {issue}"
                                    for issue in file_issues["debug_code"]
                                ]
                            )

                        if file_issues["security_issues"]:
                            results["security_issues"] += 1
                            results["issues"].extend(
                                [
                                    f"{file_path.name}: {issue}"
                                    for issue in file_issues["security_issues"]
                                ]
                            )

                    except Exception as e:
                        results["issues"].append(
                            f"{file_path.name}: Read error - {str(e)}"
                        )

        except Exception as e:
            results["issues"].append(f"Folder processing error: {str(e)}")

        # Generate recommendations
        self.generate_folder_recommendations(folder_name, results)

    def generate_folder_recommendations(self, folder_name: str, results: dict) -> None:
        """Generate specific recommendations for a folder"""
        recommendations = []

        # Structure recommendations
        structure = results.get("structure", {})
        if structure.get("purpose") == "Python Module" and not structure.get(
            "has_init"
        ):
            recommendations.append(
                "Add __init__.py to make this a proper Python package"
            )

        if results["placeholder_files"] > 0:
            recommendations.append(
                f"Implement {results['placeholder_files']} placeholder files"
            )

        if results["syntax_invalid"] > 0:
            recommendations.append(
                f"Fix {results['syntax_invalid']} files with syntax errors"
            )

        if results["debug_issues"] > 0:
            recommendations.append(
                f"Remove debug code from {results['debug_issues']} files"
            )

        if results["security_issues"] > 0:
            recommendations.append(
                f"Address security issues in {results['security_issues']} files"
            )

        if results["empty_files"] > 0:
            recommendations.append(
                f"Review {results['empty_files']} empty files - implement or remove"
            )

        # Folder-specific recommendations
        if "api" in folder_name.lower() and structure.get("structure_score", 0) < 2:
            recommendations.append(
                "API folders should have proper structure with validation and error handling"
            )

        if "test" in folder_name.lower() and results["total_files"] == 0:
            recommendations.append("Test folders should contain actual test files")

        results["recommendations"] = recommendations

    def scan_all_folders(self, root_dir: str = ".") -> None:
        """Scan all folders in the project"""
        logger.info(f"Scanning all folders in: {root_dir}")

        root_path = Path(root_dir)

        # Process root directory
        self.process_folder(root_path)

        # Process all subdirectories
        for item in root_path.iterdir():
            if item.is_dir() and item.name not in self.skip_dirs:
                self.process_folder(item)

                # Process nested directories (one level deep)
                try:
                    for subitem in item.iterdir():
                        if subitem.is_dir() and subitem.name not in self.skip_dirs:
                            self.process_folder(subitem)
                except PermissionError:
                    continue

    def generate_comprehensive_report(self) -> str:
        """Generate a comprehensive folder-by-folder report"""
        report = ["=== COMPREHENSIVE FOLDER-BY-FOLDER VALIDATION REPORT ==="]
        report.append("")

        # Summary statistics
        total_folders = len(self.folder_results)
        total_files = sum(r["total_files"] for r in self.folder_results.values())
        total_issues = sum(len(r["issues"]) for r in self.folder_results.values())

        report.append("📊 SUMMARY:")
        report.append(f"   Folders Analyzed: {total_folders}")
        report.append(f"   Total Files: {total_files}")
        report.append(f"   Total Issues Found: {total_issues}")
        report.append("")

        # Sort folders by issue count (most problematic first)
        sorted_folders = sorted(
            self.folder_results.items(), key=lambda x: len(x[1]["issues"]), reverse=True
        )

        for folder_name, results in sorted_folders:
            if results["total_files"] == 0:
                continue  # Skip empty folders

            report.append(f"📁 {folder_name.upper()}")
            report.append(
                f"   Purpose: {results.get('structure', {}).get('purpose', 'Unknown')}"
            )
            report.append(f"   Files: {results['total_files']} total")

            if results["python_files"] > 0:
                report.append(
                    f"   Python: {results['python_files']} files ({results['syntax_valid']} valid, {results['syntax_invalid']} invalid)"
                )

            if results["js_files"] > 0:
                report.append(f"   JavaScript: {results['js_files']} files")

            if results["placeholder_files"] > 0:
                report.append(
                    f"   ⚠️  Placeholder files: {results['placeholder_files']}"
                )

            if results["debug_issues"] > 0:
                report.append(f"   🐛 Debug issues: {results['debug_issues']}")

            if results["security_issues"] > 0:
                report.append(f"   🔒 Security issues: {results['security_issues']}")

            # Show top issues
            if results["issues"]:
                report.append(f"   Issues ({len(results['issues'])}):")
                for issue in results["issues"][:5]:  # Show first 5 issues
                    report.append(f"     • {issue}")
                if len(results["issues"]) > 5:
                    report.append(f"     ... and {len(results['issues']) - 5} more")

            # Show recommendations
            if results["recommendations"]:
                report.append("   Recommendations:")
                for rec in results["recommendations"]:
                    report.append(f"     ✅ {rec}")

            report.append("")

        # Priority actions
        report.append("🎯 PRIORITY ACTIONS:")

        # Find folders with most critical issues
        critical_folders = [
            (name, results)
            for name, results in sorted_folders
            if results["syntax_invalid"] > 0 or results["security_issues"] > 0
        ]

        if critical_folders:
            report.append("   HIGH PRIORITY (Syntax/Security Issues):")
            for name, results in critical_folders[:5]:
                report.append(
                    f"     • {name}: Fix {results['syntax_invalid']} syntax + {results['security_issues']} security issues"
                )

        # Find folders with many placeholders
        placeholder_folders = [
            (name, results)
            for name, results in sorted_folders
            if results["placeholder_files"] > 2
        ]

        if placeholder_folders:
            report.append("   MEDIUM PRIORITY (Implementation Needed):")
            for name, results in placeholder_folders[:5]:
                report.append(
                    f"     • {name}: Implement {results['placeholder_files']} placeholder files"
                )

        return "\n".join(report)

    def save_detailed_report(
        self, filename: str = "comprehensive_folder_report.json"
    ) -> None:
        """Save detailed JSON report"""
        with open(filename, "w") as f:
            json.dump(dict(self.folder_results), f, indent=2, default=str)
        logger.info(f"Detailed report saved to: {filename}")


def main():
    """Main function"""
    # DEBUG_REMOVED: print("🔍 Comprehensive Folder-by-Folder Validation")
    # DEBUG_REMOVED: print("=" * 60)

    validator = ComprehensiveFolderValidator()
    validator.scan_all_folders()

    # Generate and display report
    report = validator.generate_comprehensive_report()
    # DEBUG_REMOVED: print(report)

    # Save reports
    with open("comprehensive_folder_report.txt", "w") as f:
        f.write(report)

    validator.save_detailed_report()

    # DEBUG_REMOVED: print("\n✅ Comprehensive validation complete!")
    # DEBUG_REMOVED: print("📄 Reports saved:")
    print("   • comprehensive_folder_report.txt (human-readable)")
    print("   • comprehensive_folder_report.json (detailed data)")


if __name__ == "__main__":
    main()
