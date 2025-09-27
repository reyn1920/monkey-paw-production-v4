# RouteLL API Integration Guide

## Overview

This guide provides comprehensive documentation for integrating the RouteLL API into your Trae.ai project with advanced features including:

- 🎯 **Intelligent Model Routing** - Automatically select optimal models based on task type and constraints
- 💳 **Credit Monitoring** - Real-time tracking and optimization of API credit usage
- ⚡ **Rate Limiting** - Prevent API quota exhaustion with smart request management
- 📊 **Usage Analytics** - Detailed insights into API usage patterns and costs
- 🛡️ **Error Handling** - Robust fallback mechanisms and retry logic
- 🔧 **Cost Optimization** - Automatic parameter tuning to minimize costs while maintaining quality

## Quick Start

### 1. API Key Setup

Your RouteLL API key: `s2_f0b00d6897a0431f8367a7fc859b697a`

```bash
# Set environment variable
export ROUTELLM_API_KEY="s2_f0b00d6897a0431f8367a7fc859b697a"

# Or add to your .env file
echo "ROUTELLM_API_KEY=s2_f0b00d6897a0431f8367a7fc859b697a" >> .env
```

### 2. Basic Usage

```python
from examples.routellm_integration_example import RouteLL_IntegratedClient

# Initialize client
client = RouteLL_IntegratedClient()

# Simple chat completion
messages = [{"role": "user", "content": "What is machine learning?"}]
response = await client.chat_completion(messages)

if response.success:
    print(f"Response: {response.content}")
    print(f"Model used: {response.model}")
    print(f"Cost: ${response.usage.get('total_tokens', 0) * 0.002:.4f}")
else:
    print(f"Error: {response.error}")
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    RouteLL Integration Stack                    │
├─────────────────────────────────────────────────────────────────┤
│  Application Layer                                              │
│  ├── examples/routellm_integration_example.py                   │
│  └── Your Application Code                                      │
├─────────────────────────────────────────────────────────────────┤
│  Intelligence Layer                                             │
│  ├── routing/model_router.py        (Smart Model Selection)    │
│  ├── utils/rate_limiter.py          (Request Optimization)     │
│  └── monitoring/routellm_monitor.py (Usage Analytics)          │
├─────────────────────────────────────────────────────────────────┤
│  Integration Layer                                              │
│  ├── integrations/routellm_client.py (API Wrapper)             │
│  └── config/routellm_config.json    (Configuration)            │
├─────────────────────────────────────────────────────────────────┤
│  External Services                                              │
│  └── RouteLL API (https://routellm.abacus.ai/v1)              │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. RouteLL Client (`integrations/routellm_client.py`)

The main API wrapper with features:
- OpenAI-compatible interface
- Automatic retry logic
- Credit usage tracking
- Error handling and logging

```python
from integrations.routellm_client import RouteLL

client = RouteLL(api_key="your_api_key")

# Check API health
status = await client.health_check()
print(f"API Status: {status.success}")

# Get credit information
credits = await client.get_credit_status()
print(f"Remaining credits: {credits.remaining_credits}")

# Make a request
response = await client.chat_completion(
    messages=[{"role": "user", "content": "Hello!"}],
    model="route-llm",
    max_tokens=100
)
```

### 2. Model Router (`routing/model_router.py`)

Intelligent model selection based on:
- **Task Classification**: Automatically detects task type (code, math, creative, etc.)
- **Cost Optimization**: Balances quality vs. cost based on preferences
- **Performance History**: Learns from past routing decisions
- **Constraint Handling**: Respects budget and time limits

```python
from routing.model_router import ModelRouter, TaskType

router = ModelRouter()

# Route a request
messages = [{"role": "user", "content": "Write a Python function"}]
routing_result = router.route_request(
    messages,
    preferences={'cost': 0.3, 'quality': 0.7},  # Prefer quality over cost
    constraints={'max_cost_per_token': 0.01}     # Budget constraint
)

print(f"Selected model: {routing_result['routing_decision']['selected_model']}")
print(f"Task type: {routing_result['routing_decision']['task_type']}")
print(f"Estimated cost: ${routing_result['model_info']['cost_per_token']:.4f}/token")
```

### 3. Rate Limiter (`utils/rate_limiter.py`)

Prevents API quota exhaustion with:
- **Multi-window Rate Limiting**: Tracks requests across different time windows
- **Credit-aware Throttling**: Adjusts rate based on remaining credits
- **Request Optimization**: Automatically tunes parameters to reduce costs
- **Adaptive Strategies**: Learns optimal request patterns

```python
from utils.rate_limiter import RateLimiter, CreditOptimizer

