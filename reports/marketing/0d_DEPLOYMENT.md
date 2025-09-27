# Production Deployment Guide

This guide provides comprehensive instructions for deploying your application to production following security best practices and go-live rules.

## 🚀 Quick Start

### Prerequisites

1. **GitHub Repository**: Your code must be in a GitHub repository
2. **Netlify Account**: Sign up at [netlify.com](https://netlify.com)
3. **Environment Variables**: Configure all required secrets

### One-Time Setup

1. **Configure GitHub Secrets**:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add the following secrets:

   ```
   NETLIFY_AUTH_TOKEN=your_netlify_personal_access_token
   NETLIFY_SITE_ID=your_netlify_site_id
   SECRET_KEY=your_secure_random_key_for_production
   API_BASE_URL=https://your-api-domain.com
   ```

2. **Optional Pet Care API Secrets** (leave blank if not using):
   ```
   EBIRD_API_TOKEN=your_ebird_token
   DOG_API_KEY=your_dog_api_key
   CAT_API_KEY=your_cat_api_key
   PETFINDER_KEY=your_petfinder_key
   PETFINDER_SECRET=your_petfinder_secret
   VETSTER_API_KEY=your_vetster_key
   PAWP_API_KEY=your_pawp_key
   AIRVET_API_KEY=your_airvet_key
   CALENDLY_TOKEN=your_calendly_token
   ```

3. **Get Netlify Credentials**:
   - **Auth Token**: Go to Netlify → User settings → Personal access tokens → New access token
   - **Site ID**: Create a new site or find it in Site settings → General → Site details

## 🔒 Security Rules

### ✅ DO
- Store all secrets in GitHub Secrets or Netlify Environment Variables
- Use the automated deployment workflow
- Run security scans before deployment
- Test in staging before production
- Use HTTPS for all production URLs
- Validate all environment variables

### ❌ DON'T
- Hardcode API keys or secrets in code
- Skip security scans for production
- Deploy directly to production without testing
- Use HTTP in production
- Commit `.env` files with real secrets

## 🚦 Deployment Process

### Staging Deployment

1. **Create Pull Request**:
   ```bash
   git checkout -b feature/your-feature
   git add .
   git commit -m "Add new feature"
   git push origin feature/your-feature
   ```

2. **Open PR**: GitHub Actions will automatically:
   - Run security scans
   - Build the application
   - Deploy to staging
   - Provide preview URL in PR comments

### Production Deployment

1. **Merge to Main**:
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Manual Production Deploy**:
   - Go to GitHub → Actions → Deploy to Production
   - Click "Run workflow"
   - Select "production" environment
   - Click "Run workflow"

3. **Deployment Pipeline**:
   - ✅ Configuration validation
   - ✅ Security scanning
   - ✅ Automated testing
   - ✅ Production build
   - ✅ Deployment
   - ✅ Health check verification

## 🔧 Environment Configuration

### Local Development

Create `.env.local` (never commit this file):
```bash
# Development environment
NODE_ENV=development
VITE_API_BASE_URL=http://localhost:8000

# Optional: Pet Care APIs (for testing)
VITE_EBIRD_API_TOKEN=your_test_token
VITE_DOG_API_KEY=your_test_key
# ... other optional APIs
```

### Production Environment

Secrets are automatically injected by the deployment pipeline from GitHub Secrets.

## 📊 Monitoring and Verification

### Post-Deployment Checks

1. **Automated Verification**:
   - HTTP status check (200 OK)
   - Basic functionality test
   - SSL certificate validation

2. **Manual Verification**:
   - Test critical user flows
   - Verify API integrations
   - Check error monitoring
   - Validate analytics tracking

### Health Monitoring

- **Netlify Analytics**: Monitor traffic and performance
- **Browser Console**: Check for JavaScript errors
- **Network Tab**: Verify API calls are working
- **Lighthouse**: Performance and accessibility scores

## 🚨 Troubleshooting

### Common Issues

1. **Deployment Fails**:
   - Check GitHub Actions logs
   - Verify all required secrets are set
   - Ensure main branch is up to date

2. **API Calls Fail**:
   - Verify environment variables are set correctly
   - Check CORS configuration
   - Validate API endpoints are accessible

3. **Build Errors**:
   - Check Node.js version compatibility
   - Verify all dependencies are in package.json
   - Review build logs for specific errors

### Emergency Rollback

1. **Netlify Dashboard**:
   - Go to Deploys tab
   - Find previous working deployment
   - Click "Publish deploy"

2. **GitHub Revert**:
   ```bash
   git revert <commit-hash>
   git push origin main
   ```

## 📋 Pre-Launch Checklist

### Security
- [ ] All secrets stored securely (not in code)
- [ ] HTTPS enabled for production
- [ ] Security scans passing
- [ ] No hardcoded credentials
- [ ] Environment variables validated

### Functionality
- [ ] All features tested in staging
- [ ] API integrations working
- [ ] Error handling implemented
- [ ] Loading states implemented
- [ ] Mobile responsiveness verified

### Performance
- [ ] Build optimization enabled
- [ ] Images optimized
- [ ] Bundle size acceptable
- [ ] Core Web Vitals passing

### Monitoring
- [ ] Analytics configured
- [ ] Error tracking enabled
- [ ] Performance monitoring active
- [ ] Uptime monitoring configured

## 🔗 Useful Links

- [Netlify Documentation](https://docs.netlify.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review GitHub Actions logs
3. Check Netlify deploy logs
4. Verify environment configuration

---

**Remember**: Never commit secrets to your repository. Always use the secure deployment pipeline for production releases.