# 🚀 TRAE.AI COMPLETE SYSTEM RESTORATION & DEBUG PROMPT

You are an expert system architect tasked with fully debugging and restoring a complex AI agent system called **Trae.ai**. This system has multiple interconnected agents, databases, and integrations that need to work together seamlessly.

## 🎯 MISSION OBJECTIVE
Analyze the provided logs, identify ALL issues, and create a comprehensive restoration plan that brings Trae.ai back to full operational status with enhanced reliability and performance.

## 📋 SYSTEM ARCHITECTURE OVERVIEW

### Core Agents
- **ExecutorAgent**: Main orchestration (19 tools initialized)
- **ResearchAgent**: Market research, API discovery, affiliate opportunities
- **ContentAgent**: Content creation, video editing, channel management
- **MarketingAgent**: E-commerce marketing, campaign management
- **PlannerAgent**: Task planning and coordination
- **SystemAgent**: System monitoring and health checks
- **AuditorAgent**: Quality assurance and compliance

### Key Integrations
- **Ollama**: Local AI models (13 models available, healthy)
- **Blender 4.5.2**: Video composition and 3D rendering
- **FFmpeg 7.1.1**: Audio/video processing
- **SQLite Databases**: Multiple databases for different functions
- **Browser Automation**: Web scraping and AI service integration

### External AI Services Integration
- **Abacus.AI** (https://apps.abacus.ai/chatllm/?appId=1024a18ebe)
- **Google Gemini** (https://gemini.google.com/app)
- **ChatGPT** (https://chatgpt.com/)

## 🔍 IDENTIFIED CRITICAL ISSUES

### 1. Database Schema Problems
- **api_discovery_tasks** table column mismatch
- Missing or corrupted database constraints
- Data integrity issues across multiple SQLite databases

### 2. Import Dependencies
- Missing `shutil` imports in content processing modules
- Potential circular import dependencies
- Module path resolution issues

### 3. Agent Communication
- Inter-agent message passing failures
- Protocol synchronization issues
- Resource contention between agents

### 4. External Service Integration
- API authentication failures
- Rate limiting and quota management
- Service availability monitoring

### 5. Performance Bottlenecks
- High CPU usage in BlenderCompositor
- Memory leaks in long-running processes
- Inefficient database queries

## 🛠️ RESTORATION STRATEGY

### Phase 1: Database Restoration
1. **Schema Validation**
   - Audit all SQLite database schemas
   - Identify and fix column mismatches
   - Restore referential integrity

2. **Data Migration**
   - Backup existing data
   - Migrate to corrected schemas
   - Validate data consistency

### Phase 2: Dependency Resolution
1. **Import Analysis**
   - Scan all Python modules for missing imports
   - Resolve circular dependencies
   - Update import paths

2. **Module Testing**
   - Unit test each agent module
   - Integration testing between agents
   - Performance benchmarking

### Phase 3: Agent Optimization
1. **Resource Management**
   - Implement proper connection pooling
   - Add memory management for long-running processes
   - Optimize CPU-intensive operations

2. **Communication Protocol**
   - Standardize inter-agent messaging
   - Implement retry mechanisms
   - Add circuit breakers for external services

### Phase 4: Monitoring & Alerting
1. **Health Checks**
   - Implement comprehensive health endpoints
   - Add performance metrics collection
   - Create alerting thresholds

2. **Logging Enhancement**
   - Structured logging across all components
   - Log aggregation and analysis
   - Error tracking and reporting

## 🔧 IMPLEMENTATION CHECKLIST

### Database Tasks
- [ ] Run database schema validation
- [ ] Fix api_discovery_tasks table structure
- [ ] Implement database migration scripts
- [ ] Add data integrity constraints
- [ ] Create database backup procedures

### Code Quality Tasks
- [ ] Add missing shutil imports
- [ ] Resolve circular import issues
- [ ] Update deprecated API calls
- [ ] Implement proper error handling
- [ ] Add comprehensive logging

### Performance Tasks
- [ ] Optimize BlenderCompositor CPU usage
- [ ] Implement connection pooling
- [ ] Add memory leak detection
- [ ] Create performance monitoring
- [ ] Implement caching strategies

### Integration Tasks
- [ ] Test all external API connections
- [ ] Implement API rate limiting
- [ ] Add service health monitoring
- [ ] Create fallback mechanisms
- [ ] Update authentication tokens

### Testing Tasks
- [ ] Unit tests for all agents
- [ ] Integration tests for workflows
- [ ] Load testing for performance
- [ ] End-to-end system testing
- [ ] Disaster recovery testing

## 🚨 CRITICAL SUCCESS FACTORS

1. **Zero Downtime Migration**: Ensure system remains operational during restoration
2. **Data Integrity**: No data loss during schema migrations
3. **Performance Baseline**: Maintain or improve current performance metrics
4. **Monitoring Coverage**: 100% visibility into system health
5. **Documentation**: Complete system documentation for future maintenance

## 📊 SUCCESS METRICS

- **System Uptime**: >99.9%
- **Agent Response Time**: <500ms average
- **Database Query Performance**: <100ms average
- **Error Rate**: <0.1%
- **Memory Usage**: Stable over 24h periods
- **CPU Usage**: <80% sustained load

## 🔄 MAINTENANCE PROCEDURES

### Daily
- Health check validation
- Log analysis and alerting
- Performance metric review

### Weekly
- Database optimization
- Security patch assessment
- Capacity planning review

### Monthly
- Full system backup
- Disaster recovery testing
- Performance benchmarking
- Documentation updates

---

**Remember**: This is a mission-critical system restoration. Every step must be carefully planned, tested, and documented. The goal is not just to fix current issues but to build a robust, scalable, and maintainable system for the future.