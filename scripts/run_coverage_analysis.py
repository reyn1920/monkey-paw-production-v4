# scripts/run_coverage_analysis.py
import json
import subprocess
from pathlib import Path


class TestCoverageAgent:
    """
    An agent that analyzes the test suite to find untested code.
    """

    def __init__(self, project_root: Path):
        self.root = project_root

    def generate_coverage_report(self):
        """
        Runs the test suite with coverage and generates an HTML report.
        Requires 'pytest-cov' to be installed: pip install pytest-cov
        """
        print("📊 [TestCoverageAgent] Running test suite to generate coverage report...")

        report_dir = self.root / "reports/coverage"
        report_dir.mkdir(parents=True, exist_ok=True)

        # This command runs pytest and tells it to measure coverage for the 'app' directory
        cmd = [
            "python3",
            "-m",
            "pytest",
            f"--cov={self.root / 'app'}",
            f"--cov-report=html:{report_dir}",
            f"--cov-report=json:{report_dir / 'coverage.json'}",
            "--cov-report=term-missing",
            "--cov-fail-under=0",  # Don't fail on low coverage, just report
        ]

        try:
            result = subprocess.run(cmd, check=False, cwd=self.root, capture_output=True, text=True)

            print(f"\n✅ SUCCESS: Coverage report generated at {report_dir / 'index.html'}")
            print("Open this file in your browser to see all untested code.")

            # Parse and display coverage summary
            self._display_coverage_summary(report_dir)

            return True

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(
                f"❌ ERROR: Could not generate coverage report. Is pytest-cov installed? Error: {e}"
            )
            return False

    def _display_coverage_summary(self, report_dir: Path):
        """Display a summary of coverage results"""
        json_file = report_dir / "coverage.json"

        if json_file.exists():
            try:
                with open(json_file, "r") as f:
                    coverage_data = json.load(f)

                total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
                print(f"\n📈 Overall Coverage: {total_coverage:.1f}%")

                # Find files with low coverage
                files = coverage_data.get("files", {})
                low_coverage_files = []

                for file_path, file_data in files.items():
                    coverage_percent = file_data.get("summary", {}).get("percent_covered", 0)
                    if coverage_percent < 80:  # Files with less than 80% coverage
                        low_coverage_files.append((file_path, coverage_percent))

                if low_coverage_files:
                    print("\n🔍 Files needing attention (< 80% coverage):")
                    for file_path, coverage in sorted(low_coverage_files, key=lambda x: x[1]):
                        print(f"  • {file_path}: {coverage:.1f}%")

            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠️  Could not parse coverage JSON: {e}")

    def find_untested_functions(self):
        """
        Analyze the coverage report to find specific untested functions
        """
        print("\n🔍 [TestCoverageAgent] Analyzing untested functions...")

        # Run coverage with branch analysis
        cmd = [
            "python3",
            "-m",
            "pytest",
            f"--cov={self.root / 'app'}",
            "--cov-report=term-missing",
            "--cov-branch",
            "--tb=no",
            "-q",
        ]

        try:
            result = subprocess.run(cmd, cwd=self.root, capture_output=True, text=True)

            # Parse the output to find missing lines
            lines = result.stdout.split("\n")
            missing_coverage = []

            for line in lines:
                if "TOTAL" not in line and "%" in line and "Missing" in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        file_name = parts[0]
                        missing_lines = parts[-1] if parts[-1] != "0" else None
                        if missing_lines and missing_lines != "0":
                            missing_coverage.append((file_name, missing_lines))

            if missing_coverage:
                print("\n📋 Detailed Missing Coverage:")
                for file_name, missing_lines in missing_coverage:
                    print(f"  • {file_name}: Lines {missing_lines}")
            else:
                print("✅ All covered code has been tested!")

        except Exception as e:
            print(f"❌ Error analyzing untested functions: {e}")


if __name__ == "__main__":
    agent = TestCoverageAgent(Path.cwd())
    success = agent.generate_coverage_report()

    if success:
        agent.find_untested_functions()
        print("\n🎯 Next Steps:")
        print("1. Open reports/coverage/index.html in your browser")
        print("2. Review untested code sections")
        print("3. Write tests for critical untested functions")
        print("4. Run this script again to track progress")
