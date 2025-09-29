#!/usr/bin/env python3
"""
Trae.ai Startup Script
Initializes and starts the Trae.ai integration service
"""

import sys
import logging
from pathlib import Path
from trae_integration import TraeIntegration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main startup function for Trae.ai"""
    logger = logging.getLogger(__name__)
    
    print("🚀 Starting Trae.ai Integration Service...")
    
    try:
        # Initialize Trae integration
        trae = TraeIntegration()
        
        # Connect to Trae.ai
        print("🔌 Connecting to Trae.ai...")
        connection_result = trae.connect()
        
        if connection_result['status'] == 'success':
            print("✅ Trae.ai connected successfully!")
            
            # Initialize project
            project_path = str(Path.cwd())
            print(f"📁 Initializing project: {project_path}")
            
            init_result = trae.initialize_project(project_path)
            
            if init_result['status'] == 'success':
                print("✅ Trae.ai project initialized!")
                
                # Get status
                status = trae.get_status()
                print(f"📊 Trae.ai Status: {status}")
                
                print("🎉 Trae.ai is now ONLINE and ready!")
                return True
            else:
                print(f"❌ Project initialization failed: {init_result['message']}")
                return False
        else:
            print(f"❌ Connection failed: {connection_result['message']}")
            return False
            
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        print(f"❌ Startup failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)