#!/usr/bin/env python3
"""
AI Debug Assistant - Intelligent debugging and troubleshooting system
"""

import os
import sys
import ast
import traceback
import logging
import re
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IssueType(Enum):
    SYNTAX_ERROR = "syntax_error"
    RUNTIME_ERROR = "runtime_error"
    LOGIC_ERROR = "logic_error"
    PERFORMANCE_ISSUE = "performance_issue"
    IMPORT_ERROR = "import_error"
    TYPE_ERROR = "type_error"


class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DebugIssue:
    """Represents a debugging issue"""

    id: str
    file_path: str
    line_number: Optional[int]
    issue_type: IssueType
    severity: Severity
    description: str
    suggestion: str
    code_snippet: Optional[str] = None
    stack_trace: Optional[str] = None
    created_at: Optional[datetime] = None


class AIDebugAssistant:
    """AI-powered debugging assistant"""

    def __init__(self):
        self.issues: dict[str, DebugIssue] = {}
        self.analysis_patterns = self._load_analysis_patterns()

    def _load_analysis_patterns(self) -> dict[str, dict[str, Any]]:
        """Load common error patterns and their solutions"""
        return {
            "syntax_errors": {
                "missing_colon": {
                    "pattern": r"(if|for|while|def|class|try|except|with)\s+.*[^:]$",
                    "suggestion": "Add a colon (:) at the end of the statement",
                },
                "mismatched_parentheses": {
                    "pattern": r"[\(\[\{].*[\)\]\}]",
                    "suggestion": "Check for mismatched parentheses, brackets, or braces",
                },
                "indentation_error": {
                    "pattern": r"^\s*\S",
                    "suggestion": "Check indentation - use consistent spaces or tabs",
                },
            },
            "runtime_errors": {
                "name_error": {
                    "pattern": r"name '(.+)' is not defined",
                    "suggestion": "Variable or function not defined. Check spelling and scope.",
                },
                "attribute_error": {
                    "pattern": r"'(.+)' object has no attribute '(.+)'",
                    "suggestion": "Object does not have the specified attribute. Check documentation.",
                },
                "index_error": {
                    "pattern": r"list index out of range",
                    "suggestion": "List index is out of bounds. Check list length before accessing.",
                },
            },
        }

    def analyze_file(self, file_path: str) -> list[DebugIssue]:
        """Analyze a Python file for potential issues"""
        issues = []

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Check for syntax errors
            syntax_issues = self._check_syntax(file_path, content)
            issues.extend(syntax_issues)

            # Check for common patterns
            pattern_issues = self._check_patterns(file_path, content)
            issues.extend(pattern_issues)

            # Check for code quality issues
            quality_issues = self._check_code_quality(file_path, content)
            issues.extend(quality_issues)

        except Exception as e:
            issue = DebugIssue(
                id=f"file_error_{len(self.issues)}",
                file_path=file_path,
                line_number=None,
                issue_type=IssueType.RUNTIME_ERROR,
                severity=Severity.HIGH,
                description=f"Failed to analyze file: {str(e)}",
                suggestion="Check file permissions and encoding",
                created_at=datetime.now(),
            )
            issues.append(issue)

        # Store issues
        for issue in issues:
            self.issues[issue.id] = issue

        return issues

    def _check_syntax(self, file_path: str, content: str) -> list[DebugIssue]:
        """Check for syntax errors"""
        issues = []

        try:
            ast.parse(content)
        except SyntaxError as e:
            issue = DebugIssue(
                id=f"syntax_{len(self.issues)}",
                file_path=file_path,
                line_number=e.lineno,
                issue_type=IssueType.SYNTAX_ERROR,
                severity=Severity.HIGH,
                description=f"Syntax error: {e.msg}",
                suggestion=self._get_syntax_suggestion(e.msg),
                code_snippet=self._get_code_snippet(content, e.lineno),
                created_at=datetime.now(),
            )
            issues.append(issue)

        return issues

    def _check_patterns(self, file_path: str, content: str) -> list[DebugIssue]:
        """Check for common error patterns"""
        issues = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check for common issues - debug print detection removed for production

            # Check for TODO comments
            if "TODO" in line or "FIXME" in line:
                issue = DebugIssue(
                    id=f"todo_{len(self.issues)}",
                    file_path=file_path,
                    line_number=i,
                    issue_type=IssueType.LOGIC_ERROR,
                    severity=Severity.MEDIUM,
                    description="TODO or FIXME comment found",
                    suggestion="Complete the TODO item or remove the comment",
                    code_snippet=line.strip(),
                    created_at=datetime.now(),
                )
                issues.append(issue)

        return issues

    def _check_code_quality(self, file_path: str, content: str) -> list[DebugIssue]:
        """Check for code quality issues"""
        issues = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 120:
                issue = DebugIssue(
                    id=f"long_line_{len(self.issues)}",
                    file_path=file_path,
                    line_number=i,
                    issue_type=IssueType.PERFORMANCE_ISSUE,
                    severity=Severity.LOW,
                    description=f"Line too long ({len(line)} characters)",
                    suggestion="Break long lines for better readability",
                    code_snippet=line[:50] + "..." if len(line) > 50 else line,
                    created_at=datetime.now(),
                )
                issues.append(issue)

        return issues

    def _get_syntax_suggestion(self, error_msg: str) -> str:
        """Get suggestion for syntax error"""
        suggestions = {
            "invalid syntax": "Check for missing colons, parentheses, or quotes",
            "unexpected EOF": "Check for unclosed parentheses, brackets, or quotes",
            "indentation": "Use consistent indentation (spaces or tabs, not both)",
            "unindent": "Check indentation levels match the code structure",
        }

        for key, suggestion in suggestions.items():
            if key.lower() in error_msg.lower():
                return suggestion

        return "Review the syntax around the indicated line"

    def _get_code_snippet(
        self, content: str, line_number: Optional[int], context: int = 2
    ) -> str:
        """Get code snippet around the error line"""
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

    def analyze_exception(
        self, exception: Exception, file_path: str = ""
    ) -> DebugIssue:
        """Analyze a runtime exception"""
        exc_type = type(exception).__name__
        exc_msg = str(exception)
        stack_trace = traceback.format_exc()

        # Determine issue type
        issue_type_map = {
            "SyntaxError": IssueType.SYNTAX_ERROR,
            "NameError": IssueType.RUNTIME_ERROR,
            "TypeError": IssueType.TYPE_ERROR,
            "ImportError": IssueType.IMPORT_ERROR,
            "ModuleNotFoundError": IssueType.IMPORT_ERROR,
        }

        issue_type = issue_type_map.get(exc_type, IssueType.RUNTIME_ERROR)

        issue = DebugIssue(
            id=f"exception_{len(self.issues)}",
            file_path=file_path,
            line_number=None,
            issue_type=issue_type,
            severity=Severity.HIGH,
            description=f"{exc_type}: {exc_msg}",
            suggestion=self._get_exception_suggestion(exc_type, exc_msg),
            stack_trace=stack_trace,
            created_at=datetime.now(),
        )

        self.issues[issue.id] = issue
        return issue

    def _get_exception_suggestion(self, exc_type: str, exc_msg: str) -> str:
        """Get suggestion for runtime exception"""
        suggestions = {
            "NameError": "Check if the variable or function is defined and in scope",
            "TypeError": "Check data types and function arguments",
            "ImportError": "Check if the module is installed and the import path is correct",
            "AttributeError": "Check if the object has the specified attribute or method",
            "IndexError": "Check list/array bounds before accessing elements",
            "KeyError": "Check if the dictionary key exists before accessing",
            "FileNotFoundError": "Check if the file path is correct and the file exists",
        }

        return suggestions.get(
            exc_type, "Review the error message and stack trace for clues"
        )

    def get_issues_by_severity(self, severity: Severity) -> list[DebugIssue]:
        """Get issues filtered by severity"""
        return [issue for issue in self.issues.values() if issue.severity == severity]

    def get_issues_by_type(self, issue_type: IssueType) -> list[DebugIssue]:
        """Get issues filtered by type"""
        return [
            issue for issue in self.issues.values() if issue.issue_type == issue_type
        ]

    def generate_report(self) -> dict[str, Any]:
        """Generate a comprehensive debug report"""
        return {
            "total_issues": len(self.issues),
            "by_severity": {
                "critical": len(self.get_issues_by_severity(Severity.CRITICAL)),
                "high": len(self.get_issues_by_severity(Severity.HIGH)),
                "medium": len(self.get_issues_by_severity(Severity.MEDIUM)),
                "low": len(self.get_issues_by_severity(Severity.LOW)),
            },
            "by_type": {
                issue_type.value: len(self.get_issues_by_type(issue_type))
                for issue_type in IssueType
            },
            "issues": [asdict(issue) for issue in self.issues.values()],
        }


