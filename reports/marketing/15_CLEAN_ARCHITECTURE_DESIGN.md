# Clean Architecture Design
## TRAE.AI Dashboard Rebuild

**Version**: 2.0 (Clean Rebuild)  
**Date**: January 27, 2025  
**Status**: Design Phase

---

## 🏗️ Core Architectural Principles

### 1. Clean Architecture Layers
```
┌─────────────────────────────────────┐
│           Presentation Layer        │  ← FastAPI Routes, WebSocket, Frontend
├─────────────────────────────────────┤
│           Application Layer         │  ← Use Cases, Services, Orchestration
├─────────────────────────────────────┤
│             Domain Layer            │  ← Business Logic, Entities, Rules
├─────────────────────────────────────┤
│         Infrastructure Layer        │  ← Database, External APIs, File System
└─────────────────────────────────────┘
```

### 2. Dependency Flow
- **Inward Dependencies Only**: Outer layers depend on inner layers
- **Interface Segregation**: Small, focused interfaces
- **Dependency Injection**: Loose coupling through DI container
- **Single Responsibility**: Each module has one reason to change

---

## 📁 New Project Structure

```
/online production/
├── src/                           # Clean source code
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── core/                      # Core configuration and utilities
│   │   ├── __init__.py
│   │   ├── config.py              # Settings and environment variables
│   │   ├── dependencies.py        # Dependency injection container
│   │   ├── exceptions.py          # Custom exception classes
│   │   └── logging.py             # Logging configuration
│   ├── domain/                    # Business logic and entities
│   │   ├── __init__.py
│   │   ├── entities/              # Domain entities
│   │   ├── repositories/          # Repository interfaces
│   │   ├── services/              # Domain services
│   │   └── value_objects/         # Value objects
│   ├── application/               # Use cases and application services
│   │   ├── __init__.py
│   │   ├── use_cases/             # Application use cases
│   │   ├── services/              # Application services
│   │   └── dto/                   # Data transfer objects
│   ├── infrastructure/            # External concerns
│   │   ├── __init__.py
│   │   ├── database/              # Database implementations
│   │   ├── external_apis/         # External API clients
│   │   ├── file_storage/          # File storage implementations
│   │   └── messaging/             # Message queue implementations
│   ├── presentation/              # API and UI layer
│   │   ├── __init__.py
│   │   ├── api/                   # REST API endpoints
│   │   ├── websocket/             # WebSocket handlers
│   │   └── middleware/            # Custom middleware
│   └── agents/                    # AI agent system
│       ├── __init__.py
│       ├── base/                  # Base agent classes
│       ├── implementations/       # Specific agent implementations
│       └── orchestration/         # Agent coordination
├── frontend/                      # Modern React frontend
│   ├── src/
│   │   ├── components/            # Reusable UI components
│   │   ├── pages/                 # Page components
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── services/              # API service layer
│   │   ├── store/                 # State management
│   │   └── utils/                 # Utility functions
│   ├── public/                    # Static assets
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── tests/                         # Comprehensive test suite
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   ├── e2e/                       # End-to-end tests
│   └── fixtures/                  # Test fixtures and data
├── docs/                          # Documentation
├── scripts/                       # Utility scripts
├── docker/                        # Docker configurations
├── .github/                       # GitHub Actions workflows
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Python project configuration
├── .env.example                   # Environment variable template
└── README.md                      # Project documentation
```

---

## 🔧 Technology Stack (Clean)

### Backend Core
```python
# Core Framework
fastapi = "^0.104.1"
uvicorn = "^0.24.0"
pydantic = "^2.5.0"
pydantic-settings = "^2.1.0"

# Database
sqlalchemy = "^2.0.23"
alembic = "^1.13.1"
asyncpg = "^0.29.0"  # PostgreSQL async driver

# Authentication & Security
fastapi-users = "^12.1.2"
python-jose = "^3.3.0"
passlib = "^1.7.4"
python-multipart = "^0.0.6"

# Caching & Messaging
redis = "^5.0.1"
celery = "^5.3.4"

# AI/ML
openai = "^1.3.7"
anthropic = "^0.7.8"
langchain = "^0.1.0"

# Monitoring & Logging
structlog = "^23.2.0"
prometheus-client = "^0.19.0"

# Development
pytest = "^7.4.3"
pytest-asyncio = "^0.21.1"
black = "^23.11.0"
ruff = "^0.1.6"
mypy = "^1.7.1"
```

### Frontend Core
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "react-query": "^3.39.3",
    "zustand": "^4.4.7",
    "axios": "^1.6.2",
    "socket.io-client": "^4.7.4"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.1.1",
    "vite": "^5.0.0",
    "typescript": "^5.2.2",
    "tailwindcss": "^3.3.6",
    "@types/react": "^18.2.37",
    "eslint": "^8.53.0",
    "prettier": "^3.1.0"
  }
}
```

---

## 🎯 Core Domain Models

### 1. User Management
```python
# Domain Entity
class User:
    id: UUID
    email: EmailStr
    username: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

# Repository Interface
class UserRepository(Protocol):
    async def create(self, user: UserCreate) -> User: ...
    async def get_by_id(self, user_id: UUID) -> User | None: ...
    async def get_by_email(self, email: str) -> User | None: ...
    async def update(self, user_id: UUID, updates: UserUpdate) -> User: ...
    async def delete(self, user_id: UUID) -> bool: ...
