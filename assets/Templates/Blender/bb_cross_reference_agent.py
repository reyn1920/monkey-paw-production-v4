#!/usr/bin/env python3
"""
Cross-Reference Agent for Three-Way Logic Validation
Self-corrected version with proper type safety and AST handling.
"""

import ast
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class CodeSymbolExtractor(ast.NodeVisitor):
    """
    Type-safe AST visitor that correctly extracts information from code.
    Implements proper type checking before accessing node attributes.
    """

    def __init__(self):
        # CORRECT: Initialize all collections as proper lists with type hints
        self.functions: List[Dict[str, Any]] = []
        self.imports: List[str] = []
        self.calls: List[str] = []
        self.returns: List[str] = []
        self.raises: List[str] = []
        self.complexity_count: int = 1

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition and extract metadata."""
        function_info = {
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "line_start": node.lineno,
            "line_end": getattr(node, "end_lineno", node.lineno),
            "docstring": ast.get_docstring(node) or "",
        }
        self.functions.append(function_info)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit import statements."""
        if node.module:
            self.imports.append(node.module)
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statements."""
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Visit function calls with proper type checking."""
        # CORRECT: Check the type of the node before accessing attributes
        if isinstance(node.func, ast.Name):
            # This node has a '.id' attribute
            self.calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            # This node has a '.attr' attribute
            self.calls.append(node.func.attr)
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        """Visit return statements."""
        if node.value:
            if isinstance(node.value, ast.Name):
                self.returns.append(node.value.id)
            elif isinstance(node.value, ast.Attribute):
                self.returns.append(node.value.attr)
            elif isinstance(node.value, ast.Constant):
                self.returns.append(str(node.value.value))
            else:
                self.returns.append("return_value")
        self.generic_visit(node)

    def visit_Raise(self, node: ast.Raise) -> None:
        """Visit raise statements."""
        if node.exc:
            if isinstance(node.exc, ast.Name):
                self.raises.append(node.exc.id)
            elif isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
                self.raises.append(node.exc.func.id)
            else:
                self.raises.append("exception")
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        """Visit if statements for complexity calculation."""
        self.complexity_count += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        """Visit for loops for complexity calculation."""
        self.complexity_count += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        """Visit while loops for complexity calculation."""
        self.complexity_count += 1
        self.generic_visit(node)

    def visit_With(self, node: ast.With) -> None:
        """Visit with statements for complexity calculation."""
        self.complexity_count += 1
        self.generic_visit(node)


