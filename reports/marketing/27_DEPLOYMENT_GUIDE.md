# TRAE AI Production Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying TRAE AI to production environments
using a secure, automated CI/CD pipeline. The deployment process follows industry best practices for
security, reliability, and maintainability.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Security Configuration](#security-configuration)
4. [Deployment Process](#deployment-process)
5. [Monitoring and Health Checks](#monitoring-and-health-checks)
6. [Rollback Procedures](#rollback-procedures)
7. [Troubleshooting](#troubleshooting)
8. [Maintenance](#maintenance)

## Prerequisites

### Required Tools

- **Git**: Version control and repository management
- **Node.js**: v18+ for build processes
- **Python**: v3.8+ for backend services
- **Netlify CLI**: For deployment management
- **GitHub CLI** (optional): For workflow automation

### Required Accounts

- **GitHub Account**: Repository hosting and CI/CD
- **Netlify Account**: Hosting and deployment platform
- **Domain Provider**: For custom domain configuration (optional)

### System Requirements

- **Development Machine**: macOS, Linux, or Windows with WSL2
- **Memory**: Minimum 8GB RAM for local development
- **Storage**: At least 5GB free space for dependencies and builds

## Environment Setup

### 1. Repository Configuration

```bash
# Clone the repository
git clone <your-repository-url>
cd <repository-name>

# Install dependencies
npm install
pip install -r requirements.txt

# Copy environment template
cp .env.example .env.local
```

### 2. Environment Variables

Create and configure the following environment files:

#### `.env.local` (Development)

```bash
# Core System Configuration
TRAE_MASTER_KEY=your-development-master-key
TRAE_ENVIRONMENT=development
TRAE_DEBUG=true
TRAE_LOG_LEVEL=DEBUG

# Dashboard Configuration
DASHBOARD_SECRET_KEY=your-development-dashboard-secret
DASHBOARD_PORT=5000
DASHBOARD_HOST=127.0.0.1

# Database Configuration
DATABASE_URL=sqlite:///./data/trae_ai_dev.db
DATABASE_POOL_SIZE=5
DATABASE_TIMEOUT=30

# External API Keys (Development)
OLLAMA_API_URL=http://localhost:11434
OPENAI_API_KEY=your-development-openai-key
```

#### Production Environment Variables (Netlify)

Configure these in Netlify's environment variables section:

```bash
# Core System Configuration
TRAE_MASTER_KEY=<secure-production-master-key>
TRAE_ENVIRONMENT=production
TRAE_DEBUG=false
TRAE_LOG_LEVEL=INFO

# Dashboard Configuration
DASHBOARD_SECRET_KEY=<secure-production-dashboard-secret>
DASHBOARD_PORT=8080
DASHBOARD_HOST=0.0.0.0

# Database Configuration
DATABASE_URL=<production-database-url>
DATABASE_POOL_SIZE=20
DATABASE_TIMEOUT=60

# External API Keys (Production)
OLLAMA_API_URL=<production-ollama-url>
OPENAI_API_KEY=<production-openai-key>

# Security Configuration
SECURE_SSL_REDIRECT=true
SESSION_COOKIE_SECURE=true
CSRF_COOKIE_SECURE=true

# Performance Configuration
WEB_CONCURRENCY=4
MAX_WORKERS=8
WORKER_TIMEOUT=120
```

### 3. GitHub Secrets Configuration

Configure the following secrets in your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following repository secrets:

```bash
NETLIFY_AUTH_TOKEN=<your-netlify-auth-token>
NETLIFY_SITE_ID=<your-netlify-site-id>
TRAE_MASTER_KEY=<production-master-key>
DASHBOARD_SECRET_KEY=<production-dashboard-secret>
```

## Security Configuration

### 1. Secret Generation

Generate secure secrets using the provided script:

```bash
# Generate secure secrets
python -c "import secrets; print('TRAE_MASTER_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('DASHBOARD_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

### 2. Netlify Authentication

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Get your auth token
netlify status
```

### 3. Security Scanning

Run security scans before deployment:

```bash
# Run comprehensive security scan
./scripts/run-tests.sh

# Run specific security tools
bandit -r app/ -f json -o security-report.json
safety check --json --output safety-report.json
gitleaks detect --source . --verbose
```

## Deployment Process

### 1. Pre-Deployment Checklist

- [ ] All tests pass locally
- [ ] Security scans complete without critical issues
- [ ] Environment variables configured
- [ ] GitHub secrets configured
- [ ] Netlify site created and configured
- [ ] Domain configured (if using custom domain)

### 2. Staging Deployment

```bash
# Deploy to staging environment
./scripts/deploy-staging.sh

# Run smoke tests on staging
./scripts/smoke-tests.sh <staging-url>
```

### 3. Production Deployment

#### Automated Deployment (Recommended)

1. **Create a Pull Request** to the `main` branch
2. **Review and approve** the pull request
3. **Merge to main** - this triggers the production deployment workflow
4. **Monitor the deployment** in GitHub Actions

#### Manual Deployment

```bash
# Ensure you're on the main branch
git checkout main
git pull origin main

# Run the production deployment script
./scripts/deploy-production.sh
```

### 4. Post-Deployment Verification

```bash
# Run smoke tests on production
./scripts/smoke-tests.sh <production-url>

# Check health endpoints
curl https://your-domain.com/api/health
curl https://your-domain.com/netlify/functions/health-check

# Monitor logs
netlify logs --site-id=<your-site-id>
```

## Monitoring and Health Checks

### 1. Health Check Endpoints

- **Application Health**: `https://your-domain.com/api/health`
- **System Health**: `https://your-domain.com/netlify/functions/health-check`
- **Monitoring Dashboard**: `https://your-domain.com/monitoring`

### 2. Monitoring Dashboard

Access the real-time monitoring dashboard:

```bash
# Start monitoring dashboard locally
python monitoring/monitoring_dashboard.py

# Access at http://localhost:5001
```

### 3. Performance Monitoring

```bash
# Run performance monitor
python monitoring/performance_monitor.py

# Check performance metrics
python -c "from monitoring.performance_monitor import PerformanceMonitor; pm = PerformanceMonitor(); print(pm.get_health_status())"
```

### 4. Error Tracking

```bash
# Run error tracker
python monitoring/error_tracker.py

# Get error summary
python -c "from monitoring.error_tracker import ErrorTracker; et = ErrorTracker(); print(et.get_error_summary(24))"
```

## Rollback Procedures

### 1. Emergency Rollback

For critical issues requiring immediate rollback:

```bash
# Emergency rollback to previous deployment
./scripts/rollback-production.sh --emergency

# Rollback to specific deployment
./scripts/rollback-production.sh --deployment-id <deployment-id>
```

### 2. Planned Rollback

For planned rollbacks with verification:

```bash
# Rollback to last known good deployment
./scripts/rollback-production.sh --last-good

# Rollback to previous deployment with confirmation
./scripts/rollback-production.sh --previous
```

### 3. Manual Rollback via Netlify

1. **Login to Netlify Dashboard**
2. **Navigate to your site** → **Deploys**
3. **Find the stable deployment** you want to rollback to
4. **Click "Publish deploy"** to make it live
5. **Run smoke tests** to verify the rollback

### 4. Post-Rollback Actions

```bash
# Verify rollback success
./scripts/smoke-tests.sh <production-url>

# Check application health
curl https://your-domain.com/api/health

# Monitor error logs
netlify logs --site-id=<your-site-id> --follow

# Create incident report
echo "Rollback completed at $(date)" >> incident-log.txt
```

## Troubleshooting

### Common Issues

#### 1. Build Failures

```bash
# Check build logs
netlify logs --site-id=<your-site-id>

# Local build test
npm run build
python -m pytest tests/

# Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### 2. Environment Variable Issues

```bash
# Verify environment variables
netlify env:list --site-id=<your-site-id>

# Test environment loading
python -c "import os; print(os.environ.get('TRAE_MASTER_KEY', 'NOT_SET'))"

# Update environment variables
netlify env:set VARIABLE_NAME "value" --site-id=<your-site-id>
```

#### 3. Function Deployment Issues

```bash
# Test functions locally
netlify dev

# Check function logs
netlify functions:list
netlify logs --functions

# Redeploy functions
netlify deploy --functions=netlify/functions
```

#### 4. SSL/Domain Issues

```bash
# Check SSL certificate
curl -I https://your-domain.com

# Verify DNS configuration
nslookup your-domain.com

# Force SSL renewal (if needed)
# Contact Netlify support for SSL issues
```

### Debug Commands

```bash
# Check deployment status
netlify status --site-id=<your-site-id>

# View recent deployments
netlify api listSiteDeploys --data '{"site_id": "<your-site-id>"}'

# Test API endpoints
curl -v https://your-domain.com/api/health
curl -v https://your-domain.com/netlify/functions/health-check

# Check application logs
tail -f logs/trae_ai.log
tail -f logs/error.log
```

## Maintenance

### Regular Maintenance Tasks

#### Weekly

- [ ] Review error logs and alerts
- [ ] Check performance metrics
- [ ] Update dependencies (if needed)
- [ ] Verify backup integrity

#### Monthly

- [ ] Security scan and vulnerability assessment
- [ ] Performance optimization review
- [ ] Capacity planning review
- [ ] Documentation updates

#### Quarterly

- [ ] Disaster recovery testing
- [ ] Security audit
- [ ] Performance benchmarking
- [ ] Infrastructure cost review

### Maintenance Scripts

```bash
# Update dependencies
npm update
pip install --upgrade -r requirements.txt

# Clean up old logs
find logs/ -name "*.log" -mtime +30 -delete

# Database maintenance
python -c "from app.database import cleanup_old_records; cleanup_old_records()"

# Performance optimization
python monitoring/performance_monitor.py --optimize
```

### Backup Procedures

```bash
# Backup database
python -c "from app.database import backup_database; backup_database('backup_$(date +%Y%m%d).db')"

# Backup configuration
tar -czf config_backup_$(date +%Y%m%d).tar.gz .env.example netlify.toml

# Backup logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/
```

## Security Best Practices

### 1. Secret Management

- **Never commit secrets** to version control
- **Use environment variables** for all sensitive data
- **Rotate secrets regularly** (quarterly recommended)
- **Use different secrets** for each environment
- **Monitor for exposed secrets** using automated scanning

### 2. Access Control

- **Limit repository access** to necessary team members
- **Use branch protection rules** on main branch
- **Require pull request reviews** for all changes
- **Enable two-factor authentication** on all accounts
- **Regularly audit access permissions**

### 3. Network Security

- **Use HTTPS everywhere** (enforced by Netlify)
- **Configure security headers** (implemented in netlify.toml)
- **Implement rate limiting** for API endpoints
- **Monitor for suspicious activity**

### 4. Monitoring and Alerting

- **Set up error alerting** for critical issues
- **Monitor performance metrics** continuously
- **Log security events** for audit trails
- **Implement health checks** for early issue detection

## Support and Resources

### Documentation

- [Netlify Documentation](https://docs.netlify.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Security Best Practices](https://python.org/dev/security/)

### Emergency Contacts

- **Development Team**: [team-email@company.com]
- **DevOps Team**: [devops@company.com]
- **Security Team**: [security@company.com]

### Incident Response

1. **Assess the severity** of the issue
2. **Execute rollback** if necessary
3. **Notify stakeholders** of the incident
4. **Investigate root cause** after stabilization
5. **Document lessons learned** and update procedures

---

**Last Updated**: January 2025
**Version**: 1.0
**Maintained By**: TRAE AI Development Team
