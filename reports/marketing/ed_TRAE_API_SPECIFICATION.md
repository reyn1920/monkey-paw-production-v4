# TRAE.AI API Specification for ChatGPT Integration

## API Base Information

**Base URL**: `http://localhost:8080/api/v1`  
**Protocol**: HTTP/1.1  
**Authentication**: Bearer Token  
**Content-Type**: `application/json`  
**API Version**: 1.0

## Authentication

### Headers Required for All Requests

```http
Authorization: Bearer {TRAE_MASTER_KEY}
Content-Type: application/json
User-Agent: ChatGPT-Integration/1.0
X-Request-ID: {unique_request_id}
```

## Core API Endpoints

### 1. System Status and Health

#### GET/system/status

**Description**: Get current system status and health metrics

**Request**:

```http
GET/api/v1/system/status
Authorization: Bearer {TRAE_MASTER_KEY}
```

**Response**:

```json
{
  "status": "LIVE",
  "timestamp": "2024-01-15T10:30:00Z",
  "orchestrator_status": "LIVE",
  "agents": {
    "SystemAgent": {
      "status": "active",
      "last_heartbeat": "2024-01-15T10:29:55Z",
      "tasks_completed": 1247,
      "health_score": 98.5
    },
    "ResearchAgent": {
      "status": "active",
      "last_heartbeat": "2024-01-15T10:29:58Z",
      "tasks_completed": 892,
      "health_score": 96.2
    },
    "ContentAgent": {
      "status": "active",
      "last_heartbeat": "2024-01-15T10:29:59Z",
      "tasks_completed": 456,
      "health_score": 94.8
    }
  },
  "system_metrics": {
    "memory_usage_percent": 65.9,
    "cpu_usage_percent": 42.3,
    "disk_usage_percent": 23.1,
    "active_tasks": 12,
    "queued_tasks": 3
  },
  "database_health": "healthy",
  "api_version": "1.0"
}
```

#### GET/system/agents

**Description**: Get detailed information about all active agents

**Response**:

```json
{
  "agents": [
    {
      "name": "SystemAgent",
      "type": "system_management",
      "status": "active",
      "capabilities": ["health_monitoring", "self_repair", "database_management"],
      "current_tasks": 2,
      "max_concurrent_tasks": 10,
      "performance_metrics": {
        "avg_response_time_ms": 145,
        "success_rate_percent": 99.2,
        "error_count_24h": 3
      }
    }
  ]
}
```

### 2. Content Generation

#### POST/content/generate

**Description**: Generate various types of content (video, text, audio)

**Request**:

```json
{
  "task_id": "content_gen_001",
  "content_type": "video",
  "parameters": {
    "topic": "Introduction to AI automation",
    "duration_seconds": 300,
    "style": "professional",
    "voice": "professional_male",
    "resolution": "1080p",
    "include_subtitles": true,
    "background_music": true,
    "custom_script": "Optional custom script content"
  },
  "priority": "high",
  "callback_url": "https://your-domain.com/webhook/content",
  "metadata": {
    "user_id": "user_123",
    "project_id": "proj_456"
  }
}
```

**Response (Synchronous - Simple Content)**:

```json
{
  "status": "completed",
  "task_id": "content_gen_001",
  "result": {
    "content_url": "https://storage.trae.ai/content/video_123.mp4",
    "content_type": "video/mp4",
    "file_size_bytes": 52428800,
    "duration_seconds": 298,
    "resolution": "1920x1080",
    "metadata": {
      "created_at": "2024-01-15T10:35:00Z",
      "processing_time_seconds": 245,
      "quality_score": 94.2
    }
  },
  "execution_time_ms": 245000,
  "resource_usage": {
    "cpu_seconds": 180,
    "memory_peak_mb": 2048,
    "gpu_seconds": 120
  }
}
```

**Response (Asynchronous - Complex Content)**:

```json
{
  "status": "accepted",
  "task_id": "content_gen_001",
  "estimated_completion": "2024-01-15T10:45:00Z",
  "progress_url": "/api/v1/tasks/content_gen_001/progress",
  "webhook_configured": true
}
```