class CrossReferenceAgent:
    """
    Type-safe Cross-Reference Agent for three-way logic validation.
    Analyzes new code, tests, and quarantined code to find logical gaps.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self.app_dir = project_root / "app"
        self.tests_dir = project_root / "tests"
        self.quarantined_dir = project_root / "app_quarantined"

    def analyze_file_symbols(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file and return its symbols with type safety."""
        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content)
            extractor = CodeSymbolExtractor()
            extractor.visit(tree)

            return {
                "file_path": str(file_path),
                "functions": extractor.functions,
                "imports": extractor.imports,
                "calls": extractor.calls,
                "returns": extractor.returns,
                "raises": extractor.raises,
                "complexity": extractor.complexity_count,
            }
        except Exception as e:
            return {
                "file_path": str(file_path),
                "error": str(e),
                "functions": [],
                "imports": [],
                "calls": [],
                "returns": [],
                "raises": [],
                "complexity": 0,
            }

    def analyze_function_in_file(
        self, file_path: Path, func_name: str
    ) -> Dict[str, Any]:
        """Analyze a specific function in a file with proper error handling."""
        file_analysis = self.analyze_file_symbols(file_path)

        # Find the specific function
        target_function = None
        for func in file_analysis.get("functions", []):
            if isinstance(func, dict) and func.get("name") == func_name:
                target_function = func
                break

        if target_function:
            return {
                "found": True,
                "function": target_function,
                "file_complexity": file_analysis.get("complexity", 0),
                "file_imports": file_analysis.get("imports", []),
                "file_calls": file_analysis.get("calls", []),
            }
        else:
            return {
                "found": False,
                "function": None,
                "file_complexity": 0,
                "file_imports": [],
                "file_calls": [],
            }

    def find_test_cases(self, func_name: str) -> List[Dict[str, Any]]:
        """Find test cases that reference a specific function."""
        test_cases: List[Dict[str, Any]] = []

        if not self.tests_dir.exists():
            return test_cases

        for test_file in self.tests_dir.rglob("*.py"):
            try:
                content = test_file.read_text(encoding="utf-8")

                # Simple heuristic: look for function name in test file
                if func_name in content:
                    tree = ast.parse(content)

                    for node in ast.walk(tree):
                        if (
                            isinstance(node, ast.FunctionDef)
                            and "test" in node.name.lower()
                        ):
                            # Check if this test function references our target function
                            test_source = ast.get_source_segment(content, node)
                            if test_source and func_name in test_source:
                                test_case = {
                                    "test_name": node.name,
                                    "test_file": str(
                                        test_file.relative_to(self.tests_dir)
                                    ),
                                    "line_number": node.lineno,
                                    "assertions": self._extract_assertions(node),
                                }
                                test_cases.append(test_case)

            except Exception as e:
                # Log error but continue processing other files
                print(f"Warning: Could not analyze test file {test_file}: {e}")
                continue

        return test_cases

    def _extract_assertions(self, test_node: ast.FunctionDef) -> List[str]:
        """Extract assertion calls from a test function."""
        assertions: List[str] = []

        for node in ast.walk(test_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and "assert" in node.func.attr:
                    assertions.append(node.func.attr)
                elif isinstance(node.func, ast.Name) and node.func.id.startswith(
                    "assert"
                ):
                    assertions.append(node.func.id)

        return assertions

    def compare_implementations(self, func_name: str, file_path: str) -> Dict[str, Any]:
        """Compare function implementations across directories."""
        # Analyze new implementation
        new_file = self.app_dir / file_path
        new_analysis = (
            self.analyze_function_in_file(new_file, func_name)
            if new_file.exists()
            else {
                "found": False,
                "function": None,
                "file_complexity": 0,
                "file_imports": [],
                "file_calls": [],
            }
        )

        # Analyze quarantined implementation
        quarantined_file = self.quarantined_dir / file_path
        quarantined_analysis = (
            self.analyze_function_in_file(quarantined_file, func_name)
            if quarantined_file.exists()
            else {
                "found": False,
                "function": None,
                "file_complexity": 0,
                "file_imports": [],
                "file_calls": [],
            }
        )

        # Find related tests
        test_cases = self.find_test_cases(func_name)

        # Perform validation
        validation_issues = self._validate_implementations(
            new_analysis, quarantined_analysis, test_cases
        )

        return {
            "function_name": func_name,
            "file_path": file_path,
            "new_implementation": new_analysis,
            "quarantined_implementation": quarantined_analysis,
            "test_cases": test_cases,
            "validation_issues": validation_issues,
            "has_tests": len(test_cases) > 0,
            "has_new_impl": new_analysis["found"],
            "has_quarantined_impl": quarantined_analysis["found"],
        }

    def _validate_implementations(
        self,
        new_impl: Dict[str, Any],
        quarantined_impl: Dict[str, Any],
        test_cases: List[Dict[str, Any]],
    ) -> List[str]:
        """Validate consistency between implementations."""
        issues: List[str] = []

        # Check if function exists in new implementation
        if not new_impl["found"]:
            issues.append("Function not found in new implementation")

        # Check if tests exist
        if not test_cases:
            issues.append("No test cases found for this function")

        # Compare implementations if both exist
        if new_impl["found"] and quarantined_impl["found"]:
            new_func = new_impl["function"]
            old_func = quarantined_impl["function"]

            if new_func and old_func:
                # Check argument signature changes
                new_args = new_func.get("args", [])
                old_args = old_func.get("args", [])
                if new_args != old_args:
                    issues.append(
                        f"Function signature changed: {old_args} -> {new_args}"
                    )

        return issues

    def generate_validation_report(
        self, analysis_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate a comprehensive validation report with proper type safety."""
        total_functions = len(analysis_results)
        functions_with_tests = sum(
            1 for result in analysis_results if result.get("has_tests", False)
        )
        functions_with_issues = sum(
            1 for result in analysis_results if result.get("validation_issues", [])
        )

        coverage_score = 0.0
        if total_functions > 0:
            coverage_score = (functions_with_tests / total_functions) * 100

        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_functions_analyzed": total_functions,
                "functions_with_tests": functions_with_tests,
                "functions_with_issues": functions_with_issues,
                "coverage_score": coverage_score,
            },
            "function_analysis": analysis_results,
        }

    def run_full_analysis(self, output_file: Optional[str] = None) -> Dict[str, Any]:
        """Run complete three-way validation analysis."""
        print(
            "🔍 [CrossReferenceAgent] Starting type-safe three-way validation analysis..."
        )

        analysis_results: List[Dict[str, Any]] = []

        # Analyze all Python files in app directory
        if self.app_dir.exists():
            for py_file in self.app_dir.rglob("*.py"):
                try:
                    file_symbols = self.analyze_file_symbols(py_file)

                    for func_info in file_symbols.get("functions", []):
                        if isinstance(func_info, dict) and "name" in func_info:
                            relative_path = py_file.relative_to(self.app_dir)
                            comparison = self.compare_implementations(
                                func_info["name"], str(relative_path)
                            )
                            analysis_results.append(comparison)

                except Exception as e:
                    print(f"Error processing {py_file}: {e}")

        # Generate report
        report = self.generate_validation_report(analysis_results)

        # Save report if output file specified
        if output_file:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
            print(f"✅ Validation report saved to {output_file}")

        # Print summary
        summary = report["summary"]
        print("\n📊 Analysis Summary:")
        print(f"   Functions analyzed: {summary['total_functions_analyzed']}")
        print(f"   Functions with tests: {summary['functions_with_tests']}")
        print(f"   Functions with issues: {summary['functions_with_issues']}")
        print(f"   Coverage score: {summary['coverage_score']:.2f}%")

        return report


if __name__ == "__main__":
    agent = CrossReferenceAgent(Path.cwd())
    agent.run_full_analysis("reports/cross_reference_analysis.json")