# Global debug assistant instance
debug_assistant = AIDebugAssistant()


def analyze_code_file(file_path: str) -> list[dict[str, Any]]:
    """Convenience function to analyze a single file"""
    issues = debug_assistant.analyze_file(file_path)
    return [asdict(issue) for issue in issues]


def debug_exception(exception: Exception, file_path: str = "") -> dict[str, Any]:
    """Convenience function to debug an exception"""
    issue = debug_assistant.analyze_exception(exception, file_path)
    return asdict(issue)


def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python ai_debug_assistant.py <file_or_directory>")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        issues = debug_assistant.analyze_file(target)
        print(f"Found {len(issues)} issues in {target}")

        for issue in issues:
            print(f"\n{issue.severity.value.upper()}: {issue.description}")
            print(f"  Line {issue.line_number}: {issue.suggestion}")
            if issue.code_snippet:
                print(f"  Code: {issue.code_snippet}")

    elif os.path.isdir(target):
        total_issues = 0
        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    issues = debug_assistant.analyze_file(file_path)
                    total_issues += len(issues)

                    if issues:
                        print(f"\n{file_path}: {len(issues)} issues")

        print(f"\nTotal issues found: {total_issues}")

        # Generate report
        report = debug_assistant.generate_report()
        print("\nSummary:")
        print(f"  Critical: {report['by_severity']['critical']}")
        print(f"  High: {report['by_severity']['high']}")
        print(f"  Medium: {report['by_severity']['medium']}")
        print(f"  Low: {report['by_severity']['low']}")

    else:
        print(f"Error: {target} is not a valid file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
