#!/bin/bash

# TRAE AI Production Monitoring Setup Script
# This script sets up the complete monitoring and alerting infrastructure
# including Prometheus, Grafana, AlertManager, and scaling components

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MONITORING_NAMESPACE="monitoring"
APP_NAMESPACE="trae-ai"
GRAFANA_ADMIN_PASSWORD="${GRAFANA_ADMIN_PASSWORD}"
if [ -z "$GRAFANA_ADMIN_PASSWORD" ]; then
    echo "Error: GRAFANA_ADMIN_PASSWORD environment variable is required"
    exit 1
fi
ALERT_MANAGER_WEBHOOK_URL="${ALERT_MANAGER_WEBHOOK_URL:-https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK}"

echo -e "${BLUE}🚀 TRAE AI Monitoring Setup${NC}"
echo -e "${BLUE}================================${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for deployment
wait_for_deployment() {
    local namespace=$1
    local deployment=$2
    local timeout=${3:-300}

    echo -e "${YELLOW}⏳ Waiting for $deployment to be ready...${NC}"
    kubectl wait --for=condition=available --timeout=${timeout}s deployment/$deployment -n $namespace
    echo -e "${GREEN}✅ $deployment is ready${NC}"
}

# Function to create namespace if it doesn't exist
create_namespace() {
    local namespace=$1
    if ! kubectl get namespace $namespace >/dev/null 2>&1; then
        echo -e "${YELLOW}📁 Creating namespace: $namespace${NC}"
        kubectl create namespace $namespace
    else
        echo -e "${GREEN}✅ Namespace $namespace already exists${NC}"
    fi
}

# Check prerequisites
echo -e "${BLUE}🔍 Checking prerequisites...${NC}"

if ! command_exists kubectl; then
    echo -e "${RED}❌ kubectl is not installed. Please install kubectl first.${NC}"
    exit 1
fi

if ! command_exists helm; then
    echo -e "${RED}❌ Helm is not installed. Please install Helm first.${NC}"
    exit 1
fi

if ! command_exists docker; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites are installed${NC}"

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ Please run this script from the project root directory${NC}"
    exit 1
fi

# Create necessary directories
echo -e "${BLUE}📁 Creating monitoring directories...${NC}"
mkdir -p monitoring/prometheus
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/alertmanager
mkdir -p k8s/monitoring
mkdir -p logs

# Setup Kubernetes monitoring (if kubectl is configured)
if kubectl cluster-info >/dev/null 2>&1; then
    echo -e "${BLUE}☸️  Setting up Kubernetes monitoring...${NC}"

    # Create namespaces
    create_namespace $MONITORING_NAMESPACE
    create_namespace $APP_NAMESPACE

    # Add Prometheus Helm repository
    echo -e "${YELLOW}📦 Adding Prometheus Helm repository...${NC}"
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo add grafana https://grafana.github.io/helm-charts
    helm repo update

    # Install Prometheus Stack
    echo -e "${YELLOW}🔧 Installing Prometheus Stack...${NC}"
    helm upgrade --install prometheus-stack prometheus-community/kube-prometheus-stack \
        --namespace $MONITORING_NAMESPACE \
        --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
        --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \
        --set prometheus.prometheusSpec.ruleSelectorNilUsesHelmValues=false \
        --set prometheus.prometheusSpec.retention=30d \
        --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi \
        --set grafana.adminPassword=$GRAFANA_ADMIN_PASSWORD \
        --set grafana.persistence.enabled=true \
        --set grafana.persistence.size=10Gi \
        --set alertmanager.alertmanagerSpec.storage.volumeClaimTemplate.spec.resources.requests.storage=10Gi

    # Wait for deployments
    wait_for_deployment $MONITORING_NAMESPACE prometheus-stack-kube-prom-operator
    wait_for_deployment $MONITORING_NAMESPACE prometheus-stack-grafana

    # Apply custom alert rules
    echo -e "${YELLOW}📋 Applying custom alert rules...${NC}"
    kubectl create configmap prometheus-alert-rules \
        --from-file=monitoring/alert-rules.yml \
        --namespace=$MONITORING_NAMESPACE \
        --dry-run=client -o yaml | kubectl apply -f -

    # Apply HPA configuration
    echo -e "${YELLOW}⚖️  Applying HPA configuration...${NC}"
    kubectl apply -f k8s/hpa-config.yaml -n $APP_NAMESPACE

    # Create Grafana dashboard ConfigMap
    echo -e "${YELLOW}📊 Creating Grafana dashboard...${NC}"
    kubectl create configmap grafana-dashboard-trae-ai \
        --from-file=monitoring/grafana_dashboards.json \
        --namespace=$MONITORING_NAMESPACE \
        --dry-run=client -o yaml | kubectl apply -f -

    # Label the ConfigMap for Grafana to pick it up
    kubectl label configmap grafana-dashboard-trae-ai \
        grafana_dashboard=1 \
        --namespace=$MONITORING_NAMESPACE

    echo -e "${GREEN}✅ Kubernetes monitoring setup complete${NC}"
