#!/usr/bin/env node

/**
 * System Integration Audit Script
 * Verifies all AI tools, APIs, and integrations are properly configured
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class SystemIntegrationAudit {
  constructor() {
    this.basePath = path.join(__dirname, '..');
    this.auditResults = {
      applications: {},
      configurations: {},
      apiKeys: {},
      integrations: {},
      recommendations: [],
    };
  }

  /**
   * Run complete system audit
   */
  async runAudit() {
    console.log('🔍 Starting System Integration Audit...\n');

    try {
      await this.checkApplications();
      await this.checkConfigurations();
      await this.checkApiKeys();
      await this.checkIntegrations();
      await this.generateReport();

      console.log('✅ System audit completed successfully');
      return this.auditResults;
    } catch (error) {
      console.error('❌ System audit failed:', error);
      return null;
    }
  }

  /**
   * Check all AI applications
   */
  async checkApplications() {
    console.log('📱 Checking AI Applications...');

    const applications = [
      {
        name: 'Cursor',
        path: '/Applications/Cursor.app',
        command: 'cursor --version',
      },
      {
        name: 'Windsurf',
        path: '/Applications/Windsurf.app',
        command: 'windsurf --version',
      },
      {
        name: 'Sublime Text',
        path: '/Applications/Sublime Text.app',
        command: 'subl --version',
      },
      {
        name: 'VS Code',
        path: '/Applications/Visual Studio Code.app',
        command: 'code --version',
      },
      {
        name: 'Ollama',
        path: '/Applications/Ollama.app',
        command: 'ollama --version',
      },
      {
        name: 'Trae',
        path: '/Applications/Trae.app',
        command: 'trae --version',
      },
      {
        name: 'DaVinci Resolve',
        path: '/Applications/DaVinci Resolve/DaVinci Resolve.app',
        command: 'resolve --version',
      },
      {
        name: 'Blender',
        path: '/Applications/Blender.app',
        command: 'blender --version',
      },
      {
        name: 'Docker',
        path: '/usr/local/bin/docker',
        command: 'docker --version',
      },
    ];

    for (const app of applications) {
      const exists = fs.existsSync(app.path);
      let version = 'Unknown';
      let status = exists ? 'Installed' : 'Missing';

      if (exists) {
        try {
          version = execSync(app.command, {
            encoding: 'utf8',
            timeout: 5000,
          }).trim();
        } catch (error) {
          version = 'Version check failed';
          status = 'Installed (version check failed)';
        }
      }

      this.auditResults.applications[app.name] = {
        path: app.path,
        exists,
        version,
        status,
      };

      console.log(
        `  ${exists ? '✅' : '❌'} ${app.name}: ${status} (${version})`
      );
    }
  }

  /**
   * Check configuration files
   */
  async checkConfigurations() {
    console.log('\n🔧 Checking Configuration Files...');

    const configs = [
      { name: 'Shared Environment', path: '~/.config/dev-stack/shared.env' },
      {
        name: 'Windsurf Aliases',
        path: '~/.config/dev-stack/windsurf-aliases.sh',
      },
      { name: 'Package.json', path: path.join(this.basePath, 'package.json') },
      {
        name: 'Requirements.txt',
        path: path.join(this.basePath, 'requirements.txt'),
      },
      { name: 'Vite Config', path: path.join(this.basePath, 'vite.config.ts') },
      {
        name: 'TypeScript Config',
        path: path.join(this.basePath, 'tsconfig.json'),
      },
      {
        name: 'ESLint Config',
        path: path.join(this.basePath, '.eslintrc.cjs'),
      },
      {
        name: 'Tailwind Config',
        path: path.join(this.basePath, 'tailwind.config.js'),
      },
      {
        name: 'Firebase Config',
        path: path.join(this.basePath, 'firebase.json'),
      },
    ];

    for (const config of configs) {
      const expandedPath = config.path.startsWith('~')
        ? path.join(process.env.HOME, config.path.slice(2))
        : config.path;

      const exists = fs.existsSync(expandedPath);
      let size = 0;
      let lastModified = null;

      if (exists) {
        const stats = fs.statSync(expandedPath);
        size = stats.size;
        lastModified = stats.mtime.toISOString();
      }

      this.auditResults.configurations[config.name] = {
        path: expandedPath,
        exists,
        size,
        lastModified,
      };

      console.log(
        `  ${exists ? '✅' : '❌'} ${config.name}: ${
          exists ? 'Found' : 'Missing'
        }`
      );
    }
  }

  /**
   * Check API keys and environment variables
   */
  async checkApiKeys() {
    console.log('\n🔑 Checking API Keys & Environment Variables...');

    const apiKeys = [
      'WINDSURF_API_KEY',
      'OLLAMA_BASE_URL',
      'FASTAPI_URL',
      'BACKEND_URL',
      'OPENAI_API_KEY',
      'ANTHROPIC_API_KEY',
      'GOOGLE_GENERATIVE_AI_API_KEY',
      'GROQ_API_KEY',
      'GROK_API_KEY',
      'YOUTUBE_API_KEY',
    ];

    for (const key of apiKeys) {
      const value = process.env[key];
      const configured =
        value && value.length > 0 && !value.includes('your_actual_');

      this.auditResults.apiKeys[key] = {
        configured,
        hasValue: !!value,
        length: value ? value.length : 0,
        masked: value ? `${value.substring(0, 10)}...` : 'Not set',
      };

      console.log(
        `  ${configured ? '✅' : '⚠️'} ${key}: ${
          configured ? 'Configured' : 'Needs setup'
        }`
      );
    }
  }

  /**
   * Check integrations and services
   */
  async checkIntegrations() {
    console.log('\n🔗 Checking Integrations & Services...');

    // Check Ollama models
    try {
      const ollamaList = execSync('ollama list', {
        encoding: 'utf8',
        timeout: 10000,
      });
      const models = ollamaList
        .split('\n')
        .filter(line => line.trim() && !line.includes('NAME'));
      this.auditResults.integrations.ollamaModels = {
        count: models.length,
        models: models.map(line => line.split(/\s+/)[0]).filter(Boolean),
      };
      console.log(`  ✅ Ollama Models: ${models.length} models installed`);
    } catch (error) {
      this.auditResults.integrations.ollamaModels = {
        count: 0,
        error: error.message,
      };
      console.log(`  ❌ Ollama Models: Failed to check (${error.message})`);
    }

    // Check Node.js and npm
    try {
      const nodeVersion = execSync('node --version', {
        encoding: 'utf8',
      }).trim();
      const npmVersion = execSync('npm --version', { encoding: 'utf8' }).trim();
      this.auditResults.integrations.nodejs = { nodeVersion, npmVersion };
      console.log(`  ✅ Node.js: ${nodeVersion}, NPM: ${npmVersion}`);
    } catch (error) {
      this.auditResults.integrations.nodejs = { error: error.message };
      console.log(`  ❌ Node.js: Failed to check (${error.message})`);
    }

    // Check Python
    try {
      const pythonVersion = execSync('python3 --version', {
        encoding: 'utf8',
      }).trim();
      this.auditResults.integrations.python = { version: pythonVersion };
      console.log(`  ✅ Python: ${pythonVersion}`);
    } catch (error) {
      this.auditResults.integrations.python = { error: error.message };
      console.log(`  ❌ Python: Failed to check (${error.message})`);
    }

    // Check Homebrew
    try {
      const brewVersion = execSync('brew --version', { encoding: 'utf8' })
        .trim()
        .split('\n')[0];
      this.auditResults.integrations.homebrew = { version: brewVersion };
      console.log(`  ✅ Homebrew: ${brewVersion}`);
    } catch (error) {
      this.auditResults.integrations.homebrew = { error: error.message };
      console.log(`  ❌ Homebrew: Failed to check (${error.message})`);
    }
  }

  /**
   * Generate audit report
   */
  async generateReport() {
    console.log('\n📊 Generating Audit Report...');

    const report = {
      timestamp: new Date().toISOString(),
      system: {
        platform: process.platform,
        arch: process.arch,
        nodeVersion: process.version,
        homeDirectory: process.env.HOME,
      },
      summary: {
        applicationsInstalled: Object.values(
          this.auditResults.applications
        ).filter(app => app.exists).length,
        applicationsTotal: Object.keys(this.auditResults.applications).length,
        configurationsFound: Object.values(
          this.auditResults.configurations
        ).filter(config => config.exists).length,
        configurationsTotal: Object.keys(this.auditResults.configurations)
          .length,
        apiKeysConfigured: Object.values(this.auditResults.apiKeys).filter(
          key => key.configured
        ).length,
        apiKeysTotal: Object.keys(this.auditResults.apiKeys).length,
      },
      details: this.auditResults,
    };

    // Save report
    const reportPath = path.join(this.basePath, 'SYSTEM_AUDIT_REPORT.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));

    console.log(`\n📋 Audit Report Summary:`);
    console.log(
      `  📱 Applications: ${report.summary.applicationsInstalled}/${report.summary.applicationsTotal} installed`
    );
    console.log(
      `  🔧 Configurations: ${report.summary.configurationsFound}/${report.summary.configurationsTotal} found`
    );
    console.log(
      `  🔑 API Keys: ${report.summary.apiKeysConfigured}/${report.summary.apiKeysTotal} configured`
    );
    console.log(`  📄 Full report saved to: ${reportPath}`);

    // Generate recommendations
    this.generateRecommendations();
  }

  /**
   * Generate recommendations based on audit results
   */
  generateRecommendations() {
    console.log('\n💡 Recommendations:');

    // Check missing applications
    const missingApps = Object.entries(this.auditResults.applications)
      .filter(([name, app]) => !app.exists)
      .map(([name]) => name);

    if (missingApps.length > 0) {
      console.log(
        `  ⚠️  Install missing applications: ${missingApps.join(', ')}`
      );
      this.auditResults.recommendations.push(
        `Install missing applications: ${missingApps.join(', ')}`
      );
    }

    // Check missing configurations
    const missingConfigs = Object.entries(this.auditResults.configurations)
      .filter(([name, config]) => !config.exists)
      .map(([name]) => name);

    if (missingConfigs.length > 0) {
      console.log(
        `  ⚠️  Create missing configurations: ${missingConfigs.join(', ')}`
      );
      this.auditResults.recommendations.push(
        `Create missing configurations: ${missingConfigs.join(', ')}`
      );
    }

    // Check unconfigured API keys
    const unconfiguredKeys = Object.entries(this.auditResults.apiKeys)
      .filter(([name, key]) => !key.configured)
      .map(([name]) => name);

    if (unconfiguredKeys.length > 0) {
      console.log(`  ⚠️  Configure API keys: ${unconfiguredKeys.join(', ')}`);
      this.auditResults.recommendations.push(
        `Configure API keys: ${unconfiguredKeys.join(', ')}`
      );
    }

    // Check Ollama models
    if (this.auditResults.integrations.ollamaModels?.count === 0) {
      console.log(`  ⚠️  Install Ollama models for local AI development`);
      this.auditResults.recommendations.push(
        'Install Ollama models for local AI development'
      );
    }

    if (this.auditResults.recommendations.length === 0) {
      console.log(`  ✅ All systems properly configured!`);
    }
  }
}

// CLI Interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const audit = new SystemIntegrationAudit();
  audit.runAudit().then(results => {
    if (results) {
      console.log('\n🎉 System audit completed successfully!');
      process.exit(0);
    } else {
      console.log('\n💥 System audit failed!');
      process.exit(1);
    }
  });
}

export default SystemIntegrationAudit;
