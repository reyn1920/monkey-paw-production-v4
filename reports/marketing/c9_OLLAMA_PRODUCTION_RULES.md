# Ollama Production Integration Rules

## Executive Summary
This document establishes production-ready rules for preserving and deploying Ollama LLM integration in the TRAE.AI application. Ollama is confirmed as installed locally with multiple models and comprehensive integration code exists.

## Current Ollama Status
- **Installation**: Confirmed installed and operational
- **Models Available**: 13 models including mistral:7b, llama2:13b, codellama:latest, llama3.2:latest, etc.
- **Integration**: Comprehensive integration module exists at `backend/integrations/ollama_integration.py`
- **Total Storage**: ~50GB of model data

## Production Deployment Rules

### Rule 1: Ollama Service Preservation
**CRITICAL**: Ollama and its models MUST NOT be deleted during deployment or cleanup operations.

- Add `ollama` to protected services list
- Exclude Ollama model directory from cleanup scripts
- Preserve Ollama configuration and model cache
- Ensure Ollama service auto-starts with application

### Rule 2: Environment Configuration
```bash
# Production environment variables
OLLAMA_ENDPOINT=http://localhost:11434
OLLAMA_MODELS_PATH=/Users/thomasbrianreynolds/.ollama/models
OLLAMA_DEFAULT_MODEL=llama2:7b
OLLAMA_MAX_CONCURRENT=5
OLLAMA_CACHE_ENABLED=true
```

### Rule 3: Service Dependencies
- Ollama service MUST be running before application starts
- Health checks MUST verify Ollama connectivity
- Fallback mechanisms for Ollama service failures
- Auto-restart capabilities for Ollama service

### Rule 4: Model Management
- Preserve all 13 existing models during deployment
- Implement model health checks
- Cache model responses for performance
- Monitor model usage and performance metrics

### Rule 5: Integration Code Protection
- Preserve `backend/integrations/ollama_integration.py`
- Maintain Ollama-related configuration files
- Protect Ollama database cache
- Ensure proper error handling and logging

### Rule 6: Security Considerations
- Ollama runs on localhost:11434 (secure by default)
- No external API keys required (local models)
- Implement rate limiting for Ollama requests
- Monitor resource usage and model access

### Rule 7: Performance Optimization
- Pre-load frequently used models
- Implement response caching
- Monitor memory usage (50GB+ models)
- Optimize concurrent request handling

### Rule 8: Monitoring and Logging
- Track Ollama service health
- Monitor model response times
- Log model usage statistics
- Alert on service failures

## Deployment Checklist

### Pre-Deployment
- [ ] Verify Ollama service is running
- [ ] Confirm all 13 models are accessible
- [ ] Test integration endpoints
- [ ] Backup Ollama configuration

### During Deployment
- [ ] Preserve Ollama service and models
- [ ] Update environment variables
- [ ] Deploy integration code
- [ ] Configure service dependencies

### Post-Deployment
- [ ] Verify Ollama connectivity
- [ ] Test model responses
- [ ] Monitor performance metrics
- [ ] Validate error handling

## Available Models for Production
```
mistral:7b          (4.4 GB) - Content generation
llama2:13b          (7.4 GB) - Strategic analysis
llama2:7b           (3.8 GB) - General purpose
codellama:latest    (3.8 GB) - Code analysis
llama3.2:latest     (2.0 GB) - Latest model
llama3:8b           (4.7 GB) - Advanced reasoning
llama3.1:latest     (4.9 GB) - Enhanced capabilities
gemma2:latest       (5.4 GB) - Google's model
llama3:latest       (4.7 GB) - Meta's latest
gemma3:latest       (3.3 GB) - Compact model
llama3.1:8b         (4.9 GB) - Optimized version
llama3-chatqa:8b    (4.7 GB) - Q&A specialized
```

## Integration Architecture
- **Service Management**: Auto-start/health monitoring
- **Model Management**: Multi-model support with fallbacks
- **Caching**: SQLite-based response caching
- **Performance**: Concurrent request handling
- **Monitoring**: Comprehensive metrics and logging

## Critical Warning
**DO NOT DELETE**: Ollama installation, models, or integration code during any deployment, cleanup, or optimization process. This represents significant computational assets (50GB+) and critical AI capabilities.

---
*This document ensures Ollama integration remains operational in production environments while maintaining security, performance, and reliability standards.*