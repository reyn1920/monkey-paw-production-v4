#!/usr/bin/env python3
"""
Integration Example: Replacing WebAIClient with ResilientAIGateway

This example demonstrates how to update existing code to use the ResilientAIGateway
instead of calling WebAIClient directly, providing automatic failover and circuit
breaker functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add the parent directory to the path to import the gateway
sys.path.insert(0, str(Path(__file__).parent.parent))

# Direct import from local file
from resilient_ai_gateway import ResilientAIGateway


class IntegratedAIService:
    """
    Example service class showing how to integrate the ResilientAIGateway
    """

    def __init__(self, provider_priority=None):
        """Initialize with the resilient gateway instead of direct WebAIClient"""
        # OLD WAY (unreliable):
        # from web_ai_client_fixed import WebAIClient
        # self.client = WebAIClient()

        # NEW WAY (resilient):
        self.gateway = ResilientAIGateway(provider_priority)

    async def send_message(self, message: str) -> str:
        """
        Send a message using the resilient gateway
        This automatically handles failover and circuit breaker logic
        """
        try:
            response = self.gateway.chat_completion(message)
            return response
        except ConnectionError as e:
            # All providers failed - handle gracefully
            return f"Service temporarily unavailable: {e}"

    def get_gateway_status(self) -> dict:
        """Get the current status of the gateway"""
        return self.gateway.get_gateway_status()


class LegacyCodeAdapter:
    """
    Adapter class to help migrate legacy code that uses WebAIClient directly
    """

    def __init__(self):
        self.gateway = ResilientAIGateway()

    async def chat_completion(
        self, platform: str, message: str, session_id=None
    ) -> dict:
        """
        Legacy-compatible method that mimics WebAIClient.chat_completion
        but uses the resilient gateway internally
        """
        try:
            # The gateway handles provider selection automatically
            response = self.gateway.chat_completion(message)

            # Return in the format expected by legacy code
            return {
                "success": True,
                "response": response,
                "platform": platform,  # Use the requested platform
                "session_id": session_id or "gateway-managed",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "platform": platform,
                "session_id": session_id,
            }

    def create_session(self, platform: str) -> str:
        """Legacy-compatible session creation (gateway manages sessions internally)"""
        return f"gateway-session-{platform}"

    def get_session_stats(self) -> dict:
        """Legacy-compatible session stats"""
        status = self.gateway.get_gateway_status()
        return {
            "active_sessions": (
                1 if status["health_summary"]["healthy_providers"] > 0 else 0
            ),
            "total_sessions": status["metrics"]["total_requests"],
            "gateway_status": status,
        }


async def demonstrate_integration():
    """Demonstrate the integration with various usage patterns"""

    print("=== ResilientAIGateway Integration Demo ===\n")

    # 1. Direct usage with new service class
    print("1. Using IntegratedAIService (recommended approach):")
    service = IntegratedAIService()

    response = await service.send_message("Explain quantum computing briefly")
    print(f"Response: {response[:100]}...")

    status = service.get_gateway_status()
    print(f"Gateway Providers: {status['gateway_info']['providers']}")
    print(f"Circuit Breakers: {status['circuit_breakers']}")
    print(f"Health Summary: {status['health_summary']}")
    print()

    # 2. Legacy code adaptation
    print("2. Using LegacyCodeAdapter (for existing code migration):")
    adapter = LegacyCodeAdapter()

    # This looks like the old WebAIClient API but uses the gateway
    legacy_response = await adapter.chat_completion(
        "chatgpt", "What is machine learning?"
    )
    print(f"Legacy Response Success: {legacy_response['success']}")
    if legacy_response["success"]:
        print(f"Response: {legacy_response['response'][:100]}...")
        print(f"Provider Used: {legacy_response['platform']}")

    stats = adapter.get_session_stats()
    print(f"Session Stats: {stats}")
    print()

    # 3. Direct gateway usage (most flexible)
    print("3. Direct ResilientAIGateway usage (most control):")
    gateway = ResilientAIGateway(["gemini", "chatgpt", "claude"])

    try:
        direct_response = gateway.chat_completion("Describe the benefits of AI")
        print(f"Direct Response: {direct_response[:100]}...")

        # Get status to see which provider was used
        status = gateway.get_gateway_status()
        print(f"Gateway Status: {status['health_summary']}")
    except Exception as e:
        print(f"Request failed: {e}")

    # Show final status
    final_status = gateway.get_gateway_status()
    print(f"Final Gateway Status: {final_status}")


def create_migration_guide():
    """Create a migration guide for existing code"""

    migration_guide = """
# Migration Guide: WebAIClient → ResilientAIGateway

## Before (Unreliable):
```python
from web_ai_client_fixed import WebAIClient

client = WebAIClient()
response = await client.chat_completion("chatgpt", "Hello")
# If ChatGPT fails, the entire request fails
```

## After (Resilient):
```python
from trae_ai.gateways.resilient_ai_gateway import ResilientAIGateway

gateway = ResilientAIGateway(["chatgpt", "gemini", "claude"])
response = await gateway.chat_completion("Hello")
# If ChatGPT fails, automatically tries Gemini, then Claude
```

## Migration Steps:

1. **Replace imports:**
   - Remove: `from web_ai_client_fixed import WebAIClient`
   - Add: `from trae_ai.gateways.resilient_ai_gateway import ResilientAIGateway`

2. **Update initialization:**
   - Replace: `client = WebAIClient()`
   - With: `gateway = ResilientAIGateway()`

3. **Update method calls:**
   - Replace: `client.chat_completion(platform, message)`
   - With: `gateway.chat_completion(message)`
   - Note: Gateway handles provider selection automatically

4. **Add error handling:**
   ```python
   try:
       response = await gateway.chat_completion(message)
   except ConnectionError:
       # All providers failed - handle gracefully
       pass
   ```

5. **Monitor gateway status:**
   ```python
   status = gateway.get_status()
   print(f"Gateway health: {status['status']}")
   ```

## Benefits:
- ✅ Automatic failover between providers
- ✅ Circuit breaker prevents wasted requests to failing services
- ✅ Detailed metrics and status reporting
- ✅ Backward compatibility with existing code patterns
- ✅ No more "Session not found" errors causing complete failures
"""

    with open(
        "/Users/thomasbrianreynolds/online production/trae_ai/gateways/MIGRATION_GUIDE.md",
        "w",
    ) as f:
        f.write(migration_guide)

    print("Migration guide created: trae_ai/gateways/MIGRATION_GUIDE.md")


if __name__ == "__main__":
    print("Starting integration demonstration...")
    asyncio.run(demonstrate_integration())
    print("\nCreating migration guide...")
    create_migration_guide()
    print("\nIntegration example completed successfully!")
