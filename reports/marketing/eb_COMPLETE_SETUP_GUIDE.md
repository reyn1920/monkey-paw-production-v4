# Complete TRAE.AI Application Setup Guide

## 🚀 Everything You Need to Run This App

This guide provides a complete checklist of everything needed to run your TRAE.AI application on this computer and ensure it stays running at all times.

## ✅ Quick Start Checklist

### 1. System Requirements ✓
- **Python 3.8+** ✓ (Currently: Python 3.13.6)
- **Node.js 16+** ✓ (Currently: Node.js 22.17.1)
- **4GB RAM minimum** ✓
- **2GB free disk space** ✓
- **Stable internet connection** ✓
- **Ollama installed** ✓ (for AI features)
- **Google Chrome installed** ✓ (for web interface)

### 2. Dependencies Installed ✓
- **Python packages**: 400+ packages from requirements.txt ✓
- **Node.js packages**: Tailwind CSS and plugins ✓
- **Virtual environment**: Active and configured ✓
- **Ollama AI service**: Auto-installed if missing ✓

### 3. Application Files ✓
- **Main application**: `main.py` ✓
- **Startup system**: `startup_system.py` ✓
- **Shell wrapper**: `start_app.sh` ✓
- **System dashboard**: `system_dashboard.py` ✓
- **Configuration files**: All present ✓

## 🎯 One-Command Startup

### Start Everything
```bash
./start_app.sh start
```

### Check Status
```bash
./start_app.sh status
```

### View Logs
```bash
./start_app.sh logs -f
```

### Install as System Service (Auto-start)
```bash
./start_app.sh install-service
```

## 📊 System Management Dashboard

### Access the Dashboard
```bash
# Start the management dashboard
python3 system_dashboard.py

# Then open: http://localhost:9000
```

### Dashboard Features
- **Real-time monitoring**: CPU, memory, disk usage
- **Service control**: Start, stop, restart all services
- **AI service management**: Ollama control and monitoring
- **Browser management**: Chrome startup with essential tabs
- **Process monitoring**: View all related processes
- **Log viewing**: System, service, and error logs
- **Health checks**: Automated endpoint monitoring
- **Auto-refresh**: Updates every 5 seconds

### Service Management
- **Main Application**: Core TRAE.AI service
- **Ollama AI**: Local AI model service (auto-installs if missing)
- **Chrome Browser**: Opens with pre-configured tabs to avoid bot detection
- **System Dashboard**: This monitoring interface

## 🔧 System Optimization

### Applications Automatically Closed
The startup system will close these resource-heavy apps:

**Media & Entertainment**
- Spotify, iTunes, Music, VLC
- Netflix, YouTube browser tabs

**Communication**
- Discord, Slack, Teams, Zoom, Skype

**Browsers** (except managed Chrome)
- Firefox, Safari, Opera

**Creative Software**
- Photoshop, Illustrator, Premiere Pro
- After Effects, Final Cut Pro

**Gaming**
- Steam, Epic Games Launcher, Battle.net

**Cloud Storage** (background sync)
- Dropbox, Google Drive, OneDrive

### Essential Applications Kept Running
- **System**: Finder, System Preferences, Activity Monitor
- **Development**: Terminal, iTerm, Trae, Sublime Text
- **Core Services**: Python, Node.js, uvicorn
- **AI Services**: Ollama (auto-started)
- **Browser**: Google Chrome (managed with essential tabs)

### Smart Service Management
- **Ollama**: Automatically installs via Homebrew if not found
- **Chrome**: Opens with predefined tabs to avoid bot detection:
  - http://localhost:8000 (Main App)
  - http://localhost:9000 (Dashboard)
  - https://github.com (Code Repository)
  - https://netlify.com (Deployment)
  - https://openai.com (AI Services)
  - And more essential development sites

## 🔍 Monitoring & Health Checks

### Built-in Health Endpoints
- **Main Health**: http://localhost:8000/health
- **System Metrics**: http://localhost:8000/api/system/metrics
- **Service Status**: http://localhost:8000/api/services
- **API Documentation**: http://localhost:8000/docs

### Automated Monitoring Features
- **Process monitoring**: Auto-restart if app crashes
- **Health checks**: HTTP endpoint monitoring every 30 seconds
- **Resource monitoring**: CPU, memory, disk usage alerts
- **Log management**: Centralized logging with rotation
- **Port monitoring**: Ensures port 8000 is available

## 📝 Log Files
- **Application Logs**: `startup_system.log`
- **Service Logs**: `service.log`
- **Error Logs**: `service.error.log`
- **Dashboard Logs**: Available in web interface

## 🚨 Troubleshooting

### Common Issues & Solutions

1. **Port 8000 Already in Use**
   ```bash
   lsof -i :8000
   kill -9 <PID>
   ./start_app.sh start
   ```

