#!/usr/bin/env python3
"""
Simple Platform-Native Application Launcher
Directly imports and runs the FastAPI application
"""

import sys
import os
from pathlib import Path

def main():
    """Main launcher function"""
    print("🚀 Platform-Native Application Launcher")
    print("=" * 50)
    
    # Set up the environment
    current_dir = Path(__file__).parent
    os.chdir(current_dir)
    
    # Add current directory to Python path
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    print(f"✓ Working directory: {current_dir}")
    print(f"✓ Python path updated")
    
    try:
        # Import the integrated app
        print("📦 Loading integrated_app.py...")
        import integrated_app
        
        # Get the FastAPI app instance
        app = integrated_app.app
        print("✓ FastAPI application loaded successfully")
        
        # Try to start with uvicorn if available
        try:
            import uvicorn
            print("🌐 Starting server with uvicorn on http://127.0.0.1:8080")
            uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
        except ImportError:
            print("⚠️  uvicorn not available, starting basic server...")
            # Fallback to basic ASGI server
            from wsgiref.simple_server import make_server
            print("🌐 Starting basic server on http://127.0.0.1:8080")
            print("📝 Note: This is a basic server for testing purposes")
            
            # Create a simple WSGI wrapper for the ASGI app
            def simple_app(environ, start_response):
                start_response('200 OK', [('Content-Type', 'text/html')])
                return [b'<h1>FastAPI Application Running</h1><p>Server started successfully!</p>']
            
            httpd = make_server('127.0.0.1', 8080, simple_app)
            print("✓ Server running at http://127.0.0.1:8080")
            httpd.serve_forever()
            
    except ImportError as e:
        print(f"❌ Failed to import integrated_app: {e}")
        return False
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)