#### GET/content/templates

**Description**: Get available content templates and styles

**Response**:

```json
{
  "video_templates": [
    {
      "id": "professional_presentation",
      "name": "Professional Presentation",
      "description": "Clean, corporate-style video template",
      "duration_range": [60, 1800],
      "supported_resolutions": ["720p", "1080p", "4K"]
    }
  ],
  "voice_options": [
    {
      "id": "professional_male",
      "name": "Professional Male",
      "language": "en-US",
      "sample_url": "https://samples.trae.ai/voice_prof_male.mp3"
    }
  ]
}
```

### 3. Research and Intelligence

#### POST/research/analyze

**Description**: Perform intelligent research and analysis on topics

**Request**:

```json
{
  "task_id": "research_001",
  "query": "Latest trends in renewable energy technology",
  "parameters": {
    "sources": ["news", "academic", "social_media", "patents"],
    "depth": "comprehensive",
    "time_range": "last_30_days",
    "language": "en",
    "max_sources": 50,
    "include_sentiment": true,
    "include_trends": true
  },
  "output_format": "structured_report",
  "callback_url": "https://your-domain.com/webhook/research"
}
```

**Response**:

```json
{
  "status": "completed",
  "task_id": "research_001",
  "result": {
    "summary": "Comprehensive analysis of renewable energy trends...",
    "key_findings": [
      {
        "finding": "Solar panel efficiency increased by 15% in 2024",
        "confidence": 0.92,
        "sources": 12
      }
    ],
    "sources_analyzed": 47,
    "sentiment_analysis": {
      "overall_sentiment": "positive",
      "confidence": 0.87,
      "positive_mentions": 156,
      "negative_mentions": 23
    },
    "trending_topics": [
      {
        "topic": "battery storage technology",
        "trend_score": 0.94,
        "mention_count": 89
      }
    ],
    "report_url": "https://storage.trae.ai/reports/research_001.pdf"
  }
}
```

#### GET/research/sources

**Description**: Get available research sources and their capabilities

**Response**:

```json
{
  "sources": [
    {
      "id": "news",
      "name": "News Sources",
      "description": "Real-time news from 500+ sources",
      "update_frequency": "15_minutes",
      "languages": ["en", "es", "fr", "de"],
      "coverage_areas": ["technology", "business", "politics"]
    }
  ]
}
```

### 4. Video Production

#### POST/video/create

**Description**: Create videos with advanced customization options

**Request**:

```json
{
  "task_id": "video_prod_001",
  "script": "Welcome to our AI automation tutorial...",
  "parameters": {
    "voice_settings": {
      "voice_id": "professional_female",
      "speed": 1.0,
      "pitch": 0.0,
      "volume": 0.8
    },
    "video_settings": {
      "resolution": "1920x1080",
      "fps": 30,
      "format": "mp4",
      "quality": "high"
    },
    "visual_elements": {
      "background_type": "gradient",
      "background_color": "#1a1a2e",
      "text_overlays": true,
      "transitions": "fade",
      "logo_url": "https://your-domain.com/logo.png"
    },
    "audio_settings": {
      "background_music": true,
      "music_volume": 0.3,
      "music_genre": "corporate",
      "noise_reduction": true
    }
  },
  "callback_url": "https://your-domain.com/webhook/video"
}
```

**Response**:

```json
{
  "status": "processing",
  "task_id": "video_prod_001",
  "estimated_completion": "2024-01-15T10:50:00Z",
  "progress": {
    "current_stage": "script_processing",
    "completion_percent": 15,
    "stages": [
      "script_processing",
      "voice_generation",
      "video_rendering",
      "audio_mixing",
      "final_encoding"
    ]
  }
}
```

#### GET/video/progress/{task_id}

**Description**: Get video production progress

**Response**:

```json
{
  "task_id": "video_prod_001",
  "status": "processing",
  "progress": {
    "current_stage": "video_rendering",
    "completion_percent": 65,
    "estimated_remaining_seconds": 180,
    "current_operation": "Rendering scene 3 of 5"
  },
  "resource_usage": {
    "cpu_percent": 85,
    "memory_mb": 3072,
    "gpu_percent": 92
  }
}
```

