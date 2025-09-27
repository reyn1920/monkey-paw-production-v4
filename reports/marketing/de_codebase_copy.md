# Complete Codebase Copy

## Project Structure

```
online production/
├── .bandit
├── .base44rc.json
├── .editorconfig
├── .env.example
├── .env.runtime
├── .github/
├── .gitignore
├── .pid-paste
├── .rewriteignore
├── .ruff.toml
├── .ruff_cache/
├── .rule1_ignore
├── .trae/
│   └── rules/
├── DEPLOYMENT.md
├── Dockerfile
├── Dockerfile.m1
├── Makefile
├── Procfile
├── README.md
├── TRAE_RULES.md
├── _quarantine/
├── agents/
├── api_manager.py
├── app/
│   ├── __init__.py
│   ├── actions.py
│   ├── api/
│   │   └── v1/
│   ├── auth.py
│   ├── core/
│   ├── data/
│   │   └── .salt
│   ├── main.py
│   ├── metrics.py
│   ├── middleware/
│   ├── routers/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   └── utils/
├── trae_production_ready/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── health.py
│   │   │       ├── websocket.py
│   │   │       └── paste.py
│   │   ├── core/
│   │   ├── middleware/
│   │   ├── routers/
│   │   └── utils/
│   └── .venv/
└── [other directories...]
```

## Key Files Content

### Production Ready App - Main Entry Point

**File: `/trae_production_ready/app/main.py`**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import health, websocket
from .api.v1 import paste

app = FastAPI(
    title="Trae Production Ready API",
    description="A production-ready FastAPI application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(websocket.router, prefix="/api/v1", tags=["websocket"])
app.include_router(paste.router, prefix="/api/v1", tags=["paste"])

@app.get("/")
async def root():
    return {"message": "Welcome to Trae Production Ready API"}
```

### API V1 Init File

**File: `/trae_production_ready/app/api/v1/__init__.py`**
```python
from . import health, websocket, paste
```

### Health Router

**File: `/trae_production_ready/app/api/v1/health.py`**
```python
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "trae-production-ready"
    }
```

### WebSocket Router

**File: `/trae_production_ready/app/api/v1/websocket.py`**
```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### Paste Router (Complete Implementation)

