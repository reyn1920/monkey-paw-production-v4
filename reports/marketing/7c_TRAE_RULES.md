# TRAE AI Project Rules

## AI Platform Integration Status

**FULLY INTEGRATED AI PLATFORMS** - The following AI platforms have been completely integrated into Trae AI on this system and are used with every prompt:

- **ChatGPT** (https://chatgpt.com/) - ✅ ACTIVE
- **Google Gemini** (https://gemini.google.com/app) - ✅ ACTIVE  
- **Abacus AI** (https://apps.abacus.ai/chatllm/?appId=1024a18ebe) - ✅ ACTIVE

### Integration Usage
These platforms are actively used for:
- **Debugging**: Advanced error analysis and troubleshooting
- **Coding**: Code generation, optimization, and best practices
- **Error Fixing**: Automated bug detection and resolution
- **Research**: Technical documentation and solution discovery
- **Development**: Full-stack application development assistance

These platforms serve as reference-quality benchmarks for correctness, clarity, and professionalism in all AI-assisted development tasks. All responses are cross-validated against these three platforms for optimal results within both the application and Trae AI system.

## Overview

This document establishes the core rules and guidelines for maintaining a secure, reliable, and
production-ready codebase in the Trae AI development environment with full AI platform integration.

## Core Principles

### 1. Security First

- **NEVER** hardcode secrets, API keys, or sensitive credentials in source code
- All sensitive data must be externalized using environment variables
- Use `.env.local` for development (ignored by Git)
- Production secrets must be injected at build time via CI/CD pipeline
- Apply principle of least privilege for all access tokens and permissions

### 2. Automation

- All builds, tests, and deployments must be fully automated
- No manual intervention in production deployment processes
- CI/CD pipeline must validate every code change
- Automated security scans are mandatory before deployment

### 3. Reliability

- Comprehensive test suite (unit, integration, E2E) required
- All tests must pass before code can be merged
- Atomic deployments with instant rollback capability
- Separate environments: development, staging, production

## Environment Management

### Development Environment

- Local workspace for code generation and testing
- Use `.env.local` for local configuration (Git ignored)
- Run all services locally for development and debugging

### Staging Environment

- Mirror of production infrastructure
- All changes must be tested in staging before production
- Use Netlify deployment previews for validation
- Comprehensive testing including security scans

### Production Environment

- Live environment serving end users
- Only deploy after successful staging validation
- Monitor all deployments and system health
- Maintain high availability and performance standards

## Code Quality Standards

### Linting and Formatting

- ESLint configuration must be enforced
- Prettier for consistent code formatting
- All code must pass linting checks before commit

### Security Scanning

- CodeQL for vulnerability detection
- Gitleaks for secret scanning
- Dependabot for dependency vulnerability management
- Regular security audits using automated tools

### Testing Requirements

- Minimum 80% code coverage for critical paths
- Unit tests for all business logic
- Integration tests for API endpoints
- End-to-end tests for user workflows

## CI/CD Pipeline Rules

### Continuous Integration (CI)

- Trigger on all push and pull request events
- Run linting, security scans, and full test suite
- Block merge if any checks fail
- Generate build artifacts for deployment

### Continuous Deployment (CD)

- Use `workflow_dispatch` for controlled production releases
- Deploy to staging automatically on main branch updates
- Require manual approval for production deployments
- Implement blue-green deployment strategy

## Secrets Management

### GitHub Secrets

- Use fine-grained Personal Access Tokens (PATs) over classic tokens
- Limit token permissions to minimum required scope
- Regular rotation of all access tokens
- Never use GITHUB_TOKEN for external service authentication

### Netlify Secrets

- Use Netlify's Secrets Controller for all production credentials
- Flag all sensitive variables as "secrets" (write-only)
- Implement automatic secret scanning
- Proxy sensitive API calls through serverless functions

## Content Validation

### Input Validation

- Implement both client-side and server-side validation
- Server-side validation is mandatory (client-side can be bypassed)
- Sanitize all user inputs to prevent injection attacks
- Use Netlify Functions for secure API proxying

### Content Security

- Validate all user-generated content
- Implement Content Security Policy (CSP) headers
- Regular security audits of user input handling
- Monitor for suspicious activity patterns

## File and Directory Rules

### Protected Files

- Never delete files marked in `tools/dnd/` directory
- Maintain audit trails for all configuration changes
- Version control all rule and configuration files

### Audit Requirements

- Run Rule-1 scanner before all commits
- Maintain clean audit logs
- Regular compliance checks using automated tools

## Git Workflow

### Branch Protection

- Main branch requires pull request reviews
- All status checks must pass before merge
- No direct pushes to main branch allowed
- Squash commits for clean history

### Commit Standards

- Use conventional commit messages
- Include issue references in commit messages
- Sign all commits with GPG keys
- Run pre-commit hooks for validation

## Monitoring and Alerting

### System Health

- Monitor application performance metrics
- Set up alerts for critical system failures
- Track deployment success/failure rates
- Monitor security scan results

### Logging

- Centralized logging for all services
- No sensitive data in log outputs
- Structured logging with appropriate levels
- Log retention policies for compliance

## Compliance and Auditing

### Regular Audits

- Weekly security scans
- Monthly dependency updates
- Quarterly access review
- Annual security assessment

### Documentation

- Keep all rules and procedures up to date
- Document all architectural decisions
- Maintain runbooks for incident response
- Regular review and update of this document

## Emergency Procedures

### Incident Response

- Immediate rollback procedures for critical issues
- Clear escalation paths for security incidents
- Post-incident review and documentation
- Communication protocols for stakeholders

### Recovery Procedures

- Database backup and restore procedures
- Service recovery protocols
- Data integrity verification steps
- Business continuity planning

---

**Last Updated:** 2025-01-28  
**Version:** 1.0  
**Next Review:** 2025-04-28

_This document is a living standard and should be reviewed and updated regularly to reflect current
best practices and security requirements._
