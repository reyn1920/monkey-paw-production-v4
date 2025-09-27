# TRAE.AI Application System Requirements

## Overview
This document outlines everything needed to run the TRAE.AI application on your computer and ensure it stays running at all times.

## System Requirements

### Minimum Hardware Requirements
- **CPU**: Intel i5 or Apple M1 (or equivalent)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free disk space minimum
- **Network**: Stable internet connection

### Software Requirements

#### Core Dependencies
1. **Python 3.8+** (Currently using Python 3.13.6)
   - Location: `/Users/thomasbrianreynolds/online production/venv/bin/python3`
   - Virtual environment activated

2. **Node.js 16+** (Currently using v22.17.1)
   - Location: `/Users/thomasbrianreynolds/.nvm/versions/node/v22.17.1/bin/node`
   - Required for Tailwind CSS build pipeline

3. **Package Managers**
   - pip (Python packages)
   - npm (Node.js packages)

#### Python Dependencies (from requirements.txt)
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Cryptography**: Security and encryption
- **HTTPx/AIOHttp**: HTTP clients
- **Pydantic**: Data validation
- **SQLite-utils**: Database management
- **Psutil**: System monitoring
- **Requests**: HTTP library
- **And 400+ other packages** (see requirements.txt)

#### Node.js Dependencies (from package.json)
- **Tailwind CSS**: CSS framework
- **@tailwindcss/forms**: Form styling
- **@tailwindcss/typography**: Typography plugin

## Application Architecture

### Main Components
1. **FastAPI Backend** (`main.py`)
   - Runs on port 8000
   - Handles API endpoints, WebSocket connections
   - Includes multiple routers for different features

2. **Static File Server**
   - Serves CSS, JS, and other static assets
   - Tailwind CSS build pipeline

3. **Database**
   - SQLite (built-in)
   - No external database server required

4. **Background Services**
   - Content processing
   - Social media integrations
   - Payment webhooks
   - Analytics

### Key Features
- **Pet Care Services**: Petfinder API integration
- **Social Media**: Multiple platform integrations
- **Payment Processing**: Stripe, PayPal support
- **Content Management**: Research and analysis tools
- **Real-time Updates**: WebSocket support
- **Authentication**: JWT-based auth system

## Startup Process

### Automated Startup (Recommended)
Use the provided startup system:

```bash
# Start the application
./start_app.sh start

# Check status
./start_app.sh status

# View logs
./start_app.sh logs -f

# Install as system service (auto-start on login)
./start_app.sh install-service
```

### Manual Startup
If you prefer manual control:

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
npm install

# 3. Build CSS
npm run build:css

# 4. Start application
python3 main.py
```

## System Optimization

### Applications to Close (for better performance)
The startup system will automatically close these resource-heavy applications:

**Media & Entertainment**
- Spotify, iTunes, Music, VLC
- Netflix, YouTube (browser tabs)

**Communication**
- Discord, Slack, Teams, Zoom, Skype

**Browsers** (except essential tabs)
- Chrome, Firefox, Safari, Opera

**Creative Software**
- Photoshop, Illustrator, Premiere Pro
- After Effects, Final Cut Pro

**Gaming**
- Steam, Epic Games Launcher, Battle.net

**Cloud Storage** (background sync)
- Dropbox, Google Drive, OneDrive

### Essential Applications (kept running)
- **System**: Finder, System Preferences, Activity Monitor
- **Development**: Terminal, iTerm, Trae, Sublime Text
- **Core Services**: Python, Node.js, uvicorn

## Monitoring & Health Checks

### Built-in Monitoring
The startup system includes:
- **Process monitoring**: Auto-restart if app crashes
- **Health checks**: HTTP endpoint monitoring
- **Resource monitoring**: CPU, memory, disk usage
- **Log management**: Centralized logging with rotation

### Health Check Endpoints
- **Main Health**: `http://localhost:8000/health`
- **System Metrics**: `http://localhost:8000/api/system/metrics`
- **Service Status**: `http://localhost:8000/api/services`
- **API Documentation**: `http://localhost:8000/docs`

### Log Files
- **Application Logs**: `startup_system.log`
- **Service Logs**: `service.log`
- **Error Logs**: `service.error.log`

## Network Configuration

### Required Ports
- **8000**: Main FastAPI application (required)
- **3000**: Frontend development server (optional)
- **5000**: Additional services (optional)

### Firewall Settings
Ensure these ports are open for localhost connections:
```bash
# Check port usage
lsof -i :8000

# Test connectivity
curl http://localhost:8000/health
```

## Environment Variables

The application uses environment variables for configuration. Key variables include:

- **API Keys**: Various service integrations
- **Database URLs**: Connection strings
- **Security Keys**: JWT secrets, encryption keys
- **Feature Flags**: Enable/disable features

*Note: Sensitive variables are managed through the SecretStore system*

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   ```

2. **Python Dependencies Missing**
   ```bash
   pip install -r requirements.txt
   ```

3. **Node Dependencies Missing**
   ```bash
   npm install
   ```

4. **Permission Errors**
   ```bash
   chmod +x start_app.sh
   ```

5. **Virtual Environment Issues**
   ```bash
   # Recreate virtual environment
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Log Analysis
```bash
# View recent logs
tail -f startup_system.log

# Search for errors
grep -i error startup_system.log

# Check system resources
top -o cpu
```

## Performance Optimization

### System Tuning
1. **Close unnecessary applications** (automated)
2. **Monitor resource usage** (built-in)
3. **Optimize database queries** (application-level)
4. **Enable caching** (Redis optional)

### Resource Limits
- **Memory**: Monitor for memory leaks
- **CPU**: Limit background processes
- **Disk**: Regular log rotation
- **Network**: Connection pooling

## Security Considerations

### Local Security
- Application runs on localhost only
- No external network exposure by default
- Secrets managed through encrypted storage

### Production Deployment
For production deployment, additional security measures are required:
- HTTPS/TLS certificates
- Firewall configuration
- Access control lists
- Security headers

## Backup & Recovery

### Important Files to Backup
- **Configuration**: `.env` files, `config/`
- **Database**: SQLite files
- **Logs**: For troubleshooting
- **Custom Code**: Any modifications

### Recovery Process
1. Restore backed up files
2. Reinstall dependencies
3. Run startup system
4. Verify health checks

## Support & Maintenance

### Regular Maintenance
- **Weekly**: Check logs for errors
- **Monthly**: Update dependencies
- **Quarterly**: System cleanup

### Getting Help
- Check logs first: `./start_app.sh logs`
- Verify system status: `./start_app.sh status`
- Review health endpoints
- Check system resources

## Quick Start Checklist

- [ ] System meets minimum requirements
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Node packages installed (`npm install`)
- [ ] CSS built (`npm run build:css`)
- [ ] Startup script executable (`chmod +x start_app.sh`)
- [ ] Application started (`./start_app.sh start`)
- [ ] Health check passes (`curl http://localhost:8000/health`)
- [ ] Optional: Install as service (`./start_app.sh install-service`)

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Compatibility**: macOS, Python 3.13.6, Node.js 22.17.1