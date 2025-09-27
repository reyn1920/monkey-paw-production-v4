# TRAE AI Production System - DO NOT DELETE LIST

## Critical Files and Directories to Preserve During Rebuild

⚠️ **WARNING**: The following files and directories contain critical data, configurations, and assets that MUST be preserved during the production rebuild process. Deleting these could result in permanent data loss, broken functionality, or security vulnerabilities.

## 🔒 **CRITICAL - NEVER DELETE**

### ⚠️ **OLLAMA AI SERVICE - PRODUCTION CRITICAL**
```
# Ollama service must remain operational for production
# Models represent significant download time and storage
.ollama/                    # Ollama configuration and models
ollama_integration.py       # Core integration code
ollama_integration_backup*  # Backup integration files
models/ollama/             # Model storage directory
```

### Environment and Configuration
```
.env.example
.env.production (if exists)
.env.staging (if exists)
.env.development (if exists)
.trae/
├── rules/
TRAE_RULES.md
.bandit
.base44rc.json
.editorconfig
.gitignore
.rule1_ignore
```

### Database and Data Storage
```
data/
├── .salt
├── backups/
├── ml_models/
databases/
backups/
├── database/
app/data/
├── .salt
backend/database/
├── conservative_research_schema.sql
├── db_singleton.py
├── chat_db.py
├── hypocrisy_db_manager.py
```

### Generated Assets and Content
```
assets/
├── generated/
├── audio/
├── avatars/
├── archive/
├── incoming/
├── releases/
content/
├── audio/
├── images/
├── models/
├── pdf/
├── scripts/
├── video/
output/
├── 3d/
├── audio/
├── content/
├── graphics/
├── voice/
outputs/
├── audio/
├── pdfs/
├── videos/
videos/
static/
├── avatars/
```

### AI Services and Models
```
.ollama/
├── models/
├── logs/
ollama_integration.py
ollama_integration_backup*.py
models/
├── ollama/
```

### Authentication and Security
```
app/auth.py
backend/security/
tokens/
constraints/
```

### Testing and Quality Assurance
```
tests/
├── artifacts/
├── data/
├── output/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── final_verification_results*.json
├── trae_verification_*.txt
├── trae_verification_*.json
test-results/
test_output/
test_outputs/
test_results/
pytest.ini
setup.cfg
```

### CI/CD and Deployment
```
.github/
├── workflows/
│   ├── ci-cd.yml
│   ├── ci.yml
│   ├── deploy.yml
│   ├── go-live.yml
│   ├── live-deployment.yml
│   ├── prod-health-watch.yml
│   ├── security.yml
│   └── sublime-integration.yml
Dockerfile
Dockerfile.test
docker-compose.yml (if exists)
Makefile
Procfile
netlify.toml
netlify/
```

### Infrastructure and Monitoring
```
k8s/
infra/
monitoring/
prometheus/
grafana/
haproxy/
nginx/
├── nginx.conf
ops/
├── watchdog.py
```

### Business Logic and Agents
```
agents/
backend/agents/
content-agent/
content_agent/
marketing-agent/
marketing_agent/
orchestrator/
revenue_tracker/
monetization/
```

### Documentation and Reports
```
README.md
DEPLOYMENT.md
DEBUG_REPORT.md
PRODUCTION_REBUILD_PLAN.md
DEEP_RESEARCH_IMPROVEMENTS.md
IMPLEMENTATION_GUIDE.md
docs/
reports/
seo_reports/
evidence/
```

### Configuration Files
```
package.json
vite.config.js
requirements.txt
constraints/
channels.json
schema.sql
init-db.sql
```

## 🟡 **PRESERVE WITH CAUTION**

### Cache and Temporary Files (Review Before Deletion)
```
cache/
queue/
snapshots/
idempotency/
venv_creative/
```

### Log Files (Archive Before Deletion)
```
server_logs.txt
run.pid
.pid-paste
```

### Development and Testing Outputs (Review Content)
```
final_test.json
test_final.json
auto_paste.html
index.html
```

## 🟢 **SAFE TO REPLACE/MODERNIZE**

### Application Code (Can be refactored/replaced)
```
app/main.py (replace with new FastAPI structure)
backend/app.py (modernize)
main.py
main_app.py
main_minimal.py
trae_ai_main.py
```

### Frontend Files (Replace with React/TypeScript)
```
frontend/ (current HTML files - replace with React)
public/
static/css/
static/js/
templates/
```

### Utility Scripts (Can be modernized)
```
utils/
shared_utils.py
scripts/
tools/
```

## 📋 **BACKUP STRATEGY**

### Before Any Deletion:
1. **Create Full System Backup**
   ```bash
   # Create timestamped backup
   tar -czf "trae_ai_backup_$(date +%Y%m%d_%H%M%S).tar.gz" \
     --exclude='node_modules' \
     --exclude='venv*' \
     --exclude='__pycache__' \
     --exclude='.git' \
     .
   ```

2. **Database Backup**
   ```bash
   # Backup all database files
   cp -r data/ "data_backup_$(date +%Y%m%d_%H%M%S)"
   cp -r databases/ "databases_backup_$(date +%Y%m%d_%H%M%S)"
   cp -r backend/database/ "backend_database_backup_$(date +%Y%m%d_%H%M%S)"
   ```

3. **Assets Backup**
   ```bash
   # Backup generated content
   cp -r assets/ "assets_backup_$(date +%Y%m%d_%H%M%S)"
   cp -r content/ "content_backup_$(date +%Y%m%d_%H%M%S)"
   cp -r output/ "output_backup_$(date +%Y%m%d_%H%M%S)"
   ```

## 🔄 **MIGRATION CHECKLIST**

### Data Migration Priority:
1. ✅ **User Data**: All user accounts, preferences, and generated content
2. ✅ **Configuration**: Environment variables, API keys, and settings
3. ✅ **Assets**: Generated videos, audio, images, and documents
4. ✅ **Analytics**: Performance data, usage metrics, and logs
5. ✅ **Security**: Authentication tokens, certificates, and access controls

### Verification Steps:
1. **Data Integrity Check**: Verify all critical data is accessible
2. **Configuration Validation**: Ensure all environment variables are properly set
3. **Asset Verification**: Confirm all generated content is preserved
4. **Security Audit**: Validate all security configurations are intact
5. **Functionality Test**: Run comprehensive tests to ensure system works

## 🚨 **EMERGENCY RECOVERY**

### If Critical Data is Accidentally Deleted:
1. **STOP ALL OPERATIONS** immediately
2. **Do not write any new data** to the affected storage
3. **Restore from most recent backup**
4. **Run data integrity checks**
5. **Document the incident** for future prevention

### Recovery Commands:
```bash
# Restore from backup
tar -xzf "trae_ai_backup_YYYYMMDD_HHMMSS.tar.gz"

# Verify restoration
python -m pytest tests/test_system_integrity.py

# Check data integrity
python backend/database/db_singleton.py --verify
```

## 📞 **SUPPORT CONTACTS**

- **System Administrator**: [Contact Information]
- **Database Administrator**: [Contact Information]
- **Security Team**: [Contact Information]
- **Backup Recovery**: [Contact Information]

---

**Last Updated**: $(date)
**Version**: 1.0
**Maintained By**: Production Team

⚠️ **REMEMBER**: When in doubt, DO NOT DELETE. Always create backups and consult with the team before removing any files or directories.
