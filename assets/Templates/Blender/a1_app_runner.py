#!/usr/bin/env python3
"""
Platform-Native Application Runner
Executes the integrated FastAPI application using available platform tools
"""

import sys
import os
import importlib
import importlib.util
import threading
import time
import json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class ApplicationRunner:
    """Main application runner class"""
    
    def __init__(self):
        self.app_instance = None
        self.server_thread = None
        self.is_running = False
        
    def setup_environment(self):
        """Setup the application environment"""
        print("Setting up application environment...")
        
        # Add current directory to Python path
        current_dir = Path(__file__).parent
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))
        
        # Create required directories
        data_dir = current_dir / "data"
        data_dir.mkdir(exist_ok=True)
        
        media_dir = data_dir / "media"
        media_dir.mkdir(exist_ok=True)
        
        print("✓ Environment setup complete")
        return True
    
    def check_dependencies(self):
        """Check if the integrated app can be loaded"""
        try:
            # Check if integrated_app.py exists
            app_file = Path("integrated_app.py")
            if not app_file.exists():
                print("✗ integrated_app.py not found")
                return False
            
            print("✓ integrated_app.py found")
            return True
            
        except Exception as e:
            print(f"✗ Dependency check failed: {e}")
            return False
    
    def load_application(self):
        """Load the FastAPI application"""
        try:
            print("Loading integrated application...")
            
            # Try to import the integrated app
            spec = importlib.util.spec_from_file_location(
                "integrated_app", 
                "integrated_app.py"
            )
            
            if spec is None:
                print("✗ Could not create module spec")
                return False
            
            integrated_module = importlib.util.module_from_spec(spec)
            
            # Execute the module
            if spec.loader:
                spec.loader.exec_module(integrated_module)
            
            # Get the app instance
            if hasattr(integrated_module, 'app'):
                self.app_instance = integrated_module.app
                print("✓ FastAPI application loaded successfully")
                return True
            else:
                print("✗ No 'app' instance found in integrated_app.py")
                return False
                
        except ImportError as e:
            print(f"✗ Import error: {e}")
            print("This likely means required packages (fastapi, uvicorn) are not installed")
            return False
        except Exception as e:
            print(f"✗ Failed to load application: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def start_fallback_server(self):
        """Start a fallback HTTP server if FastAPI is not available"""
        print("Starting fallback HTTP server...")
        
        class FallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/health':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        "status": "running",
                        "message": "Fallback server is active",
                        "note": "FastAPI dependencies not available"
                    }
                    self.wfile.write(json.dumps(response).encode())
                elif self.path == '/' or self.path == '/dashboard':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    html = """
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>TRAE.AI + Base44 - Fallback Mode</title>
                        <style>
                            body { font-family: Arial, sans-serif; margin: 40px; }
                            .container { max-width: 800px; margin: 0 auto; }
                            .status { background: #f0f8ff; padding: 20px; border-radius: 8px; }
                            .warning { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>🚀 TRAE.AI + Base44 Integrated Runtime</h1>
                            <div class="status">
                                <h2>✓ Application Status: Running (Fallback Mode)</h2>
                                <p><strong>Version:</strong> 2.0.0</p>
                                <p><strong>Mode:</strong> Platform-Native Fallback Server</p>
                                <p><strong>Host:</strong> 127.0.0.1:8080</p>
                            </div>
                            
                            <div class="warning">
                                <h3>⚠️ Notice</h3>
                                <p>The application is running in fallback mode because FastAPI dependencies are not available in the current environment.</p>
                                <p>To run the full application, ensure the following packages are installed:</p>
                                <ul>
                                    <li>fastapi</li>
                                    <li>uvicorn</li>
                                    <li>pydantic</li>
                                    <li>sqlalchemy</li>
                                </ul>
                            </div>
                            
                            <h3>📋 Available Endpoints</h3>
                            <ul>
                                <li><a href="/health">/health</a> - Health check</li>
                                <li><a href="/dashboard">/dashboard</a> - This dashboard</li>
                            </ul>
                            
                            <h3>🔧 Platform Integration</h3>
                            <p>This fallback server demonstrates that the platform can successfully:</p>
                            <ul>
                                <li>✓ Execute Python applications</li>
                                <li>✓ Start HTTP servers</li>
                                <li>✓ Serve web content</li>
                                <li>✓ Handle routing and responses</li>
                            </ul>
                        </div>
                    </body>
                    </html>
                    """
                    self.wfile.write(html.encode())
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Not Found')
            
            def log_message(self, format, *args):
                # Suppress default logging
                pass
        
        try:
            server = HTTPServer(('127.0.0.1', 8080), FallbackHandler)
            print("✓ Fallback server started successfully")
            print("📊 Dashboard: http://127.0.0.1:8080/dashboard")
            print("💚 Health Check: http://127.0.0.1:8080/health")
            print("🔄 Server is running... (Press Ctrl+C to stop)")
            
            self.is_running = True
            server.serve_forever()
            
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            self.is_running = False
        except Exception as e:
            print(f"✗ Fallback server error: {e}")
            self.is_running = False
    
    def start_fastapi_server(self):
        """Start the FastAPI server if available"""
        try:
            # Try to import uvicorn
            try:
                import uvicorn
            except ImportError:
                print("✗ uvicorn not available, cannot start FastAPI server")
                return False
            
            print("✓ Starting FastAPI server with uvicorn")
            print("📊 Dashboard: http://127.0.0.1:8080/dashboard")
            print("📚 API Docs: http://127.0.0.1:8080/docs")
            print("💚 Health Check: http://127.0.0.1:8080/health")
            print("🔄 Server is running... (Press Ctrl+C to stop)")
            
            # Configure and run the server
            config = uvicorn.Config(
                app=self.app_instance,
                host="127.0.0.1",
                port=8080,
                log_level="info"
            )
            
            server = uvicorn.Server(config)
            self.is_running = True
            server.run()
            
        except KeyboardInterrupt:
            print("\n🛑 FastAPI server stopped by user")
            self.is_running = False
        except Exception as e:
            print(f"✗ FastAPI server error: {e}")
            self.is_running = False
    
    def run(self):
        """Main run method"""
        print("=== Platform-Native Application Runner ===")
        
        # Setup environment
        if not self.setup_environment():
            return False
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Try to load the FastAPI application
        if self.load_application():
            print("🚀 Starting TRAE.AI + Base44 Integrated Runtime (Full Mode)...")
            self.start_fastapi_server()
        else:
            print("🔄 Starting TRAE.AI + Base44 Integrated Runtime (Fallback Mode)...")
            self.start_fallback_server()
        
        return True

def main():
    """Main entry point"""
    runner = ApplicationRunner()
    return runner.run()

if __name__ == "__main__":
    main()