### 5. Task Management

#### GET/tasks/{task_id}

**Description**: Get detailed information about a specific task

**Response**:

```json
{
  "task_id": "content_gen_001",
  "status": "completed",
  "task_type": "content_generation",
  "created_at": "2024-01-15T10:30:00Z",
  "started_at": "2024-01-15T10:30:05Z",
  "completed_at": "2024-01-15T10:34:10Z",
  "execution_time_seconds": 245,
  "priority": "high",
  "assigned_agent": "ContentAgent",
  "result": {
    "output_url": "https://storage.trae.ai/content/video_123.mp4",
    "metadata": {}
  },
  "error": null,
  "retry_count": 0
}
```

#### GET/tasks

**Description**: List tasks with filtering options

**Query Parameters**:

- `status`: Filter by status (pending, processing, completed, failed)
- `task_type`: Filter by task type
- `limit`: Number of results (default: 50, max: 200)
- `offset`: Pagination offset
- `created_after`: ISO timestamp
- `created_before`: ISO timestamp

**Response**:

```json
{
  "tasks": [
    {
      "task_id": "content_gen_001",
      "status": "completed",
      "task_type": "content_generation",
      "created_at": "2024-01-15T10:30:00Z",
      "priority": "high"
    }
  ],
  "pagination": {
    "total": 1247,
    "limit": 50,
    "offset": 0,
    "has_more": true
  }
}
```

#### DELETE/tasks/{task_id}

**Description**: Cancel a pending or processing task

**Response**:

```json
{
  "status": "cancelled",
  "task_id": "content_gen_001",
  "message": "Task successfully cancelled"
}
```

### 6. File Management

#### GET/files/{file_id}

**Description**: Download generated content files

**Response**: Binary file content with appropriate headers

```http
Content-Type: video/mp4
Content-Length: 52428800
Content-Disposition: attachment; filename="video_123.mp4"
X-File-ID: file_123
X-Generated-At: 2024-01-15T10:35:00Z
```

#### GET/files/{file_id}/metadata

**Description**: Get file metadata without downloading

**Response**:

```json
{
  "file_id": "file_123",
  "filename": "video_123.mp4",
  "content_type": "video/mp4",
  "file_size_bytes": 52428800,
  "created_at": "2024-01-15T10:35:00Z",
  "expires_at": "2024-02-15T10:35:00Z",
  "download_count": 3,
  "checksum_md5": "d41d8cd98f00b204e9800998ecf8427e",
  "metadata": {
    "duration_seconds": 298,
    "resolution": "1920x1080",
    "codec": "h264"
  }
}
```

## Webhook Specifications

### Webhook Payload Format

**Headers**:

```http
Content-Type: application/json
X-TRAE-Signature: sha256=signature_hash
X-TRAE-Event: task.completed
X-TRAE-Delivery: delivery_uuid
```

**Payload**:

```json
{
  "event": "task.completed",
  "timestamp": "2024-01-15T10:35:00Z",
  "task_id": "content_gen_001",
  "status": "completed",
  "result": {
    "content_url": "https://storage.trae.ai/content/video_123.mp4",
    "metadata": {}
  },
  "execution_time_seconds": 245,
  "resource_usage": {
    "cpu_seconds": 180,
    "memory_peak_mb": 2048
  }
}
```

### Webhook Events

