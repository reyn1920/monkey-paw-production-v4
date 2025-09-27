# 🚀 Live Deployment Setup Guide

This guide walks you through setting up GitHub repository secrets and Netlify configuration for automated deployment.

## 📋 Prerequisites Checklist

- [ ] GitHub repository created and code pushed to main branch
- [ ] Netlify account created
- [ ] Production domain configured (optional)
- [ ] All AI platform API keys ready

## 🔐 Step 1: Configure GitHub Repository Secrets

### Required Secrets

Navigate to your GitHub repository → Settings → Secrets and variables → Actions

#### Core Deployment Secrets

1. **NETLIFY_AUTH_TOKEN**
   - Go to [Netlify User Settings](https://app.netlify.com/user/applications#personal-access-tokens)
   - Click "New access token"
   - Name: "GitHub Actions Deployment"
   - Copy the token and add to GitHub secrets

2. **NETLIFY_SITE_ID**
   - Create a new site on Netlify or use existing
   - Go to Site settings → General → Site details
   - Copy the "Site ID" and add to GitHub secrets

#### Production Environment Secrets

3. **SECRET_KEY**
   ```bash
   # Generate a secure secret key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

4. **OPENAI_API_KEY** (if using ChatGPT integration)
   - Get from [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Format: `sk-...`

5. **GOOGLE_API_KEY** (if using Gemini integration)
   - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Format: `AIza...`

6. **ABACUS_API_KEY** (if using Abacus AI integration)
   - Get from Abacus AI dashboard
   - Contact support if needed

### Optional Production Secrets

7. **DATABASE_URL** (if using external database)
8. **REDIS_URL** (if using Redis caching)
9. **SENTRY_DSN** (for error monitoring)

## 🌐 Step 2: Configure Netlify Site

### Create Netlify Site

1. **Via Netlify Dashboard:**
   ```bash
   # Option 1: Manual site creation
   # 1. Go to https://app.netlify.com/# 2. Click "Add new site" → "Import an existing project"
   # 3. Connect to GitHub and select your repository
   # 4. Build settings:
   #    - Build command: npm run build
   #    - Publish directory: dist
   ```

2. **Via Netlify CLI (Recommended):**
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli
   
   # Login to Netlify
   netlify login
   
   # Initialize site
   netlify init
   
   # Follow prompts to create new site or link existing
   ```

### Configure Build Settings

```toml
# netlify.toml (already exists in your project)
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "18"
  NPM_VERSION = "9"

# Production environment variables
[context.production.environment]
  NODE_ENV = "production"
  VITE_API_URL = "https://your-api-domain.com"
  VITE_APP_ENV = "production"

# Staging environment variables
[context.deploy-preview.environment]
  NODE_ENV = "staging"
  VITE_API_URL = "https://staging-api.your-domain.com"
  VITE_APP_ENV = "staging"
```

### Set Environment Variables in Netlify

1. Go to Site settings → Environment variables
2. Add production environment variables:

```bash
# Core application variables
NODE_ENV=production
VITE_APP_ENV=production
VITE_API_URL=https://your-production-api.com

# AI Platform Configuration
VITE_ENABLE_CHATGPT=true
VITE_ENABLE_GEMINI=true
VITE_ENABLE_ABACUS=true

# Security (mark as secret)
SECRET_KEY=[your-secret-key]
OPENAI_API_KEY=[your-openai-key]  # Mark as secret
GOOGLE_API_KEY=[your-google-key]  # Mark as secret
ABACUS_API_KEY=[your-abacus-key]  # Mark as secret
```

## 🔧 Step 3: Update Package.json Scripts

Ensure your `package.json` has the required build scripts:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "test": "jest",
    "test:ci": "jest --ci --coverage --watchAll=false"
  }
}
```

## 🚀 Step 4: Deploy to Staging

### Test Staging Deployment

1. **Create Pull Request:**
   ```bash
   git checkout -b feature/deployment-test
   git add .
   git commit -m "feat: prepare for staging deployment"
   git push origin feature/deployment-test
   ```

2. **Create PR on GitHub:**
   - This will trigger automatic staging deployment
   - Review the deploy preview URL in PR comments

3. **Manual Staging Deployment:**
   ```bash
   # Via GitHub Actions
   # Go to Actions tab → Deploy to Production → Run workflow
   # Select "staging" environment
   ```

## 🎯 Step 5: Production Deployment

### Pre-deployment Checklist

- [ ] All tests passing in staging
- [ ] Security scans completed
- [ ] Environment variables configured
- [ ] Domain/DNS configured (if custom domain)
- [ ] Monitoring setup (optional)

### Deploy to Production

1. **Via GitHub Actions (Recommended):**
   ```bash
   # Go to GitHub Actions → Deploy to Production
   # Click "Run workflow"
   # Select "production" environment
   # Confirm deployment
   ```

2. **Via Netlify CLI:**
   ```bash
   # Build locally
   npm run build
   
   # Deploy to production
   netlify deploy --prod --dir=dist
   ```

## 📊 Step 6: Post-Deployment Verification

### Automated Checks

The deployment workflow includes:
- Health checks
- API endpoint verification
- AI platform integration tests

### Manual Verification

1. **Test Core Functionality:**
   - [ ] Main dashboard loads
   - [ ] User authentication works
   - [ ] AI platforms respond correctly

2. **Test AI Integrations:**
   - [ ] ChatGPT integration functional
   - [ ] Gemini integration functional
   - [ ] Abacus AI integration functional

3. **Performance Check:**
   - [ ] Page load times acceptable
   - [ ] API response times normal
   - [ ] No console errors

## 🔍 Monitoring and Maintenance

### Set Up Monitoring (Optional)

```bash
# Add Sentry for error tracking
npm install @sentry/browser @sentry/tracing

# Configure in your app
# Add SENTRY_DSN to environment variables
```

### Regular Maintenance

- Monitor deployment logs
- Check AI platform usage and costs
- Update dependencies regularly
- Review security scans

## 🆘 Troubleshooting

### Common Issues

1. **Build Failures:**
   ```bash
   # Check build logs in GitHub Actions
   # Verify all dependencies in package.json
   # Ensure environment variables are set
   ```

2. **Deployment Failures:**
   ```bash
   # Verify Netlify secrets in GitHub
   # Check Netlify site configuration
   # Review deployment logs
   ```

3. **Runtime Errors:**
   ```bash
   # Check browser console for errors
   # Verify API endpoints are accessible
   # Confirm environment variables are loaded
   ```

### Support Resources

- [Netlify Documentation](https://docs.netlify.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)

---

## 🎉 Success!

Once completed, your integrated AI platform will be live with:
- ✅ Automated CI/CD pipeline
- ✅ Secure secrets management
- ✅ Multi-environment support
- ✅ AI platform integrations
- ✅ Monitoring and error tracking

**Next Steps:** Monitor your live application and iterate based on user feedback!