# TRAE.AI System - Complete Architectural Map

## Executive Summary

This document provides a comprehensive architectural map of the TRAE.AI system, a sophisticated AI-powered development environment with integrated production capabilities. The system follows a microservices architecture with multiple entry points, robust API orchestration, and comprehensive data management.

## System Overview

### Core Architecture Pattern
- **Pattern**: Microservices with API Gateway
- **Entry Points**: Multiple FastAPI applications with orchestrated routing
- **Data Layer**: SQLite-based with comprehensive schema management
- **Frontend**: Hybrid HTML/JavaScript with React components
- **Deployment**: Multi-server architecture with health monitoring

## 1. Application Entry Points

### 1.1 Primary Entry Points

#### Main Application (`main.py`)
- **Purpose**: Primary orchestrator and fallback server
- **Port**: 8000 (configurable via PORT env var)
- **Features**:
  - Optimized startup with essential services
  - FastAPI server with fallback to minimal HTTP server
  - Environment-based configuration
  - Graceful error handling and recovery

#### Backend API Server (`backend/app.py`)
- **Purpose**: Core API services and dashboard
- **Port**: 7860
- **Features**:
  - Comprehensive router integration
  - Static file serving for frontend
  - Production status aggregation
  - Health monitoring and cross-service communication

#### Dashboard Server (`dashboard.py`)
- **Purpose**: Dedicated dashboard interface
- **Features**:
  - Real-time monitoring
  - User interface for system management
  - Performance analytics

### 1.2 Specialized Servers

#### TDD Agent Server (`agents/tdd_agent.py`)
- **Purpose**: Test-Driven Development automation
- **Features**:
  - Automated test generation
  - Code analysis and failure detection
  - Integration with pytest framework

#### SOLO Agent Server (`trae_ai/servers/main_server.py`)
- **Purpose**: Autonomous development agent
- **Features**:
  - Genesis interviews
  - Orchestrator events
  - WebSocket support for real-time communication

## 2. Backend Architecture

### 2.1 API Orchestration Layer

#### API Orchestrator (`backend/api_orchestrator.py`)
```python
class APIOrchestrator:
    - FastAPI application management
    - Route registration and management
    - Request history and rate limiting
    - CORS middleware configuration
    - Dynamic route handling
```

#### Router Architecture
The system uses a modular router approach with conditional imports:

**Core Routers:**
- `production_health_router`: System health monitoring
- `api_discovery_router`: API endpoint discovery
- `channels_router`: Channel management
- `pets_router`: Pet management (example API)
- `runtime_router`: Runtime operations
- `auth_router`: Authentication services
- `users_router`: User management
- `admin_router`: Administrative functions
- `policy_router`: Policy management
- `solo_agent_router`: SOLO agent endpoints

### 2.2 Authentication & Security Layer

#### Authentication System (`backend/auth/`)
```
auth/
├── routes.py          # FastAPI authentication routes
├── models.py          # Pydantic models for auth
├── service.py         # Business logic layer
└── security.py        # JWT and security utilities
```

**Key Components:**
- JWT token management
- User registration and login
- Role-based access control (RBAC)
- Password hashing and validation
- Refresh token handling

### 2.3 Service Layer Architecture

#### Core Services
- **User Service**: User management and profile operations
- **Auth Service**: Authentication and authorization logic
- **Content Service**: Content management and processing
- **Analytics Service**: Performance and usage analytics

### 2.4 Data Persistence Layer

#### Database Architecture
The system uses a sophisticated SQLite-based architecture with multiple specialized databases:

**Primary Databases:**
1. **right_perspective.db** - Core system data
2. **intelligence.db** - AI and analytics data
3. **secrets.sqlite** - Encrypted secrets storage

#### Schema Overview (`schema.sql` - 2137 lines)

**Core Tables:**
- `task_queue`: Asynchronous task management
- `api_registry`: External API integration tracking
- `author_personas`: AI personality management
- `hypocrisy_tracker`: Content consistency analysis
- `evidence`: Research and source management
- `performance_metrics`: System performance tracking
- `component_health`: Service health monitoring

**Advanced Features:**
- JSON column support for flexible data storage
- Comprehensive indexing for performance
- Foreign key constraints for data integrity
- Audit logging and change tracking
- Automated backup and recovery systems

## 3. Frontend Architecture

### 3.1 Multi-Framework Approach

#### HTML/JavaScript Dashboard (`app/templates/dashboard.html`)
- **Size**: 1,462 lines of comprehensive dashboard
- **Features**:
  - Real-time system monitoring
  - Interactive charts and analytics
  - User management interface
  - Responsive design with Tailwind CSS
  - Progressive Web App capabilities

#### React Components (`frontend/components/`)
```
frontend/
├── components/
│   └── RuntimeHQ.jsx      # Runtime monitoring component
└── package.json           # React dependencies
```

**React Architecture:**
- Modern React 18.3.1 with hooks
- Vite build system for fast development
- Tailwind CSS for styling
- Component-based architecture

### 3.2 UI/UX Features

#### Dashboard Capabilities
- **Real-time Monitoring**: Live system status updates
- **Interactive Analytics**: Charts and performance metrics
- **User Management**: Authentication and role management
- **Module System**: Tabbed interface for different functionalities
- **Responsive Design**: Mobile-first approach
- **Progressive Enhancement**: Graceful degradation

