"""
ArchitectureReviewAgent: An agent that analyzes the "big picture" of a project.
This agent looks at how all files and classes fit together and identifies architectural
problems that lead to bugs and make the code hard to maintain.
"""

from pathlib import Path
from typing import Any, Optional
import ast
import json
from collections import defaultdict, Counter
from trae_ai.oracle.agents import query_llm


class ArchitectureReviewAgent:
    """
    An agent that performs architectural analysis of a codebase to identify structural issues.
    """

    def __init__(self):
        self.project_metrics: dict[str, Any] = {}
        self.dependencies: dict[str, set[str]] = defaultdict(set)
        self.class_metrics: dict[str, dict[str, Any]] = {}
        self.file_metrics: dict[str, dict[str, Any]] = {}

    def analyze_project(
        self, project_path: Path, exclude_patterns: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """
        Perform comprehensive architectural analysis of a project.

        Args:
            project_path: Path to the project root
            exclude_patterns: List of patterns to exclude (e.g., ['test_*', '__pycache__'])

        Returns:
            Dictionary containing architectural analysis results
        """
        print(
            f"🏗️ [ArchitectureReviewer] Analyzing project architecture: {project_path.name}"
        )

        if not project_path.exists() or not project_path.is_dir():
            error_msg = f"❌ ERROR: Project directory not found: {project_path}"
            print(error_msg)
            return {"error": error_msg}

        exclude_patterns = exclude_patterns or [
            "test_*",
            "__pycache__",
            ".git",
            "node_modules",
            ".env*",
        ]

        # Collect all Python files
        python_files = self._collect_python_files(project_path, exclude_patterns)

        if not python_files:
            print("⚠️ No Python files found to analyze")
            return {"error": "No Python files found"}

        # Analyze each file
        for file_path in python_files:
            self._analyze_file(file_path, project_path)

        # Perform architectural analysis
        architectural_issues = self._identify_architectural_issues()

        # Generate LLM-based architectural review
        llm_review = self._generate_llm_architectural_review(project_path, python_files)

        results = {
            "project_path": str(project_path),
            "total_files": len(python_files),
            "project_metrics": self.project_metrics,
            "architectural_issues": architectural_issues,
            "llm_review": llm_review,
            "recommendations": self._generate_recommendations(architectural_issues),
            "health_score": self._calculate_architectural_health_score(
                architectural_issues
            ),
        }

        self._print_architectural_report(results)
        return results

    def _collect_python_files(
        self, project_path: Path, exclude_patterns: list[str]
    ) -> list[Path]:
        """Collect all Python files, excluding specified patterns."""
        python_files = []

        for py_file in project_path.rglob("*.py"):
            # Check if file should be excluded
            relative_path = py_file.relative_to(project_path)
            should_exclude = False

            for pattern in exclude_patterns:
                if pattern.replace("*", "") in str(relative_path):
                    should_exclude = True
                    break

            if not should_exclude:
                python_files.append(py_file)

        return python_files

    def _analyze_file(self, file_path: Path, project_root: Path):
        """Analyze a single Python file for architectural metrics."""
        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content)

            relative_path = str(file_path.relative_to(project_root))

            # File-level metrics
            file_metrics: dict[str, Any] = {
                "path": relative_path,
                "lines_of_code": len(content.splitlines()),
                "classes": [],
                "functions": [],
                "imports": [],
                "complexity_score": 0,
            }

            # Analyze AST nodes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = self._analyze_class(node, content)
                    file_metrics["classes"].append(class_info)
                    self.class_metrics[f"{relative_path}::{node.name}"] = class_info

                elif isinstance(node, ast.FunctionDef):
                    func_info = self._analyze_function(node, content)
                    file_metrics["functions"].append(func_info)

                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_info = self._analyze_import(node)
                    file_metrics["imports"].extend(import_info)

            # Calculate file complexity
            file_metrics["complexity_score"] = self._calculate_file_complexity(
                file_metrics
            )

            self.file_metrics[relative_path] = file_metrics

        except Exception as e:
            print(f"⚠️ Warning: Could not analyze {file_path}: {str(e)}")

    def _analyze_class(self, node: ast.ClassDef, content: str) -> dict[str, Any]:
        """Analyze a class definition."""
        methods = []
        properties = []

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = {
                    "name": item.name,
                    "line_count": (item.end_lineno or item.lineno) - item.lineno,
                    "is_private": item.name.startswith("_"),
                    "is_property": any(
                        isinstance(d, ast.Name) and d.id == "property"
                        for d in item.decorator_list
                    ),
                    "parameters": len(item.args.args),
                }

                if method_info["is_property"]:
                    properties.append(method_info)
                else:
                    methods.append(method_info)

        return {
            "name": node.name,
            "line_count": (node.end_lineno or node.lineno) - node.lineno,
            "methods": methods,
            "properties": properties,
            "method_count": len(methods),
            "property_count": len(properties),
            "inheritance": [
                base.id for base in node.bases if isinstance(base, ast.Name)
            ],
            "is_abstract": any(
                isinstance(d, ast.Name) and d.id in ["abstractmethod", "ABC"]
                for d in ast.walk(node)
            ),
        }

    def _analyze_function(self, node: ast.FunctionDef, content: str) -> dict[str, Any]:
        """Analyze a function definition."""
        return {
            "name": node.name,
            "line_count": (node.end_lineno or node.lineno) - node.lineno,
            "parameters": len(node.args.args),
            "is_private": node.name.startswith("_"),
            "has_docstring": ast.get_docstring(node) is not None,
            "cyclomatic_complexity": self._calculate_cyclomatic_complexity(node),
        }

    def _analyze_import(self, node: ast.AST) -> list[dict[str, Any]]:
        """Analyze import statements."""
        imports = []

        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    {
                        "type": "import",
                        "module": alias.name,
                        "alias": alias.asname,
                        "is_standard_library": self._is_standard_library(alias.name),
                        "is_local": alias.name.startswith("."),
                    }
                )

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(
                    {
                        "type": "from_import",
                        "module": module,
                        "name": alias.name,
                        "alias": alias.asname,
                        "is_standard_library": self._is_standard_library(module),
                        "is_local": module.startswith("."),
                    }
                )

        return imports

    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _calculate_file_complexity(self, file_metrics: dict[str, Any]) -> int:
        """Calculate overall complexity score for a file."""
        score = 0

        # Penalize large files
        if file_metrics["lines_of_code"] > 500:
            score += 3
        elif file_metrics["lines_of_code"] > 200:
            score += 1

        # Penalize too many classes in one file
        if len(file_metrics["classes"]) > 5:
            score += 2

        # Penalize complex functions
        for func in file_metrics["functions"]:
            if func.get("cyclomatic_complexity", 0) > 10:
                score += 2
            elif func.get("cyclomatic_complexity", 0) > 5:
                score += 1

        return score

    def _is_standard_library(self, module_name: str) -> bool:
        """Check if a module is part of the Python standard library."""
        # This is a simplified check - in practice, you might want a more comprehensive list
        standard_modules = {
            "os",
            "sys",
            "json",
            "ast",
            "pathlib",
            "typing",
            "collections",
            "itertools",
            "functools",
            "re",
            "datetime",
            "time",
            "math",
            "random",
            "urllib",
            "http",
            "logging",
            "unittest",
            "sqlite3",
        }

        base_module = module_name.split(".")[0]
        return base_module in standard_modules

    def _identify_architectural_issues(self) -> list[dict[str, Any]]:
        """Identify architectural issues in the codebase."""
        issues = []

        # Check for god classes (classes with too many methods/lines)
        for class_name, class_info in self.class_metrics.items():
            if class_info["method_count"] > 20:
                issues.append(
                    {
                        "type": "god_class",
                        "severity": "high",
                        "location": class_name,
                        "message": f"Class has {class_info['method_count']} methods (>20)",
                        "recommendation": "Consider breaking this class into smaller, more focused classes",
                    }
                )

            if class_info["line_count"] > 500:
                issues.append(
                    {
                        "type": "large_class",
                        "severity": "medium",
                        "location": class_name,
                        "message": f"Class has {class_info['line_count']} lines (>500)",
                        "recommendation": "Consider splitting this class or extracting functionality",
                    }
                )

        # Check for god files (files with too many lines)
        for file_path, file_info in self.file_metrics.items():
            if file_info["lines_of_code"] > 1000:
                issues.append(
                    {
                        "type": "god_file",
                        "severity": "high",
                        "location": file_path,
                        "message": f"File has {file_info['lines_of_code']} lines (>1000)",
                        "recommendation": "Consider splitting this file into multiple modules",
                    }
                )

            if len(file_info["classes"]) > 10:
                issues.append(
                    {
                        "type": "too_many_classes",
                        "severity": "medium",
                        "location": file_path,
                        "message": f"File contains {len(file_info['classes'])} classes (>10)",
                        "recommendation": "Consider organizing classes into separate files",
                    }
                )

        # Calculate project-wide metrics
        total_lines = sum(f["lines_of_code"] for f in self.file_metrics.values())
        total_classes = sum(len(f["classes"]) for f in self.file_metrics.values())
        total_functions = sum(len(f["functions"]) for f in self.file_metrics.values())

        self.project_metrics = {
            "total_lines_of_code": total_lines,
            "total_classes": total_classes,
            "total_functions": total_functions,
            "average_file_size": (
                total_lines / len(self.file_metrics) if self.file_metrics else 0
            ),
            "files_analyzed": len(self.file_metrics),
        }

        return issues

    def _generate_llm_architectural_review(
        self, project_path: Path, python_files: list[Path]
    ) -> str:
        """Generate LLM-based architectural review."""
        # Create a summary of the project structure
        structure_summary = self._create_project_structure_summary(
            python_files, project_path
        )

        # Get the largest files for detailed analysis
        largest_files = sorted(
            self.file_metrics.items(), key=lambda x: x[1]["lines_of_code"], reverse=True
        )[:3]

        largest_files_info = "\n".join(
            [
                f"- {path}: {info['lines_of_code']} lines, {len(info['classes'])} classes, {len(info['functions'])} functions"
                for path, info in largest_files
            ]
        )

        prompt = f"""
You are a senior software architect reviewing a Python project for architectural issues.

Project Overview:
- Total files: {len(python_files)}
- Total lines of code: {self.project_metrics.get("total_lines_of_code", 0)}
- Total classes: {self.project_metrics.get("total_classes", 0)}
- Total functions: {self.project_metrics.get("total_functions", 0)}

Project Structure:
{structure_summary}

Largest Files:
{largest_files_info}

Please provide an architectural review focusing on:

1. **Separation of Concerns**: Are responsibilities properly separated?
2. **Module Organization**: Is the code well-organized into logical modules?
3. **Coupling and Cohesion**: Are modules loosely coupled and highly cohesive?
4. **Scalability Issues**: What might become problematic as the project grows?
5. **Maintainability**: How easy would it be to modify or extend this codebase?

Provide specific, actionable recommendations in markdown format.
"""

        return query_llm(prompt, model="llama3.1")

    def _create_project_structure_summary(
        self, python_files: list[Path], project_root: Path
    ) -> str:
        """Create a summary of the project structure."""
        structure = defaultdict(list)

        for file_path in python_files:
            relative_path = file_path.relative_to(project_root)
            directory = (
                str(relative_path.parent)
                if relative_path.parent != Path(".")
                else "root"
            )
            structure[directory].append(relative_path.name)

        summary_lines = []
        for directory, files in sorted(structure.items()):
            summary_lines.append(f"{directory}/")
            for file in sorted(files):
                file_info = self.file_metrics.get(str(Path(directory) / file), {})
                lines = file_info.get("lines_of_code", 0)
                classes = len(file_info.get("classes", []))
                summary_lines.append(f"  - {file} ({lines} lines, {classes} classes)")

        return "\n".join(summary_lines)

    def _generate_recommendations(self, issues: list[dict[str, Any]]) -> list[str]:
        """Generate actionable recommendations based on identified issues."""
        recommendations = []

        # Group issues by type
        issue_counts = Counter(issue["type"] for issue in issues)

        if issue_counts.get("god_file", 0) > 0:
            recommendations.append(
                "🔧 Split large files: Consider breaking down files with >1000 lines into smaller, "
                "more focused modules. Each file should have a single, clear responsibility."
            )

        if issue_counts.get("god_class", 0) > 0:
            recommendations.append(
                "🏗️ Refactor large classes: Classes with >20 methods often violate the Single "
                "Responsibility Principle. Consider extracting related methods into separate classes."
            )

        if issue_counts.get("too_many_classes", 0) > 0:
            recommendations.append(
                "📁 Organize classes: Files with >10 classes should be reorganized. Group related "
                "classes into separate modules or use packages to create logical boundaries."
            )

        # Add general recommendations
        recommendations.extend(
            [
                "📋 Implement dependency injection to reduce coupling between modules",
                "🧪 Add comprehensive unit tests to ensure refactoring doesn't break functionality",
                "📚 Document architectural decisions and design patterns used in the codebase",
                "🔍 Set up automated code quality checks to prevent architectural debt",
            ]
        )

        return recommendations

    def _calculate_architectural_health_score(
        self, issues: list[dict[str, Any]]
    ) -> int:
        """Calculate an overall architectural health score (0-100)."""
        base_score = 100

        # Deduct points based on issue severity
        for issue in issues:
            if issue["severity"] == "high":
                base_score -= 15
            elif issue["severity"] == "medium":
                base_score -= 8
            elif issue["severity"] == "low":
                base_score -= 3

        # Bonus points for good practices
        if self.project_metrics.get("average_file_size", 0) < 200:
            base_score += 5

        return max(0, min(100, base_score))

    def _print_architectural_report(self, results: dict[str, Any]):
        """Print a formatted architectural analysis report."""
        print("\n" + "=" * 70)
        print("🏗️ ARCHITECTURAL ANALYSIS REPORT")
        print("=" * 70)
        print(f"📁 Project: {results['project_path']}")
        print(f"📊 Files Analyzed: {results['total_files']}")
        print(f"🏥 Architectural Health Score: {results['health_score']}/100")
        print()

        metrics = results["project_metrics"]
        print("📈 PROJECT METRICS:")
        print(f"   Total Lines of Code: {metrics.get('total_lines_of_code', 0):,}")
        print(f"   Total Classes: {metrics.get('total_classes', 0)}")
        print(f"   Total Functions: {metrics.get('total_functions', 0)}")
        print(f"   Average File Size: {metrics.get('average_file_size', 0):.1f} lines")
        print()

        issues = results["architectural_issues"]
        if issues:
            print("⚠️ ARCHITECTURAL ISSUES:")
            issue_counts = Counter(issue["severity"] for issue in issues)
            print(f"   High Severity: {issue_counts.get('high', 0)}")
            print(f"   Medium Severity: {issue_counts.get('medium', 0)}")
            print(f"   Low Severity: {issue_counts.get('low', 0)}")
            print()

            for issue in issues[:5]:  # Show first 5 issues
                severity_emoji = {"high": "🚨", "medium": "⚠️", "low": "💡"}.get(
                    issue["severity"], "ℹ️"
                )
                print(f"   {severity_emoji} {issue['location']}: {issue['message']}")

            if len(issues) > 5:
                print(f"   ... and {len(issues) - 5} more issues")
            print()

        print("🧠 ARCHITECTURAL REVIEW:")
        print(results["llm_review"])
        print()

        print("💡 RECOMMENDATIONS:")
        for i, rec in enumerate(results["recommendations"][:5], 1):
            print(f"   {i}. {rec}")

        print("=" * 70)


if __name__ == "__main__":
    # Analyze the current project
    reviewer = ArchitectureReviewAgent()

    # Analyze the project root
    project_root = Path(".")
    results = reviewer.analyze_project(project_root)

    # Save results to file for further analysis
    output_file = Path("architectural_analysis.json")
    with open(output_file, "w") as f:
        # Convert Path objects to strings for JSON serialization
        json_results = json.loads(json.dumps(results, default=str))
        json.dump(json_results, f, indent=2)

    print(f"\n📄 Detailed results saved to: {output_file}")
