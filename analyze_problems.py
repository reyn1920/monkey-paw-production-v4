#!/usr/bin/env python3
"""
Problem Analysis System - Comprehensive issue detection and analysis
"""

import os
import sys
import json
import re
import ast
import logging
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Optional
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProblemCategory(Enum):
    SYNTAX = "syntax"
    LOGIC = "logic"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    COMPATIBILITY = "compatibility"
    DOCUMENTATION = "documentation"


class ProblemSeverity(Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Problem:
    """Represents a detected problem"""

    id: str
    file_path: str
    line_number: Optional[int]
    category: ProblemCategory
    severity: ProblemSeverity
    title: str
    description: str
    recommendation: str
    code_snippet: Optional[str] = None
    affected_lines: Optional[list[int]] = None
    created_at: Optional[datetime] = None


class ProblemAnalyzer:
    """Comprehensive problem analysis system"""

    def __init__(self):
        self.problems: dict[str, Problem] = {}
        self.analysis_rules = self._load_analysis_rules()
        self.file_extensions = {".py", ".js", ".html", ".css", ".json", ".md"}

    def _load_analysis_rules(self) -> dict[str, list[dict[str, Any]]]:
        """Load analysis rules for different problem categories"""
        return {
            "syntax": [
                {
                    "pattern": r"^\s*#.*TODO|FIXME|XXX|HACK",
                    "severity": ProblemSeverity.MEDIUM,
                    "title": "TODO/FIXME comment found",
                    "description": "Code contains TODO or FIXME comments indicating incomplete work",
                    "recommendation": "Complete the TODO item or remove the comment if no longer needed",
                },
                {
                    "pattern": r"print\s*\([^)]*debug|DEBUG|Debug[^)]*\)",
                    "severity": ProblemSeverity.LOW,
                    "title": "Debug print statement",
                    "description": "Debug print statement found in code",
                    "recommendation": "Remove debug print statements before production deployment",
                },
            ],
            "security": [
                {
                    "pattern": r'password\s*=\s*["\'][^"\']+["\']',
                    "severity": ProblemSeverity.CRITICAL,
                    "title": "Hardcoded password",
                    "description": "Password appears to be hardcoded in source code",
                    "recommendation": "Use environment variables or secure configuration for passwords",
                },
                {
                    "pattern": r'api_key\s*=\s*["\'][^"\']+["\']',
                    "severity": ProblemSeverity.HIGH,
                    "title": "Hardcoded API key",
                    "description": "API key appears to be hardcoded in source code",
                    "recommendation": "Use environment variables or secure configuration for API keys",
                },
                {
                    "pattern": r"eval\s*\(",
                    "severity": ProblemSeverity.HIGH,
                    "title": "Use of eval() function",
                    "description": "eval() function can execute arbitrary code and is a security risk",
                    "recommendation": "Avoid using eval(). Use safer alternatives like ast.literal_eval()",
                },
            ],
            "performance": [
                {
                    "pattern": r"for\s+\w+\s+in\s+range\s*\(\s*len\s*\([^)]+\)\s*\)",
                    "severity": ProblemSeverity.MEDIUM,
                    "title": "Inefficient loop pattern",
                    "description": "Using range(len()) in for loop is inefficient",
                    "recommendation": "Use enumerate() or iterate directly over the collection",
                },
                {
                    "pattern": r"\+\s*=.*\[.*\]",
                    "severity": ProblemSeverity.LOW,
                    "title": "Potential inefficient list concatenation",
                    "description": "Using += with lists can be inefficient for large datasets",
                    "recommendation": "Consider using list.extend() or list comprehensions",
                },
            ],
            "maintainability": [
                {
                    "pattern": r"^.{120,}$",
                    "severity": ProblemSeverity.LOW,
                    "title": "Long line",
                    "description": "Line exceeds recommended length limit",
                    "recommendation": "Break long lines for better readability (PEP 8 recommends 79-88 characters)",
                },
                {
                    "pattern": r"def\s+\w+\s*\([^)]*\)\s*:\s*$\n(\s*.*\n){20,}",
                    "severity": ProblemSeverity.MEDIUM,
                    "title": "Long function",
                    "description": "Function is very long and may be difficult to maintain",
                    "recommendation": "Consider breaking this function into smaller, more focused functions",
                },
            ],
        }

    def analyze_file(self, file_path: str) -> list[Problem]:
        """Analyze a single file for problems"""
        problems = []

        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Get file extension
            ext = Path(file_path).suffix.lower()

            if ext == ".py":
                problems.extend(self._analyze_python_file(file_path, content))
            elif ext == ".js":
                problems.extend(self._analyze_javascript_file(file_path, content))
            elif ext == ".html":
                problems.extend(self._analyze_html_file(file_path, content))
            elif ext == ".css":
                problems.extend(self._analyze_css_file(file_path, content))

            # Run general analysis on all files
            problems.extend(self._analyze_general_patterns(file_path, content))

        except Exception as e:
            problem = Problem(
                id=f"file_error_{len(self.problems)}",
                file_path=file_path,
                line_number=None,
                category=ProblemCategory.SYNTAX,
                severity=ProblemSeverity.HIGH,
                title="File analysis error",
                description=f"Failed to analyze file: {str(e)}",
                recommendation="Check file permissions, encoding, or file corruption",
                created_at=datetime.now(),
            )
            problems.append(problem)

        # Store problems
        for problem in problems:
            self.problems[problem.id] = problem

        return problems

    def _analyze_python_file(self, file_path: str, content: str) -> list[Problem]:
        """Analyze Python-specific problems"""
        problems = []

        # Check syntax
        try:
            ast.parse(content)
        except SyntaxError as e:
            problem = Problem(
                id=f"syntax_error_{len(self.problems)}",
                file_path=file_path,
                line_number=e.lineno,
                category=ProblemCategory.SYNTAX,
                severity=ProblemSeverity.CRITICAL,
                title="Python syntax error",
                description=f"Syntax error: {e.msg}",
                recommendation="Fix the syntax error to make the code executable",
                code_snippet=self._get_code_snippet(content, e.lineno),
                created_at=datetime.now(),
            )
            problems.append(problem)

        # Check for common Python issues
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            # Check for bare except clauses
            if re.search(r"except\s*:", line):
                problem = Problem(
                    id=f"bare_except_{len(self.problems)}",
                    file_path=file_path,
                    line_number=i,
                    category=ProblemCategory.MAINTAINABILITY,
                    severity=ProblemSeverity.MEDIUM,
                    title="Bare except clause",
                    description="Bare except clause catches all exceptions, including system exits",
                    recommendation="Specify the exception type or use 'except Exception:' instead",
                    code_snippet=line.strip(),
                    created_at=datetime.now(),
                )
                problems.append(problem)

            # Check for unused imports (simple heuristic)
            import_match = re.match(r"^\s*import\s+(\w+)", line)
            if import_match:
                module_name = import_match.group(1)
                if module_name not in content[content.find(line) + len(line) :]:
                    problem = Problem(
                        id=f"unused_import_{len(self.problems)}",
                        file_path=file_path,
                        line_number=i,
                        category=ProblemCategory.MAINTAINABILITY,
                        severity=ProblemSeverity.LOW,
                        title="Potentially unused import",
                        description=f"Import '{module_name}' may not be used",
                        recommendation="Remove unused imports to keep code clean",
                        code_snippet=line.strip(),
                        created_at=datetime.now(),
                    )
                    problems.append(problem)

        return problems

    def _analyze_javascript_file(self, file_path: str, content: str) -> list[Problem]:
        """Analyze JavaScript-specific problems"""
        problems = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check for console.log statements
            if re.search(r"console\.log\s*\(", line):
                problem = Problem(
                    id=f"console_log_{len(self.problems)}",
                    file_path=file_path,
                    line_number=i,
                    category=ProblemCategory.MAINTAINABILITY,
                    severity=ProblemSeverity.LOW,
                    title="Console.log statement",
                    description="Console.log statement found in code",
                    recommendation="Remove console.log statements before production",
                    code_snippet=line.strip(),
                    created_at=datetime.now(),
                )
                problems.append(problem)

            # Check for == instead of ===
            if re.search(r"[^=!]==[^=]", line):
                problem = Problem(
                    id=f"loose_equality_{len(self.problems)}",
                    file_path=file_path,
                    line_number=i,
                    category=ProblemCategory.LOGIC,
                    severity=ProblemSeverity.MEDIUM,
                    title="Loose equality comparison",
                    description="Using == instead of === can lead to unexpected type coercion",
                    recommendation="Use === for strict equality comparison",
                    code_snippet=line.strip(),
                    created_at=datetime.now(),
                )
                problems.append(problem)

        return problems

    def _analyze_html_file(self, file_path: str, content: str) -> list[Problem]:
        """Analyze HTML-specific problems"""
        problems = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check for missing alt attributes in img tags
            if re.search(r"<img[^>]*(?!.*alt=)", line):
                problem = Problem(
                    id=f"missing_alt_{len(self.problems)}",
                    file_path=file_path,
                    line_number=i,
                    category=ProblemCategory.COMPATIBILITY,
                    severity=ProblemSeverity.MEDIUM,
                    title="Missing alt attribute",
                    description="Image tag missing alt attribute for accessibility",
                    recommendation="Add alt attribute to img tags for screen readers",
                    code_snippet=line.strip(),
                    created_at=datetime.now(),
                )
                problems.append(problem)

            # Check for inline styles
            if re.search(r'style\s*=\s*["\'][^"\']+["\']', line):
                problem = Problem(
                    id=f"inline_style_{len(self.problems)}",
                    file_path=file_path,
                    line_number=i,
                    category=ProblemCategory.MAINTAINABILITY,
                    severity=ProblemSeverity.LOW,
                    title="Inline style detected",
                    description="Inline styles make CSS harder to maintain",
                    recommendation="Move styles to external CSS files or style blocks",
                    code_snippet=line.strip(),
                    created_at=datetime.now(),
                )
                problems.append(problem)

        return problems

    def _analyze_css_file(self, file_path: str, content: str) -> list[Problem]:
        """Analyze CSS-specific problems"""
        problems = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check for !important usage
            if "!important" in line:
                problem = Problem(
                    id=f"important_usage_{len(self.problems)}",
                    file_path=file_path,
                    line_number=i,
                    category=ProblemCategory.MAINTAINABILITY,
                    severity=ProblemSeverity.LOW,
                    title="!important usage",
                    description="Overuse of !important can make CSS hard to maintain",
                    recommendation="Avoid !important when possible, use more specific selectors instead",
                    code_snippet=line.strip(),
                    created_at=datetime.now(),
                )
                problems.append(problem)

        return problems

    def _analyze_general_patterns(self, file_path: str, content: str) -> list[Problem]:
        """Analyze general patterns across all file types"""
        problems = []
        lines = content.split("\n")

        for category, rules in self.analysis_rules.items():
            for rule in rules:
                pattern = rule["pattern"]

                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        problem = Problem(
                            id=f"{category}_{len(self.problems)}",
                            file_path=file_path,
                            line_number=i,
                            category=ProblemCategory(category),
                            severity=rule["severity"],
                            title=rule["title"],
                            description=rule["description"],
                            recommendation=rule["recommendation"],
                            code_snippet=line.strip(),
                            created_at=datetime.now(),
                        )
                        problems.append(problem)

        return problems

    def _get_code_snippet(
        self, content: str, line_number: Optional[int], context: int = 2
    ) -> str:
        """Get code snippet around the specified line"""
        if line_number is None:
            return ""

        lines = content.split("\n")
        start = max(0, line_number - context - 1)
        end = min(len(lines), line_number + context)

        snippet_lines = []
        for i in range(start, end):
            marker = ">>> " if i == line_number - 1 else "    "
            snippet_lines.append(f"{marker}{i + 1}: {lines[i]}")

        return "\n".join(snippet_lines)

    def analyze_directory(
        self, directory_path: str, recursive: bool = True
    ) -> dict[str, list[Problem]]:
        """Analyze all files in a directory"""
        results = {}

        if recursive:
            for root, dirs, files in os.walk(directory_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith(".")]

                for file in files:
                    file_path = os.path.join(root, file)
                    if Path(file_path).suffix.lower() in self.file_extensions:
                        problems = self.analyze_file(file_path)
                        if problems:
                            results[file_path] = problems
        else:
            for file in os.listdir(directory_path):
                file_path = os.path.join(directory_path, file)
                if (
                    os.path.isfile(file_path)
                    and Path(file_path).suffix.lower() in self.file_extensions
                ):
                    problems = self.analyze_file(file_path)
                    if problems:
                        results[file_path] = problems

        return results

    def get_problems_by_severity(self, severity: ProblemSeverity) -> list[Problem]:
        """Get problems filtered by severity"""
        return [p for p in self.problems.values() if p.severity == severity]

    def get_problems_by_category(self, category: ProblemCategory) -> list[Problem]:
        """Get problems filtered by category"""
        return [p for p in self.problems.values() if p.category == category]

    def generate_report(self) -> dict[str, Any]:
        """Generate a comprehensive analysis report"""
        total_problems = len(self.problems)

        severity_counts = {
            severity.value: len(self.get_problems_by_severity(severity))
            for severity in ProblemSeverity
        }

        category_counts = {
            category.value: len(self.get_problems_by_category(category))
            for category in ProblemCategory
        }

        # Get top problem files
        file_problem_counts = {}
        for problem in self.problems.values():
            file_path = problem.file_path
            file_problem_counts[file_path] = file_problem_counts.get(file_path, 0) + 1

        top_files = sorted(
            file_problem_counts.items(), key=lambda x: x[1], reverse=True
        )[:10]

        return {
            "summary": {
                "total_problems": total_problems,
                "files_analyzed": len({p.file_path for p in self.problems.values()}),
                "analysis_date": datetime.now().isoformat(),
            },
            "severity_breakdown": severity_counts,
            "category_breakdown": category_counts,
            "top_problem_files": [
                {"file": file, "problems": count} for file, count in top_files
            ],
            "problems": [asdict(problem) for problem in self.problems.values()],
        }

    def export_report(self, output_file: str, format_type: str = "json") -> None:
        """Export analysis report to file"""
        report = self.generate_report()

        if format_type.lower() == "json":
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format: {format_type}")


def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_problems.py <file_or_directory> [output_file]")
        sys.exit(1)

    target = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    analyzer = ProblemAnalyzer()

    if os.path.isfile(target):
        problems = analyzer.analyze_file(target)
        print(f"Found {len(problems)} problems in {target}")

        for problem in problems:
            print(f"\n{problem.severity.value.upper()}: {problem.title}")
            print(f"  Line {problem.line_number}: {problem.description}")
            print(f"  Recommendation: {problem.recommendation}")
            if problem.code_snippet:
                print(f"  Code: {problem.code_snippet}")

    elif os.path.isdir(target):
        results = analyzer.analyze_directory(target)
        total_problems = sum(len(problems) for problems in results.values())

        print(f"Analyzed {len(results)} files, found {total_problems} problems")

        # Show summary by file
        for file_path, problems in results.items():
            print(f"\n{file_path}: {len(problems)} problems")

            # Show critical and high severity problems
            critical_high = [
                p
                for p in problems
                if p.severity in [ProblemSeverity.CRITICAL, ProblemSeverity.HIGH]
            ]
            for problem in critical_high:
                print(
                    f"  {problem.severity.value.upper()}: {problem.title} (line {problem.line_number})"
                )

        # Generate and display report
        report = analyzer.generate_report()
        print("\nSummary:")
        print(f"  Critical: {report['severity_breakdown']['critical']}")
        print(f"  High: {report['severity_breakdown']['high']}")
        print(f"  Medium: {report['severity_breakdown']['medium']}")
        print(f"  Low: {report['severity_breakdown']['low']}")

        if output_file:
            analyzer.export_report(output_file)
            print(f"\nDetailed report exported to: {output_file}")

    else:
        print(f"Error: {target} is not a valid file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