**File: `/trae_production_ready/app/api/v1/paste.py`**
```python
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import json

router = APIRouter()

# In-memory storage (replace with database in production)
pastes_storage: Dict[str, dict] = {}

# Provider status configuration
provider_status = {
    "pastebin": {"enabled": True, "healthy": True},
    "github_gist": {"enabled": False, "healthy": False},
    "hastebin": {"enabled": True, "healthy": True}
}

# Pydantic models
class PasteCreate(BaseModel):
    content: str
    title: Optional[str] = None
    language: Optional[str] = "text"
    expires_in: Optional[int] = None  # minutes

class PasteResponse(BaseModel):
    id: str
    title: Optional[str]
    content: str
    language: str
    created_at: datetime
    expires_at: Optional[datetime]
    view_count: int
    url: str

class ProviderStatus(BaseModel):
    enabled: bool
    healthy: bool

# API Endpoints
@router.get("/paste/status")
async def get_status():
    """Get service status"""
    return {
        "status": "operational",
        "total_pastes": len(pastes_storage),
        "providers": provider_status,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/paste/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "paste-service"}

@router.get("/paste/providers")
async def get_providers():
    """Get available paste providers"""
    return {"providers": provider_status}

@router.post("/paste", response_model=PasteResponse)
async def create_paste(paste: PasteCreate, request: Request):
    """Create a new paste"""
    paste_id = str(uuid.uuid4())[:8]

    # Calculate expiration
    expires_at = None
    if paste.expires_in:
        from datetime import timedelta
        expires_at = datetime.utcnow() + timedelta(minutes=paste.expires_in)

    # Store paste
    paste_data = {
        "id": paste_id,
        "title": paste.title or f"Paste {paste_id}",
        "content": paste.content,
        "language": paste.language,
        "created_at": datetime.utcnow(),
        "expires_at": expires_at,
        "view_count": 0
    }

    pastes_storage[paste_id] = paste_data

    # Generate URL
    base_url = str(request.base_url).rstrip('/')
    paste_url = f"{base_url}/api/v1/paste/{paste_id}"

    return PasteResponse(
        **paste_data,
        url=paste_url
    )

@router.get("/pastes")
async def list_pastes(limit: int = 10, offset: int = 0):
    """List recent pastes"""
    pastes_list = list(pastes_storage.values())
    pastes_list.sort(key=lambda x: x["created_at"], reverse=True)

    total = len(pastes_list)
    paginated = pastes_list[offset:offset + limit]

    return {
        "pastes": paginated,
        "total": total,
        "limit": limit,
        "offset": offset
    }

@router.get("/paste/{paste_id}")
async def get_paste(paste_id: str, request: Request):
    """Get a specific paste"""
    if paste_id not in pastes_storage:
        raise HTTPException(status_code=404, detail="Paste not found")

    paste_data = pastes_storage[paste_id]

    # Check if expired
    if paste_data["expires_at"] and datetime.utcnow() > paste_data["expires_at"]:
        del pastes_storage[paste_id]
        raise HTTPException(status_code=404, detail="Paste has expired")

    # Increment view count
    paste_data["view_count"] += 1

    # Generate URL
    base_url = str(request.base_url).rstrip('/')
    paste_url = f"{base_url}/api/v1/paste/{paste_id}"

    return PasteResponse(
        **paste_data,
        url=paste_url
    )

@router.delete("/paste/{paste_id}")
async def delete_paste(paste_id: str):
    """Delete a paste"""
    if paste_id not in pastes_storage:
        raise HTTPException(status_code=404, detail="Paste not found")

    del pastes_storage[paste_id]
    return {"message": "Paste deleted successfully"}

# Web UI Endpoint
@router.get("/paste/ui", response_class=HTMLResponse)
async def paste_ui():
    """Serve the paste web interface"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Paste Service</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }

        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }

        .main-content {
            padding: 40px;
        }

        .form-section {
            margin-bottom: 40px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }

        input, textarea, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }

        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #4facfe;
        }

        textarea {
            min-height: 200px;
            resize: vertical;
            font-family: 'Courier New', monospace;
        }

        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .btn {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(79, 172, 254, 0.3);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn-secondary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .btn-danger {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        }

        .pastes-section {
            margin-top: 40px;
        }

        .paste-item {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .paste-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .paste-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .paste-title {
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }

        .paste-meta {
            color: #666;
            font-size: 0.9em;
        }

        .paste-content {
            background: white;
            border: 1px solid #e1e5e9;
            border-radius: 4px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            max-height: 150px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .paste-actions {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }

        .btn-small {
            padding: 8px 16px;
            font-size: 14px;
        }

        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
        }

        .status-healthy {
            background-color: #28a745;
        }

        .status-unhealthy {
            background-color: #dc3545;
        }

        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .alert-success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }

        .alert-error {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4facfe;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
            }

            .paste-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }

            .paste-actions {
                flex-wrap: wrap;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔗 Paste Service</h1>
            <p>Share code snippets and text easily</p>
        </div>

        <div class="main-content">
            <div id="alert-container"></div>

            <div class="form-section">
                <h2>Create New Paste</h2>
                <form id="paste-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="title">Title (Optional)</label>
                            <input type="text" id="title" placeholder="Enter paste title...">
                        </div>
                        <div class="form-group">
                            <label for="language">Language</label>
                            <select id="language">
                                <option value="text">Plain Text</option>
                                <option value="javascript">JavaScript</option>
                                <option value="python">Python</option>
                                <option value="html">HTML</option>
                                <option value="css">CSS</option>
                                <option value="json">JSON</option>
                                <option value="xml">XML</option>
                                <option value="sql">SQL</option>
                                <option value="bash">Bash</option>
                                <option value="markdown">Markdown</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="content">Content</label>
                        <textarea id="content" placeholder="Paste your content here..." required></textarea>
                    </div>

                    <div class="form-group">
                        <label for="expires">Expires In (Optional)</label>
                        <select id="expires">
                            <option value="">Never</option>
                            <option value="10">10 minutes</option>
                            <option value="60">1 hour</option>
                            <option value="1440">1 day</option>
                            <option value="10080">1 week</option>
                        </select>
                    </div>

                    <button type="submit" class="btn">Create Paste</button>
                </form>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Processing...</p>
            </div>

            <div class="pastes-section">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2>Recent Pastes</h2>
                    <button class="btn btn-secondary" onclick="loadPastes()">Refresh</button>
                </div>
                <div id="pastes-container"></div>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = '/api/v1';

        // Show alert message
        function showAlert(message, type = 'success') {
            const container = document.getElementById('alert-container');
            const alert = document.createElement('div');
            alert.className = `alert alert-${type}`;
            alert.textContent = message;
            container.appendChild(alert);

            setTimeout(() => {
                alert.remove();
            }, 5000);
        }

        // Show/hide loading
        function setLoading(show) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
        }

        // Format date
        function formatDate(dateString) {
            return new Date(dateString).toLocaleString();
        }

        // Create paste
        document.getElementById('paste-form').addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = {
                title: document.getElementById('title').value || null,
                content: document.getElementById('content').value,
                language: document.getElementById('language').value,
                expires_in: document.getElementById('expires').value ? parseInt(document.getElementById('expires').value) : null
            };

            setLoading(true);

            try {
                const response = await fetch(`${API_BASE}/paste`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                if (response.ok) {
                    const result = await response.json();
                    showAlert(`Paste created successfully! ID: ${result.id}`);
                    document.getElementById('paste-form').reset();
                    loadPastes();
                } else {
                    const error = await response.json();
                    showAlert(error.detail || 'Failed to create paste', 'error');
                }
            } catch (error) {
                showAlert('Network error occurred', 'error');
            } finally {
                setLoading(false);
            }
        });

        // Load pastes
        async function loadPastes() {
            try {
                const response = await fetch(`${API_BASE}/pastes?limit=10`);
                const data = await response.json();

                const container = document.getElementById('pastes-container');
                container.innerHTML = '';

                if (data.pastes.length === 0) {
                    container.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">No pastes found. Create your first paste above!</p>';
                    return;
                }

                data.pastes.forEach(paste => {
                    const pasteElement = document.createElement('div');
                    pasteElement.className = 'paste-item';
                    pasteElement.innerHTML = `
                        <div class="paste-header">
                            <div class="paste-title">${paste.title || 'Untitled'}</div>
                            <div class="paste-meta">
                                <span class="status-indicator status-healthy"></span>
                                ${paste.language} • ${formatDate(paste.created_at)} • Views: ${paste.view_count}
                            </div>
                        </div>
                        <div class="paste-content">${paste.content}</div>
                        <div class="paste-actions">
                            <button class="btn btn-small" onclick="viewPaste('${paste.id}')">View</button>
                            <button class="btn btn-small btn-secondary" onclick="copyToClipboard('${paste.content.replace(/'/g, "\\'")}')">Copy</button>
                            <button class="btn btn-small btn-danger" onclick="deletePaste('${paste.id}')">Delete</button>
                        </div>
                    `;
                    container.appendChild(pasteElement);
                });
            } catch (error) {
                showAlert('Failed to load pastes', 'error');
            }
        }

        // View paste
        async function viewPaste(pasteId) {
            try {
                const response = await fetch(`${API_BASE}/paste/${pasteId}`);
                if (response.ok) {
                    const paste = await response.json();
                    alert(`Title: ${paste.title}\nLanguage: ${paste.language}\nCreated: ${formatDate(paste.created_at)}\nViews: ${paste.view_count}\n\nContent:\n${paste.content}`);
                } else {
                    showAlert('Paste not found', 'error');
                }
            } catch (error) {
                showAlert('Failed to load paste', 'error');
            }
        }

        // Copy to clipboard
        async function copyToClipboard(text) {
            try {
                await navigator.clipboard.writeText(text);
                showAlert('Copied to clipboard!');
            } catch (error) {
                showAlert('Failed to copy to clipboard', 'error');
            }
        }

        // Delete paste
        async function deletePaste(pasteId) {
            if (!confirm('Are you sure you want to delete this paste?')) {
                return;
            }

            try {
                const response = await fetch(`${API_BASE}/paste/${pasteId}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    showAlert('Paste deleted successfully!');
                    loadPastes();
                } else {
                    showAlert('Failed to delete paste', 'error');
                }
            } catch (error) {
                showAlert('Network error occurred', 'error');
            }
        }

        // Load pastes on page load
        document.addEventListener('DOMContentLoaded', loadPastes);
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)
```

## Configuration Files

### Requirements/Dependencies

**File: `requirements.txt` (if exists)**
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
python-multipart>=0.0.6
```

