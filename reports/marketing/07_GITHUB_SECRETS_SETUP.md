# 🔐 GitHub Secrets Configuration Guide

## Overview

This guide provides step-by-step instructions for configuring GitHub repository secrets required for the production CI/CD pipeline. These secrets enable secure authentication with external services while keeping sensitive credentials out of the codebase.

## 🚨 Security Requirements

**CRITICAL**: Never commit these values to your repository. Always use GitHub's encrypted secrets feature.

## Required Secrets

### Core Application Secrets

| Secret Name | Description | Example/Format | Required |
|-------------|-------------|----------------|----------|
| `ADMIN_PASSWORD` | Admin user password | `SecureP@ssw0rd123!` | ✅ |
| `CONFIG_MASTER_PASSWORD` | Configuration encryption key | `base64-encoded-32-chars` | ✅ |
| `GRAFANA_ADMIN_PASSWORD` | Monitoring dashboard password | `MonitorP@ss2024!` | ✅ |
| `MASTER_API_KEY` | Internal API master key | `trae-master-abc123...` | ✅ |
| `FLASK_SECRET_KEY` | Flask session encryption | `hex-encoded-64-chars` | ✅ |

### Database & Infrastructure

| Secret Name | Description | Example/Format | Required |
|-------------|-------------|----------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` | ✅ |
| `POSTGRES_PASSWORD` | Database password | `DbSecureP@ss2024!` | ✅ |
| `REDIS_URL` | Redis connection string | `redis://user:pass@host:6379` | ⚠️ |

### External API Keys

| Secret Name | Description | Example/Format | Required |
|-------------|-------------|----------------|----------|
| `OPENAI_API_KEY` | OpenAI API access | `sk-...` | ✅ |
| `YOUTUBE_API_KEY` | YouTube Data API | `AIza...` | ⚠️ |

### Deployment & CDN

| Secret Name | Description | Example/Format | Required |
|-------------|-------------|----------------|----------|
| `NETLIFY_AUTH_TOKEN` | Netlify deployment token | `nfp_...` | ✅ |
| `NETLIFY_SITE_ID` | Production site ID | `abc123-def456-...` | ✅ |
| `NETLIFY_STAGING_SITE_ID` | Staging site ID | `xyz789-uvw012-...` | ⚠️ |

### Client-Side Environment Variables

| Secret Name | Description | Example/Format | Required |
|-------------|-------------|----------------|----------|
| `VITE_API_URL` | Frontend API endpoint | `https://api.yourdomain.com` | ✅ |
| `VITE_APP_NAME` | Application display name | `TRAE AI Production` | ⚠️ |

**Legend**: ✅ Required | ⚠️ Optional

## 📋 Setup Instructions

### Step 1: Generate Secure Credentials

```bash
# Navigate to your project directory
cd /path/to/your/project

# Generate all required credentials
python scripts/generate_credentials.py --format github

# Save credentials securely (optional)
python scripts/generate_credentials.py --save
```

### Step 2: Access GitHub Secrets

1. Navigate to your GitHub repository
2. Click **Settings** tab
3. In the left sidebar, click **Secrets and variables**
4. Click **Actions**
5. Click **New repository secret**

### Step 3: Add Each Secret

For each secret in the table above:

1. Click **New repository secret**
2. Enter the **Name** exactly as shown (case-sensitive)
3. Paste the **Value** (generated from Step 1)
4. Click **Add secret**

### Step 4: Verify Configuration

```bash
# Test the GitHub Actions workflow
gh workflow run production-deploy.yml \
  --field environment=staging \
  --field skip_tests=false

# Check workflow status
gh run list --workflow=production-deploy.yml
```

## 🔧 Netlify Configuration

### Required Netlify Tokens

#### 1. Personal Access Token

1. Go to [Netlify User Settings](https://app.netlify.com/user/applications)
2. Click **New access token**
3. Name: `GitHub Actions CI/CD`
4. Copy the token → Add as `NETLIFY_AUTH_TOKEN` in GitHub

#### 2. Site IDs

```bash
# Get site ID for existing site
netlify sites:list

# Or create new site
netlify sites:create --name your-app-production
netlify sites:create --name your-app-staging
```

### Netlify Environment Variables

Add these in Netlify dashboard (Site settings → Environment variables):

```bash
# Mark as SECRET in Netlify UI
MASTER_API_KEY=<from-github-secrets>
FLASK_SECRET_KEY=<from-github-secrets>
OPENAI_API_KEY=<your-openai-key>

# Public variables (not secret)
VITE_API_URL=https://api.yourdomain.com
VITE_APP_NAME=TRAE AI Production
ENVIRONMENT=production
```

## 🔍 Security Validation

### Pre-Deployment Checklist

- [ ] All required secrets added to GitHub
- [ ] No secrets committed to repository
- [ ] Netlify tokens have minimal required permissions
- [ ] Database credentials use strong passwords
- [ ] API keys are from production accounts (not test/demo)
- [ ] All secrets follow naming convention exactly

### Validation Commands

```bash
# Check for accidentally committed secrets
grep -r "sk-" . --exclude-dir=".git" --exclude-dir="node_modules"
grep -r "nfp_" . --exclude-dir=".git" --exclude-dir="node_modules"

# Verify environment variable loading
python -c "
import os
required = ['ADMIN_PASSWORD', 'MASTER_API_KEY', 'DATABASE_URL']
missing = [var for var in required if not os.getenv(var)]
if missing: print(f'Missing: {missing}'); exit(1)
else: print('✅ All secrets configured')
"
```

## 🚨 Security Best Practices

### 1. Principle of Least Privilege

- Use separate API keys for different environments
- Grant minimum required permissions to each token
- Regularly audit and rotate credentials

### 2. Secret Rotation Schedule

| Secret Type | Rotation Frequency | Method |
|-------------|-------------------|--------|
| Database passwords | Quarterly | Manual + notification |
| API keys | Bi-annually | Automated where possible |
| Deployment tokens | Annually | Manual verification |
| Internal secrets | Quarterly | Automated generation |

### 3. Incident Response

If secrets are compromised:

1. **Immediate** (< 5 minutes):
   - Revoke compromised credentials
   - Generate new credentials
   - Update GitHub secrets

2. **Short-term** (< 1 hour):
   - Redeploy application with new credentials
   - Audit access logs
   - Notify security team

3. **Long-term** (< 24 hours):
   - Complete security review
   - Update incident response procedures
   - Implement additional monitoring

## 📞 Support & Troubleshooting

### Common Issues

**Issue**: Workflow fails with "Secret not found"
**Solution**: Verify secret name matches exactly (case-sensitive)

**Issue**: Netlify deployment fails
**Solution**: Check `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID` are correct

**Issue**: Database connection fails
**Solution**: Verify `DATABASE_URL` format and credentials

### Getting Help

- **GitHub Actions**: [GitHub Actions Documentation](https://docs.github.com/en/actions)
- **Netlify**: [Netlify Documentation](https://docs.netlify.com/)
- **Security Issues**: Contact security team immediately

## 📊 Monitoring & Alerts

### Set up monitoring for:

- Failed deployments
- Secret rotation reminders
- Unusual API usage patterns
- Security scan failures

### Recommended Tools

- **GitHub**: Dependabot alerts
- **Netlify**: Deploy notifications
- **External**: Uptime monitoring (Pingdom, StatusCake)

---

**Last Updated**: $(date)
**Next Review**: Quarterly
**Owner**: DevOps Team