#!/usr/bin/env node

/**
 * Automation Orchestrator - Master Control System
 *
 * This system coordinates all automation tasks:
 * - Content generation
 * - Video processing
 * - Social media posting
 * - Analytics tracking
 * - Performance monitoring
 *
 * Features:
 * - Scheduled automation
 * - Error handling and recovery
 * - Performance metrics
 * - Multi-platform integration
 * - Real-time monitoring
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import ContentGenerator from './content-generator.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class AutomationOrchestrator {
  constructor() {
    this.config = {
      schedule: {
        contentGeneration: '0 9 * * *', // Daily at 9 AM
        socialMediaPosting: '0 12,18 * * *', // Daily at 12 PM and 6 PM
        analyticsUpdate: '0 23 * * *', // Daily at 11 PM
        cleanup: '0 2 * * 0', // Weekly on Sunday at 2 AM
      },
      limits: {
        maxDailyContent: 10,
        maxDailyPosts: 5,
        maxRetries: 3,
        timeout: 30000,
      },
      platforms: {
        youtube: { enabled: true, priority: 1 },
        instagram: { enabled: true, priority: 2 },
        tiktok: { enabled: true, priority: 3 },
        twitter: { enabled: true, priority: 4 },
        linkedin: { enabled: true, priority: 5 },
      },
    };

    this.contentGenerator = new ContentGenerator();
    this.metrics = {
      totalContentGenerated: 0,
      totalPostsPublished: 0,
      successRate: 0,
      averageProcessingTime: 0,
      lastRun: null,
      errors: [],
    };

    this.isRunning = false;
    this.currentTasks = new Map();
  }

  /**
   * Start the automation system
   */
  async start() {
    if (this.isRunning) {
      console.log('⚠️  Automation system is already running');
      return;
    }

    console.log('🚀 Starting Automation Orchestrator...');
    this.isRunning = true;

    try {
      await this.initialize();
      await this.loadMetrics();
      await this.startScheduler();

      console.log('✅ Automation system started successfully');
      console.log(
        `📊 Current metrics: ${JSON.stringify(this.metrics, null, 2)}`
      );
    } catch (error) {
      console.error('❌ Failed to start automation system:', error);
      this.isRunning = false;
      throw error;
    }
  }

  /**
   * Stop the automation system
   */
  async stop() {
    console.log('🛑 Stopping Automation Orchestrator...');
    this.isRunning = false;

    // Cancel all running tasks
    for (const [taskId, task] of this.currentTasks) {
      if (task.cancel) {
        task.cancel();
      }
      this.currentTasks.delete(taskId);
    }

    await this.saveMetrics();
    console.log('✅ Automation system stopped');
  }

  /**
   * Initialize the system
   */
  async initialize() {
    // Create necessary directories
    const dirs = [
      'artifacts/staging',
      'artifacts/published',
      'logs',
      'metrics',
      'backups',
    ];

    for (const dir of dirs) {
      await fs.mkdir(path.join(__dirname, '..', dir), { recursive: true });
    }

    // Load configuration
    await this.loadConfiguration();

    // Initialize content generator
    await this.contentGenerator.initialize?.();
  }

  /**
   * Load configuration from file
   */
  async loadConfiguration() {
    const configPath = path.join(__dirname, '..', 'config', 'automation.json');

    try {
      const configData = await fs.readFile(configPath, 'utf-8');
      this.config = { ...this.config, ...JSON.parse(configData) };
      console.log('📋 Configuration loaded');
    } catch (error) {
      console.log('📋 Using default configuration');
      await this.saveConfiguration();
    }
  }

  /**
   * Save configuration to file
   */
  async saveConfiguration() {
    const configPath = path.join(__dirname, '..', 'config', 'automation.json');
    await fs.mkdir(path.dirname(configPath), { recursive: true });
    await fs.writeFile(configPath, JSON.stringify(this.config, null, 2));
  }

  /**
   * Start the task scheduler
   */
  async startScheduler() {
    console.log('⏰ Starting task scheduler...');

    // Run initial tasks
    await this.runScheduledTasks();

    // Set up interval for regular checks
    this.schedulerInterval = setInterval(async () => {
      if (this.isRunning) {
        await this.runScheduledTasks();
      }
    }, 60000); // Check every minute
  }

  /**
   * Run scheduled tasks
   */
  async runScheduledTasks() {
    const now = new Date();
    const currentTime = now.toTimeString().split(' ')[0].substring(0, 5);

    // Check if it's time for content generation
    if (this.shouldRunTask('contentGeneration', currentTime)) {
      await this.scheduleTask('contentGeneration', () =>
        this.generateDailyContent()
      );
    }

    // Check if it's time for social media posting
    if (this.shouldRunTask('socialMediaPosting', currentTime)) {
      await this.scheduleTask('socialMediaPosting', () =>
        this.postToSocialMedia()
      );
    }

    // Check if it's time for analytics update
    if (this.shouldRunTask('analyticsUpdate', currentTime)) {
      await this.scheduleTask('analyticsUpdate', () => this.updateAnalytics());
    }

    // Check if it's time for cleanup
    if (this.shouldRunTask('cleanup', currentTime)) {
      await this.scheduleTask('cleanup', () => this.performCleanup());
    }
  }

  /**
   * Check if a task should run
   */
  shouldRunTask(taskName, currentTime) {
    const schedule = this.config.schedule[taskName];
    if (!schedule) return false;

    // Simple time-based check (in production, use a proper cron parser)
    const times = schedule.split(' ')[1].split(',');
    return times.includes(currentTime);
  }

  /**
   * Schedule a task for execution
   */
  async scheduleTask(taskName, taskFunction) {
    const taskId = `${taskName}_${Date.now()}`;

    console.log(`📅 Scheduling task: ${taskName}`);

    const task = {
      id: taskId,
      name: taskName,
      startTime: Date.now(),
      status: 'running',
      cancel: null,
    };

    this.currentTasks.set(taskId, task);

    try {
      const result = await taskFunction();
      task.status = 'completed';
      task.endTime = Date.now();
      task.duration = task.endTime - task.startTime;

      console.log(`✅ Task completed: ${taskName} (${task.duration}ms)`);
      this.updateMetrics(taskName, true, task.duration);

      return result;
    } catch (error) {
      task.status = 'failed';
      task.error = error.message;
      task.endTime = Date.now();
      task.duration = task.endTime - task.startTime;

      console.error(`❌ Task failed: ${taskName} - ${error.message}`);
      this.updateMetrics(taskName, false, task.duration, error);

      throw error;
    } finally {
      this.currentTasks.delete(taskId);
    }
  }

  /**
   * Generate daily content
   */
  async generateDailyContent() {
    console.log('📝 Generating daily content...');

    const topics = await this.getDailyTopics();
    const results = [];

    for (const topic of topics) {
      try {
        // Generate article
        const article = await this.contentGenerator.generateContent(
          topic,
          'article'
        );
        if (article.success) results.push(article);

        // Generate YouTube script
        const script = await this.contentGenerator.generateContent(
          topic,
          'youtube_script'
        );
        if (script.success) results.push(script);

        // Generate short script
        const short = await this.contentGenerator.generateContent(
          topic,
          'short_script'
        );
        if (short.success) results.push(short);

        // Small delay between topics
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error) {
        console.error(
          `❌ Failed to generate content for topic: ${topic}`,
          error
        );
      }
    }

    console.log(`✅ Generated ${results.length} pieces of content`);
    return results;
  }

  /**
   * Get daily topics from various sources
   */
  async getDailyTopics() {
    // In a real implementation, this would fetch from:
    // - RSS feeds
    // - Trending topics APIs
    // - User-defined topics
    // - AI-generated suggestions

    const defaultTopics = [
      'AI and Machine Learning Trends',
      'Remote Work Productivity Tips',
      'Sustainable Technology Solutions',
      'Digital Marketing Strategies',
      'Personal Development Techniques',
    ];

    // Return random selection of topics
    const shuffled = defaultTopics.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, 3); // Generate 3 topics per day
  }

  /**
   * Post to social media platforms
   */
  async postToSocialMedia() {
    console.log('📱 Posting to social media...');

    const content = await this.getContentForPosting();
    const results = [];

    for (const platform of Object.keys(this.config.platforms)) {
      if (this.config.platforms[platform].enabled) {
        try {
          const result = await this.postToPlatform(platform, content);
          results.push({ platform, success: true, result });
        } catch (error) {
          console.error(`❌ Failed to post to ${platform}:`, error);
          results.push({ platform, success: false, error: error.message });
        }
      }
    }

    console.log(
      `✅ Posted to ${results.filter(r => r.success).length} platforms`
    );
    return results;
  }

  /**
   * Get content ready for posting
   */
  async getContentForPosting() {
    const stagingDir = path.join(__dirname, '..', 'artifacts', 'staging');

    try {
      const files = await fs.readdir(stagingDir);
      const contentFiles = files.filter(f => f.endsWith('.txt'));

      if (contentFiles.length === 0) {
        throw new Error('No content available for posting');
      }

      // Get the most recent content file
      const latestFile = contentFiles.sort().pop();
      const contentPath = path.join(stagingDir, latestFile);
      const contentData = await fs.readFile(contentPath, 'utf-8');

      return JSON.parse(contentData);
    } catch (error) {
      console.error('❌ Failed to get content for posting:', error);
      throw error;
    }
  }

  /**
   * Post content to a specific platform
   */
  async postToPlatform(platform, content) {
    console.log(`📤 Posting to ${platform}...`);

    // Simulate platform posting
    await new Promise(resolve => setTimeout(resolve, 2000));

    // In a real implementation, this would:
    // - Format content for the platform
    // - Upload media if needed
    // - Use platform APIs to post
    // - Handle authentication
    // - Return posting results

    return {
      platform,
      postId: `post_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      url: `https://${platform}.com/post/${Date.now()}`,
      timestamp: new Date().toISOString(),
    };
  }

  /**
   * Update analytics and metrics
   */
  async updateAnalytics() {
    console.log('📊 Updating analytics...');

    // Simulate analytics update
    await new Promise(resolve => setTimeout(resolve, 1500));

    // In a real implementation, this would:
    // - Fetch data from platform APIs
    // - Update performance metrics
    // - Generate reports
    // - Store in database

    const analytics = {
      timestamp: new Date().toISOString(),
      views: Math.floor(Math.random() * 10000),
      likes: Math.floor(Math.random() * 1000),
      shares: Math.floor(Math.random() * 100),
      comments: Math.floor(Math.random() * 50),
      engagement: Math.random() * 10,
    };

    console.log(`✅ Analytics updated: ${JSON.stringify(analytics)}`);
    return analytics;
  }

  /**
   * Perform system cleanup
   */
  async performCleanup() {
    console.log('🧹 Performing system cleanup...');

    // Clean up old files
    await this.cleanupOldFiles();

    // Archive completed tasks
    await this.archiveCompletedTasks();

    // Update metrics
    await this.saveMetrics();

    console.log('✅ Cleanup completed');
  }

  /**
   * Clean up old files
   */
  async cleanupOldFiles() {
    const stagingDir = path.join(__dirname, '..', 'artifacts', 'staging');
    const publishedDir = path.join(__dirname, '..', 'artifacts', 'published');

    try {
      // Move old staging files to published
      const stagingFiles = await fs.readdir(stagingDir);
      const oldFiles = stagingFiles.filter(f => {
        const filePath = path.join(stagingDir, f);
        const stats = fs.stat(filePath);
        const age = Date.now() - stats.mtime.getTime();
        return age > 7 * 24 * 60 * 60 * 1000; // 7 days
      });

      for (const file of oldFiles) {
        const sourcePath = path.join(stagingDir, file);
        const destPath = path.join(publishedDir, file);
        await fs.rename(sourcePath, destPath);
      }

      console.log(`📁 Moved ${oldFiles.length} files to published`);
    } catch (error) {
      console.error('❌ Failed to cleanup files:', error);
    }
  }

  /**
   * Archive completed tasks
   */
  async archiveCompletedTasks() {
    // In a real implementation, this would archive task history
    console.log('📦 Archiving completed tasks...');
  }

  /**
   * Update metrics
   */
  updateMetrics(taskName, success, duration, error = null) {
    this.metrics.lastRun = new Date().toISOString();

    if (success) {
      this.metrics.totalContentGenerated++;
      this.metrics.totalPostsPublished++;
    } else {
      this.metrics.errors.push({
        task: taskName,
        error: error?.message || 'Unknown error',
        timestamp: new Date().toISOString(),
      });
    }

    // Update success rate
    const totalTasks =
      this.metrics.totalContentGenerated +
      this.metrics.totalPostsPublished +
      this.metrics.errors.length;
    this.metrics.successRate =
      totalTasks > 0
        ? (this.metrics.totalContentGenerated +
            this.metrics.totalPostsPublished) /
          totalTasks
        : 0;

    // Update average processing time
    this.metrics.averageProcessingTime =
      (this.metrics.averageProcessingTime + duration) / 2;
  }

  /**
   * Load metrics from file
   */
  async loadMetrics() {
    const metricsPath = path.join(
      __dirname,
      '..',
      'metrics',
      'automation-metrics.json'
    );

    try {
      const metricsData = await fs.readFile(metricsPath, 'utf-8');
      this.metrics = { ...this.metrics, ...JSON.parse(metricsData) };
    } catch (error) {
      console.log('📊 Using default metrics');
    }
  }

  /**
   * Save metrics to file
   */
  async saveMetrics() {
    const metricsPath = path.join(
      __dirname,
      '..',
      'metrics',
      'automation-metrics.json'
    );
    await fs.mkdir(path.dirname(metricsPath), { recursive: true });
    await fs.writeFile(metricsPath, JSON.stringify(this.metrics, null, 2));
  }

  /**
   * Get system status
   */
  getStatus() {
    return {
      isRunning: this.isRunning,
      currentTasks: Array.from(this.currentTasks.values()),
      metrics: this.metrics,
      config: this.config,
      uptime: this.isRunning ? Date.now() - this.startTime : 0,
    };
  }

  /**
   * Manual task execution
   */
  async executeTask(taskName, options = {}) {
    console.log(`🔧 Manually executing task: ${taskName}`);

    const tasks = {
      generateContent: () => this.generateDailyContent(),
      postSocial: () => this.postToSocialMedia(),
      updateAnalytics: () => this.updateAnalytics(),
      cleanup: () => this.performCleanup(),
    };

    if (!tasks[taskName]) {
      throw new Error(`Unknown task: ${taskName}`);
    }

    return await this.scheduleTask(`manual_${taskName}`, tasks[taskName]);
  }
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const orchestrator = new AutomationOrchestrator();

  const command = process.argv[2];
  const taskName = process.argv[3];

  switch (command) {
    case 'start':
      orchestrator
        .start()
        .then(() => {
          console.log('🎯 Automation system is running. Press Ctrl+C to stop.');
          process.on('SIGINT', async () => {
            await orchestrator.stop();
            process.exit(0);
          });
        })
        .catch(error => {
          console.error('❌ Failed to start:', error);
          process.exit(1);
        });
      break;

    case 'stop':
      orchestrator
        .stop()
        .then(() => process.exit(0))
        .catch(error => {
          console.error('❌ Failed to stop:', error);
          process.exit(1);
        });
      break;

    case 'status':
      console.log(
        '📊 System Status:',
        JSON.stringify(orchestrator.getStatus(), null, 2)
      );
      break;

    case 'execute':
      if (!taskName) {
        console.error('❌ Please provide a task name');
        process.exit(1);
      }
      orchestrator
        .executeTask(taskName)
        .then(result => {
          console.log(`✅ Task completed:`, result);
          process.exit(0);
        })
        .catch(error => {
          console.error(`❌ Task failed:`, error);
          process.exit(1);
        });
      break;

    default:
      console.log(`
🎯 Automation Orchestrator Usage:

Start system:
  node automation-orchestrator.js start

Stop system:
  node automation-orchestrator.js stop

Check status:
  node automation-orchestrator.js status

Execute task manually:
  node automation-orchestrator.js execute [taskName]

Available tasks: generateContent, postSocial, updateAnalytics, cleanup
      `);
  }
}

export default AutomationOrchestrator;
