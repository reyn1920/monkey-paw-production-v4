from pathlib import Path
from trae_ai.oracle.agents import query_llm  # Uses the same local LLM


class TypeInferrer:
    """An agent that uses an LLM to add type annotations to Python code."""

    def annotate_file(self, file_path: Path):
        """Reads a Python file, adds type hints, and overwrites it."""
        print(f"🧠 [TypeInferrer] Analyzing and annotating {file_path.name}...")
        try:
            original_code = file_path.read_text()

            prompt = f"""
            You are an expert Python programmer specializing in type safety.
            Add comprehensive type annotations to the following Python code.
            - Do NOT change any logic.
            - Add all necessary imports from the `typing` module.
            - Return only the full, updated Python code block.

            ```python
            {original_code}
            ```
            """

            annotated_code = query_llm(prompt, model="wizardcoder:33b")

            # Clean the response to get only the code
            if "```python" in annotated_code:
                annotated_code = annotated_code.split("```python")[1].split("```")[0]

            file_path.write_text(annotated_code)
            print(f"✅ [TypeInferrer] Successfully annotated {file_path.name}")

        except Exception as e:
            print(f"❌ [TypeInferrer] Failed to annotate {file_path.name}: {e}")
