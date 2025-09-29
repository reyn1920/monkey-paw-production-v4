#!/usr/bin/env python3
"""
Test script for Nemotron-9B integration via OpenRouter API
Tests coding, debugging, and diff generation capabilities
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from backend.llm.providers.nemotron_client import (
    nemo9b_chat,
    nemo9b_code_generation,
    nemo9b_code_review,
    nemo9b_debug_assistance,
    nemo9b_propose_diff,
    nemo9b_guided_debugging_loop
)

async def test_basic_chat():
    """Test basic chat functionality"""
    print("🧪 Testing basic chat functionality...")
    
    messages = [
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Hello! Can you help me with Python programming?"}
    ]
    
    try:
        response = await nemo9b_chat(messages)
        print("✅ Basic chat test passed")
        print(f"Response: {response.get('choices', [{}])[0].get('message', {}).get('content', 'No content')[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Basic chat test failed: {e}")
        return False

async def test_code_generation():
    """Test code generation functionality"""
    print("\n🧪 Testing code generation...")
    
    prompt = "Create a Python function that calculates the factorial of a number using recursion"
    
    try:
        code = await nemo9b_code_generation(prompt, "python")
        print("✅ Code generation test passed")
        print(f"Generated code preview:\n{code[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Code generation test failed: {e}")
        return False

async def test_code_review():
    """Test code review functionality"""
    print("\n🧪 Testing code review...")
    
    sample_code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
"""
    
    try:
        review = await nemo9b_code_review(sample_code, "python")
        print("✅ Code review test passed")
        print(f"Review preview:\n{review[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Code review test failed: {e}")
        return False

async def test_debug_assistance():
    """Test debugging assistance"""
    print("\n🧪 Testing debug assistance...")
    
    error_message = "RecursionError: maximum recursion depth exceeded"
    code_context = """
def factorial(n):
    return n * factorial(n-1)

result = factorial(5)
"""
    
    try:
        debug_help = await nemo9b_debug_assistance(error_message, code_context, "python")
        print("✅ Debug assistance test passed")
        print(f"Debug help preview:\n{debug_help[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Debug assistance test failed: {e}")
        return False

async def test_propose_diff():
    """Test diff proposal functionality"""
    print("\n🧪 Testing diff proposal...")
    
    original_code = """
def greet(name):
    print("Hello " + name)
"""
    
    requirements = "Add error handling for empty names and return the greeting instead of printing it"
    
    try:
        diff = await nemo9b_propose_diff(original_code, requirements, "python")
        print("✅ Diff proposal test passed")
        print(f"Proposed changes preview:\n{diff[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Diff proposal test failed: {e}")
        return False

async def test_guided_debugging():
    """Test guided debugging loop"""
    print("\n🧪 Testing guided debugging loop...")
    
    problem = "Function returns incorrect results for edge cases"
    code = """
def divide_numbers(a, b):
    return a / b
"""
    
    try:
        debugging_steps = await nemo9b_guided_debugging_loop(problem, code, "python", max_iterations=1)
        print("✅ Guided debugging test passed")
        print(f"Debugging steps: {len(debugging_steps)} step(s) generated")
        if debugging_steps:
            print(f"First step preview:\n{debugging_steps[0]['solution'][:200]}...")
        return True
    except Exception as e:
        print(f"❌ Guided debugging test failed: {e}")
        return False

async def check_environment():
    """Check if environment is properly configured"""
    print("🔧 Checking environment configuration...")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("LLM_MODEL_NEMO9B")
    
    if not api_key or api_key == "__PASTE_KEY_HERE__":
        print("⚠️  OPENROUTER_API_KEY not set or still placeholder")
        print("   Please update .env.local with your actual OpenRouter API key")
        return False
    
    if not model:
        print("⚠️  LLM_MODEL_NEMO9B not set, using default")
    else:
        print(f"✅ Model configured: {model}")
    
    print(f"✅ API key configured (length: {len(api_key)})")
    return True

async def main():
    """Run all integration tests"""
    print("🚀 Starting Nemotron-9B Integration Tests")
    print("=" * 50)
    
    # Check environment first
    env_ok = await check_environment()
    if not env_ok:
        print("\n❌ Environment configuration issues detected")
        print("Please fix configuration before running tests")
        return
    
    # Run all tests
    tests = [
        test_basic_chat,
        test_code_generation,
        test_code_review,
        test_debug_assistance,
        test_propose_diff,
        test_guided_debugging
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Nemotron-9B integration is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the configuration and try again.")

if __name__ == "__main__":
    # Load environment variables from .env.local
    env_local_path = Path(__file__).parent / ".env.local"
    if env_local_path.exists():
        with open(env_local_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    # Remove quotes if present
                    value = value.strip('"\'')
                    os.environ[key] = value
    
    asyncio.run(main())