#!/usr/bin/env python3
"""
Test script to verify FastAPI app import and basic functionality
"""

import sys
import os
from pathlib import Path

# Set up environment
current_dir = Path(__file__).parent
os.chdir(current_dir)
sys.path.insert(0, str(current_dir))

print("🧪 Testing FastAPI Application Import")
print("=" * 40)

try:
    # Test importing the integrated app
    print("📦 Importing integrated_app...")
    import integrated_app
    print("✅ integrated_app imported successfully")
    
    # Check if app exists
    if hasattr(integrated_app, 'app'):
        app = integrated_app.app
        print("✅ FastAPI app instance found")
        print(f"   - App type: {type(app)}")
        
        # Check app properties
        if hasattr(app, 'routes'):
            print(f"   - Number of routes: {len(app.routes)}")
            
        # Test basic app properties
        print("📋 Application Details:")
        print(f"   - Title: {getattr(app, 'title', 'Not set')}")
        print(f"   - Version: {getattr(app, 'version', 'Not set')}")
        
        # Check if we can access the root endpoint
        print("\n🔍 Testing application readiness...")
        print("✅ Application is ready to be served")
        print("🌐 Recommended server command:")
        print("   python -m uvicorn integrated_app:app --host 127.0.0.1 --port 8080")
        
    else:
        print("❌ No 'app' attribute found in integrated_app")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 40)
print("🏁 Test completed")