else
    echo -e "${YELLOW}⚠️  Kubernetes cluster not accessible, skipping K8s setup${NC}"
fi

# Setup Docker Compose monitoring
echo -e "${BLUE}🐳 Setting up Docker Compose monitoring...${NC}"

# Create Prometheus configuration
cat > monitoring/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert-rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'trae-ai-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  - job_name: 'trae-ai-api'
    static_configs:
      - targets: ['api:3000']
    metrics_path: '/metrics'

  - job_name: 'trae-ai-content-agent'
    static_configs:
      - targets: ['content-agent:5000']
    metrics_path: '/metrics'

  - job_name: 'trae-ai-marketing-agent'
    static_configs:
      - targets: ['marketing-agent:5001']
    metrics_path: '/metrics'

  - job_name: 'haproxy'
    static_configs:
      - targets: ['load-balancer:8404']
    metrics_path: '/metrics'
EOF

# Copy alert rules to Prometheus directory
cp monitoring/alert-rules.yml monitoring/prometheus/# Copy AlertManager configuration
cp monitoring/alertmanager.yml monitoring/alertmanager/# Create Grafana provisioning configuration
mkdir -p monitoring/grafana/provisioning/datasources
mkdir -p monitoring/grafana/provisioning/dashboards

cat > monitoring/grafana/provisioning/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
EOF

cat > monitoring/grafana/provisioning/dashboards/dashboard.yml << EOF
apiVersion: 1

providers:
  - name: 'TRAE AI Dashboards'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path:/var/lib/grafana/dashboards
EOF

# Copy dashboard to Grafana directory
cp monitoring/grafana_dashboards.json monitoring/grafana/dashboards/# Create environment file for monitoring
cat > .env.monitoring << EOF
# Monitoring Configuration
GRAFANA_ADMIN_PASSWORD=$GRAFANA_ADMIN_PASSWORD
PROMETHEUS_RETENTION=30d
ALERT_MANAGER_WEBHOOK_URL=$ALERT_MANAGER_WEBHOOK_URL

# Scaling Configuration
SCALING_ENABLED=true
SCALING_CHECK_INTERVAL=30
SCALING_COOLDOWN=300

# Notification Configuration
SLACK_WEBHOOK_URL=$ALERT_MANAGER_WEBHOOK_URL
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_FROM=alerts@trae.ai
EMAIL_TO=admin@trae.ai
EOF

echo -e "${GREEN}✅ Docker Compose monitoring setup complete${NC}"

# Setup scaling policies
echo -e "${BLUE}⚖️  Setting up scaling policies...${NC}"

# Make scaling policies executable
if [ -f "monitoring/scaling-policies.py" ]; then
    chmod +x monitoring/scaling-policies.py
fi

# Create scaling service script
cat > scripts/start-scaling-service.sh << 'EOF'
#!/bin/bash

# Start the intelligent scaling service
echo "🚀 Starting TRAE AI Intelligent Scaling Service..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install required packages
pip install -q prometheus-client requests numpy scikit-learn pyyaml

# Start the scaling service
cd monitoring
python scaling-policies.py
EOF

chmod +x scripts/start-scaling-service.sh

echo -e "${GREEN}✅ Scaling policies setup complete${NC}"

# Create monitoring startup script
cat > scripts/start-monitoring.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting TRAE AI Monitoring Stack..."

# Load monitoring environment
if [ -f ".env.monitoring" ]; then
    source .env.monitoring
fi

# Start monitoring services
echo "📊 Starting monitoring services..."
docker-compose -f docker-compose.scaling.yml up -d prometheus grafana alertmanager node-exporter cadvisor

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
curl -f http://localhost:9090/-/healthy && echo "✅ Prometheus is healthy"
curl -f http://localhost:3000/api/health && echo "✅ Grafana is healthy"
curl -f http://localhost:9093/-/healthy && echo "✅ AlertManager is healthy"

echo "🎉 Monitoring stack is ready!"
echo "📊 Grafana: http://localhost:3000 (admin/admin123!@#)"
echo "🔍 Prometheus: http://localhost:9090"
echo "🚨 AlertManager: http://localhost:9093"
EOF

chmod +x scripts/start-monitoring.sh

# Create monitoring test script
cat > scripts/test-monitoring.sh << 'EOF'
#!/bin/bash

echo "🧪 Testing TRAE AI Monitoring Setup..."

