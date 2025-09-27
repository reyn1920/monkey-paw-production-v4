#!/bin/bash

# Trae AI Zero-Cost Monitoring Stack Setup Script
# This script sets up a complete monitoring infrastructure using Prometheus, Grafana, and related tools

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MONITORING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$MONITORING_DIR")"
DOCKER_COMPOSE_FILE="$MONITORING_DIR/docker-compose.monitoring.yml"
ENV_FILE="$MONITORING_DIR/.env"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."

    local missing_deps=()

    if ! command_exists docker; then
        missing_deps+=("docker")
    fi

    if ! command_exists docker-compose; then
        missing_deps+=("docker-compose")
    fi

    if ! command_exists curl; then
        missing_deps+=("curl")
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        print_status "Please install the missing dependencies and run this script again."

        print_status "Installation commands:"
        echo "  macOS: brew install docker docker-compose curl"
        echo "  Ubuntu: sudo apt-get install docker.io docker-compose curl"
        echo "  CentOS: sudo yum install docker docker-compose curl"

        exit 1
    fi

    # Check if Docker daemon is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker daemon is not running. Please start Docker and try again."
        exit 1
    fi

    print_success "All prerequisites are satisfied."
}

# Function to create environment file
create_env_file() {
    print_status "Creating environment configuration..."

    if [ ! -f "$ENV_FILE" ]; then
        cat > "$ENV_FILE" << EOF
# Trae AI Monitoring Stack Environment Configuration

# Grafana Configuration
GF_SECURITY_ADMIN_PASSWORD=admin123
GF_USERS_ALLOW_SIGN_UP=false
GF_SECURITY_ALLOW_EMBEDDING=true

# Prometheus Configuration
PROMETHEUS_RETENTION_TIME=15d
PROMETHEUS_STORAGE_PATH=/prometheus

# Alertmanager Configuration
SMTP_SMARTHOST=localhost:587
SMTP_FROM=alerts@trae-ai.com
SMTP_AUTH_USERNAME=alerts@trae-ai.com
SMTP_AUTH_PASSWORD=your-email-password
SLACK_API_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK

# Application Configuration
APP_PORT=8000
REDIS_URL=redis://redis:6379
LOG_LEVEL=INFO
ENVIRONMENT=production

# Security Configuration
SECRET_KEY=${SECRET_KEY:-$(openssl rand -hex 32)}
JWT_SECRET=${JWT_SECRET:-$(openssl rand -hex 32)}

# External Service URLs (for blackbox monitoring)
EXTERNAL_URLS=https://api.publicapis.org,https://rapidapi.com,https://github.com

# Backup Configuration
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30
BACKUP_S3_BUCKET=trae-ai-monitoring-backups

EOF
        print_success "Environment file created at $ENV_FILE"
        print_warning "Please update the environment variables in $ENV_FILE with your actual values."
    else
        print_status "Environment file already exists at $ENV_FILE"
    fi
}