rate_limiter = RateLimiter()
optimizer = CreditOptimizer(rate_limiter)

# Check if request is allowed
if rate_limiter.can_make_request():
    # Optimize request parameters
    optimized = optimizer.optimize_request(
        messages,
        preferences={'cost': 0.8, 'speed': 0.2}
    )
    print(f"Optimized max_tokens: {optimized['max_tokens']}")
    print(f"Optimized temperature: {optimized['temperature']}")
else:
    wait_time = rate_limiter.get_wait_time()
    print(f"Rate limited. Wait {wait_time:.1f} seconds")
```

### 4. Credit Monitor (`monitoring/routellm_monitor.py`)

Real-time credit tracking with:
- **Usage Analytics**: Detailed breakdowns of credit consumption
- **Alert System**: Notifications for low credits or unusual usage
- **Trend Analysis**: Historical usage patterns and predictions
- **Cost Reporting**: Detailed cost analysis and optimization suggestions

```python
from monitoring.routellm_monitor import RouteLL_Monitor

monitor = RouteLL_Monitor()

# Start monitoring
monitor.start_monitoring()

# Get current status
status = monitor.get_current_status()
print(f"Credits remaining: {status['credits_remaining']}")
print(f"Daily usage: {status['daily_usage']}")
print(f"Projected monthly cost: ${status['projected_monthly_cost']:.2f}")

# Get usage analytics
analytics = monitor.get_usage_analytics()
print(f"Total requests today: {analytics['daily_stats']['total_requests']}")
print(f"Average cost per request: ${analytics['daily_stats']['avg_cost_per_request']:.4f}")
```

### 5. Usage Dashboard (`dashboard/routellm_dashboard.py`)

Web-based monitoring interface:
- **Real-time Metrics**: Live credit usage and API status
- **Usage Trends**: Historical charts and analytics
- **Alert Management**: Configure and manage alerts
- **API Testing**: Built-in API testing tools
- **Cost Optimization**: Recommendations and settings

```bash
# Start the dashboard
python dashboard/routellm_dashboard.py

# Access at http://localhost:5000
```

## Configuration

### Main Configuration (`config/routellm_config.json`)

```json
{
  "api": {
    "base_url": "https://routellm.abacus.ai/v1",
    "timeout": 30,
    "max_retries": 3,
    "retry_delay": 1.0
  },
  "credit_system": {
    "low_credit_threshold": 100,
    "critical_credit_threshold": 10,
    "unlimited_models": ["llama-3.1-8b", "gemma-2-9b"],
    "high_cost_models": ["gpt-4", "claude-3-opus"]
  },
  "rate_limiting": {
    "requests_per_minute": 60,
    "requests_per_hour": 1000,
    "burst_limit": 10,
    "adaptive_throttling": true
  },
  "model_routing": {
    "enabled": true,
    "learning_enabled": true,
    "fallback_model": "route-llm",
    "max_routing_time": 0.1
  },
  "monitoring": {
    "enabled": true,
    "alert_webhooks": [],
    "log_level": "INFO",
    "metrics_retention_days": 30
  }
}
```

### Provider Configuration (`config/integrations.providers.json`)

The RouteLL provider is automatically added to your existing providers:

```json
{
  "routellm": {
    "id": "routellm",
    "kind": "llm_api",
    "name": "RouteLL API",
    "enabled": true,
    "key_env_var": "ROUTELLM_API_KEY",
    "base_url": "https://routellm.abacus.ai/v1",
    "docs_url": "https://routellm.abacus.ai/docs",
    "health": {
      "status": "unknown",
      "last_check": null,
      "last_error": null,
      "last_ok": null
    },
    "usage": {
      "requests_today": 0,
      "credits_used_today": 0,
      "total_requests": 0,
      "total_credits_used": 0
    },
    "features": {
      "unlimited_models": ["llama-3.1-8b", "gemma-2-9b"],
      "premium_models": ["gpt-4", "claude-3-opus", "gemini-pro"]
    }
  }
}
```

## Advanced Usage

### 1. Custom Model Routing

```python
from routing.model_router import ModelRouter, TaskType, ModelCapability, ModelTier

router = ModelRouter()

