import os
from pathlib import Path

# --- Configuration ---
# The root directory of the project (where this script is located)
PROJECT_ROOT = Path(__file__).parent

# The name of the output file
OUTPUT_FILENAME = "code_snapshot.md"

# List of directories to completely ignore
DIRECTORIES_TO_IGNORE = [
    ".git",
    "__pycache__",
    ".vscode",
    "venv",
    ".idea",
    "node_modules",
]

# List of specific files to ignore (for security and privacy)
FILES_TO_IGNORE = [
    ".env",
    ".env.development",
    ".env.production",
    "trae_ai.db",  # Ignore the database file
    "right_perspective.db",
    OUTPUT_FILENAME,  # Don't include the output file in itself
]

# File extensions to include in the snapshot
ALLOWED_EXTENSIONS = [
    ".py",
    ".js",
    ".html",
    ".css",
    ".json",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    "Dockerfile",
    ".sh",
]


def create_code_snapshot():
    """
    Scans the project directory, reads all relevant files, and compiles them
    into a single Markdown file for easy sharing.
    """
    print("🚀 Starting to create code snapshot for TRAE.AI...")

    with open(PROJECT_ROOT / OUTPUT_FILENAME, "w", encoding="utf-8") as output_file:
        output_file.write("# Code Snapshot for TRAE.AI\n")
        output_file.write(
            f"Generated on: {__import__('datetime').datetime.now().isoformat()}\n\n"
        )

        all_files = []
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Remove ignored directories from the walk
            dirs[:] = [d for d in dirs if d not in DIRECTORIES_TO_IGNORE]

            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(PROJECT_ROOT)

                # Check if the file should be ignored
                if file in FILES_TO_IGNORE:
                    continue

                # Check if the file extension is allowed
                if file_path.suffix in ALLOWED_EXTENSIONS or file in ALLOWED_EXTENSIONS:
                    all_files.append(relative_path)

        print(f"Found {len(all_files)} files to include.")

        # First, write the project structure
        output_file.write("## Project Structure\n\n```\n")
        for file_path in sorted(all_files):
            output_file.write(f"{str(file_path).replace(os.sep, '/')}\n")
        output_file.write("```\n\n---\n\n")

        # Then, write the content of each file
        for file_path in sorted(all_files):
            try:
                with open(PROJECT_ROOT / file_path, encoding="utf-8") as code_file:
                    content = code_file.read()

                # Determine the language for markdown code block
                lang = file_path.suffix.lstrip(".")
                if lang == "py":
                    lang = "python"
                if lang == "js":
                    lang = "javascript"

                output_file.write(
                    f"### `File: {str(file_path).replace(os.sep, '/')}`\n\n"
                )
                output_file.write(f"```{lang}\n")
                output_file.write(content)
                output_file.write("\n```\n\n---\n\n")
                print(f"  - Added: {file_path}")

            except Exception as e:
                print(f"  - ⚠️  Could not read file {file_path}: {e}")

    print(f"\n✅ Success! Snapshot created: {OUTPUT_FILENAME}")
    print("You can now upload this single file to give me full access to the code.")


if __name__ == "__main__":
    create_code_snapshot()
