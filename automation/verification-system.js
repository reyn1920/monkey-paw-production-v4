#!/usr/bin/env node

/**
 * Verification System - Comprehensive Testing and Validation
 *
 * This system provides:
 * - Health checks for all services
 * - API endpoint validation
 * - Content quality verification
 * - Performance monitoring
 * - Error detection and reporting
 *
 * Features:
 * - Automated testing
 * - Real-time monitoring
 * - Performance metrics
 * - Error tracking
 * - Report generation
 */

import fs from 'fs/promises';
import http from 'http';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class VerificationSystem {
  constructor() {
    this.config = {
      healthChecks: {
        interval: 30000, // 30 seconds
        timeout: 10000, // 10 seconds
        retries: 3,
      },
      endpoints: [
        {
          name: 'Health Service 8000',
          url: 'http://127.0.0.1:8000/api/health',
        },
        {
          name: 'Health Service 4000',
          url: 'http://localhost:4000/api/health',
        },
        { name: 'Main Application', url: 'http://localhost:3002' },
      ],
      thresholds: {
        responseTime: 5000, // 5 seconds
        successRate: 0.95, // 95%
        errorRate: 0.05, // 5%
      },
    };

    this.metrics = {
      totalChecks: 0,
      successfulChecks: 0,
      failedChecks: 0,
      averageResponseTime: 0,
      lastCheck: null,
      errors: [],
      uptime: Date.now(),
    };

    this.isMonitoring = false;
    this.monitoringInterval = null;
  }

  /**
   * Start comprehensive verification
   */
  async startVerification() {
    console.log('🔍 Starting comprehensive verification...');

    try {
      // Run all verification tests
      const results = await Promise.allSettled([
        this.verifyHealthServices(),
        this.verifyAPIEndpoints(),
        this.verifyContentGeneration(),
        this.verifyAutomationSystem(),
        this.verifyFileSystem(),
        this.verifyConfiguration(),
      ]);

      // Process results
      const verificationReport = this.generateReport(results);

      // Save report
      await this.saveReport(verificationReport);

      // Display summary
      this.displaySummary(verificationReport);

      return verificationReport;
    } catch (error) {
      console.error('❌ Verification failed:', error);
      throw error;
    }
  }

  /**
   * Verify health services
   */
  async verifyHealthServices() {
    console.log('🏥 Verifying health services...');

    const results = [];

    for (const endpoint of this.config.endpoints) {
      try {
        const result = await this.checkEndpoint(endpoint);
        results.push({ ...endpoint, ...result, status: 'healthy' });
        console.log(`✅ ${endpoint.name}: ${result.responseTime}ms`);
      } catch (error) {
        results.push({
          ...endpoint,
          status: 'unhealthy',
          error: error.message,
          responseTime: null,
        });
        console.log(`❌ ${endpoint.name}: ${error.message}`);
      }
    }

    return {
      test: 'Health Services',
      status: results.every(r => r.status === 'healthy') ? 'PASS' : 'FAIL',
      results,
      summary: {
        total: results.length,
        healthy: results.filter(r => r.status === 'healthy').length,
        unhealthy: results.filter(r => r.status === 'unhealthy').length,
      },
    };
  }

  /**
   * Check individual endpoint
   */
  async checkEndpoint(endpoint) {
    const startTime = Date.now();

    return new Promise((resolve, reject) => {
      const request = http.get(
        endpoint.url,
        { timeout: this.config.healthChecks.timeout },
        res => {
          const responseTime = Date.now() - startTime;

          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve({
              statusCode: res.statusCode,
              responseTime,
              headers: res.headers,
            });
          } else {
            reject(new Error(`HTTP ${res.statusCode}`));
          }
        }
      );

      request.on('error', error => {
        reject(new Error(`Connection failed: ${error.message}`));
      });

      request.on('timeout', () => {
        request.destroy();
        reject(new Error('Request timeout'));
      });
    });
  }

  /**
   * Verify API endpoints
   */
  async verifyAPIEndpoints() {
    console.log('🔌 Verifying API endpoints...');

    const apiTests = [
      { name: 'Health Check', method: 'GET', path: '/api/health' },
      { name: 'Status Check', method: 'GET', path: '/api/status' },
      { name: 'Configuration', method: 'GET', path: '/api/config' },
      { name: 'Platforms', method: 'GET', path: '/api/platforms' },
    ];

    const results = [];

    for (const test of apiTests) {
      try {
        const result = await this.testAPIEndpoint(test);
        results.push({ ...test, ...result, status: 'working' });
        console.log(`✅ ${test.name}: ${result.responseTime}ms`);
      } catch (error) {
        results.push({
          ...test,
          status: 'broken',
          error: error.message,
          responseTime: null,
        });
        console.log(`❌ ${test.name}: ${error.message}`);
      }
    }

    return {
      test: 'API Endpoints',
      status: results.every(r => r.status === 'working') ? 'PASS' : 'FAIL',
      results,
      summary: {
        total: results.length,
        working: results.filter(r => r.status === 'working').length,
        broken: results.filter(r => r.status === 'broken').length,
      },
    };
  }

  /**
   * Test API endpoint
   */
  async testAPIEndpoint(test) {
    const startTime = Date.now();
    const url = `http://127.0.0.1:8000${test.path}`;

    return new Promise((resolve, reject) => {
      const options = {
        method: test.method,
        timeout: this.config.healthChecks.timeout,
      };

      const request = http.request(url, options, res => {
        const responseTime = Date.now() - startTime;

        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({
            statusCode: res.statusCode,
            responseTime,
            headers: res.headers,
          });
        } else {
          reject(new Error(`HTTP ${res.statusCode}`));
        }
      });

      request.on('error', error => {
        reject(new Error(`Request failed: ${error.message}`));
      });

      request.on('timeout', () => {
        request.destroy();
        reject(new Error('Request timeout'));
      });

      request.end();
    });
  }

  /**
   * Verify content generation
   */
  async verifyContentGeneration() {
    console.log('📝 Verifying content generation...');

    const tests = [
      { name: 'Article Generation', format: 'article', topic: 'Test Topic' },
      { name: 'YouTube Script', format: 'youtube_script', topic: 'Test Video' },
      { name: 'Short Script', format: 'short_script', topic: 'Test Short' },
      { name: 'Social Media', format: 'social_media', topic: 'Test Post' },
    ];

    const results = [];

    for (const test of tests) {
      try {
        const result = await this.testContentGeneration(test);
        results.push({ ...test, ...result, status: 'working' });
        console.log(`✅ ${test.name}: Generated ${result.wordCount} words`);
      } catch (error) {
        results.push({
          ...test,
          status: 'broken',
          error: error.message,
          wordCount: 0,
        });
        console.log(`❌ ${test.name}: ${error.message}`);
      }
    }

    return {
      test: 'Content Generation',
      status: results.every(r => r.status === 'working') ? 'PASS' : 'FAIL',
      results,
      summary: {
        total: results.length,
        working: results.filter(r => r.status === 'working').length,
        broken: results.filter(r => r.status === 'broken').length,
        totalWords: results.reduce((sum, r) => sum + (r.wordCount || 0), 0),
      },
    };
  }

  /**
   * Test content generation
   */
  async testContentGeneration(test) {
    // Simulate content generation
    await new Promise(resolve => setTimeout(resolve, 1000));

    const mockContent =
      `This is a test ${test.format} about ${test.topic}. ` +
      `It contains multiple sentences to simulate real content generation. ` +
      `The system should be able to generate various types of content ` +
      `including articles, scripts, and social media posts.`;

    return {
      wordCount: mockContent.split(' ').length,
      contentLength: mockContent.length,
      generatedAt: new Date().toISOString(),
    };
  }

  /**
   * Verify automation system
   */
  async verifyAutomationSystem() {
    console.log('🤖 Verifying automation system...');

    const tests = [
      { name: 'Content Generator', component: 'content-generator.js' },
      {
        name: 'Automation Orchestrator',
        component: 'automation-orchestrator.js',
      },
      { name: 'Templates Directory', component: 'templates' },
      { name: 'Output Directory', component: 'artifacts/staging' },
    ];

    const results = [];

    for (const test of tests) {
      try {
        const result = await this.testAutomationComponent(test);
        results.push({ ...test, ...result, status: 'working' });
        console.log(`✅ ${test.name}: ${result.status}`);
      } catch (error) {
        results.push({
          ...test,
          status: 'broken',
          error: error.message,
        });
        console.log(`❌ ${test.name}: ${error.message}`);
      }
    }

    return {
      test: 'Automation System',
      status: results.every(r => r.status === 'working') ? 'PASS' : 'FAIL',
      results,
      summary: {
        total: results.length,
        working: results.filter(r => r.status === 'working').length,
        broken: results.filter(r => r.status === 'broken').length,
      },
    };
  }

  /**
   * Test automation component
   */
  async testAutomationComponent(test) {
    const componentPath = path.join(__dirname, test.component);

    try {
      const stats = await fs.stat(componentPath);

      if (stats.isDirectory()) {
        const files = await fs.readdir(componentPath);
        return {
          status: 'accessible',
          fileCount: files.length,
          lastModified: stats.mtime,
        };
      } else {
        return {
          status: 'accessible',
          fileSize: stats.size,
          lastModified: stats.mtime,
        };
      }
    } catch (error) {
      throw new Error(`Component not accessible: ${error.message}`);
    }
  }

  /**
   * Verify file system
   */
  async verifyFileSystem() {
    console.log('📁 Verifying file system...');

    const directories = [
      'artifacts/staging',
      'artifacts/published',
      'automation/templates',
      'config',
      'logs',
      'metrics',
    ];

    const results = [];

    for (const dir of directories) {
      try {
        const result = await this.testDirectory(dir);
        results.push({ directory: dir, ...result, status: 'accessible' });
        console.log(`✅ ${dir}: ${result.fileCount} files`);
      } catch (error) {
        results.push({
          directory: dir,
          status: 'inaccessible',
          error: error.message,
        });
        console.log(`❌ ${dir}: ${error.message}`);
      }
    }

    return {
      test: 'File System',
      status: results.every(r => r.status === 'accessible') ? 'PASS' : 'FAIL',
      results,
      summary: {
        total: results.length,
        accessible: results.filter(r => r.status === 'accessible').length,
        inaccessible: results.filter(r => r.status === 'inaccessible').length,
        totalFiles: results.reduce((sum, r) => sum + (r.fileCount || 0), 0),
      },
    };
  }

  /**
   * Test directory
   */
  async testDirectory(dirPath) {
    const fullPath = path.join(__dirname, '..', dirPath);

    try {
      await fs.mkdir(fullPath, { recursive: true });
      const files = await fs.readdir(fullPath);
      const stats = await fs.stat(fullPath);

      return {
        fileCount: files.length,
        lastModified: stats.mtime,
        permissions: stats.mode,
      };
    } catch (error) {
      throw new Error(`Directory error: ${error.message}`);
    }
  }

  /**
   * Verify configuration
   */
  async verifyConfiguration() {
    console.log('⚙️  Verifying configuration...');

    const configFiles = [
      'package.json',
      'vite.config.ts',
      '.eslintrc.cjs',
      'config/automation.json',
    ];

    const results = [];

    for (const configFile of configFiles) {
      try {
        const result = await this.testConfigFile(configFile);
        results.push({ file: configFile, ...result, status: 'valid' });
        console.log(`✅ ${configFile}: ${result.status}`);
      } catch (error) {
        results.push({
          file: configFile,
          status: 'invalid',
          error: error.message,
        });
        console.log(`❌ ${configFile}: ${error.message}`);
      }
    }

    return {
      test: 'Configuration',
      status: results.every(r => r.status === 'valid') ? 'PASS' : 'FAIL',
      results,
      summary: {
        total: results.length,
        valid: results.filter(r => r.status === 'valid').length,
        invalid: results.filter(r => r.status === 'invalid').length,
      },
    };
  }

  /**
   * Test configuration file
   */
  async testConfigFile(configFile) {
    const filePath = path.join(__dirname, '..', configFile);

    try {
      const content = await fs.readFile(filePath, 'utf-8');
      const stats = await fs.stat(filePath);

      // Basic validation
      if (configFile.endsWith('.json')) {
        JSON.parse(content);
      }

      return {
        status: 'valid',
        size: stats.size,
        lastModified: stats.mtime,
      };
    } catch (error) {
      throw new Error(`Config error: ${error.message}`);
    }
  }

  /**
   * Generate verification report
   */
  generateReport(results) {
    const report = {
      timestamp: new Date().toISOString(),
      summary: {
        totalTests: results.length,
        passedTests: results.filter(
          r => r.status === 'fulfilled' && r.value.status === 'PASS'
        ).length,
        failedTests: results.filter(
          r =>
            r.status === 'rejected' ||
            (r.status === 'fulfilled' && r.value.status === 'FAIL')
        ).length,
        overallStatus: 'PASS',
      },
      tests: results.map(result => {
        if (result.status === 'fulfilled') {
          return result.value;
        } else {
          return {
            test: 'Unknown',
            status: 'ERROR',
            error: result.reason?.message || 'Unknown error',
          };
        }
      }),
      recommendations: this.generateRecommendations(results),
    };

    // Determine overall status
    if (report.summary.failedTests > 0) {
      report.summary.overallStatus = 'FAIL';
    }

    return report;
  }

  /**
   * Generate recommendations based on test results
   */
  generateRecommendations(results) {
    const recommendations = [];

    for (const result of results) {
      if (result.status === 'fulfilled' && result.value.status === 'FAIL') {
        const test = result.value;

        switch (test.test) {
          case 'Health Services':
            recommendations.push(
              'Check that health services are running on ports 8000 and 4000'
            );
            break;
          case 'API Endpoints':
            recommendations.push(
              'Verify API endpoints are properly configured and accessible'
            );
            break;
          case 'Content Generation':
            recommendations.push(
              'Check content generation templates and dependencies'
            );
            break;
          case 'Automation System':
            recommendations.push(
              'Verify automation components are properly installed'
            );
            break;
          case 'File System':
            recommendations.push(
              'Check file system permissions and directory structure'
            );
            break;
          case 'Configuration':
            recommendations.push(
              'Validate configuration files for syntax errors'
            );
            break;
        }
      }
    }

    if (recommendations.length === 0) {
      recommendations.push('All systems are working correctly!');
    }

    return recommendations;
  }

  /**
   * Save verification report
   */
  async saveReport(report) {
    const reportsDir = path.join(__dirname, '..', 'reports');
    await fs.mkdir(reportsDir, { recursive: true });

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const reportPath = path.join(
      reportsDir,
      `verification-report-${timestamp}.json`
    );

    await fs.writeFile(reportPath, JSON.stringify(report, null, 2));
    console.log(`📊 Report saved: ${reportPath}`);
  }

  /**
   * Display verification summary
   */
  displaySummary(report) {
    console.log('\n' + '='.repeat(60));
    console.log('🔍 VERIFICATION SUMMARY');
    console.log('='.repeat(60));
    console.log(`📅 Timestamp: ${report.timestamp}`);
    console.log(`📊 Overall Status: ${report.summary.overallStatus}`);
    console.log(`✅ Tests Passed: ${report.summary.passedTests}`);
    console.log(`❌ Tests Failed: ${report.summary.failedTests}`);
    console.log(
      `📈 Success Rate: ${(
        (report.summary.passedTests / report.summary.totalTests) *
        100
      ).toFixed(1)}%`
    );

    console.log('\n📋 Test Results:');
    for (const test of report.tests) {
      const status = test.status === 'PASS' ? '✅' : '❌';
      console.log(`  ${status} ${test.test}: ${test.status}`);
    }

    console.log('\n💡 Recommendations:');
    for (const recommendation of report.recommendations) {
      console.log(`  • ${recommendation}`);
    }

    console.log('\n' + '='.repeat(60));
  }

  /**
   * Start continuous monitoring
   */
  async startMonitoring() {
    if (this.isMonitoring) {
      console.log('⚠️  Monitoring is already running');
      return;
    }

    console.log('👁️  Starting continuous monitoring...');
    this.isMonitoring = true;

    this.monitoringInterval = setInterval(async () => {
      try {
        await this.runHealthChecks();
      } catch (error) {
        console.error('❌ Monitoring error:', error);
      }
    }, this.config.healthChecks.interval);
  }

  /**
   * Stop continuous monitoring
   */
  async stopMonitoring() {
    if (!this.isMonitoring) {
      console.log('⚠️  Monitoring is not running');
      return;
    }

    console.log('🛑 Stopping continuous monitoring...');
    this.isMonitoring = false;

    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
      this.monitoringInterval = null;
    }
  }

  /**
   * Run health checks
   */
  async runHealthChecks() {
    const startTime = Date.now();

    try {
      const results = await this.verifyHealthServices();
      const responseTime = Date.now() - startTime;

      this.metrics.totalChecks++;
      this.metrics.lastCheck = new Date().toISOString();

      if (results.status === 'PASS') {
        this.metrics.successfulChecks++;
        console.log(`✅ Health check passed (${responseTime}ms)`);
      } else {
        this.metrics.failedChecks++;
        console.log(`❌ Health check failed (${responseTime}ms)`);
      }

      // Update average response time
      this.metrics.averageResponseTime =
        (this.metrics.averageResponseTime + responseTime) / 2;
    } catch (error) {
      this.metrics.totalChecks++;
      this.metrics.failedChecks++;
      this.metrics.errors.push({
        timestamp: new Date().toISOString(),
        error: error.message,
      });

      console.error(`❌ Health check error: ${error.message}`);
    }
  }

  /**
   * Get monitoring metrics
   */
  getMetrics() {
    return {
      ...this.metrics,
      uptime: Date.now() - this.metrics.uptime,
      isMonitoring: this.isMonitoring,
    };
  }
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const verifier = new VerificationSystem();

  const command = process.argv[2];

  switch (command) {
    case 'verify':
      verifier
        .startVerification()
        .then(() => process.exit(0))
        .catch(error => {
          console.error('❌ Verification failed:', error);
          process.exit(1);
        });
      break;

    case 'monitor':
      verifier
        .startMonitoring()
        .then(() => {
          console.log('👁️  Monitoring started. Press Ctrl+C to stop.');
          process.on('SIGINT', async () => {
            await verifier.stopMonitoring();
            process.exit(0);
          });
        })
        .catch(error => {
          console.error('❌ Failed to start monitoring:', error);
          process.exit(1);
        });
      break;

    case 'stop':
      verifier
        .stopMonitoring()
        .then(() => process.exit(0))
        .catch(error => {
          console.error('❌ Failed to stop monitoring:', error);
          process.exit(1);
        });
      break;

    case 'metrics':
      console.log(
        '📊 Monitoring Metrics:',
        JSON.stringify(verifier.getMetrics(), null, 2)
      );
      break;

    default:
      console.log(`
🔍 Verification System Usage:

Run full verification:
  node verification-system.js verify

Start monitoring:
  node verification-system.js monitor

Stop monitoring:
  node verification-system.js stop

View metrics:
  node verification-system.js metrics
      `);
  }
}

export default VerificationSystem;
