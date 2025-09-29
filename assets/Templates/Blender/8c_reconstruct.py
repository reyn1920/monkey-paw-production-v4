#!/usr/bin/env python3
"""
Git Time Machine Protocol - Advanced Codebase Reconstruction
Implements GitAgent to find the last good commit in Git history.
"""

import shutil
import subprocess
from pathlib import Path
from typing import Optional
import logging

# Setup logging
log_file = "reconstruction.log"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)


class GitAgent:
    """An agent for interacting with the Git repository."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_commit_history(self, file_path: Path) -> list[str]:
        """Returns a list of commit hashes for a given file, from newest to oldest."""
        try:
            cmd = ["git", "log", "--pretty=format:%H", "--", str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            commits = result.stdout.strip().split("\n")
            return [c for c in commits if c]  # Filter empty strings
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get commit history: {e}")
            return []

    def get_file_version_at_commit(self, file_path: Path, commit_hash: str) -> str:
        """Returns the content of a file at a specific commit."""
        try:
            cmd = ["git", "show", f"{commit_hash}:{file_path}"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Failed to get file version at commit {commit_hash}: {e}"
            )
            return ""

    def get_commit_info(self, commit_hash: str) -> str:
        """Get commit information (date, message)."""
        try:
            cmd = [
                "git",
                "show",
                "--no-patch",
                "--pretty=format:%cd - %s",
                "--date=short",
                commit_hash,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "Unknown commit info"


class CodebaseReconstructor:
    """Implements the Git Time Machine Protocol for codebase reconstruction."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.git_agent = GitAgent()

    def log_step(self, step: str, message: str):
        """Log a reconstruction step."""
        self.logger.info(f"[{step}] {message}")

    def syntax_check_content(self, content: str, filename: str) -> bool:
        """Check if Python content has valid syntax."""
        try:
            compile(content, filename, "exec")
            return True
        except (SyntaxError, TypeError):
            return False

    def syntax_check_file(self, file_path: Path) -> bool:
        """Check if a Python file has valid syntax."""
        try:
            with open(file_path) as f:
                content = f.read()
            return self.syntax_check_content(content, str(file_path))
        except (UnicodeDecodeError, FileNotFoundError):
            return False

    def find_last_good_commit(self, file_path: Path) -> Optional[str]:
        """Scans Git history to find the most recent syntactically valid version of a file."""
        self.log_step(
            "GIT_TIME_MACHINE", f"🔍 Scanning Git history for {file_path.name}"
        )

        try:
            commit_history = self.git_agent.get_commit_history(file_path)
            if not commit_history:
                self.log_step(
                    "GIT_TIME_MACHINE",
                    "❌ No Git history found. Is this a Git repository?",
                )
                return None

            self.log_step(
                "GIT_TIME_MACHINE",
                f"Found {len(commit_history)} commits. Scanning for last good version...",
            )
        except Exception as e:
            self.log_step("GIT_TIME_MACHINE", f"❌ Could not retrieve Git history: {e}")
            return None

        for i, commit in enumerate(commit_history):
            commit_info = self.git_agent.get_commit_info(commit)
            self.log_step(
                "GIT_TIME_MACHINE",
                f"  [{i + 1}/{len(commit_history)}] Checking commit {commit[:7]} ({commit_info})",
            )

            try:
                file_content = self.git_agent.get_file_version_at_commit(
                    file_path, commit
                )
                if not file_content:
                    self.log_step(
                        "GIT_TIME_MACHINE", "    ❌ Could not retrieve file content"
                    )
                    continue

                # Use compile() to check syntax without writing to a file
                if self.syntax_check_content(file_content, file_path.name):
                    self.log_step(
                        "GIT_TIME_MACHINE", "    ✅ Found syntactically valid version!"
                    )
                    return commit
                else:
                    self.log_step("GIT_TIME_MACHINE", "    ❌ Invalid syntax")
            except Exception as e:
                self.log_step("GIT_TIME_MACHINE", f"    ❌ Error checking commit: {e}")
                continue

        self.log_step(
            "GIT_TIME_MACHINE", "🛑 No syntactically valid version found in Git history"
        )
        return None

    def restore_from_git_commit(self, target_file: Path, commit_hash: str):
        """Restore target file from a specific Git commit."""
        self.log_step(
            "GIT_RESTORE", f"Restoring {target_file.name} from commit {commit_hash[:7]}"
        )

        # Get the good content from Git
        good_content = self.git_agent.get_file_version_at_commit(
            target_file, commit_hash
        )

        if not good_content:
            raise Exception(
                f"Could not retrieve file content from commit {commit_hash}"
            )

        # Create a final backup of the broken file before overwriting
        broken_backup_path = target_file.with_suffix(
            f"{target_file.suffix}.BROKEN_FINAL"
        )
        if target_file.exists():
            shutil.copy2(target_file, broken_backup_path)
            self.log_step(
                "GIT_RESTORE", f"📦 Backed up broken file to {broken_backup_path.name}"
            )

        # Write the good content
        with open(target_file, "w") as f:
            f.write(good_content)

        self.log_step("GIT_RESTORE", f"✅ Successfully restored {target_file.name}")

    def reconstruct_from_git(self, target_file_path: str) -> bool:
        """Execute the full Git Time Machine Protocol."""
        self.log_step("PROTOCOL", "🚀 Starting Git Time Machine Protocol")

        target_file = Path(target_file_path)

        if not target_file.exists():
            self.log_step("PROTOCOL", f"❌ Target file {target_file} does not exist")
            return False

        # Find the last good commit
        last_good_commit = self.find_last_good_commit(target_file)

        if not last_good_commit:
            self.log_step(
                "PROTOCOL",
                "🛑 CRITICAL: No syntactically valid version found in Git history",
            )
            return False

        commit_info = self.git_agent.get_commit_info(last_good_commit)
        self.log_step(
            "PROTOCOL", f"📍 Last good commit: {last_good_commit[:7]} ({commit_info})"
        )

        # Restore from Git
        try:
            self.restore_from_git_commit(target_file, last_good_commit)
        except Exception as e:
            self.log_step("PROTOCOL", f"❌ Failed to restore from Git: {e}")
            return False

        # Verify restoration
        if not self.syntax_check_file(target_file):
            self.log_step(
                "PROTOCOL", "❌ Restoration failed - file still has syntax errors"
            )
            return False

        self.log_step("PROTOCOL", "✅ Git Time Machine Protocol completed successfully")
        self.log_step(
            "PROTOCOL", "🎯 Codebase restored to stable state from Git history"
        )
        return True


def main():
    """Main entry point for the Git Time Machine reconstruction."""
    import sys

    if len(sys.argv) != 2:
        print("Usage: python reconstruct.py <target_file>")
        print("Example: python reconstruct.py app/dashboard.py")
        sys.exit(1)

    target_file = sys.argv[1]
    reconstructor = CodebaseReconstructor()

    success = reconstructor.reconstruct_from_git(target_file)

    if success:
        print(f"✅ Successfully reconstructed {target_file} using Git Time Machine")
        print("🎯 Your codebase has been restored to a stable state!")
        sys.exit(0)
    else:
        print(f"❌ Failed to reconstruct {target_file}")
        print("💡 Consider checking if this is a Git repository with commit history")
        sys.exit(1)


if __name__ == "__main__":
    main()