```

### 2. Agent System
```python
# Domain Entity
class Agent:
    id: UUID
    name: str
    type: AgentType
    configuration: dict[str, Any]
    status: AgentStatus
    created_at: datetime
    last_execution: datetime | None

# Agent Types
class AgentType(str, Enum):
    CONTENT_GENERATOR = "content_generator"
    RESEARCH_ANALYST = "research_analyst"
    SEO_OPTIMIZER = "seo_optimizer"
    SOCIAL_MEDIA = "social_media"
    MONITORING = "monitoring"

# Agent Status
class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
```

### 3. Task Management
```python
# Domain Entity
class Task:
    id: UUID
    agent_id: UUID
    name: str
    description: str
    parameters: dict[str, Any]
    status: TaskStatus
    priority: TaskPriority
    scheduled_at: datetime | None
    started_at: datetime | None
    completed_at: datetime | None
    result: dict[str, Any] | None
    error_message: str | None

# Task Status
class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
```

---

## 🔌 API Design

### 1. RESTful Endpoints
```python
# User Management
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
GET    /api/v1/auth/me
PUT    /api/v1/auth/me

# Agent Management
GET    /api/v1/agents
POST   /api/v1/agents
GET    /api/v1/agents/{agent_id}
PUT    /api/v1/agents/{agent_id}
DELETE /api/v1/agents/{agent_id}
POST   /api/v1/agents/{agent_id}/start
POST   /api/v1/agents/{agent_id}/stop

# Task Management
GET    /api/v1/tasks
POST   /api/v1/tasks
GET    /api/v1/tasks/{task_id}
PUT    /api/v1/tasks/{task_id}
DELETE /api/v1/tasks/{task_id}

# Dashboard & Monitoring
GET    /api/v1/dashboard/stats
GET    /api/v1/dashboard/metrics
GET    /api/v1/health
```

### 2. WebSocket Events
```python
# Real-time Updates
"agent.status_changed"     # Agent status updates
"task.created"             # New task created
"task.status_changed"      # Task status updates
"system.metrics"           # System performance metrics
"notification.new"         # User notifications
```

---

## 🛡️ Security Architecture

### 1. Authentication Flow
```
1. User Login → JWT Token Generation
2. Token Validation → Middleware Check
3. Role-Based Access → Permission Verification
4. Secure Headers → CORS, CSP, HSTS
```

### 2. Data Protection
- **Input Validation**: Pydantic models for all inputs
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **XSS Protection**: Content Security Policy headers
- **Rate Limiting**: Redis-based rate limiting per endpoint
- **Secret Management**: Environment variables only

---

## 📊 Database Schema

### 1. Core Tables
```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agents table
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    configuration JSONB NOT NULL DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'idle',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_execution TIMESTAMP WITH TIME ZONE
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    parameters JSONB NOT NULL DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'pending',
    priority INTEGER DEFAULT 5,
    scheduled_at TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    result JSONB,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 2. Indexes for Performance
```sql
-- User indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Agent indexes
CREATE INDEX idx_agents_user_id ON agents(user_id);
CREATE INDEX idx_agents_type ON agents(type);
CREATE INDEX idx_agents_status ON agents(status);

-- Task indexes
CREATE INDEX idx_tasks_agent_id ON tasks(agent_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_scheduled_at ON tasks(scheduled_at);
CREATE INDEX idx_tasks_priority ON tasks(priority);
```

---

## 🚀 Implementation Strategy

### Phase 1: Foundation (Days 1-2)
1. **Project Setup**
   - Initialize clean directory structure
   - Configure development environment
   - Set up dependency management

2. **Core Infrastructure**
   - FastAPI application setup
   - Database connection and models
   - Basic authentication system
   - Logging and error handling

### Phase 2: Core Services (Days 3-4)
1. **User Management**
   - Registration and login endpoints
   - JWT token management
   - User profile management

2. **Agent System Foundation**
   - Base agent classes
   - Agent repository implementation
   - Basic CRUD operations

### Phase 3: Business Logic (Days 5-6)
1. **Task Management**
   - Task creation and scheduling
   - Task execution framework
   - Status tracking and updates

2. **Agent Implementations**
   - Content generator agent
   - Research analyst agent
   - Basic orchestration

### Phase 4: Frontend & Integration (Days 7-8)
1. **React Frontend**
   - Modern UI components
   - Dashboard implementation
   - Real-time updates with WebSocket

2. **API Integration**
   - Complete API client
   - State management
   - Error handling

---

## ✅ Success Criteria

### 1. Code Quality
- **Zero** circular imports
- **100%** type coverage with mypy
- **90%+** test coverage
- **Zero** critical security vulnerabilities

### 2. Performance
- **<100ms** API response times
- **<2s** page load times
- **Real-time** WebSocket updates
- **Graceful** error handling

### 3. Maintainability
- **Clear** separation of concerns
- **Comprehensive** documentation
- **Consistent** code style
- **Easy** to extend and modify

---

## 🎯 Next Steps

1. ✅ **Analysis Complete** - Requirements documented
2. ✅ **Design Complete** - Architecture defined
3. ⏳ **Implementation** - Begin core services
4. ⏳ **Testing** - Comprehensive validation
5. ⏳ **Deployment** - Production setup
6. ⏳ **Guardian Validation** - Final quality check

**Ready to begin implementation of the clean, modern TRAE.AI Dashboard!**