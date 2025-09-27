#!/usr/bin/env python3
"""
Test script for WebAI Client - ChatGPT Session Management Fix
"""

import asyncio
import sys
import json
from pathlib import Path

# Add the current directory to the path for the fixed client
sys.path.insert(0, str(Path(__file__).parent))

from web_ai_client_fixed import get_web_ai_client


async def test_chatgpt_session_management():
    """Test ChatGPT session management functionality"""
    print("🧪 Testing WebAI Client - ChatGPT Session Management Fix")
    print("=" * 60)

    # Initialize client
    client = get_web_ai_client()

    # Test 1: Create ChatGPT session
    print("\n1️⃣ Testing ChatGPT session creation...")
    try:
        session_id = client.create_session("chatgpt")
        print(f"✅ Created ChatGPT session: {session_id}")
    except Exception as e:
        print(f"❌ Failed to create ChatGPT session: {e}")
        return False

    # Test 2: Verify session exists
    print("\n2️⃣ Testing session retrieval...")
    try:
        session = client.get_session(session_id)
        if session:
            print(
                f"✅ Retrieved session: {session.session_id} for platform: {session.platform}"
            )
        else:
            print("❌ Session not found")
            return False
    except Exception as e:
        print(f"❌ Failed to retrieve session: {e}")
        return False

    # Test 3: Send web request
    print("\n3️⃣ Testing web request with ChatGPT session...")
    try:
        response = await client.send_web_request(session_id, "Hello, ChatGPT!")
        print("✅ Web request successful:")
        print(f"   Session ID: {response['session_id']}")
        print(f"   Platform: {response['platform']}")
        print(f"   Status: {response['status']}")
    except Exception as e:
        print(f"❌ Web request failed: {e}")
        return False

    # Test 4: Chat completion
    print("\n4️⃣ Testing chat completion...")
    try:
        response = await client.chat_completion("chatgpt", "Test message for ChatGPT")
        print("✅ Chat completion successful:")
        print(f"   Platform: {response['platform']}")
        print(f"   Status: {response['status']}")
    except Exception as e:
        print(f"❌ Chat completion failed: {e}")
        return False

    # Test 5: Session reuse
    print("\n5️⃣ Testing session reuse...")
    try:
        # Create another session for ChatGPT - should reuse existing
        new_session_id = client.create_session("chatgpt")
        print(f"✅ Session creation returned: {new_session_id}")

        # Check if it's the same session (reused) or different
        if new_session_id == session_id:
            print("✅ Session was reused (expected behavior)")
        else:
            print("ℹ️ New session created (also valid)")
    except Exception as e:
        print(f"❌ Session reuse test failed: {e}")
        return False

    # Test 6: Multiple platforms
    print("\n6️⃣ Testing multiple platform sessions...")
    try:
        gemini_session = client.create_session("gemini")
        claude_session = client.create_session("claude")

        print(f"✅ Created Gemini session: {gemini_session}")
        print(f"✅ Created Claude session: {claude_session}")

        # Test session stats
        stats = client.get_session_stats()
        print(f"✅ Session stats: {json.dumps(stats, indent=2)}")

    except Exception as e:
        print(f"❌ Multiple platform test failed: {e}")
        return False

    # Test 7: Session with invalid ID
    print("\n7️⃣ Testing invalid session handling...")
    try:
        invalid_session = client.get_session("invalid_session_id")
        if invalid_session is None:
            print("✅ Invalid session correctly returned None")
        else:
            print("❌ Invalid session should return None")
            return False
    except Exception as e:
        print(f"❌ Invalid session test failed: {e}")
        return False

    # Test 8: Web request with invalid session
    print("\n8️⃣ Testing web request with invalid session...")
    try:
        await client.send_web_request("invalid_session", "test message")
        print("❌ Should have raised ValueError for invalid session")
        return False
    except ValueError as e:
        if "not found" in str(e):
            print("✅ Correctly raised ValueError for invalid session")
        else:
            print(f"❌ Unexpected ValueError: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

    print("\n" + "=" * 60)
    print("🎉 All tests passed! ChatGPT session management is working correctly.")
    return True


async def test_session_cleanup():
    """Test session cleanup functionality"""
    print("\n🧹 Testing session cleanup...")

    client = get_web_ai_client()

    # Create multiple sessions
    sessions = []
    for i in range(5):
        session_id = client.create_session("chatgpt")
        sessions.append(session_id)

    print(f"Created {len(sessions)} sessions")

    # Check active sessions
    active_sessions = client.get_active_sessions()
    print(f"Active sessions: {len(active_sessions)}")

    # Force cleanup
    client._cleanup_expired_sessions()

    # Check stats
    stats = client.get_session_stats()
    print(f"Final stats: {json.dumps(stats, indent=2)}")


def main():
    """Main test function"""
    print("Starting WebAI Client Tests...")

    try:
        # Run async tests
        success = asyncio.run(test_chatgpt_session_management())

        if success:
            # Run cleanup test
            asyncio.run(test_session_cleanup())
            print("\n✅ All tests completed successfully!")
            return 0
        else:
            print("\n❌ Some tests failed!")
            return 1

    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
