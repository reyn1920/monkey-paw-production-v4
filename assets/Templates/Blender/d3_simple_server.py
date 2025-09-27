#!/usr/bin/env python3
"""
Simple HTTP Server for testing
"""
import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>TRAE AI Application</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                    .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #333; text-align: center; }
                    .status { background: #e8f5e8; padding: 20px; border-radius: 5px; margin: 20px 0; }
                    .endpoints { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }
                    .endpoint { margin: 10px 0; padding: 10px; background: white; border-left: 4px solid #007bff; }
                    a { color: #007bff; text-decoration: none; }
                    a:hover { text-decoration: underline; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚀 TRAE AI Application is Running!</h1>
                    <div class="status">
                        <h3>✅ Status: Online</h3>
                        <p>The application is successfully running on your Google Drive system.</p>
                    </div>
                    <div class="endpoints">
                        <h3>Available Endpoints:</h3>
                        <div class="endpoint">
                            <strong><a href="/health">/health</a></strong> - Health check endpoint
                        </div>
                        <div class="endpoint">
                            <strong><a href="/test">/test</a></strong> - Test endpoint
                        </div>
                        <div class="endpoint">
                            <strong><a href="/api/status">/api/status</a></strong> - API status
                        </div>
                    </div>
                    <p style="text-align: center; color: #666; margin-top: 40px;">
                        Server running on port 8000 | Built with TRAE AI
                    </p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        elif parsed_path.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "message": "TRAE AI Application is running",
                "port": 8000,
                "endpoints": ["/", "/health", "/test", "/api/status"]
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif parsed_path.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "ok",
                "message": "Test endpoint working",
                "server": "Simple HTTP Server",
                "version": "1.0.0"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif parsed_path.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "api_status": "running",
                "server_type": "Simple HTTP Server",
                "application": "TRAE AI Application",
                "environment": "development",
                "features": ["health_check", "test_endpoints", "json_responses"]
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Page Not Found</h1><p><a href="/">Go back to home</a></p>')

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

if __name__ == "__main__":
    PORT = 8000
    print(f"🚀 Starting TRAE AI Application on port {PORT}")
    print(f"📱 Open http://localhost:{PORT} in your browser")
    print("🔍 Available endpoints:")
    print("   • http://localhost:8000/ - Main application")
    print("   • http://localhost:8000/health - Health check")
    print("   • http://localhost:8000/test - Test endpoint")
    print("   • http://localhost:8000/api/status - API status")
    print("\n✨ Press Ctrl+C to stop the server")
    
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
