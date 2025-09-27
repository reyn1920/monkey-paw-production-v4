#!/usr/bin/env python3
"""
Platform-Native Application Launcher
Launches the integrated_app.py FastAPI application using platform tools only
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path

def check_dependencies():
    """Check if required packages are available"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'sqlalchemy',
        'starlette'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is available")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is missing")
    
    return missing_packages

def install_dependencies():
    """Install dependencies using subprocess (platform-native)"""
    print("Installing dependencies using platform's Python environment...")
    try:
        # Use subprocess to install packages
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✓ Dependencies installed successfully")
            return True
        else:
            print(f"✗ Dependency installation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def launch_application():
    """Launch the FastAPI application"""
    print("Launching TRAE.AI + Base44 Integrated Runtime...")
    
    # Import and run the application
    try:
        # Add current directory to Python path
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        
        # Import the integrated app
        spec = importlib.util.spec_from_file_location(
            "integrated_app", 
            current_dir / "integrated_app.py"
        )
        integrated_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(integrated_app)
        
        # Get the FastAPI app instance
        app = integrated_app.app
        
        # Import uvicorn and run the server
        import uvicorn
        
        print("🚀 Starting TRAE.AI + Base44 Integrated Runtime...")
        print("📊 Dashboard: http://127.0.0.1:8080/dashboard")
        print("📚 API Docs: http://127.0.0.1:8080/docs")
        print("💚 Health Check: http://127.0.0.1:8080/health")
        
        # Run the server
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8080,
            log_level="info"
        )
        
    except Exception as e:
        print(f"✗ Failed to launch application: {e}")
        return False

def main():
    """Main launcher function"""
    print("=== Platform-Native Application Launcher ===")
    print("Checking system requirements...")
    
    # Check if we're in the right directory
    if not Path("integrated_app.py").exists():
        print("✗ integrated_app.py not found in current directory")
        return False
    
    if not Path("requirements.txt").exists():
        print("✗ requirements.txt not found in current directory")
        return False
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"Missing packages: {missing}")
        print("Attempting to install dependencies...")
        if not install_dependencies():
            print("✗ Failed to install dependencies")
            return False
        
        # Re-check after installation
        missing = check_dependencies()
        if missing:
            print(f"✗ Still missing packages after installation: {missing}")
            return False
    
    print("✓ All dependencies are available")
    
    # Launch the application
    return launch_application()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)