2. **Ollama Service Issues**
   ```bash
   # Check if Ollama is installed
   which ollama

   # Install Ollama manually if needed
   brew install ollama

   # Start Ollama service
   ollama serve

   # Test Ollama
   ollama list
   ```

3. **Chrome Not Opening Properly**
   ```bash
   # Check if Chrome is installed
   open -a "Google Chrome" --version

   # Manually open Chrome with tabs
   open -a "Google Chrome"
   open -u "http://localhost:8000"

   # Reset Chrome if needed
   killall "Google Chrome"
   ./start_app.sh start
   ```

4. **Dependencies Missing**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

5. **Permission Errors**
   ```bash
   chmod +x start_app.sh
   chmod +x startup_system.py
   chmod +x system_dashboard.py
   ```

6. **Virtual Environment Issues**
   ```bash
   source venv/bin/activate
   ```

7. **Service Won't Start**
   ```bash
   ./start_app.sh stop
   ./start_app.sh start
   ```

## 🔄 Always Running Setup

### Option 1: System Service (Recommended)
```bash
# Install as macOS LaunchAgent
./start_app.sh install-service

# The app will now start automatically on login
# and restart if it crashes
```

### Option 2: Manual Monitoring
```bash
# Start with monitoring
python3 startup_system.py --monitor-only

# This will keep the app running and restart it if needed
```

### Option 3: Dashboard Monitoring
```bash
# Start the dashboard for visual monitoring
python3 system_dashboard.py

# Access at http://localhost:9000
# Use the web interface to control the service
```

## 📋 Complete File Structure

```/Users/thomasbrianreynolds/online production/├── main.py                           # Main FastAPI application
├── requirements.txt                  # Python dependencies
├── package.json                      # Node.js dependencies
├── startup_system.py                 # Automated startup system
├── start_app.sh                      # Shell wrapper script
├── system_dashboard.py               # Web management dashboard
├── SYSTEM_REQUIREMENTS.md            # Detailed requirements
├── COMPLETE_SETUP_GUIDE.md           # This guide
├── venv/# Python virtual environment
├── templates/# Dashboard HTML templates
├── static/# Static assets
├── logs/# Log files
└── config/# Configuration files
```

## 🎯 Success Verification

### Verify Everything is Working
1. **Start the application**:
   ```bash
   ./start_app.sh start
   ```

2. **Check all services**:
   ```bash
   ./start_app.sh status

   # Verify individual services
   ps aux | grep ollama
   ps aux | grep chrome
   ps aux | grep uvicorn
   ```

3. **Check health endpoint**:
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status": "healthy"}`

4. **Verify AI services**:
   ```bash
   # Test Ollama
   curl http://localhost:11434/api/tags

   # Check Ollama models
   ollama list
   ```

5. **Check browser setup**:
   - Chrome should be running with multiple tabs
   - Essential development sites should be open
   - No bot detection warnings

6. **Access main application**:
   Open: http://localhost:8000

7. **Access management dashboard**:
   ```bash
   python3 system_dashboard.py
   ```
   Open: http://localhost:9000

8. **Verify auto-restart**:
   ```bash
   # Kill the process and watch it restart
   pkill -f "python3 main.py"
   # Check logs to see restart
   ./start_app.sh logs -f
   ```

### System Resources
Check the dashboard at http://localhost:9000 for:
- CPU usage < 80%
- Memory usage < 80%
- All services showing green status:
  - ✅ Main Application
  - ✅ Ollama AI
  - ✅ Chrome Browser
  - ✅ System Dashboard

## 🔐 Security Notes

- Application runs on localhost only (127.0.0.1)
- No external network exposure by default
- Secrets managed through encrypted storage
- Log files contain no sensitive information
- Dashboard requires local access only

## 📞 Support Commands

### Quick Status Check
```bash
./start_app.sh status
```

### View Real-time Logs
```bash
./start_app.sh logs -f
```

### Restart Everything
```bash
./start_app.sh restart
```

### Emergency Stop
```bash
./start_app.sh stop
```

### System Information
```bash
python3 startup_system.py --help
```

## 🎉 You're All Set!

Your TRAE.AI application is now:
- ✅ **Fully configured** with all dependencies
- ✅ **Automatically starting** and staying running
- ✅ **Monitored** with health checks and auto-restart
- ✅ **Optimized** with unnecessary apps closed
- ✅ **Manageable** through web dashboard
- ✅ **Logged** with comprehensive monitoring

### Final Command to Start Everything:
```bash
# Start the main application
./start_app.sh start

# Install as system service (optional)
./start_app.sh install-service

# Start management dashboard (optional)
python3 system_dashboard.py
```

**Your TRAE.AI application will now run continuously and restart automatically if needed!**

---

*Last Updated: January 2025*
*Version: 1.0.0*
*Status: Production Ready* ✅
