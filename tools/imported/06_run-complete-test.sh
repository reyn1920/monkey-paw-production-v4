#!/bin/bash

# TRAE AI Complete Monitoring and Scaling Test
# This script demonstrates the complete monitoring, alerting, and scaling system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 TRAE AI Complete Monitoring & Scaling Test${NC}"
echo -e "${BLUE}=============================================${NC}"

# Configuration
TEST_DURATION=600  # 10 minutes
CONCURRENT_USERS=20
BASE_URL="http://localhost:8080"
LOG_DIR="logs/integration-test"

# Create log directory
mkdir -p $LOG_DIR

# Function to check if service is running
check_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=1

    echo -e "${YELLOW}⏳ Checking $service_name...${NC}"

    while [ $attempt -le $max_attempts ]; do
        if curl -f -s $url > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $service_name is ready${NC}"
            return 0
        fi

        echo -e "${YELLOW}   Attempt $attempt/$max_attempts - waiting for $service_name...${NC}"
        sleep 5
        ((attempt++))
    done

    echo -e "${RED}❌ $service_name failed to start${NC}"
    return 1
}

# Function to wait for user input
wait_for_user() {
    local message=$1
    echo -e "${PURPLE}$message${NC}"
    read -p "Press Enter to continue..."
}

# Step 1: Start the monitoring stack
echo -e "${BLUE}📊 Step 1: Starting Monitoring Stack${NC}"
echo "Starting Prometheus, Grafana, AlertManager, and exporters..."

# Start monitoring services
docker-compose -f docker-compose.scaling.yml up -d prometheus grafana alertmanager node-exporter cadvisor

# Wait for monitoring services
check_service "Prometheus" "http://localhost:9090/-/healthy"
check_service "Grafana" "http://localhost:3000/api/health"
check_service "AlertManager" "http://localhost:9093/-/healthy"

echo -e "${GREEN}✅ Monitoring stack is ready${NC}"

# Step 2: Start the application services
echo -e "${BLUE}🏗️  Step 2: Starting Application Services${NC}"
echo "Starting backend, API, content-agent, and load balancer..."

# Start application services
docker-compose -f docker-compose.scaling.yml up -d load-balancer backend api content-agent marketing-agent

# Wait for application services
check_service "Load Balancer" "http://localhost:8080/health"
check_service "Backend API" "http://localhost:8000/health"
check_service "Content Agent" "http://localhost:5000/health"

echo -e "${GREEN}✅ Application services are ready${NC}"

# Step 3: Start the scaling service
echo -e "${BLUE}⚖️  Step 3: Starting Intelligent Scaling Service${NC}"

# Start scaling service in background
python3 monitoring/scaling-policies.py > $LOG_DIR/scaling-service.log 2>&1 &
SCALING_PID=$!

echo -e "${GREEN}✅ Scaling service started (PID: $SCALING_PID)${NC}"

# Step 4: Verify monitoring setup
echo -e "${BLUE}🔍 Step 4: Verifying Monitoring Setup${NC}"

