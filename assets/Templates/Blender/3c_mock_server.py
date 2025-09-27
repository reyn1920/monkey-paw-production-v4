#!/usr/bin/env python3
"""
Mock FastAPI Server for Platform Testing
Demonstrates the application structure without external dependencies
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

class MockFastAPIHandler(BaseHTTPRequestHandler):
    """Mock handler that simulates FastAPI responses"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Route handling
        if path == '/':
            self.send_dashboard_response()
        elif path == '/health':
            self.send_health_response()
        elif path == '/api/status':
            self.send_status_response()
        elif path.startswith('/docs'):
            self.send_docs_response()
        else:
            self.send_404_response()
    
    def send_dashboard_response(self):
        """Send the main dashboard response"""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Integrated FastAPI Application</title>
            <style>
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 2rem;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                }
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 2rem;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }
                h1 { color: #fff; margin-bottom: 1rem; }
                .status { 
                    background: rgba(76, 175, 80, 0.2);
                    padding: 1rem;
                    border-radius: 8px;
                    margin: 1rem 0;
                    border-left: 4px solid #4CAF50;
                }
                .info-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 1rem;
                    margin: 2rem 0;
                }
                .info-card {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 1rem;
                    border-radius: 8px;
                    text-align: center;
                }
                .endpoint-list {
                    background: rgba(255, 255, 255, 0.05);
                    padding: 1rem;
                    border-radius: 8px;
                    margin: 1rem 0;
                }
                .endpoint { 
                    margin: 0.5rem 0;
                    padding: 0.5rem;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 4px;
                }
                a { color: #81C784; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Integrated FastAPI Application</h1>
                
                <div class="status">
                    <strong>✅ Application Status: RUNNING</strong><br>
                    Platform-native execution successful!
                </div>
                
                <div class="info-grid">
                    <div class="info-card">
                        <h3>🌐 Server Info</h3>
                        <p>Host: 127.0.0.1<br>Port: 8080</p>
                    </div>
                    <div class="info-card">
                        <h3>⚡ Framework</h3>
                        <p>FastAPI<br>Mock Server</p>
                    </div>
                    <div class="info-card">
                        <h3>🔧 Platform</h3>
                        <p>Trae AI<br>Native Tools</p>
                    </div>
                </div>
                
                <div class="endpoint-list">
                    <h3>📋 Available Endpoints:</h3>
                    <div class="endpoint">
                        <strong>GET /</strong> - Dashboard (this page)
                    </div>
                    <div class="endpoint">
                        <strong>GET /health</strong> - <a href="/health">Health Check</a>
                    </div>
                    <div class="endpoint">
                        <strong>GET /api/status</strong> - <a href="/api/status">API Status</a>
                    </div>
                    <div class="endpoint">
                        <strong>GET /docs</strong> - <a href="/docs">API Documentation</a>
                    </div>
                </div>
                
                <div style="margin-top: 2rem; text-align: center; opacity: 0.8;">
                    <p>🎉 Platform-native execution completed successfully!</p>
                    <p>Application launched without terminal commands using Trae AI tools.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', str(len(html_content.encode())))
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def send_health_response(self):
        """Send health check response"""
        response = {"status": "healthy", "timestamp": time.time(), "service": "integrated-app"}
        self.send_json_response(response)
    
    def send_status_response(self):
        """Send API status response"""
        response = {
            "application": "Integrated FastAPI App",
            "version": "1.0.0",
            "platform": "Trae AI Native",
            "status": "running",
            "endpoints": ["/", "/health", "/api/status", "/docs"]
        }
        self.send_json_response(response)
    
    def send_docs_response(self):
        """Send API documentation response"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>API Documentation</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 2rem; }
                .endpoint { margin: 1rem 0; padding: 1rem; border: 1px solid #ddd; border-radius: 4px; }
            </style>
        </head>
        <body>
            <h1>API Documentation</h1>
            <div class="endpoint">
                <h3>GET /</h3>
                <p>Returns the main dashboard</p>
            </div>
            <div class="endpoint">
                <h3>GET /health</h3>
                <p>Returns health status of the application</p>
            </div>
            <div class="endpoint">
                <h3>GET /api/status</h3>
                <p>Returns detailed application status</p>
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', str(len(html_content.encode())))
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def send_json_response(self, data):
        """Send JSON response"""
        json_data = json.dumps(data, indent=2)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', str(len(json_data.encode())))
        self.end_headers()
        self.wfile.write(json_data.encode())
    
    def send_404_response(self):
        """Send 404 response"""
        response = {"error": "Not Found", "message": f"Path {self.path} not found"}
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[{self.address_string()}] {format % args}")

def start_server():
    """Start the mock server"""
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, MockFastAPIHandler)
    
    print("🚀 Mock FastAPI Server Starting")
    print(f"🌐 Server running at http://127.0.0.1:8080")
    print("📋 Available endpoints:")
    print("   - GET / (Dashboard)")
    print("   - GET /health (Health Check)")
    print("   - GET /api/status (API Status)")
    print("   - GET /docs (Documentation)")
    print("\n✅ Server ready for Puppeteer testing!")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == "__main__":
    start_server()