#### JavaScript Architecture (`app/static/js/dashboard.js`)
- **Size**: 1,351 lines of interactive functionality
- **Features**:
  - Event-driven architecture
  - AJAX-based API communication
  - Real-time data updates
  - Form validation and submission
  - Keyboard shortcuts
  - Search and filtering capabilities

## 4. Agent Architecture

### 4.1 TDD Agent System

#### Core Components
```python
class TDDAgent:
    - Test failure analysis
    - Code generation and fixes
    - Integration with pytest
    - Visual feedback system
```

**Capabilities:**
- Automated test failure detection
- Intelligent code fix generation
- Integration with testing frameworks
- Real-time feedback and reporting

### 4.2 SOLO Agent System

#### Architecture
```python
class SOLOAgent:
    - Autonomous development capabilities
    - Genesis interview system
    - Task orchestration
    - WebSocket communication
```

**Features:**
- Self-directed development tasks
- Interactive requirement gathering
- Automated code generation
- Real-time progress reporting

## 5. Integration & Communication Layer

### 5.1 API Integration

#### External API Management
- **OpenAI API**: AI model integration
- **YouTube API**: Video platform integration
- **Twitter API**: Social media integration
- **Custom APIs**: Extensible integration framework

#### Rate Limiting & Monitoring
- Per-minute, per-hour, and per-day limits
- Usage tracking and analytics
- Automatic failover and retry logic
- Health monitoring and alerting

### 5.2 Inter-Service Communication

#### Communication Patterns
- **HTTP/REST**: Primary API communication
- **WebSocket**: Real-time updates
- **Event-Driven**: Asynchronous task processing
- **Database Sharing**: Shared data layer

## 6. Monitoring & Observability

### 6.1 Health Monitoring System

#### Component Health Tracking
```sql
component_health:
- component_name: Service identifier
- status: healthy/degraded/failing/critical
- uptime_percentage: Availability metrics
- consecutive_failures: Failure tracking
- recovery_time_avg: Performance metrics
```

### 6.2 Performance Analytics

#### Metrics Collection
- **Response Times**: API endpoint performance
- **Resource Usage**: CPU, memory, disk utilization
- **Error Rates**: Failure tracking and analysis
- **User Analytics**: Usage patterns and behavior

## 7. Security Architecture

### 7.1 Authentication & Authorization

#### Security Layers
- **JWT Tokens**: Stateless authentication
- **Role-Based Access**: Granular permissions
- **API Key Management**: Secure external integrations
- **Secrets Management**: Encrypted storage system

### 7.2 Data Protection

#### Security Measures
- **Encrypted Secrets**: Secure credential storage
- **CORS Configuration**: Cross-origin protection
- **Input Validation**: SQL injection prevention
- **Audit Logging**: Security event tracking

## 8. Deployment Architecture

### 8.1 Multi-Server Configuration

#### Server Distribution
- **Main Server** (Port 8000): Primary application
- **Backend API** (Port 7860): Core services
- **Dashboard Server**: User interface
- **Agent Servers**: Specialized AI services

### 8.2 Environment Management

#### Configuration Strategy
- **Environment Variables**: Runtime configuration
- **Config Files**: Application settings
- **Database Migrations**: Schema management
- **Health Checks**: Service monitoring

## 9. Data Flow Architecture

### 9.1 Request Flow

```
User Request → API Gateway → Router → Service Layer → Database
                    ↓
            Authentication → Authorization → Business Logic
```

### 9.2 Data Processing Pipeline

```
Input → Validation → Processing → Storage → Response
   ↓        ↓           ↓          ↓         ↓
Logging → Metrics → Analytics → Audit → Monitoring
```

## 10. Scalability & Performance

### 10.1 Performance Optimizations

#### Database Optimizations
- **WAL Mode**: Write-Ahead Logging for concurrency
- **Indexing Strategy**: Optimized query performance
- **Connection Pooling**: Efficient resource usage
- **Caching Layer**: Response caching system

### 10.2 Scalability Considerations

#### Horizontal Scaling
- **Microservices**: Independent service scaling
- **Load Balancing**: Request distribution
- **Database Sharding**: Data partitioning
- **Caching Strategy**: Performance optimization

## 11. Technology Stack Summary

### Backend Technologies
- **FastAPI**: Modern Python web framework
- **SQLite**: Embedded database system
- **Uvicorn**: ASGI server implementation
- **Pydantic**: Data validation and serialization
- **JWT**: Authentication token system

### Frontend Technologies
- **React 18.3.1**: Modern UI framework
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Data visualization
- **Font Awesome**: Icon library

### Development Tools
- **Python 3.9+**: Core programming language
- **Node.js**: Frontend build environment
- **Git**: Version control system
- **Docker**: Containerization (planned)

## 12. Future Architecture Considerations

### 12.1 Planned Enhancements
- **Kubernetes Deployment**: Container orchestration
- **Redis Integration**: Advanced caching
- **PostgreSQL Migration**: Production database
- **Microservices Expansion**: Service decomposition

### 12.2 Monitoring Improvements
- **Prometheus Integration**: Metrics collection
- **Grafana Dashboards**: Advanced visualization
- **ELK Stack**: Centralized logging
- **APM Integration**: Application performance monitoring

---

**Document Version**: 1.0.0  
**Last Updated**: January 2025  
**Author**: TRAE.AI System Analysis  
**Status**: Production Ready