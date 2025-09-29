#!/usr/bin/env python3
"""
Direct Application Launcher
Runs the integrated FastAPI application directly within the current Python process
"""

import sys
import os
import threading
import time
from pathlib import Path

def setup_environment():
    """Setup the environment for the application"""
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    # Ensure data directory exists
    data_dir = current_dir / "data"
    data_dir.mkdir(exist_ok=True)
    
    media_dir = data_dir / "media"
    media_dir.mkdir(exist_ok=True)
    
    print("✓ Environment setup complete")

def check_imports():
    """Check if all required modules can be imported"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        import sqlite3
        print("✓ All required modules are available")
        return True
    except ImportError as e:
        print(f"✗ Missing required module: {e}")
        return False

def run_server():
    """Run the FastAPI server"""
    try:
        # Import the integrated app
        import integrated_app
        
        # Get the app instance
        app = integrated_app.app
        
        print("🚀 Starting TRAE.AI + Base44 Integrated Runtime...")
        print("📊 Dashboard: http://127.0.0.1:8080/dashboard")
        print("📚 API Docs: http://127.0.0.1:8080/docs")
        print("💚 Health Check: http://127.0.0.1:8080/health")
        print("🔄 Server is running... (Press Ctrl+C to stop)")
        
        # Import uvicorn
        import uvicorn
        
        # Configure and run the server
        config = uvicorn.Config(
            app=app,
            host="127.0.0.1",
            port=8080,
            log_level="info",
            access_log=True
        )
        
        server = uvicorn.Server(config)
        
        # Run the server in the current thread
        server.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"✗ Server error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function"""
    print("=== Direct Application Launcher ===")
    
    # Setup environment
    setup_environment()
    
    # Check if integrated_app.py exists
    if not Path("integrated_app.py").exists():
        print("✗ integrated_app.py not found in current directory")
        return False
    
    # Check imports
    if not check_imports():
        print("✗ Required modules not available")
        return False
    
    # Run the server
    run_server()
    return True

if __name__ == "__main__":
    main()