#!/usr/bin/env python3
"""
Direct FastAPI Application Starter
Platform-native execution approach
"""

import sys
import os
from pathlib import Path

# Set up environment
current_dir = Path(__file__).parent
os.chdir(current_dir)
sys.path.insert(0, str(current_dir))

print("🚀 Starting FastAPI Application")
print(f"📁 Working directory: {current_dir}")

try:
    # Import the FastAPI application
    from integrated_app import app
    print("✅ FastAPI app imported successfully")
    
    # Check if uvicorn is available
    try:
        import uvicorn
        print("🌐 Starting server with uvicorn on http://127.0.0.1:8080")
        print("🔗 Application will be available at: http://127.0.0.1:8080")
        
        # Start the server
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8080, 
            log_level="info",
            access_log=True
        )
        
    except ImportError:
        print("⚠️ uvicorn not available")
        print("🔧 Please install uvicorn: pip install uvicorn")
        
        # Alternative: Show that the app is loaded
        print("✅ FastAPI app is loaded and ready")
        print("📋 App details:")
        print(f"   - Type: {type(app)}")
        print(f"   - Routes available: {len(app.routes) if hasattr(app, 'routes') else 'Unknown'}")
        print("🌐 To start the server, install uvicorn and run:")
        print("   uvicorn integrated_app:app --host 127.0.0.1 --port 8080")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()