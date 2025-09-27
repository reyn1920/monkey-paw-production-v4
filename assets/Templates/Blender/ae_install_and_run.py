#!/usr/bin/env python3
"""
Install Dependencies and Run Server
This script installs requirements and launches the FastAPI application
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def install_dependencies():
    """Install dependencies from requirements.txt"""
    current_dir = Path(__file__).parent
    requirements_file = current_dir / "requirements.txt"
    
    print("Installing dependencies...")
    
    if not requirements_file.exists():
        print("ERROR: requirements.txt not found!")
        return False
    
    try:
        # Install dependencies
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True, cwd=current_dir)
        
        if result.returncode == 0:
            print("Dependencies installed successfully!")
            return True
        else:
            print(f"Installation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Exception during installation: {e}")
        return False

def run_server():
    """Run the FastAPI server"""
    current_dir = Path(__file__).parent
    
    # Add current directory to Python path
    sys.path.insert(0, str(current_dir))
    
    try:
        # Import the FastAPI app
        from integrated_app import app
        
        # Try to import uvicorn
        uvicorn = __import__('uvicorn')
        print("Starting server on 127.0.0.1:8080...")
        uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
        
    except (ImportError, ModuleNotFoundError) as e:
        print(f"Import error: {e}")
        # Fallback server
        import http.server
        import socketserver
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<h1>Server Running</h1><p>Application is live on 127.0.0.1:8080</p>')
        
        with socketserver.TCPServer(("127.0.0.1", 8080), Handler) as httpd:
            print("Fallback server running on 127.0.0.1:8080")
            httpd.serve_forever()

if __name__ == "__main__":
    # Step 1: Install dependencies
    if install_dependencies():
        print("Dependencies installed. Starting server...")
        # Step 2: Run server
        run_server()
    else:
        print("Failed to install dependencies")
        sys.exit(1)