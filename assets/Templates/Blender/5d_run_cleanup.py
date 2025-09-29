# scripts/run_cleanup.py
import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from trae_ai.agents.type_inferrer import TypeInferrer

PROJECT_ROOT = Path(__file__).parent.parent
APP_DIR = PROJECT_ROOT / "app"


def run_janitor_pass():
    """Runs the phase 1 automated cleanup tools."""
    print("--- Running Phase 1: Code Janitor ---")

    # Run autoflake to remove unused imports
    print("🧹 Removing unused imports...")
    try:
        subprocess.run(
            [
                "autoflake",
                "--remove-all-unused-imports",
                "--in-place",
                "--recursive",
                str(PROJECT_ROOT),
            ],
            check=True,
        )
        print("✅ Unused imports removed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Autoflake failed: {e}")

    # Run pyupgrade to modernize syntax
    print("🔧 Modernizing Python syntax...")
    try:
        # Use find to avoid argument list too long error
        subprocess.run(
            [
                "find",
                str(PROJECT_ROOT),
                "-name",
                "*.py",
                "-exec",
                "pyupgrade",
                "--py39-plus",
                "{}",
                "+",
            ],
            check=True,
        )
        print("✅ Python syntax modernized successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Pyupgrade failed: {e}")

    print("--- Phase 1 Complete ---")


def run_type_inference_pass():
    """Runs the phase 2 AI-powered type annotation."""
    print("\n--- Running Phase 2: Type Inference ---")
    inferrer = TypeInferrer()

    # We will only run it on the most problematic file for now as an example
    target_file = APP_DIR / "dashboard.py"
    if target_file.exists():
        inferrer.annotate_file(target_file)
    else:
        print(f"ERROR: Target file {target_file} not found.")

    print("--- Phase 2 Complete ---")


def run_final_validation():
    """Runs final validation to check the cleanup results."""
    print("\n--- Running Final Validation ---")

    # Check for remaining linting issues
    print("🔍 Checking for remaining linting issues...")
    try:
        result = subprocess.run(
            ["python3", "-m", "pyflakes", str(APP_DIR / "dashboard.py")],
            capture_output=True,
            text=True,
        )

        if result.stdout.strip():
            print(f"⚠️  Remaining issues found:\n{result.stdout}")
        else:
            print("✅ No linting issues found!")

    except Exception as e:
        print(f"❌ Validation failed: {e}")

    # Test compilation
    print("🧪 Testing compilation...")
    try:
        subprocess.run(
            ["python3", "-m", "py_compile", str(APP_DIR / "dashboard.py")], check=True
        )
        print("✅ Code compiles successfully!")
    except subprocess.CalledProcessError:
        print("❌ Compilation failed!")

    print("--- Final Validation Complete ---")


if __name__ == "__main__":
    print("🚀 Starting Systematic Cleanup Protocol")
    print("=" * 50)

    run_janitor_pass()
    run_type_inference_pass()
    run_final_validation()

    print("\n" + "=" * 50)
    print("✅ Systematic Cleanup Protocol Finished.")
    print("Run `pyflakes` again to see the dramatically reduced error list.")
