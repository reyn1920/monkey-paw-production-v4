#!/usr/bin/env node

/**
 * AI Extensions Health Check Script
 * Monitors and optimizes performance of all AI tools
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class AIHealthChecker {
  constructor() {
    this.configPath = path.join(__dirname, '../config/extensions_audit.json');
    this.logPath = path.join(__dirname, '../logs/ai_health.log');
    this.config = this.loadConfig();
  }

  loadConfig() {
    try {
      return JSON.parse(fs.readFileSync(this.configPath, 'utf8'));
    } catch (error) {
      console.error('Failed to load config:', error.message);
      return null;
    }
  }

  saveConfig() {
    try {
      fs.writeFileSync(this.configPath, JSON.stringify(this.config, null, 2));
    } catch (error) {
      console.error('Failed to save config:', error.message);
    }
  }

  log(message) {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] ${message}\n`;
    
    console.log(message);
    
    try {
      fs.appendFileSync(this.logPath, logMessage);
    } catch (error) {
      console.error('Failed to write to log file:', error.message);
    }
  }

  checkSystemResources() {
    this.log('🔍 Checking system resources...');
    
    try {
      // Check memory usage
      const memInfo = execSync('ps -A -o %mem,comm | grep -E "(cursor|code|node)" | head -10').toString();
      this.log(`Memory usage for AI tools:\n${memInfo}`);
      
      // Check CPU usage
      const cpuInfo = execSync('top -l 1 -n 10 | grep -E "(cursor|code|node)"').toString();
      this.log(`CPU usage for AI tools:\n${cpuInfo}`);
      
      return true;
    } catch (error) {
      this.log(`❌ Error checking system resources: ${error.message}`);
      return false;
    }
  }

  checkAWSConfiguration() {
    this.log('🔍 Checking AWS configuration for Amazon Q...');
    
    try {
      const awsConfig = execSync('aws configure list').toString();
      
      if (awsConfig.includes('<not set>')) {
        this.log('⚠️  AWS credentials not configured. Amazon Q may not work properly.');
        this.config.ai_extensions_audit.required_extensions.find(ext => 
          ext.name === 'Amazon Q Developer'
        ).status = 'needs_aws_setup';
        return false;
      } else {
        this.log('✅ AWS credentials configured properly.');
        return true;
      }
    } catch (error) {
      this.log(`❌ Error checking AWS configuration: ${error.message}`);
      return false;
    }
  }

  checkNodeModules() {
    this.log('🔍 Checking Node.js dependencies...');
    
    const packageJsonPath = path.join(__dirname, '../package.json');
    
    try {
      if (fs.existsSync(packageJsonPath)) {
        const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
        this.log(`✅ Project: ${packageJson.name} v${packageJson.version}`);
        
        // Check if node_modules exists
        const nodeModulesPath = path.join(__dirname, '../node_modules');
        if (fs.existsSync(nodeModulesPath)) {
          this.log('✅ Node modules installed.');
          return true;
        } else {
          this.log('⚠️  Node modules not found. Run npm install.');
          return false;
        }
      }
    } catch (error) {
      this.log(`❌ Error checking Node.js setup: ${error.message}`);
      return false;
    }
  }

  checkGitConfiguration() {
    this.log('🔍 Checking Git configuration...');
    
    try {
      const gitStatus = execSync('git status --porcelain').toString();
      const gitConfig = execSync('git config --list').toString();
      
      if (gitConfig.includes('user.name') && gitConfig.includes('user.email')) {
        this.log('✅ Git properly configured.');
        
        if (gitStatus.trim()) {
          this.log(`⚠️  Uncommitted changes found:\n${gitStatus}`);
        } else {
          this.log('✅ Working directory clean.');
        }
        
        return true;
      } else {
        this.log('⚠️  Git user configuration incomplete.');
        return false;
      }
    } catch (error) {
      this.log(`❌ Error checking Git: ${error.message}`);
      return false;
    }
  }

  optimizeAISettings() {
    this.log('⚙️  Optimizing AI settings...');
    
    const recommendations = [];
    
    // Check for potential conflicts
    this.config.ai_extensions_audit.potential_conflicts.forEach(conflict => {
      this.log(`🔧 Addressing conflict: ${conflict.conflict_type}`);
      this.log(`   Resolution: ${conflict.resolution}`);
      recommendations.push(conflict.resolution);
    });
    
    // Update health check
    this.config.health_check.last_audit = new Date().toISOString();
    this.config.health_check.recommendations = recommendations;
    
    this.saveConfig();
    
    return recommendations;
  }

  generateReport() {
    this.log('📊 Generating health report...');
    
    const report = {
      timestamp: new Date().toISOString(),
      system_health: 'checking...',
      aws_status: 'checking...',
      git_status: 'checking...',
      node_status: 'checking...',
      recommendations: []
    };
    
    // Run all checks
    const systemOk = this.checkSystemResources();
    const awsOk = this.checkAWSConfiguration();
    const gitOk = this.checkGitConfiguration();
    const nodeOk = this.checkNodeModules();
    
    report.system_health = systemOk ? 'healthy' : 'needs_attention';
    report.aws_status = awsOk ? 'configured' : 'needs_setup';
    report.git_status = gitOk ? 'configured' : 'needs_setup';
    report.node_status = nodeOk ? 'ready' : 'needs_install';
    
    // Generate recommendations
    const recommendations = this.optimizeAISettings();
    report.recommendations = recommendations;
    
    // Save report
    const reportPath = path.join(__dirname, '../logs/ai_health_report.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    
    this.log('✅ Health check complete! Report saved to logs/ai_health_report.json');
    
    return report;
  }

  fixCommonIssues() {
    this.log('🔧 Attempting to fix common issues...');
    
    try {
      // Ensure logs directory exists
      const logsDir = path.join(__dirname, '../logs');
      if (!fs.existsSync(logsDir)) {
        fs.mkdirSync(logsDir, { recursive: true });
        this.log('✅ Created logs directory.');
      }
      
      // Check and fix .gitignore
      const gitignorePath = path.join(__dirname, '../.gitignore');
      if (fs.existsSync(gitignorePath)) {
        const gitignoreContent = fs.readFileSync(gitignorePath, 'utf8');
        if (!gitignoreContent.includes('logs/')) {
          fs.appendFileSync(gitignorePath, '\n# Logs\nlogs/\n*.log\n');
          this.log('✅ Updated .gitignore to exclude logs.');
        }
      }
      
      return true;
    } catch (error) {
      this.log(`❌ Error fixing issues: ${error.message}`);
      return false;
    }
  }
}

// Main execution
if (require.main === module) {
  const checker = new AIHealthChecker();
  
  console.log('🚀 Starting AI Extensions Health Check...\n');
  
  // Fix common issues first
  checker.fixCommonIssues();
  
  // Generate comprehensive report
  const report = checker.generateReport();
  
  console.log('\n📋 HEALTH CHECK SUMMARY:');
  console.log(`System Health: ${report.system_health}`);
  console.log(`AWS Status: ${report.aws_status}`);
  console.log(`Git Status: ${report.git_status}`);
  console.log(`Node Status: ${report.node_status}`);
  
  if (report.recommendations.length > 0) {
    console.log('\n💡 RECOMMENDATIONS:');
    report.recommendations.forEach((rec, index) => {
      console.log(`${index + 1}. ${rec}`);
    });
  }
  
  console.log('\n✨ Health check complete!');
}

module.exports = AIHealthChecker;