# Function to create additional configuration files
create_additional_configs() {
    print_status "Creating additional configuration files..."

    # Create Grafana provisioning directory
    mkdir -p "$MONITORING_DIR/grafana-provisioning/datasources"
    mkdir -p "$MONITORING_DIR/grafana-provisioning/dashboards"

    # Create Grafana datasource configuration
    cat > "$MONITORING_DIR/grafana-provisioning/datasources/prometheus.yml" << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: true

  - name: Jaeger
    type: jaeger
    access: proxy
    url: http://jaeger:16686
    editable: true
EOF

    # Create Grafana dashboard provisioning
    cat > "$MONITORING_DIR/grafana-provisioning/dashboards/dashboard.yml" << EOF
apiVersion: 1

providers:
  - name: 'Trae AI Dashboards'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path:/var/lib/grafana/dashboards
EOF

    # Create blackbox exporter configuration
    cat > "$MONITORING_DIR/blackbox.yml" << EOF
modules:
  http_2xx:
    prober: http
    timeout: 5s
    http:
      valid_http_versions: ["HTTP/1.1", "HTTP/2.0"]
      valid_status_codes: []
      method: GET
      follow_redirects: true
      fail_if_ssl: false
      fail_if_not_ssl: false

  http_post_2xx:
    prober: http
    timeout: 5s
    http:
      method: POST
      headers:
        Content-Type: application/json
      body: '{"test": "data"}'

  tcp_connect:
    prober: tcp
    timeout: 5s

  icmp:
    prober: icmp
    timeout: 5s
EOF

    # Create Loki configuration
    cat > "$MONITORING_DIR/loki-config.yml" << EOF
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

common:
  path_prefix:/loki
  storage:
    filesystem:
      chunks_directory:/loki/chunks
      rules_directory:/loki/rules
  replication_factor: 1
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: inmemory

query_range:
  results_cache:
    cache:
      embedded_cache:
        enabled: true
        max_size_mb: 100

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

ruler:
  alertmanager_url: http://alertmanager:9093
EOF

    # Create Promtail configuration
    cat > "$MONITORING_DIR/promtail-config.yml" << EOF
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename:/tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__:/var/log/*log

  - job_name: containers
    static_configs:
      - targets:
          - localhost
        labels:
          job: containerlogs
          __path__:/var/lib/docker/containers/*/*log

  - job_name: trae-app
    static_configs:
      - targets:
          - localhost
        labels:
          job: trae-app
          __path__:/app/logs/*.log
EOF

    # Create Nginx configuration
    cat > "$MONITORING_DIR/nginx.conf" << EOF
events {
    worker_connections 1024;
}

http {
    upstream grafana {
        server grafana:3000;
    }

    upstream prometheus {
        server prometheus:9090;
    }

    upstream app {
        server trae-app:8000;
    }

    server {
        listen 80;
        server_name localhost;

        # Enable nginx status for monitoring
        location/nginx_status {
            stub_status on;
            access_log off;
            allow 127.0.0.1;
            allow 172.0.0.0/8;
            deny all;
        }

        # Health check endpoint
        location/health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # Grafana
        location/grafana/{
            proxy_pass http://grafana/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }

        # Prometheus
        location/prometheus/{
            proxy_pass http://prometheus/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }

        # Application
        location/{
            proxy_pass http://app;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF

    print_success "Additional configuration files created."
}

# Function to create SSL certificates (self-signed for development)
create_ssl_certificates() {
    print_status "Creating SSL certificates..."

    mkdir -p "$MONITORING_DIR/ssl"

    if [ ! -f "$MONITORING_DIR/ssl/nginx.crt" ]; then
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout "$MONITORING_DIR/ssl/nginx.key" \
            -out "$MONITORING_DIR/ssl/nginx.crt" \
            -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" \
            2>/dev/null || print_warning "OpenSSL not available, skipping SSL certificate generation."

        if [ -f "$MONITORING_DIR/ssl/nginx.crt" ]; then
            print_success "SSL certificates created."
        fi
    else
        print_status "SSL certificates already exist."
    fi
}

# Function to pull Docker images
pull_docker_images() {
    print_status "Pulling Docker images..."

    local images=(
        "prom/prometheus:latest"
        "grafana/grafana:latest"
        "prom/node-exporter:latest"
        "prom/alertmanager:latest"
        "prom/blackbox-exporter:latest"
        "gcr.io/cadvisor/cadvisor:latest"
        "redis:7-alpine"
        "oliver006/redis_exporter:latest"
        "nginx:alpine"
        "nginx/nginx-prometheus-exporter:latest"
        "grafana/loki:latest"
        "grafana/promtail:latest"
        "jaegertracing/all-in-one:latest"
    )

    for image in "${images[@]}"; do
        print_status "Pulling $image..."
        docker pull "$image" || print_warning "Failed to pull $image"
    done

    print_success "Docker images pulled."
}

# Function to start monitoring stack
start_monitoring_stack() {
    print_status "Starting monitoring stack..."

    cd "$MONITORING_DIR"

    # Create networks if they don't exist
    docker network create trae-monitoring 2>/dev/null || true
    docker network create trae-app 2>/dev/null || true

    # Start the stack
    docker-compose -f "$DOCKER_COMPOSE_FILE" up -d

    print_success "Monitoring stack started."
}

# Function to wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."

    local services=(
        "http://localhost:9090/-/ready:Prometheus"
        "http://localhost:3000/api/health:Grafana"
        "http://localhost:9093/-/ready:Alertmanager"
        "http://localhost:6379:Redis"
    )

    for service in "${services[@]}"; do
        local url="${service%:*}"
        local name="${service#*:}"

        print_status "Waiting for $name to be ready..."

        local retries=30
        local count=0

        while [ $count -lt $retries ]; do
            if curl -s "$url" >/dev/null 2>&1; then
                print_success "$name is ready."
                break
            fi

            count=$((count + 1))
            sleep 2
        done

        if [ $count -eq $retries ]; then
            print_warning "$name did not become ready within expected time."
        fi
    done
}

# Function to import Grafana dashboard
import_grafana_dashboard() {
    print_status "Importing Grafana dashboard..."

    # Wait a bit more for Grafana to be fully ready
    sleep 10

    # Import the dashboard via API
    curl -X POST \
        -H "Content-Type: application/json" \
        -d @"$MONITORING_DIR/grafana_dashboard.json" \
        "http://admin:admin123@localhost:3000/api/dashboards/db" \
        2>/dev/null || print_warning "Failed to import Grafana dashboard via API. You can import it manually."

    print_success "Grafana dashboard import attempted."
}

# Function to display access information
display_access_info() {
    print_success "Monitoring stack is now running!"
    echo
    echo "Access URLs:"
    echo "  📊 Grafana Dashboard: http://localhost:3000 (admin/admin123)"
    echo "  📈 Prometheus: http://localhost:9090"
    echo "  🚨 Alertmanager: http://localhost:9093"
    echo "  🖥️  Node Exporter: http://localhost:9100"
    echo "  📦 cAdvisor: http://localhost:8080"
    echo "  🔍 Jaeger Tracing: http://localhost:16686"
    echo "  📝 Loki Logs: http://localhost:3100"
    echo "  🌐 Application: http://localhost:8000"
    echo "  ⚡ Redis: localhost:6379"
    echo
    echo "Useful Commands:"
    echo "  📋 View logs: docker-compose -f $DOCKER_COMPOSE_FILE logs -f [service]"
    echo "  📊 Check status: docker-compose -f $DOCKER_COMPOSE_FILE ps"
    echo "  🛑 Stop stack: docker-compose -f $DOCKER_COMPOSE_FILE down"
    echo "  🔄 Restart service: docker-compose -f $DOCKER_COMPOSE_FILE restart [service]"
    echo
    echo "Configuration Files:"
    echo "  🔧 Environment: $ENV_FILE"
    echo "  🐳 Docker Compose: $DOCKER_COMPOSE_FILE"
    echo "  📊 Prometheus Config: $MONITORING_DIR/prometheus.yml"
    echo "  🚨 Alert Rules: $MONITORING_DIR/alert_rules.yml"
    echo
}

# Function to run health checks
run_health_checks() {
    print_status "Running health checks..."

    local failed_checks=()

    # Check if containers are running
    local containers=(
        "trae-prometheus"
        "trae-grafana"
        "trae-alertmanager"
        "trae-node-exporter"
        "trae-redis"
    )

    for container in "${containers[@]}"; do
        if ! docker ps --format "table {{.Names}}" | grep -q "$container"; then
            failed_checks+=("Container $container is not running")
        fi
    done

    # Check service endpoints
    local endpoints=(
        "http://localhost:9090/-/ready:Prometheus"
        "http://localhost:3000/api/health:Grafana"
        "http://localhost:9093/-/ready:Alertmanager"
    )

    for endpoint in "${endpoints[@]}"; do
        local url="${endpoint%:*}"
        local name="${endpoint#*:}"

        if ! curl -s "$url" >/dev/null 2>&1; then
            failed_checks+=("$name endpoint is not responding")
        fi
    done

    if [ ${#failed_checks[@]} -eq 0 ]; then
        print_success "All health checks passed."
    else
        print_warning "Some health checks failed:"
        for check in "${failed_checks[@]}"; do
            echo "  ❌ $check"
        done
    fi
}

# Function to create backup script
create_backup_script() {
    print_status "Creating backup script..."

    cat > "$MONITORING_DIR/backup_monitoring.sh" << 'EOF'
#!/bin/bash

# Backup script for Trae AI monitoring stack

set -euo pipefail

BACKUP_DIR="/tmp/trae-monitoring-backup-$(date +%Y%m%d-%H%M%S)"
MONITORING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Creating backup directory: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Backup Prometheus data
echo "Backing up Prometheus data..."
docker run --rm -v trae-prometheus-data:/data -v "$BACKUP_DIR":/backup alpine tar czf/backup/prometheus-data.tar.gz -C/data .

# Backup Grafana data
echo "Backing up Grafana data..."
docker run --rm -v trae-grafana-data:/data -v "$BACKUP_DIR":/backup alpine tar czf/backup/grafana-data.tar.gz -C/data .

# Backup configuration files
echo "Backing up configuration files..."
cp -r "$MONITORING_DIR"/*.yml "$BACKUP_DIR/"
cp -r "$MONITORING_DIR"/*.yaml "$BACKUP_DIR/" 2>/dev/null || true
cp -r "$MONITORING_DIR"/*.json "$BACKUP_DIR/" 2>/dev/null || true
cp "$MONITORING_DIR/.env" "$BACKUP_DIR/" 2>/dev/null || true

# Create archive
echo "Creating backup archive..."
tar czf "$MONITORING_DIR/monitoring-backup-$(date +%Y%m%d-%H%M%S).tar.gz" -C "$(dirname "$BACKUP_DIR")" "$(basename "$BACKUP_DIR")"

# Cleanup
rm -rf "$BACKUP_DIR"

echo "Backup completed successfully."
EOF

    chmod +x "$MONITORING_DIR/backup_monitoring.sh"
    print_success "Backup script created at $MONITORING_DIR/backup_monitoring.sh"
}

# Main execution
main() {
    echo "🚀 Trae AI Zero-Cost Monitoring Stack Setup"
    echo "==========================================="
    echo

    check_prerequisites
    create_env_file
    create_additional_configs
    create_ssl_certificates
    pull_docker_images
    start_monitoring_stack
    wait_for_services
    import_grafana_dashboard
    run_health_checks
    create_backup_script

    echo
    display_access_info

    print_success "Setup completed successfully! 🎉"
}

# Handle script arguments
case "${1:-}" in
    "start")
        start_monitoring_stack
        ;;
    "stop")
        print_status "Stopping monitoring stack..."
        docker-compose -f "$DOCKER_COMPOSE_FILE" down
        print_success "Monitoring stack stopped."
        ;;
    "restart")
        print_status "Restarting monitoring stack..."
        docker-compose -f "$DOCKER_COMPOSE_FILE" restart
        print_success "Monitoring stack restarted."
        ;;
    "status")
        docker-compose -f "$DOCKER_COMPOSE_FILE" ps
        ;;
    "logs")
        docker-compose -f "$DOCKER_COMPOSE_FILE" logs -f "${2:-}"
        ;;
    "health")
        run_health_checks
        ;;
    "backup")
        "$MONITORING_DIR/backup_monitoring.sh"
        ;;
    "clean")
        print_warning "This will remove all monitoring data. Are you sure? (y/N)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            docker-compose -f "$DOCKER_COMPOSE_FILE" down -v
            docker system prune -f
            print_success "Monitoring stack cleaned."
        fi
        ;;
    "help"|"--help"|"")
        if [ "${1:-}" = "" ]; then
            main
        else
            echo "Trae AI Monitoring Stack Management"
            echo "Usage: $0 [command]"
            echo
            echo "Commands:"
            echo "  start     Start the monitoring stack"
            echo "  stop      Stop the monitoring stack"
            echo "  restart   Restart the monitoring stack"
            echo "  status    Show status of all services"
            echo "  logs      Show logs (optionally for specific service)"
            echo "  health    Run health checks"
            echo "  backup    Create backup of monitoring data"
            echo "  clean     Remove all monitoring data (destructive)"
            echo "  help      Show this help message"
            echo
        fi
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Run '$0 help' for usage information."
        exit 1
        ;;
esac