- `task.created`: Task has been created and queued
- `task.started`: Task processing has begun
- `task.progress`: Task progress update (for long-running tasks)
- `task.completed`: Task completed successfully
- `task.failed`: Task failed with error
- `task.cancelled`: Task was cancelled
- `system.alert`: System-level alerts and notifications

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "TRAE_ERROR_CODE",
    "message": "Human readable error description",
    "details": {
      "component": "ContentAgent",
      "timestamp": "2024-01-15T10:30:00Z",
      "trace_id": "trace_12345",
      "request_id": "req_67890"
    },
    "recovery_suggestions": [
      "Check system status at/api/v1/system/status",
      "Verify your API key is valid",
      "Retry the request with exponential backoff"
    ]
  }
}
```

### HTTP Status Codes

- `200`: Success
- `201`: Created
- `202`: Accepted (for async operations)
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `409`: Conflict
- `429`: Too Many Requests
- `500`: Internal Server Error
- `502`: Bad Gateway
- `503`: Service Unavailable
- `504`: Gateway Timeout

## Rate Limiting

### Rate Limit Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248000
X-RateLimit-Window: 60
```

### Rate Limit Exceeded Response

```json
{
  "error": {
    "code": "TRAE_RATE_002",
    "message": "Rate limit exceeded",
    "details": {
      "limit": 100,
      "window_seconds": 60,
      "reset_at": "2024-01-15T10:31:00Z"
    }
  }
}
```

## SDK Examples

### Python SDK Usage

```python
import requests
import json
from datetime import datetime

class TraeAIClient:
    def __init__(self, api_key, base_url="http://localhost:8080/api/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ChatGPT-Integration/1.0"
        })

    def get_system_status(self):
        response = self.session.get(f"{self.base_url}/system/status")
        response.raise_for_status()
        return response.json()

    def generate_content(self, content_type, topic, **kwargs):
        payload = {
            "task_id": f"task_{datetime.now().isoformat()}",
            "content_type": content_type,
            "parameters": {
                "topic": topic,
                **kwargs
            },
            "priority": "high"
        }

        response = self.session.post(
            f"{self.base_url}/content/generate",
            json=payload
        )
        response.raise_for_status()
        return response.json()

    def get_task_status(self, task_id):
        response = self.session.get(f"{self.base_url}/tasks/{task_id}")
        response.raise_for_status()
        return response.json()

# Usage example
client = TraeAIClient("your_api_key_here")

# Check system status
status = client.get_system_status()
print(f"System status: {status['status']}")

# Generate video content
result = client.generate_content(
    content_type="video",
    topic="Introduction to AI",
    duration_seconds=300,
    style="professional"
)
print(f"Task ID: {result['task_id']}")
```

### JavaScript SDK Usage

```javascript
class TraeAIClient {
  constructor(apiKey, baseUrl = 'http://localhost:8080/api/v1') {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
    this.headers = {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'User-Agent': 'ChatGPT-Integration/1.0',
    };
  }

  async getSystemStatus() {
    const response = await fetch(`${this.baseUrl}/system/status`, {
      headers: this.headers,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  }

  async generateContent(contentType, topic, options = {}) {
    const payload = {
      task_id: `task_${new Date().toISOString()}`,
      content_type: contentType,
      parameters: {
        topic: topic,
        ...options,
      },
      priority: 'high',
    };

    const response = await fetch(`${this.baseUrl}/content/generate`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  }
}//Usage example
const client = new TraeAIClient('your_api_key_here');//Check system status
client
  .getSystemStatus()
  .then(status => console.log(`System status: ${status.status}`))
  .catch(error => console.error('Error:', error));//Generate content
client
  .generateContent('video', 'AI Automation Basics', {
    duration_seconds: 300,
    style: 'professional',
  })
  .then(result => console.log(`Task ID: ${result.task_id}`))
  .catch(error => console.error('Error:', error));
```

## Testing and Validation

### API Testing Checklist

- [ ] Authentication with valid API key
- [ ] Authentication with invalid API key (should return 401)
- [ ] Rate limiting behavior
- [ ] Error response format validation
- [ ] Webhook delivery and signature verification
- [ ] Large file upload/download
- [ ] Concurrent request handling
- [ ] System status endpoint availability

### Performance Benchmarks

- System status endpoint: < 100ms response time
- Content generation (simple): < 30 seconds
- Video generation (5 minutes): < 5 minutes
- Research analysis: < 3 minutes
- File download: > 10 MB/s transfer rate

---

**API Version**: 1.0  
**Last Updated**: January 2024  
**Compatibility**: ChatGPT Integration v1.0+
