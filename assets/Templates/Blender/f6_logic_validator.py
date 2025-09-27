"""
LogicValidationAgent: An agent that performs deep, semantic review of code to find logical flaws.
This agent doesn't just check if the code runs; it checks if the code makes sense.
"""

from typing import Any
import ast
import re
from pathlib import Path
from trae_ai.oracle.agents import query_llm


class LogicValidationAgent:
    """
    An agent that performs a deep, semantic review of code to find logical flaws.
    """

    def __init__(self):
        self.issues_found: list[dict[str, Any]] = []
        self.recommendations: list[str] = []

    def audit_file(self, file_path: Path) -> dict[str, Any]:
        """
        Audits a single file for logical errors, missed edge cases, and architectural smells.

        Args:
            file_path: Path to the Python file to audit

        Returns:
            Dictionary containing audit results
        """
        print(f"🧐 [LogicValidator] Performing semantic audit of {file_path.name}...")

        if not file_path.exists():
            error_msg = f"❌ ERROR: File not found: {file_path}"
            print(error_msg)
            return {"error": error_msg}

        try:
            code_content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            error_msg = f"❌ ERROR: Could not read file {file_path}: {str(e)}"
            print(error_msg)
            return {"error": error_msg}

        # Perform basic static analysis first
        static_issues = self._perform_static_analysis(code_content, file_path)

        # Then perform LLM-based semantic analysis
        semantic_analysis = self._perform_semantic_analysis(code_content, file_path)

        # Combine results
        audit_results = {
            "file_path": str(file_path),
            "file_size": len(code_content),
            "line_count": len(code_content.splitlines()),
            "static_issues": static_issues,
            "semantic_analysis": semantic_analysis,
            "overall_score": self._calculate_health_score(
                static_issues, semantic_analysis
            ),
        }

        self._print_audit_report(audit_results)
        return audit_results

    def _perform_static_analysis(
        self, code_content: str, file_path: Path
    ) -> dict[str, Any]:
        """Perform basic static analysis to identify obvious issues."""
        issues: list[dict[str, Any]] = []

        try:
            # Parse the AST to find structural issues
            tree = ast.parse(code_content)

            # Check for overly long functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_lines = (node.end_lineno or node.lineno) - node.lineno
                    if func_lines > 50:
                        issues.append(
                            {
                                "type": "complexity",
                                "severity": "high",
                                "message": f"Function '{node.name}' is {func_lines} lines long (>50 lines)",
                                "line": node.lineno,
                            }
                        )

                # Check for deeply nested code
                if isinstance(node, (ast.For, ast.While, ast.If)):
                    nesting_level = self._calculate_nesting_level(node, tree)
                    if nesting_level > 4:
                        issues.append(
                            {
                                "type": "complexity",
                                "severity": "medium",
                                "message": f"Deep nesting detected (level {nesting_level})",
                                "line": node.lineno,
                            }
                        )

        except SyntaxError as e:
            issues.append(
                {
                    "type": "syntax",
                    "severity": "critical",
                    "message": f"Syntax error: {str(e)}",
                    "line": getattr(e, "lineno", 0),
                }
            )

        # Check for common anti-patterns
        issues.extend(self._check_antipatterns(code_content))

        return {
            "issues": issues,
            "total_issues": len(issues),
            "critical_issues": len([i for i in issues if i["severity"] == "critical"]),
            "high_issues": len([i for i in issues if i["severity"] == "high"]),
            "medium_issues": len([i for i in issues if i["severity"] == "medium"]),
        }

    def _perform_semantic_analysis(self, code_content: str, file_path: Path) -> str:
        """Use LLM to perform deep semantic analysis."""
        # Limit content to avoid overwhelming the LLM
        content_preview = code_content[:8000]
        if len(code_content) > 8000:
            content_preview += "\n\n... (content truncated for analysis)"

        prompt = f"""
You are a principal software architect performing a deep code review.
Analyze the following Python code from file: {file_path.name}

Do not comment on simple style issues. Focus on:

1. **Logical Flaws:** Does the code do what it appears to intend to do? Are there any subtle bugs?
2. **Missed Edge Cases:** What happens with empty lists, null inputs, or zero values?
3. **Architectural Smells:** Is the code overly complex? Should functions be broken down?
4. **Security Issues:** Are there potential security vulnerabilities?
5. **Performance Issues:** Are there obvious performance bottlenecks?

Provide your analysis as a brief, actionable report in markdown format.

```python
{content_preview}
```
"""

        return query_llm(prompt, model="llama3.1")

    def _check_antipatterns(self, code_content: str) -> list[dict[str, any]]:
        """Check for common anti-patterns in the code."""
        issues = []
        lines = code_content.splitlines()

        for i, line in enumerate(lines, 1):
            # Check for hardcoded credentials
            if re.search(
                r'(password|secret|key|token)\s*=\s*["\'][^"\']+["\']',
                line,
                re.IGNORECASE,
            ):
                issues.append(
                    {
                        "type": "security",
                        "severity": "critical",
                        "message": "Potential hardcoded credential detected",
                        "line": i,
                    }
                )

            # Check for SQL injection vulnerabilities
            if re.search(r'execute\s*\(\s*["\'].*%.*["\']', line):
                issues.append(
                    {
                        "type": "security",
                        "severity": "high",
                        "message": "Potential SQL injection vulnerability",
                        "line": i,
                    }
                )

            # Check for bare except clauses
            if re.search(r"except\s*:", line):
                issues.append(
                    {
                        "type": "error_handling",
                        "severity": "medium",
                        "message": "Bare except clause - should specify exception type",
                        "line": i,
                    }
                )

        return issues

    def _calculate_nesting_level(self, node: ast.AST, tree: ast.AST) -> int:
        """Calculate the nesting level of a node."""
        level = 0
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                if child == node:
                    if isinstance(
                        parent, (ast.For, ast.While, ast.If, ast.With, ast.Try)
                    ):
                        level += 1
        return level

    def _calculate_health_score(
        self, static_issues: dict, semantic_analysis: str
    ) -> int:
        """Calculate an overall health score for the file (0-100)."""
        base_score = 100

        # Deduct points for static issues
        base_score -= static_issues["critical_issues"] * 30
        base_score -= static_issues["high_issues"] * 15
        base_score -= static_issues["medium_issues"] * 5

        # Deduct points based on semantic analysis keywords
        if "critical" in semantic_analysis.lower():
            base_score -= 20
        if "security" in semantic_analysis.lower():
            base_score -= 15
        if "performance" in semantic_analysis.lower():
            base_score -= 10

        return max(0, base_score)

    def _print_audit_report(self, results: dict[str, any]):
        """Print a formatted audit report."""
        print("\n" + "=" * 60)
        print("🔍 SEMANTIC AUDIT REPORT")
        print("=" * 60)
        print(f"📁 File: {results['file_path']}")
        print(f"📊 Size: {results['file_size']} bytes, {results['line_count']} lines")
        print(f"🏥 Health Score: {results['overall_score']}/100")
        print()

        static = results["static_issues"]
        if static["total_issues"] > 0:
            print("🔧 STATIC ANALYSIS ISSUES:")
            print(f"   Critical: {static['critical_issues']}")
            print(f"   High: {static['high_issues']}")
            print(f"   Medium: {static['medium_issues']}")
            print()

            for issue in static["issues"][:5]:  # Show first 5 issues
                severity_emoji = {"critical": "🚨", "high": "⚠️", "medium": "💡"}.get(
                    issue["severity"], "ℹ️"
                )
                print(f"   {severity_emoji} Line {issue['line']}: {issue['message']}")

            if len(static["issues"]) > 5:
                print(f"   ... and {len(static['issues']) - 5} more issues")
            print()

        print("🧠 SEMANTIC ANALYSIS:")
        print(results["semantic_analysis"])
        print("=" * 60)

    def audit_directory(
        self, directory_path: Path, pattern: str = "*.py"
    ) -> dict[str, Any]:
        """
        Audit all Python files in a directory.

        Args:
            directory_path: Path to the directory to audit
            pattern: File pattern to match (default: *.py)

        Returns:
            Dictionary containing aggregated audit results
        """
        print(f"🔍 [LogicValidator] Auditing directory: {directory_path}")

        if not directory_path.exists() or not directory_path.is_dir():
            error_msg = f"❌ ERROR: Directory not found: {directory_path}"
            print(error_msg)
            return {"error": error_msg}

        results = {
            "directory": str(directory_path),
            "files_audited": [],
            "total_files": 0,
            "total_issues": 0,
            "average_health_score": 0,
        }

        python_files = list(directory_path.rglob(pattern))
        results["total_files"] = len(python_files)

        if not python_files:
            print("⚠️ No Python files found to audit")
            return results

        total_score = 0
        for file_path in python_files:
            if file_path.name.startswith("."):
                continue  # Skip hidden files

            file_result = self.audit_file(file_path)
            if "error" not in file_result:
                results["files_audited"].append(file_result)
                results["total_issues"] += file_result["static_issues"]["total_issues"]
                total_score += file_result["overall_score"]

        if results["files_audited"]:
            results["average_health_score"] = total_score / len(
                results["files_audited"]
            )

        print("\n📋 DIRECTORY AUDIT SUMMARY:")
        print(f"   Files audited: {len(results['files_audited'])}")
        print(f"   Total issues: {results['total_issues']}")
        print(f"   Average health score: {results['average_health_score']:.1f}/100")

        return results


if __name__ == "__main__":
    # Command the agent to audit the problematic dashboard file
    validator = LogicValidationAgent()

    # Check if dashboard.py exists in app/ directory
    dashboard_path = Path("app/dashboard.py")
    if dashboard_path.exists():
        validator.audit_file(dashboard_path)
    else:
        print("⚠️ dashboard.py not found in app/ directory")
        print("Available Python files in app/:")
        app_dir = Path("app")
        if app_dir.exists():
            for py_file in app_dir.rglob("*.py"):
                print(f"   📄 {py_file}")
