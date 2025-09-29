import subprocess
import sys

def run_server_and_capture_output():
    """Runs the Uvicorn server command and captures its output."""
    command = [
        sys.executable,
        "-m",
        "uvicorn",
        "integrated_app:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8080"
    ]
    
    print(f"--- Running Command: {' '.join(command)} ---")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60  # Wait up to 60 seconds for the process
        )
        
        print("\n--- STDOUT (Standard Output) ---")
        print(result.stdout if result.stdout else "[No Standard Output]")
        
        print("\n--- STDERR (Error Output) ---")
        print(result.stderr if result.stderr else "[No Error Output]")
        
        print(f"\n--- Process Finished with Exit Code: {result.returncode} ---")

    except FileNotFoundError:
        print("\n--- CRITICAL ERROR ---")
        print("The 'uvicorn' command was not found.")
        print("This indicates a problem with the dependency installation.")
    except subprocess.TimeoutExpired:
        print("\n--- CRITICAL ERROR ---")
        print("The server process timed out. It may be running correctly in the background, or it hung.")
    except Exception as e:
        print(f"\n--- An unexpected Python error occurred: {e} ---")

if __name__ == "__main__":
    run_server_and_capture_output()