# Test Prometheus targets
echo "🎯 Testing Prometheus targets..."
prometheus_targets=$(curl -s http://localhost:9090/api/v1/targets | jq -r '.data.activeTargets[] | select(.health == "up") | .labels.job' | sort | uniq)
echo "Active targets: $prometheus_targets"

# Test Grafana API
echo "📊 Testing Grafana API..."
grafana_health=$(curl -s http://localhost:3000/api/health | jq -r '.database')
echo "Grafana database status: $grafana_health"

# Test AlertManager
echo "🚨 Testing AlertManager..."
alertmanager_status=$(curl -s http://localhost:9093/api/v1/status | jq -r '.status')
echo "AlertManager status: $alertmanager_status"

# Test scaling service
echo "⚖️  Testing scaling service..."
if pgrep -f "scaling-policies.py" >/dev/null; then
    echo "✅ Scaling service is running"
else
    echo "❌ Scaling service is not running"
fi

# Generate test metrics
echo "📈 Generating test metrics..."
curl -X POST http://localhost:8000/metrics/test || echo "⚠️  Test metrics endpoint not available"

echo "🎉 Monitoring test complete!"
EOF

chmod +x scripts/test-monitoring.sh

# Create cleanup script
cat > scripts/cleanup-monitoring.sh << 'EOF'
#!/bin/bash

echo "🧹 Cleaning up TRAE AI Monitoring..."

# Stop Docker services
echo "🛑 Stopping monitoring services..."
docker-compose -f docker-compose.scaling.yml down

# Clean up Kubernetes resources (if applicable)
if kubectl cluster-info >/dev/null 2>&1; then
    echo "☸️  Cleaning up Kubernetes resources..."
    kubectl delete namespace monitoring --ignore-not-found=true
    kubectl delete namespace trae-ai --ignore-not-found=true
fi

# Remove monitoring data (optional)
read -p "Do you want to remove monitoring data? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing monitoring data..."
    docker volume rm $(docker volume ls -q | grep -E '(prometheus|grafana|alertmanager)') 2>/dev/null || true
fi

echo "✅ Cleanup complete!"
EOF

chmod +x scripts/cleanup-monitoring.sh

# Final setup steps
echo -e "${BLUE}🔧 Final setup steps...${NC}"

# Create logs directory
mkdir -p logs/monitoring

# Set proper permissions
chmod -R 755 monitoring/chmod -R 755 scripts/# Create monitoring documentation
cat > monitoring/README.md << 'EOF'
# TRAE AI Monitoring Setup

This directory contains the complete monitoring and alerting infrastructure for the TRAE AI application.

## Components

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **AlertManager**: Alert routing and notifications
- **Node Exporter**: System metrics
- **cAdvisor**: Container metrics
- **Scaling Policies**: Intelligent auto-scaling

## Quick Start

1. Start monitoring stack:
   ```bash
   ./scripts/start-monitoring.sh
   ```

2. Test the setup:
   ```bash
   ./scripts/test-monitoring.sh
   ```

3. Start scaling service:
   ```bash
   ./scripts/start-scaling-service.sh
   ```

## Access URLs

- Grafana: http://localhost:3000 (admin/admin123!@#)
- Prometheus: http://localhost:9090
- AlertManager: http://localhost:9093

## Configuration Files

- `prometheus.yml`: Prometheus configuration
- `alert-rules.yml`: Alert rules
- `alertmanager.yml`: AlertManager configuration
- `grafana_dashboards.json`: Grafana dashboards
- `scaling-policies.py`: Intelligent scaling logic

## Scaling Rules

Scaling rules are defined in `config/scaling-rules.yaml` and include:

- CPU-based scaling
- Memory-based scaling
- Request rate scaling
- Custom metric scaling
- Predictive scaling

## Alerts

Alert rules cover:

- System resource usage
- Application performance
- Service health
- Security events
- Business metrics
- Scaling events

## Troubleshooting

1. Check service logs:
   ```bash
   docker-compose -f docker-compose.scaling.yml logs [service-name]
   ```

2. Verify Prometheus targets:
   ```bash
   curl http://localhost:9090/api/v1/targets
   ```

3. Test AlertManager:
   ```bash
   curl http://localhost:9093/api/v1/status
   ```

## Cleanup

To remove all monitoring components:
```bash
./scripts/cleanup-monitoring.sh
```
EOF

echo -e "${GREEN}🎉 TRAE AI Monitoring Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo -e "${YELLOW}1. Review and customize configuration files${NC}"
echo -e "${YELLOW}2. Update Slack webhook URL in .env.monitoring${NC}"
echo -e "${YELLOW}3. Run: ./scripts/start-monitoring.sh${NC}"
echo -e "${YELLOW}4. Run: ./scripts/test-monitoring.sh${NC}"
echo -e "${YELLOW}5. Access Grafana at http://localhost:3000${NC}"
echo -e "${GREEN}================================${NC}"

echo -e "${BLUE}📋 Configuration Summary:${NC}"
echo -e "${BLUE}• Prometheus: Metrics collection and alerting${NC}"
echo -e "${BLUE}• Grafana: Dashboards and visualization${NC}"
echo -e "${BLUE}• AlertManager: Alert routing and notifications${NC}"
echo -e "${BLUE}• HPA: Kubernetes horizontal pod autoscaling${NC}"
echo -e "${BLUE}• Scaling Policies: Intelligent auto-scaling${NC}"
echo -e "${BLUE}• Load Balancer: HAProxy with health checks${NC}"
echo -e "${BLUE}• Security: Rate limiting and DDoS protection${NC}"

echo -e "${GREEN}✨ Your TRAE AI application is now ready for production monitoring and scaling!${NC}"
