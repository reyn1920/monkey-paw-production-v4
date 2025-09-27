#!/usr/bin/env python3
"""
Quick Start Web Server - Immediate Terminal Activity
"""
import http.server
import socketserver
import webbrowser
import threading
import time
import os
from typing_extensions import override

PORT = 8000

class QuickHandler(http.server.SimpleHTTPRequestHandler):
    @override
    def do_GET(self):
        print(f"🌐 REQUEST: {self.path} from {self.client_address[0]}")
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>TRAE.AI Application Running!</title>
                <style>
                    body { font-family: Arial; text-align: center; padding: 50px; background: #1a1a1a; color: #00ff00; }
                    h1 { color: #00ff00; font-size: 3em; }
                    .status { background: #333; padding: 20px; border-radius: 10px; margin: 20px; }
                </style>
            </head>
            <body>
                <h1>🚀 TRAE.AI APPLICATION IS RUNNING!</h1>
                <div class="status">
                    <h2>✅ Server Status: ACTIVE</h2>
                    <p>Port: 8000</p>
                    <p>Time: """ + time.strftime("%Y-%m-%d %H:%M:%S") + """</p>
                </div>
                <p>Your application is now live and working!</p>
            </body>
            </html>
            """
            _ = self.wfile.write(html.encode())
        else:
            super().do_GET()

def start_server():
    print("=" * 60)
    print("🚀 STARTING TRAE.AI QUICK SERVER")
    print("=" * 60)
    
    with socketserver.TCPServer(("", PORT), QuickHandler) as httpd:
        print(f"✅ Server running at http://localhost:{PORT}")
        print(f"📁 Serving directory: {os.getcwd()}")
        print("🔥 TERMINAL IS ACTIVE AND WORKING!")
        print("=" * 60)
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            try:
                _ = webbrowser.open(f'http://localhost:{PORT}')
                print("🌐 Browser opened automatically")
            except:
                print("🌐 Please open http://localhost:8000 in your browser")
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")

if __name__ == "__main__":
    start_server()