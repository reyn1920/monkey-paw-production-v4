# Abacus AI MCP Server

This is a Model Context Protocol (MCP) server implementation for integrating Abacus.AI's Route LLM APIs with Trae.AI.

## Features

- **Route LLM Integration**: Access to Abacus.AI's intelligent model routing capabilities
- **Chat Completions**: Support for conversational AI interactions
- **Model Management**: Automatic model selection and routing optimization
- **Cost Tracking**: Monitor usage and costs across different models
- **Conversation Context**: Maintain conversation history and context
- **Async Support**: Built with async/await for optimal performance

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables:
```bash
# Create a .env file with your Abacus.AI credentials
ABACUS_AI_API_KEY=your_api_key_here
ABACUS_AI_BASE_URL=https://api.abacus.ai/v1  # Optional, defaults to this
```

## Usage

### Starting the MCP Server

```python
import asyncio
from abacus_ai_mcp import AbacusAIMCPServer, AbacusAIConfig

async def main():
    config = AbacusAIConfig(
        api_key="your_api_key",
        base_url="https://api.abacus.ai/v1",
        timeout=30.0
    )
    
    server = AbacusAIMCPServer(config)
    await server.start()
    
    # Server is now running and ready to handle MCP messages
    
if __name__ == "__main__":
    asyncio.run(main())
```

### Available Tools

1. **chat_completion**: Generate chat completions using Abacus.AI's Route LLM
   - Parameters: `messages`, `model` (optional), `max_tokens`, `temperature`, etc.

2. **route_llm_optimize**: Optimize model routing for specific tasks
   - Parameters: `task_type`, `priority`, `max_cost_per_token`

3. **get_model_metrics**: Retrieve usage and performance metrics
   - Returns: Token usage, costs, response times per model

4. **list_conversations**: Get active conversation contexts
   - Returns: List of conversation IDs and metadata

## Configuration

The server supports the following configuration options:

- `api_key`: Your Abacus.AI API key (required)
- `base_url`: API base URL (default: https://api.abacus.ai/v1)
- `timeout`: Request timeout in seconds (default: 30.0)
- `max_retries`: Maximum retry attempts (default: 3)
- `retry_delay`: Delay between retries in seconds (default: 1.0)

## Error Handling

The server includes comprehensive error handling for:
- Network connectivity issues
- API rate limiting
- Invalid requests
- Authentication failures
- Timeout scenarios

## Security

- API keys are never logged or exposed
- All requests use HTTPS
- Environment variables are used for sensitive configuration
- Input validation prevents injection attacks

## Development

To contribute to this project:

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
pytest tests/
```

3. Format code:
```bash
black abacus_ai_mcp.py
flake8 abacus_ai_mcp.py
```

4. Type checking:
```bash
mypy abacus_ai_mcp.py
```

## License

This project is licensed under the MIT License.