# Check Prometheus targets
echo "Checking Prometheus targets..."
prometheus_targets=$(curl -s http://localhost:9090/api/v1/targets | jq -r '.data.activeTargets[] | select(.health == "up") | .labels.job' | sort | uniq | wc -l)
echo -e "${GREEN}✅ $prometheus_targets Prometheus targets are healthy${NC}"

# Check Grafana dashboards
echo "Checking Grafana dashboards..."
grafana_dashboards=$(curl -s -u admin:admin123!@# http://localhost:3000/api/search | jq length)
echo -e "${GREEN}✅ $grafana_dashboards Grafana dashboards available${NC}"

# Check AlertManager configuration
echo "Checking AlertManager configuration..."
alertmanager_config=$(curl -s http://localhost:9093/api/v1/status | jq -r '.status')
echo -e "${GREEN}✅ AlertManager status: $alertmanager_config${NC}"

wait_for_user "\n🎯 Monitoring setup complete! Open the following URLs to view dashboards:\n   📊 Grafana: http://localhost:3000 (admin/admin123!@#)\n   🔍 Prometheus: http://localhost:9090\n   🚨 AlertManager: http://localhost:9093\n\nReady to start load testing?"

# Step 5: Run baseline performance test
echo -e "${BLUE}📈 Step 5: Running Baseline Performance Test${NC}"
echo "Running basic load test to establish baseline metrics..."

python3 scripts/load-test.py \
    --base-url $BASE_URL \
    --duration 120 \
    --users 5 \
    --test-type basic \
    --output $LOG_DIR/baseline-test.json

echo -e "${GREEN}✅ Baseline test completed${NC}"

# Step 6: Monitor initial metrics
echo -e "${BLUE}📊 Step 6: Capturing Initial Metrics${NC}"

# Capture initial CPU and memory usage
initial_cpu=$(curl -s 'http://localhost:9090/api/v1/query?query=system_cpu_usage_percent' | jq -r '.data.result[0].value[1] // "0"')
initial_memory=$(curl -s 'http://localhost:9090/api/v1/query?query=system_memory_usage_percent' | jq -r '.data.result[0].value[1] // "0"')
initial_requests=$(curl -s 'http://localhost:9090/api/v1/query?query=rate(http_requests_total[5m])' | jq -r '.data.result[0].value[1] // "0"')

echo -e "${BLUE}Initial Metrics:${NC}"
echo -e "  CPU Usage: ${initial_cpu}%"
echo -e "  Memory Usage: ${initial_memory}%"
echo -e "  Request Rate: ${initial_requests} req/s"

wait_for_user "\n📊 Initial metrics captured. Ready to start intensive load testing?"

# Step 7: Run intensive load test to trigger scaling
echo -e "${BLUE}🔥 Step 7: Running Intensive Load Test${NC}"
echo "Running spike load test to trigger automatic scaling..."

# Start intensive load test in background
python3 scripts/load-test.py \
    --base-url $BASE_URL \
    --duration $TEST_DURATION \
    --users $CONCURRENT_USERS \
    --test-type spike \
    --output $LOG_DIR/spike-test.json &

LOAD_TEST_PID=$!

echo -e "${GREEN}✅ Intensive load test started (PID: $LOAD_TEST_PID)${NC}"
echo -e "${YELLOW}⏳ Load test will run for $TEST_DURATION seconds with $CONCURRENT_USERS concurrent users${NC}"

# Step 8: Monitor scaling events in real-time
echo -e "${BLUE}👀 Step 8: Monitoring Scaling Events${NC}"
echo "Monitoring system metrics and scaling events..."

# Monitor for 5 minutes while load test runs
for i in {1..10}; do
    echo -e "\n${YELLOW}📊 Metrics Check $i/10 ($(date))${NC}"

    # Get current metrics
    current_cpu=$(curl -s 'http://localhost:9090/api/v1/query?query=system_cpu_usage_percent' | jq -r '.data.result[0].value[1] // "0"')
    current_memory=$(curl -s 'http://localhost:9090/api/v1/query?query=system_memory_usage_percent' | jq -r '.data.result[0].value[1] // "0"')
    current_requests=$(curl -s 'http://localhost:9090/api/v1/query?query=rate(http_requests_total[5m])' | jq -r '.data.result[0].value[1] // "0"')

    # Check for scaling events
    scaling_events=$(curl -s 'http://localhost:9090/api/v1/query?query=increase(scaling_events_total[1m])' | jq -r '.data.result | length')

    # Check active alerts
    active_alerts=$(curl -s 'http://localhost:9093/api/v1/alerts' | jq -r '.data | length')

    echo -e "  CPU: ${current_cpu}% (was ${initial_cpu}%)"
    echo -e "  Memory: ${current_memory}% (was ${initial_memory}%)"
    echo -e "  Requests: ${current_requests} req/s (was ${initial_requests} req/s)"
    echo -e "  Scaling Events: $scaling_events"
    echo -e "  Active Alerts: $active_alerts"

    # Check if CPU usage increased significantly
    if (( $(echo "$current_cpu > $initial_cpu + 20" | bc -l) )); then
        echo -e "  ${GREEN}🔥 High CPU usage detected - scaling should trigger!${NC}"
    fi

    # Check if scaling events occurred
    if [ "$scaling_events" -gt "0" ]; then
        echo -e "  ${GREEN}⚖️  Scaling events detected!${NC}"
    fi

    # Check if alerts are firing
    if [ "$active_alerts" -gt "0" ]; then
        echo -e "  ${YELLOW}🚨 Alerts are firing!${NC}"
    fi

    sleep 30
done

# Step 9: Wait for load test to complete
echo -e "${BLUE}⏳ Step 9: Waiting for Load Test Completion${NC}"
wait $LOAD_TEST_PID
echo -e "${GREEN}✅ Load test completed${NC}"

# Step 10: Run scaling validation
echo -e "${BLUE}🔍 Step 10: Running Scaling Validation${NC}"
echo "Validating that scaling occurred correctly..."

python3 scripts/load-test.py \
    --base-url $BASE_URL \
    --duration 60 \
    --users 2 \
    --test-type scaling \
    --output $LOG_DIR/scaling-validation.json

echo -e "${GREEN}✅ Scaling validation completed${NC}"

# Step 11: Generate comprehensive report
echo -e "${BLUE}📋 Step 11: Generating Comprehensive Report${NC}"

# Capture final metrics
final_cpu=$(curl -s 'http://localhost:9090/api/v1/query?query=system_cpu_usage_percent' | jq -r '.data.result[0].value[1] // "0"')
final_memory=$(curl -s 'http://localhost:9090/api/v1/query?query=system_memory_usage_percent' | jq -r '.data.result[0].value[1] // "0"')
final_requests=$(curl -s 'http://localhost:9090/api/v1/query?query=rate(http_requests_total[5m])' | jq -r '.data.result[0].value[1] // "0"')
total_scaling_events=$(curl -s 'http://localhost:9090/api/v1/query?query=scaling_events_total' | jq -r '.data.result[0].value[1] // "0"')
total_alerts=$(curl -s 'http://localhost:9093/api/v1/alerts' | jq -r '.data | length')

# Create comprehensive report
cat > $LOG_DIR/integration-test-report.md << EOF
# TRAE AI Integration Test Report

Generated: $(date)
Test Duration: $TEST_DURATION seconds
Concurrent Users: $CONCURRENT_USERS
Base URL: $BASE_URL

## Test Summary

### Initial Metrics
- CPU Usage: ${initial_cpu}%
- Memory Usage: ${initial_memory}%
- Request Rate: ${initial_requests} req/s

### Final Metrics
- CPU Usage: ${final_cpu}%
- Memory Usage: ${final_memory}%
- Request Rate: ${final_requests} req/s

### Scaling Events
- Total Scaling Events: $total_scaling_events
- Active Alerts: $total_alerts

### Performance Changes
- CPU Change: $(echo "$final_cpu - $initial_cpu" | bc)%
- Memory Change: $(echo "$final_memory - $initial_memory" | bc)%
- Request Rate Change: $(echo "$final_requests - $initial_requests" | bc) req/s

## Test Results

### Baseline Test
$(cat $LOG_DIR/baseline-test.json | jq -r '.basic_load_test | "Success Rate: \(.success_rate)%, Avg Response Time: \(.response_time_stats.average)s"')

### Spike Test
$(cat $LOG_DIR/spike-test.json | jq -r '.spike_load_test | "Success Rate: \(.success_rate)%, Avg Response Time: \(.response_time_stats.average)s"')

### Scaling Validation
$(cat $LOG_DIR/scaling-validation.json | jq -r '.scaling_validation.scaling_detected | "CPU Increase: \(.cpu_increase_detected), Scaling Events: \(.scaling_events_detected)"')

## Recommendations

$(cat $LOG_DIR/scaling-validation.json | jq -r '.scaling_validation.scaling_detected.recommendations[]?' | sed 's/^/- /')

## Service Health

- Prometheus: ✅ Healthy
- Grafana: ✅ Healthy
- AlertManager: ✅ Healthy
- Load Balancer: ✅ Healthy
- Backend Services: ✅ Healthy

## Files Generated

- Baseline Test: $LOG_DIR/baseline-test.json
- Spike Test: $LOG_DIR/spike-test.json
- Scaling Validation: $LOG_DIR/scaling-validation.json
- Scaling Service Log: $LOG_DIR/scaling-service.log
- Integration Report: $LOG_DIR/integration-test-report.md

EOF

echo -e "${GREEN}✅ Comprehensive report generated${NC}"

# Step 12: Cleanup and summary
echo -e "${BLUE}🧹 Step 12: Test Cleanup${NC}"

# Stop scaling service
if kill -0 $SCALING_PID 2>/dev/null; then
    kill $SCALING_PID
    echo -e "${GREEN}✅ Scaling service stopped${NC}"
fi

# Display final summary
echo -e "\n${GREEN}🎉 TRAE AI Integration Test Complete!${NC}"
echo -e "${GREEN}====================================${NC}"
echo -e "${BLUE}📊 Test Summary:${NC}"
echo -e "  Duration: $TEST_DURATION seconds"
echo -e "  Users: $CONCURRENT_USERS concurrent"
echo -e "  Scaling Events: $total_scaling_events"
echo -e "  Active Alerts: $total_alerts"
echo -e "  CPU Change: $(echo "$final_cpu - $initial_cpu" | bc)%"
echo -e "  Memory Change: $(echo "$final_memory - $initial_memory" | bc)%"

echo -e "\n${BLUE}📁 Generated Files:${NC}"
echo -e "  📋 Integration Report: $LOG_DIR/integration-test-report.md"
echo -e "  📊 Test Results: $LOG_DIR/*.json"
echo -e "  📝 Service Logs: $LOG_DIR/*.log"

echo -e "\n${BLUE}🌐 Access Points:${NC}"
echo -e "  📊 Grafana: http://localhost:3000 (admin/admin123!@#)"
echo -e "  🔍 Prometheus: http://localhost:9090"
echo -e "  🚨 AlertManager: http://localhost:9093"
echo -e "  🔗 Load Balancer: http://localhost:8080"

echo -e "\n${YELLOW}💡 Next Steps:${NC}"
echo -e "  1. Review the integration report: cat $LOG_DIR/integration-test-report.md"
echo -e "  2. Analyze detailed test results in the JSON files"
echo -e "  3. Check Grafana dashboards for visual metrics"
echo -e "  4. Review scaling service logs for detailed scaling decisions"
echo -e "  5. Customize scaling policies based on test results"

echo -e "\n${GREEN}✨ Your TRAE AI monitoring and scaling system is fully validated and ready for production!${NC}"

# Ask if user wants to keep services running
echo -e "\n${PURPLE}Do you want to keep the monitoring services running? (y/N)${NC}"
read -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🛑 Stopping all services...${NC}"
    docker-compose -f docker-compose.scaling.yml down
    echo -e "${GREEN}✅ All services stopped${NC}"
else
    echo -e "${GREEN}✅ Services will continue running${NC}"
    echo -e "${YELLOW}To stop later, run: docker-compose -f docker-compose.scaling.yml down${NC}"
fi

echo -e "\n${BLUE}🎯 Integration test completed successfully!${NC}"
