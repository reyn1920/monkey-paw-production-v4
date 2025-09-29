# TRAE.AI Integration Guide

This document provides comprehensive instructions for connecting and using the TRAE.AI integration in your Monkey Paw Production v4 system.

## Overview

The TRAE.AI integration provides seamless connectivity to three major AI platforms:
- **ChatGPT** (OpenAI)
- **Google Gemini** 
- **Abacus AI**

All platforms work together with cross-validation to ensure high-quality, reliable AI-generated content.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Configuration

Run the setup script to create configuration files:

```bash
python setup_trae_ai.py
```

This will create:
- `.env` file with environment variables
- `config/trae_ai_config.json` with API configurations

### 3. Configure API Keys

Edit the `.env` file and add your API keys:

```bash
# OpenAI API Key (for ChatGPT)
OPENAI_API_KEY=sk-your-openai-key-here

# Google AI API Key (for Gemini)
GOOGLE_AI_API_KEY=your-google-ai-key-here

# Abacus AI API Key (for Abacus AI)
ABACUS_API_KEY=your-abacus-key-here

# TRAE.AI Master Key (if using local TRAE.AI system)
TRAE_MASTER_KEY=your-trae-master-key-here
```

### 4. Test Integration

```bash
python setup_trae_ai.py --test
```

### 5. Start the Application

```bash
python -m uvicorn app.main:app --reload
```

## API Endpoints

The TRAE.AI integration adds the following endpoints to your FastAPI application:

### System Status
- `GET /api/trae-ai/status` - Get TRAE.AI system status
- `GET /api/trae-ai/health` - Health check for all platforms
- `GET /api/trae-ai/test-connection` - Test all AI platform connections

### Content Generation
- `POST /api/trae-ai/generate-content` - Generate content using all AI platforms
- `POST /api/trae-ai/batch/generate-content` - Batch content generation

### Research & Analysis
- `POST /api/trae-ai/research` - Perform research analysis across platforms

### Video Production
- `POST /api/trae-ai/create-video` - Create videos using TRAE.AI pipeline

### Platform Management
- `GET /api/trae-ai/platforms/status` - Get status of individual AI platforms
- `GET /api/trae-ai/config` - Get current configuration
- `POST /api/trae-ai/reload-config` - Reload configuration

### Webhooks
- `POST /api/trae-ai/webhook/task-completed` - Handle task completion callbacks
- `POST /api/trae-ai/webhook/task-progress` - Handle progress updates

## Usage Examples

### Generate Content

```python
import requests

# Generate content with cross-validation
response = requests.post("http://localhost:8000/api/trae-ai/generate-content", json={
    "prompt": "Create a video script about AI automation",
    "content_type": "video",
    "cross_validate": True,
    "parameters": {
        "duration": 300,
        "style": "professional"
    }
})

result = response.json()
print(f"Generated content: {result['result']['content']}")
print(f"Confidence: {result['result']['confidence']}")
```

### Research Analysis

```python
# Perform research analysis
response = requests.post("http://localhost:8000/api/trae-ai/research", json={
    "query": "Latest trends in renewable energy technology",
    "sources": ["news", "academic", "social_media"],
    "depth": "comprehensive"
})

research = response.json()
print(f"Key findings: {research['result']['synthesized_findings']}")
```

### Create Video

```python
# Create video with custom settings
response = requests.post("http://localhost:8000/api/trae-ai/create-video", json={
    "script": "Welcome to our AI automation tutorial...",
    "voice_settings": {
        "voice_id": "professional_male",
        "speed": 1.0,
        "volume": 0.8
    },
    "video_settings": {
        "resolution": "1920x1080",
        "fps": 30,
        "quality": "high"
    }
})

video_result = response.json()
print(f"Video created: {video_result['result']}")
```

## Configuration Options

### Cross-Validation Settings

```json
{
  "cross_validate": true,
  "confidence_threshold": 0.8
}
```

- `cross_validate`: Enable/disable cross-validation across AI platforms
- `confidence_threshold`: Minimum confidence score for accepting results

### Platform-Specific Settings

```json
{
  "chatgpt": {
    "api_key": "your-openai-key",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4"
  },
  "gemini": {
    "api_key": "your-google-ai-key",
    "base_url": "https://generativelanguage.googleapis.com/v1",
    "model": "gemini-pro"
  },
  "abacus": {
    "api_key": "your-abacus-key",
    "base_url": "https://apps.abacus.ai/chatllm",
    "app_id": "1024a18ebe"
  }
}
```

## Integration Features

### Cross-Validation
- All AI platforms generate content for the same prompt
- Results are compared and validated for consistency
- Highest confidence result is selected or consensus is built

### Error Handling
- Graceful fallback if one platform fails
- Detailed error reporting and logging
- Automatic retry mechanisms

### Performance Optimization
- Asynchronous processing for all AI calls
- Connection pooling and session management
- Caching of frequently used configurations

### Security
- API keys stored securely in environment variables
- No sensitive data in logs or responses
- Rate limiting and request validation

## Troubleshooting

### Common Issues

1. **API Key Errors**
   ```
   Error: Invalid API key
   Solution: Check your API keys in .env file
   ```

2. **Connection Timeouts**
   ```
   Error: Connection timeout
   Solution: Check internet connection and API endpoint URLs
   ```

3. **Cross-Validation Failures**
   ```
   Error: Insufficient results for cross-validation
   Solution: Ensure at least 2 AI platforms are configured
   ```

### Debug Mode

Enable debug logging by setting:
```bash
export LOG_LEVEL=DEBUG
```

### Health Checks

Check individual platform status:
```bash
curl http://localhost:8000/api/trae-ai/platforms/status
```

## Advanced Usage

### Custom AI Models

You can configure custom models for each platform:

```json
{
  "chatgpt": {
    "model": "gpt-4-turbo"
  },
  "gemini": {
    "model": "gemini-pro-vision"
  }
}
```

### Batch Processing

Process multiple requests efficiently:

```python
requests_data = [
    {"prompt": "Script 1", "content_type": "video"},
    {"prompt": "Script 2", "content_type": "video"},
    {"prompt": "Script 3", "content_type": "video"}
]

response = requests.post(
    "http://localhost:8000/api/trae-ai/batch/generate-content",
    json=requests_data
)
```

### Webhook Integration

Set up webhooks for async processing:

```python
# Your webhook endpoint
@app.post("/webhook/trae-ai")
async def handle_trae_webhook(request: dict):
    task_id = request.get("task_id")
    status = request.get("status")
    
    if status == "completed":
        # Process completed task
        result = request.get("result")
        # ... handle result
```

## Monitoring and Analytics

### Usage Analytics

Get usage statistics:
```bash
curl http://localhost:8000/api/trae-ai/analytics/usage
```

### System Health

Monitor system health:
```bash
curl http://localhost:8000/api/trae-ai/health
```

## Support

For issues or questions:
1. Check the logs for detailed error messages
2. Run the test connection endpoint
3. Verify API keys and configuration
4. Check network connectivity to AI platforms

## Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables for sensitive data**
3. **Regularly rotate API keys**
4. **Monitor usage and set up alerts**
5. **Use HTTPS in production**

## Performance Tips

1. **Enable cross-validation only when needed**
2. **Use batch processing for multiple requests**
3. **Cache frequently used configurations**
4. **Monitor response times and optimize accordingly**

---

**Note**: This integration requires valid API keys for the AI platforms you want to use. At least one platform must be configured for the system to function properly.