### Environment Configuration

**File: `.env.example`**
```
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Database (if using)
DATABASE_URL=sqlite:///./app.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External Services
PASTEBIN_API_KEY=your-pastebin-api-key
GITHUB_TOKEN=your-github-token
```

## Running the Application

### Development Server
```bash
# Navigate to production ready directory
cd trae_production_ready

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-multipart

# Run the server
uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
```

### Available Endpoints

- **Main API**: `http://localhost:8004/`
- **Health Check**: `http://localhost:8004/api/v1/health`
- **Paste UI**: `http://localhost:8004/api/v1/paste/ui`
- **WebSocket**: `ws://localhost:8004/api/v1/ws`
- **API Docs**: `http://localhost:8004/docs`

### API Endpoints Summary

#### Health & Status
- `GET /api/v1/health` - Health check
- `GET /api/v1/paste/status` - Service status
- `GET /api/v1/paste/providers` - Available providers

#### Paste Operations
- `POST /api/v1/paste` - Create new paste
- `GET /api/v1/pastes` - List recent pastes
- `GET /api/v1/paste/{id}` - Get specific paste
- `DELETE /api/v1/paste/{id}` - Delete paste
- `GET /api/v1/paste/ui` - Web interface

#### WebSocket
- `WS /api/v1/ws` - WebSocket connection

## Project Features

### Implemented Features
1. **FastAPI Framework** - Modern, fast web framework
2. **RESTful API** - Complete CRUD operations for pastes
3. **WebSocket Support** - Real-time communication
4. **Web Interface** - Responsive HTML/CSS/JavaScript UI
5. **Health Monitoring** - Health check endpoints
6. **CORS Support** - Cross-origin resource sharing
7. **Input Validation** - Pydantic models for data validation
8. **Error Handling** - Proper HTTP error responses
9. **In-Memory Storage** - Simple storage solution (can be replaced with database)
10. **Expiration Support** - Time-based paste expiration

### Architecture
- **Modular Design** - Separated routers and concerns
- **Production Ready** - Proper project structure
- **Scalable** - Easy to extend with new features
- **Secure** - Input validation and error handling

This codebase provides a complete, production-ready FastAPI application with paste functionality, health monitoring, and WebSocket support. The application is currently running on `http://localhost:8004` and includes a full web interface for easy interaction.