# Add custom model
custom_model = ModelCapability(
    name="custom-model",
    tier=ModelTier.SPECIALIZED,
    cost_per_token=0.005,
    max_tokens=8192,
    strengths=[TaskType.CODE_GENERATION, TaskType.ANALYSIS],
    quality_score=0.9
)
router.models["custom-model"] = custom_model

# Route with custom preferences
result = router.route_request(
    messages,
    preferences={'cost': 0.2, 'quality': 0.6, 'speed': 0.2},
    constraints={'max_cost_per_token': 0.01, 'min_context_window': 4096}
)
```

### 2. Streaming with Optimization

```python
async def optimized_streaming():
    client = RouteLL_IntegratedClient()

    messages = [{"role": "user", "content": "Write a long story about AI"}]

    print("Streaming optimized response:")
    async for chunk in client.stream_completion(
        messages,
        preferences={'cost': 0.7, 'quality': 0.3},  # Optimize for cost
        temperature=0.7,
        max_tokens=1000
    ):
        print(chunk, end='', flush=True)

    # Get session analytics
    analytics = client.get_session_analytics()
    print(f"\nTotal cost: ${analytics['estimated_total_cost']:.4f}")
```

### 3. Batch Processing with Rate Limiting

```python
async def batch_process_requests(requests_list):
    client = RouteLL_IntegratedClient()
    results = []

    for i, messages in enumerate(requests_list):
        print(f"Processing request {i+1}/{len(requests_list)}")

        # The client automatically handles rate limiting
        response = await client.chat_completion(
            messages,
            preferences={'cost': 0.8, 'speed': 0.2}  # Optimize for cost in batch
        )

        results.append(response)

        # Optional: Add delay between requests
        if i < len(requests_list) - 1:
            await asyncio.sleep(0.1)

    return results
```

### 4. Custom Alert Handlers

```python
from monitoring.routellm_monitor import RouteLL_Monitor

class CustomAlertHandler:
    def handle_low_credits(self, credits_remaining):
        print(f"⚠️ Low credits alert: {credits_remaining} remaining")
        # Send email, Slack notification, etc.

    def handle_high_usage(self, usage_rate):
        print(f"📈 High usage alert: {usage_rate} requests/hour")
        # Implement throttling, notifications, etc.

# Set up monitoring with custom handlers
monitor = RouteLL_Monitor()
alert_handler = CustomAlertHandler()

monitor.add_alert_handler('low_credits', alert_handler.handle_low_credits)
monitor.add_alert_handler('high_usage', alert_handler.handle_high_usage)
monitor.start_monitoring()
```

## API Reference

### RouteLL_IntegratedClient

#### Methods

- `chat_completion(messages, **kwargs)` - Enhanced chat completion with routing and optimization
- `stream_completion(messages, **kwargs)` - Streaming completion with full integration
- `get_session_analytics()` - Get comprehensive session statistics
- `health_check()` - Check system health and connectivity

#### Parameters

- `messages`: List of message dictionaries (required)
- `preferences`: Dict with 'cost', 'quality', 'speed' weights (0-1)
- `constraints`: Dict with 'max_cost_per_token', 'max_time', etc.
- `temperature`: Sampling temperature (0-2)
- `max_tokens`: Maximum tokens to generate
- `stream`: Enable streaming response
- `model`: Override model selection (optional)

### ModelRouter

#### Methods

- `route_request(messages, preferences, constraints)` - Route request to optimal model
- `classify_task(messages)` - Classify task type from messages
- `suggest_model_for_task(description, budget)` - Get model recommendation
- `record_request_outcome(model, task_type, success, time, quality)` - Record performance
- `get_routing_analytics()` - Get routing statistics

### RateLimiter

#### Methods

- `can_make_request()` - Check if request is allowed
- `record_request()` - Record a completed request
- `get_wait_time()` - Get time to wait before next request
- `get_current_usage()` - Get current usage statistics

### CreditOptimizer

#### Methods

- `optimize_request(messages, preferences)` - Optimize request parameters
- `estimate_cost(messages, params)` - Estimate request cost
- `suggest_budget_allocation(total_budget, time_period)` - Budget recommendations

## Monitoring and Analytics

### Dashboard Features

1. **Real-time Status**
   - Current credit balance
   - API health status
   - Active rate limits
   - Recent request activity

2. **Usage Analytics**
   - Daily/weekly/monthly usage trends
   - Cost breakdown by model
   - Request success rates
   - Average response times

3. **Model Performance**
   - Model usage distribution
   - Quality ratings by model
   - Cost efficiency metrics
   - Routing decision analytics

4. **Alerts and Notifications**
   - Low credit warnings
   - High usage alerts
   - API error notifications
   - Cost threshold breaches

### Accessing Analytics

```python
# Get comprehensive analytics
client = RouteLL_IntegratedClient()
analytics = client.get_session_analytics()

