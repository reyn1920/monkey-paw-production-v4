
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
