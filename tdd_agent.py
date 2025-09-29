# trae_ai/agents/tdd_agent.py
import subprocess
from pathlib import Path
from trae_ai.agents.code_generator import (
    CodeGenerator,
)  # Assumes a powerful code-writing agent


class TDDAgent:
    """
    An agent that implements Test-Driven Development. It reads a failing test
    and writes the minimum code required to make the test pass.
    """

    def __init__(self):
        self.generator = CodeGenerator()

    def get_failing_tests(self, project_root: Path) -> str:
        """Runs pytest and captures the failure output."""
        print("🔬 [TDDAgent] Running tests to identify failures...")
        result = subprocess.run(
            ["python3", "-m", "pytest", "tests/"],
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        # We only need the failure summary for the LLM
        return result.stdout + result.stderr

    def fix_failures(self, project_root: Path):
        """Runs the full TDD cycle: test, analyze failure, generate code, repeat."""
        failure_log = self.get_failing_tests(project_root)

        if "failed" not in failure_log and "ERROR" not in failure_log:
            print("✅🎉 [TDDAgent] All tests are passing! No work to do.")
            return

        print("Analyzing test failures to generate corrective code...")

        # This is a powerful prompt that asks the AI to act like a TDD practitioner
        prompt = f""" 
        You are an expert Test-Driven Development AI. Based on the following pytest failure log, 
        identify the first major failure (e.g., the AttributeError for 'ServiceRegistry' not having 'register'). 
        
        Write the specific, minimal Python code required to fix ONLY that first failure. For example, 
        if a method is missing, add the method definition to the correct class. 
        
        Return only the new Python code for the fix. 

        Pytest Failure Log: 
        --- 
        {failure_log} 
        --- 
        """

        # This calls the code generation agent with the TDD context
        code_fix_patch = self.generator.implement_from_prompt(prompt)

        print("\n--- Generated Code Fix ---")
        print(code_fix_patch)
        print("------------------------\n")
        print("Apply this patch, then re-run the TDD agent to fix the next failure.")
        # In a fully autonomous loop, the agent would apply the patch and re-run itself.


if __name__ == "__main__":
    tdd_agent = TDDAgent()
    tdd_agent.fix_failures(Path.cwd())