print(f"Session Summary:")
print(f"  Duration: {analytics['session_duration_minutes']:.1f} minutes")
print(f"  Requests: {analytics['total_requests']}")
print(f"  Success Rate: {analytics['success_rate']:.1f}%")
print(f"  Total Cost: ${analytics['estimated_total_cost']:.4f}")
print(f"  Avg Cost/Request: ${analytics['avg_cost_per_request']:.4f}")

# Model usage breakdown
routing_stats = analytics['routing']
print(f"\nModel Usage:")
for model, count in routing_stats['model_usage_distribution'].items():
    percentage = (count / routing_stats['total_routing_decisions']) * 100
    print(f"  {model}: {count} requests ({percentage:.1f}%)")

# Task type distribution
print(f"\nTask Types:")
for task, count in routing_stats['task_type_distribution'].items():
    percentage = (count / routing_stats['total_routing_decisions']) * 100
    print(f"  {task}: {count} requests ({percentage:.1f}%)")
```

## Best Practices

### 1. Credit Management

- **Monitor Usage**: Set up alerts for 80% and 95% credit consumption
- **Use Free Models**: Leverage unlimited models for simple tasks
- **Optimize Parameters**: Use the CreditOptimizer for cost-sensitive applications
- **Batch Requests**: Group similar requests to optimize routing decisions

### 2. Performance Optimization

- **Cache Results**: Implement response caching for repeated queries
- **Async Processing**: Use async/await for concurrent requests
- **Smart Routing**: Let the ModelRouter learn from your usage patterns
- **Parameter Tuning**: Adjust temperature and max_tokens based on task requirements

### 3. Error Handling

- **Implement Retries**: The client includes automatic retry logic
- **Handle Rate Limits**: Use the built-in rate limiting to prevent quota exhaustion
- **Monitor Health**: Regular health checks ensure API availability
- **Fallback Strategies**: Configure fallback models for critical applications

### 4. Security

- **Environment Variables**: Store API keys in environment variables, not code
- **Access Control**: Limit API key permissions to necessary scopes
- **Audit Logs**: Monitor API usage for unusual patterns
- **Rotate Keys**: Regularly rotate API keys for security

## Troubleshooting

### Common Issues

1. **API Key Issues**
   ```bash
   # Verify API key is set
   echo $ROUTELLM_API_KEY

   # Test API connectivity
   python -c "from integrations.routellm_client import RouteLL; import asyncio; asyncio.run(RouteLL().health_check())"
   ```

2. **Rate Limiting**
   ```python
   # Check current rate limit status
   from utils.rate_limiter import RateLimiter
   limiter = RateLimiter()
   print(f"Can make request: {limiter.can_make_request()}")
   print(f"Wait time: {limiter.get_wait_time():.1f}s")
   ```

3. **Model Routing Issues**
   ```python
   # Debug routing decisions
   from routing.model_router import ModelRouter
   router = ModelRouter()
   analytics = router.get_routing_analytics()
   print(f"Available models: {analytics['available_models']}")
   print(f"Recent decisions: {len(router.routing_history)}")
   ```

4. **Credit Monitoring**
   ```python
   # Check credit status
   from integrations.routellm_client import RouteLL
   client = RouteLL()
   status = await client.get_credit_status()
   print(f"Credits remaining: {status.remaining_credits}")
   ```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Initialize client with debug info
client = RouteLL_IntegratedClient()
print("Debug info:")
print(f"  Config loaded: {bool(client.config)}")
print(f"  Models available: {len(client.router.models)}")
print(f"  Rate limiter active: {client.rate_limiter is not None}")
print(f"  Monitor running: {client.monitor is not None}")
```

## Support and Resources

- **RouteLL Documentation**: https://routellm.abacus.ai/docs
- **API Reference**: https://routellm.abacus.ai/v1/docs
- **Trae.ai Documentation**: https://trae.ai/docs
- **GitHub Issues**: Report issues in your project repository

## License

This integration is part of your Trae.ai project and follows the same licensing terms.

---

**Note**: This integration maximizes your RouteLL API credits through intelligent routing, cost optimization, and usage monitoring. The system automatically balances cost, quality, and performance based on your preferences and constraints.
