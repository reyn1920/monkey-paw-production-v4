#!/usr/bin/env python3
"""
Optimized Main Application Entry Point
Loads only essential components to minimize memory usage
"""

import os
import sys
import logging
import asyncio
from pathlib import Path
from uvicorn import Config, Server

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure minimal logging
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings and errors
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def setup_environment():
    """Setup minimal environment variables"""
    os.environ.setdefault("PYTHONPATH", str(project_root))
    os.environ.setdefault("PORT", "8000")
    os.environ.setdefault("HOST", "0.0.0.0")

    # Disable unnecessary features to save memory
    os.environ.setdefault("DISABLE_ANALYTICS", "1")
    os.environ.setdefault("DISABLE_MONITORING", "1")
    os.environ.setdefault("MINIMAL_MODE", "1")


async def start_essential_services():
    """Start only essential services"""
    try:
        from config.startup_config import startup_manager

        print("Starting essential services...")
        results = startup_manager.load_essential_only()

        loaded_count = sum(1 for success in results.values() if success)
        print(f"Loaded {loaded_count}/{len(results)} essential services")

        if loaded_count == 0:
            print("WARNING: No essential services loaded successfully")
            return False

        return True

    except Exception as e:
        print(f"Error starting essential services: {e}")
        return False


async def start_api_server():
    """Start the API server with minimal configuration"""
    try:
        # Try to import and start FastAPI server
        from backend.api_orchestrator import APIOrchestrator

        orchestrator = APIOrchestrator()

        # Check if FastAPI app is available
        if orchestrator.app is None:
            print("FastAPI not available, starting minimal HTTP server instead...")
            await start_minimal_server()
            return

        # Start server on specified port
        port = int(os.environ.get("PORT", 8000))
        host = os.environ.get("HOST", "0.0.0.0")

        print(f"Starting API server on {host}:{port}")

        # Use uvicorn Server to work within existing event loop
        config = Config(
            app=orchestrator.app,
            host=host,
            port=port,
            log_level="warning",
            access_log=False,
            reload=False,
        )
        server = Server(config)
        await server.serve()

    except ImportError as e:
        print(f"Failed to import API components: {e}")
        print("Starting minimal HTTP server instead...")
        await start_minimal_server()
    except Exception as e:
        import traceback

        print(f"Error starting API server: {e}")
        print("Full traceback:")
        traceback.print_exc()
        print("Starting minimal HTTP server instead...")
        await start_minimal_server()
        return False


async def start_minimal_server():
    """Fallback minimal HTTP server"""
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    import threading

    port = int(os.environ.get("PORT", 8000))

    class MinimalHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/health":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "ok", "mode": "minimal"}')
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>Application Running in Minimal Mode</h1>")

    server = HTTPServer(("0.0.0.0", port), MinimalHandler)
    print(f"Starting minimal server on port {port}")

    def run_server():
        server.serve_forever()

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()

    # Keep the main thread alive
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()


async def main():
    """Main application entry point"""
    print("=== Optimized Application Startup ===")

    # Setup environment
    setup_environment()

    # Start essential services
    services_started = await start_essential_services()

    if not services_started:
        print("Running in minimal mode due to service startup failures")

    # Start API server
    await start_api_server()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Application failed to start: {e}")
        sys.exit(1)
