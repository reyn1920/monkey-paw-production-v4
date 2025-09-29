#!/usr/bin/env python3
"""
TRAE.AI Setup Script
Helps configure TRAE.AI integration with API keys and settings
"""

import os
import json
import sys
from pathlib import Path

def create_env_file():
    """Create .env file with TRAE.AI configuration"""
    env_content = """# TRAE.AI Integration Environment Variables
# Fill in your actual API keys below

# TRAE.AI Master Key (for local TRAE.AI system)
TRAE_MASTER_KEY=your_trae_master_key_here

# OpenAI API Key (for ChatGPT integration)
OPENAI_API_KEY=your_openai_api_key_here

# Google AI API Key (for Gemini integration)
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# Abacus AI API Key (for Abacus AI integration)
ABACUS_API_KEY=your_abacus_api_key_here

# TRAE.AI Base URL (default: localhost:8080)
TRAE_BASE_URL=http://localhost:8080/api/v1

# Cross-validation settings
TRAE_CROSS_VALIDATE=true
TRAE_CONFIDENCE_THRESHOLD=0.8

# Optional: Custom model configurations
CHATGPT_MODEL=gpt-4
GEMINI_MODEL=gemini-pro
ABACUS_APP_ID=1024a18ebe
"""
    
    env_path = Path(".env")
    if env_path.exists():
        print("⚠️  .env file already exists. Backing up to .env.backup")
        env_path.rename(".env.backup")
    
    with open(env_path, "w") as f:
        f.write(env_content)
    
    print("✅ Created .env file with TRAE.AI configuration")
    print("📝 Please edit .env file and add your actual API keys")

def update_config_from_env():
    """Update trae_ai_config.json from environment variables"""
    config_path = Path("config/trae_ai_config.json")
    
    if not config_path.exists():
        print("❌ config/trae_ai_config.json not found")
        return False
    
    # Load existing config
    with open(config_path, "r") as f:
        config = json.load(f)
    
    # Update from environment variables
    env_mappings = {
        "TRAE_MASTER_KEY": ["trae_master_key"],
        "OPENAI_API_KEY": ["openai_api_key", "chatgpt", "api_key"],
        "GOOGLE_AI_API_KEY": ["google_ai_api_key", "gemini", "api_key"],
        "ABACUS_API_KEY": ["abacus_api_key", "abacus", "api_key"],
        "TRAE_BASE_URL": ["base_url"],
        "CHATGPT_MODEL": ["chatgpt", "model"],
        "GEMINI_MODEL": ["gemini", "model"],
        "ABACUS_APP_ID": ["abacus", "app_id"]
    }
    
    updated = False
    for env_var, config_paths in env_mappings.items():
        env_value = os.getenv(env_var)
        if env_value and env_value != "your_" + env_var.lower() + "_here":
            # Navigate to the config location
            current = config
            for path in config_paths[:-1]:
                if path not in current:
                    current[path] = {}
                current = current[path]
            
            # Set the value
            current[config_paths[-1]] = env_value
            updated = True
            print(f"✅ Updated {'.'.join(config_paths)} from {env_var}")
    
    if updated:
        # Save updated config
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        print("✅ Updated config/trae_ai_config.json")
    else:
        print("ℹ️  No environment variables found to update config")
    
    return True

def test_integration():
    """Test TRAE.AI integration"""
    try:
        from app.trae_ai_integration import test_trae_ai_connection
        import asyncio
        
        print("🧪 Testing TRAE.AI integration...")
        result = asyncio.run(test_trae_ai_connection())
        
        if result.get("status") == "success":
            print("✅ TRAE.AI integration test passed!")
            platforms = result.get("platforms_available", {})
            for platform, available in platforms.items():
                status = "✅" if available else "❌"
                print(f"  {status} {platform.upper()}: {'Available' if available else 'Not configured'}")
        else:
            print("❌ TRAE.AI integration test failed:")
            print(f"   Error: {result.get('error', 'Unknown error')}")
        
        return result.get("status") == "success"
        
    except ImportError as e:
        print(f"❌ Cannot test integration: {e}")
        print("   Make sure you're running from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 TRAE.AI Integration Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("app/main.py").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Update config from environment variables
    if update_config_from_env():
        print("✅ Configuration updated successfully")
    else:
        print("⚠️  Could not update configuration")
    
    print("\n📋 Next Steps:")
    print("1. Edit .env file and add your API keys")
    print("2. Run: python setup_trae_ai.py --test")
    print("3. Start your application: python -m uvicorn app.main:app --reload")
    
    # Test if requested
    if "--test" in sys.argv:
        print("\n🧪 Running integration test...")
        test_integration()

if __name__ == "__main__":
    main()
