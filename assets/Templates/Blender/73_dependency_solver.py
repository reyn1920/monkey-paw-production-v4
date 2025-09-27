from pathlib import Path
from trae_ai.oracle.agents import query_llm
from trae_ai.workbench.verified_corrector import (
    VerifiedCorrector,
)  # We reuse the verifier


class DependencySolver:
    """
    An agent that resolves dependency conflicts in a requirements.txt file.
    """

    def resolve_dependencies(self, project_root: Path):
        """
        Reads, analyzes, and proposes a fixed requirements.txt file.
        """
        requirements_file = project_root / "requirements.txt"
        if not requirements_file.exists():
            print("INFO: No requirements.txt found.")
            return

        print("🧐 [DependencySolver] Analyzing dependencies for conflicts...")
        original_deps = requirements_file.read_text()

        prompt = f"""
        You are a Python dependency resolution expert. Analyze the following requirements.txt file
        for any version conflicts, security vulnerabilities, or outdated packages.
        Produce a new, clean requirements.txt file with the latest compatible and secure versions.

        Original requirements.txt:
        ---
        {original_deps}
        ---

        Return only the content of the new requirements.txt file.
        """

        proposed_deps = query_llm(prompt, model="wizardcoder:33b")

        print(
            "\n✅ [DependencySolver] A new, conflict-free dependency list has been generated."
        )

        # We now use the same self-healing logic to verify the change
        verifier = VerifiedCorrector()
        is_safe = verifier.verify_dependency_change(project_root, proposed_deps)

        if is_safe:
            requirements_file.write_text(proposed_deps)
            print(
                "🎉 [DependencySolver] Dependencies successfully resolved and verified!"
            )
        else:
            print(
                "❌ [DependencySolver] The proposed dependency changes broke the test suite. Reverting."
            )


if __name__ == "__main__":
    solver = DependencySolver()
    solver.resolve_dependencies(Path.cwd())
