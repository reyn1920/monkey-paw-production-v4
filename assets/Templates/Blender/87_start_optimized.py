#!/usr/bin/env python3
"""
Optimized Startup Script
Minimal memory usage with automatic startup configuration
"""

import os
import sys
import subprocess
import signal
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def setup_environment():
    """Setup optimized environment variables"""
    os.environ.setdefault("PYTHONPATH", str(project_root))
    os.environ.setdefault("PORT", "8000")
    os.environ.setdefault("HOST", "0.0.0.0")

    # Memory optimization settings
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")  # Don't create .pyc files
    os.environ.setdefault("PYTHONUNBUFFERED", "1")  # Unbuffered output
    os.environ.setdefault("DISABLE_ANALYTICS", "1")
    os.environ.setdefault("DISABLE_MONITORING", "1")
    os.environ.setdefault("MINIMAL_MODE", "1")

    print("Environment configured for minimal memory usage")


def cleanup_system():
    """Clean up system to free memory"""
    print("Cleaning up system...")

    # Clean Python cache files
    try:
        subprocess.run(
            [
                "find",
                ".",
                "-name",
                "__pycache__",
                "-type",
                "d",
                "-exec",
                "rm",
                "-rf",
                "{}",
                "+",
            ],
            capture_output=True,
            check=False,
        )

        subprocess.run(
            ["find", ".", "-name", "*.pyc", "-delete"], capture_output=True, check=False
        )

        print("✓ Python cache cleaned")
    except Exception as e:
        print(f"Cache cleanup warning: {e}")


def start_minimal_server():
    """Start minimal HTTP server"""
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    print(f"Starting minimal server on {host}:{port}")

    # Try to start with Python's built-in server first
    try:
        import http.server
        import socketserver

        class OptimizedHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/health":
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(b'{"status": "ok", "mode": "optimized"}')
                elif self.path == "/":
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    html = b"""
                    <!DOCTYPE html>
                    <html>
                    <head><title>Application Running</title></head>
                    <body>
                        <h1>Application Running in Optimized Mode</h1>
                        <p>Memory usage minimized</p>
                        <p>Only essential services loaded</p>
                        <a href="/health">Health Check</a>
                    </body>
                    </html>
                    """
                    self.wfile.write(html)
                else:
                    self.send_response(404)
                    self.end_headers()

            def log_message(self, format, *args):
                # Suppress access logs to save memory
                pass

        with socketserver.TCPServer((host, port), OptimizedHandler) as httpd:
            print(f"✓ Server started at http://{host}:{port}")
            print("✓ Memory optimized mode active")
            print("✓ Press Ctrl+C to stop")

            def signal_handler(signum, frame):
                print("\nShutting down server...")
                httpd.shutdown()
                sys.exit(0)

            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)

            httpd.serve_forever()

    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)


def check_dependencies():
    """Check if essential dependencies are available"""
    essential_modules = ["http.server", "socketserver", "json", "os", "sys"]
    missing = []

    for module in essential_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)

    if missing:
        print(f"Warning: Missing modules: {missing}")
        return False

    print("✓ Essential dependencies available")
    return True


def setup_auto_startup():
    """Setup automatic startup configuration"""
    print("Setting up automatic startup...")

    # Create a simple startup script
    startup_script = project_root / "auto_start.sh"

    script_content = f"""#!/bin/bash
# Auto-generated startup script
cd "{project_root}"
export PYTHONPATH="{project_root}"
export MINIMAL_MODE=1
export DISABLE_ANALYTICS=1
export DISABLE_MONITORING=1
python3 start_optimized.py
"""

    try:
        with open(startup_script, "w") as f:
            f.write(script_content)

        # Make executable
        os.chmod(startup_script, 0o755)

        print(f"✓ Startup script created: {startup_script}")
        print("  To auto-start: ./auto_start.sh")

    except Exception as e:
        print(f"Warning: Could not create startup script: {e}")


def main():
    """Main entry point"""
    print("=== Optimized Application Startup ===")
    print("Memory usage minimized, only essential components loaded")
    print()

    # Setup environment
    setup_environment()

    # Clean up system
    cleanup_system()

    # Check dependencies
    if not check_dependencies():
        print("Warning: Some dependencies missing, continuing anyway...")

    # Setup auto-startup
    setup_auto_startup()

    # Start server
    start_minimal_server()


if __name__ == "__main__":
    main()
