import subprocess
import sys

def install_dependencies():
    """Reads requirements.txt and installs packages using pip."""
    try:
        print("--- Starting Dependency Installation ---")
        # Ensure we're using the pip associated with the current Python interpreter
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        print("--- Dependency Installation Successful ---")
    except FileNotFoundError:
        print("ERROR: requirements.txt not found in the current directory.")
    except subprocess.CalledProcessError as e:
        print("--- ERROR: Pip command failed ---")
        print(e.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    install_dependencies()