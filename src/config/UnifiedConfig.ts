/**
 * Unified Configuration System
 * 
 * Manages API keys, settings, and environment variables for all four platforms:
 * - Cursor AI
 * - Bolt.diy  
 * - Firebase
 * - Trae.ai
 * 
 * Provides secure credential management and environment-specific configurations.
 */

import { EventEmitter } from 'events';

// Platform-specific configuration interfaces
interface CursorConfig {
  enabled: boolean;
  apiKey?: string;
  baseUrl: string;
  websocketUrl: string;
  timeout: number;
  retryAttempts: number;
  features: {
    codeCompletion: boolean;
    realTimeSync: boolean;
    aiAssistance: boolean;
  };
}

interface BoltDiyConfig {
  enabled: boolean;
  apiKey?: string;
  baseUrl: string;
  websocketUrl: string;
  projectId?: string;
  timeout: number;
  retryAttempts: number;
  features: {
    componentLibrary: boolean;
    deployment: boolean;
    realTimeSync: boolean;
    previewEnvironment: boolean;
  };
}

interface FirebaseConfig {
  enabled: boolean;
  apiKey?: string;
  authDomain?: string;
  projectId: string;
  storageBucket?: string;
  messagingSenderId?: string;
  appId?: string;
  measurementId?: string;
  websocketUrl: string;
  timeout: number;
  retryAttempts: number;
  features: {
    authentication: boolean;
    firestore: boolean;
    storage: boolean;
    hosting: boolean;
    functions: boolean;
    realTimeSync: boolean;
  };
}

interface TraeAiConfig {
  enabled: boolean;
  apiKey?: string;
  baseUrl: string;
  websocketUrl: string;
  workspaceId?: string;
  timeout: number;
  retryAttempts: number;
  features: {
    codeGeneration: boolean;
    projectManagement: boolean;
    realTimeSync: boolean;
    aiOrchestration: boolean;
  };
}

// Unified configuration interface
interface UnifiedPlatformConfig {
  environment: 'development' | 'staging' | 'production';
  debug: boolean;
  logLevel: 'error' | 'warn' | 'info' | 'debug';
  
  // Global sync settings
  sync: {
    enabled: boolean;
    interval: number;
    retryAttempts: number;
    conflictResolution: 'manual' | 'auto-merge' | 'last-write-wins';
    enableRealTime: boolean;
  };

  // Security settings
  security: {
    encryptCredentials: boolean;
    tokenRefreshInterval: number;
    sessionTimeout: number;
    enableMFA: boolean;
  };

  // Platform configurations
  platforms: {
    cursor: CursorConfig;
    boltDiy: BoltDiyConfig;
    firebase: FirebaseConfig;
    traeAi: TraeAiConfig;
  };

  // Integration settings
  integration: {
    enableCrossPlatformSync: boolean;
    syncConflictStrategy: 'merge' | 'overwrite' | 'prompt';
    enableEventBroadcasting: boolean;
    maxConcurrentConnections: number;
  };
}

// Configuration validation interface
interface ConfigValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
  missingCredentials: string[];
}

// Environment variable mappings
const ENV_MAPPINGS = {
  // Cursor
  CURSOR_API_KEY: 'platforms.cursor.apiKey',
  CURSOR_BASE_URL: 'platforms.cursor.baseUrl',
  CURSOR_WS_URL: 'platforms.cursor.websocketUrl',
  
  // Bolt.diy
  BOLT_DIY_API_KEY: 'platforms.boltDiy.apiKey',
  BOLT_DIY_BASE_URL: 'platforms.boltDiy.baseUrl',
  BOLT_DIY_WS_URL: 'platforms.boltDiy.websocketUrl',
  BOLT_DIY_PROJECT_ID: 'platforms.boltDiy.projectId',
  
  // Firebase
  FIREBASE_API_KEY: 'platforms.firebase.apiKey',
  FIREBASE_AUTH_DOMAIN: 'platforms.firebase.authDomain',
  FIREBASE_PROJECT_ID: 'platforms.firebase.projectId',
  FIREBASE_STORAGE_BUCKET: 'platforms.firebase.storageBucket',
  FIREBASE_MESSAGING_SENDER_ID: 'platforms.firebase.messagingSenderId',
  FIREBASE_APP_ID: 'platforms.firebase.appId',
  FIREBASE_MEASUREMENT_ID: 'platforms.firebase.measurementId',
  FIREBASE_WS_URL: 'platforms.firebase.websocketUrl',
  
  // Trae.ai
  TRAE_AI_API_KEY: 'platforms.traeAi.apiKey',
  TRAE_AI_BASE_URL: 'platforms.traeAi.baseUrl',
  TRAE_AI_WS_URL: 'platforms.traeAi.websocketUrl',
  TRAE_AI_WORKSPACE_ID: 'platforms.traeAi.workspaceId',
  
  // Global settings
  NODE_ENV: 'environment',
  DEBUG: 'debug',
  LOG_LEVEL: 'logLevel'
};

class UnifiedConfigManager extends EventEmitter {
  private config: UnifiedPlatformConfig;
  private configPath: string;
  private encryptionKey?: string;
  private watchers: Map<string, NodeJS.Timeout> = new Map();

  constructor(configPath?: string) {
    super();
    this.configPath = configPath || './config/unified-config.json';
    this.config = this.getDefaultConfig();
    this.loadEnvironmentVariables();
  }

  /**
   * Get default configuration
   */
  private getDefaultConfig(): UnifiedPlatformConfig {
    return {
      environment: 'development',
      debug: false,
      logLevel: 'info',
      
      sync: {
        enabled: true,
        interval: 5000,
        retryAttempts: 3,
        conflictResolution: 'manual',
        enableRealTime: true
      },

      security: {
        encryptCredentials: true,
        tokenRefreshInterval: 3600000, // 1 hour
        sessionTimeout: 86400000, // 24 hours
        enableMFA: false
      },

      platforms: {
        cursor: {
          enabled: false,
          baseUrl: 'https://api.cursor.sh',
          websocketUrl: 'wss://ws.cursor.sh',
          timeout: 30000,
          retryAttempts: 3,
          features: {
            codeCompletion: true,
            realTimeSync: true,
            aiAssistance: true
          }
        },

        boltDiy: {
          enabled: false,
          baseUrl: 'https://api.bolt.diy',
          websocketUrl: 'wss://ws.bolt.diy',
          timeout: 30000,
          retryAttempts: 3,
          features: {
            componentLibrary: true,
            deployment: true,
            realTimeSync: true,
            previewEnvironment: true
          }
        },

        firebase: {
          enabled: false,
          projectId: '',
          websocketUrl: 'wss://ws.firebase.google.com',
          timeout: 30000,
          retryAttempts: 3,
          features: {
            authentication: true,
            firestore: true,
            storage: true,
            hosting: true,
            functions: true,
            realTimeSync: true
          }
        },

        traeAi: {
          enabled: false,
          baseUrl: 'https://api.trae.ai',
          websocketUrl: 'wss://ws.trae.ai',
          timeout: 30000,
          retryAttempts: 3,
          features: {
            codeGeneration: true,
            projectManagement: true,
            realTimeSync: true,
            aiOrchestration: true
          }
        }
      },

      integration: {
        enableCrossPlatformSync: true,
        syncConflictStrategy: 'merge',
        enableEventBroadcasting: true,
        maxConcurrentConnections: 10
      }
    };
  }

  /**
   * Load configuration from environment variables
   */
  private loadEnvironmentVariables(): void {
    for (const [envVar, configPath] of Object.entries(ENV_MAPPINGS)) {
      const value = process.env[envVar];
      if (value) {
        this.setNestedValue(this.config, configPath, this.parseEnvValue(value));
      }
    }

    // Set environment-specific defaults
    if (this.config.environment === 'production') {
      this.config.debug = false;
      this.config.security.encryptCredentials = true;
      this.config.security.enableMFA = true;
    } else if (this.config.environment === 'development') {
      this.config.debug = true;
      this.config.logLevel = 'debug';
    }
  }

  /**
   * Parse environment variable value
   */
  private parseEnvValue(value: string): any {
    // Handle boolean values
    if (value.toLowerCase() === 'true') return true;
    if (value.toLowerCase() === 'false') return false;
    
    // Handle numeric values
    if (!isNaN(Number(value))) return Number(value);
    
    // Return as string
    return value;
  }

  /**
   * Set nested object value using dot notation
   */
  private setNestedValue(obj: any, path: string, value: any): void {
    const keys = path.split('.');
    let current = obj;
    
    for (let i = 0; i < keys.length - 1; i++) {
      if (!(keys[i] in current)) {
        current[keys[i]] = {};
      }
      current = current[keys[i]];
    }
    
    current[keys[keys.length - 1]] = value;
  }

  /**
   * Get nested object value using dot notation
   */
  private getNestedValue(obj: any, path: string): any {
    return path.split('.').reduce((current, key) => current?.[key], obj);
  }

  /**
   * Load configuration from file
   */
  async loadConfig(filePath?: string): Promise<void> {
    const path = filePath || this.configPath;
    
    try {
      // In a real implementation, you would read from file system
      // For now, we'll simulate loading from localStorage or a mock
      const configData = this.loadFromStorage(path);
      
      if (configData) {
        this.config = { ...this.config, ...configData };
        this.emit('configLoaded', { path, config: this.config });
      }
    } catch (error) {
      console.error('Failed to load config:', error);
      this.emit('configError', { error, path });
    }
  }

  /**
   * Save configuration to file
   */
  async saveConfig(filePath?: string): Promise<void> {
    const path = filePath || this.configPath;
    
    try {
      // In a real implementation, you would write to file system
      this.saveToStorage(path, this.config);
      this.emit('configSaved', { path, config: this.config });
    } catch (error) {
      console.error('Failed to save config:', error);
      this.emit('configError', { error, path });
    }
  }

  /**
   * Mock storage operations (replace with actual file I/O in production)
   */
  private loadFromStorage(path: string): Partial<UnifiedPlatformConfig> | null {
    if (typeof localStorage !== 'undefined') {
      const stored = localStorage.getItem(`unified-config-${path}`);
      return stored ? JSON.parse(stored) : null;
    }
    return null;
  }

  private saveToStorage(path: string, config: UnifiedPlatformConfig): void {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(`unified-config-${path}`, JSON.stringify(config));
    }
  }

  /**
   * Get current configuration
   */
  getConfig(): UnifiedPlatformConfig {
    return { ...this.config };
  }

  /**
   * Get platform-specific configuration
   */
  getPlatformConfig<T extends keyof UnifiedPlatformConfig['platforms']>(
    platform: T
  ): UnifiedPlatformConfig['platforms'][T] {
    return { ...this.config.platforms[platform] };
  }

  /**
   * Update platform configuration
   */
  updatePlatformConfig<T extends keyof UnifiedPlatformConfig['platforms']>(
    platform: T,
    updates: Partial<UnifiedPlatformConfig['platforms'][T]>
  ): void {
    this.config.platforms[platform] = {
      ...this.config.platforms[platform],
      ...updates
    };

    this.emit('platformConfigUpdated', { platform, config: this.config.platforms[platform] });
  }

  /**
   * Enable/disable platform
   */
  setPlatformEnabled(platform: keyof UnifiedPlatformConfig['platforms'], enabled: boolean): void {
    this.config.platforms[platform].enabled = enabled;
    this.emit('platformToggled', { platform, enabled });
  }

  /**
   * Set API key for platform
   */
  setPlatformApiKey(platform: keyof UnifiedPlatformConfig['platforms'], apiKey: string): void {
    this.config.platforms[platform].apiKey = apiKey;
    this.emit('apiKeyUpdated', { platform });
  }

  /**
   * Validate configuration
   */
  validateConfig(): ConfigValidationResult {
    const result: ConfigValidationResult = {
      isValid: true,
      errors: [],
      warnings: [],
      missingCredentials: []
    };

    // Check enabled platforms have required credentials
    for (const [platformName, platformConfig] of Object.entries(this.config.platforms)) {
      if (platformConfig.enabled) {
        if (!platformConfig.apiKey) {
          result.missingCredentials.push(`${platformName}.apiKey`);
        }

        // Platform-specific validations
        if (platformName === 'firebase') {
          const fbConfig = platformConfig as FirebaseConfig;
          if (!fbConfig.projectId) {
            result.errors.push('Firebase project ID is required');
          }
        }

        if (platformName === 'boltDiy') {
          const boltConfig = platformConfig as BoltDiyConfig;
          if (boltConfig.features.deployment && !boltConfig.projectId) {
            result.warnings.push('Bolt.diy project ID recommended for deployment features');
          }
        }
      }
    }

    // Check sync configuration
    if (this.config.sync.enabled && this.config.sync.interval < 1000) {
      result.warnings.push('Sync interval less than 1 second may cause performance issues');
    }

    // Check security settings
    if (this.config.environment === 'production' && !this.config.security.encryptCredentials) {
      result.errors.push('Credential encryption must be enabled in production');
    }

    result.isValid = result.errors.length === 0;
    return result;
  }

  /**
   * Get enabled platforms
   */
  getEnabledPlatforms(): Array<keyof UnifiedPlatformConfig['platforms']> {
    return Object.entries(this.config.platforms)
      .filter(([_, config]) => config.enabled)
      .map(([name, _]) => name as keyof UnifiedPlatformConfig['platforms']);
  }

  /**
   * Check if platform is enabled
   */
  isPlatformEnabled(platform: keyof UnifiedPlatformConfig['platforms']): boolean {
    return this.config.platforms[platform].enabled;
  }

  /**
   * Get sync configuration for UnifiedSyncService
   */
  getSyncConfig(): {
    enableRealTimeSync: boolean;
    syncInterval: number;
    retryAttempts: number;
    platforms: Record<string, {
      enabled: boolean;
      websocketUrl: string;
      apiKey?: string;
      projectId?: string;
    }>;
  } {
    return {
      enableRealTimeSync: this.config.sync.enableRealTime,
      syncInterval: this.config.sync.interval,
      retryAttempts: this.config.sync.retryAttempts,
      platforms: {
        cursor: {
          enabled: this.config.platforms.cursor.enabled,
          websocketUrl: this.config.platforms.cursor.websocketUrl,
          apiKey: this.config.platforms.cursor.apiKey
        },
        boltDiy: {
          enabled: this.config.platforms.boltDiy.enabled,
          websocketUrl: this.config.platforms.boltDiy.websocketUrl,
          apiKey: this.config.platforms.boltDiy.apiKey,
          projectId: this.config.platforms.boltDiy.projectId
        },
        firebase: {
          enabled: this.config.platforms.firebase.enabled,
          websocketUrl: this.config.platforms.firebase.websocketUrl,
          apiKey: this.config.platforms.firebase.apiKey,
          projectId: this.config.platforms.firebase.projectId
        },
        traeAi: {
          enabled: this.config.platforms.traeAi.enabled,
          websocketUrl: this.config.platforms.traeAi.websocketUrl,
          apiKey: this.config.platforms.traeAi.apiKey
        }
      }
    };
  }

  /**
   * Watch for configuration changes
   */
  watchConfig(callback: (config: UnifiedPlatformConfig) => void): string {
    const watcherId = `watcher-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const watcher = setInterval(() => {
      callback(this.getConfig());
    }, 5000);

    this.watchers.set(watcherId, watcher);
    return watcherId;
  }

  /**
   * Stop watching configuration changes
   */
  unwatchConfig(watcherId: string): void {
    const watcher = this.watchers.get(watcherId);
    if (watcher) {
      clearInterval(watcher);
      this.watchers.delete(watcherId);
    }
  }

  /**
   * Reset configuration to defaults
   */
  resetToDefaults(): void {
    this.config = this.getDefaultConfig();
    this.loadEnvironmentVariables();
    this.emit('configReset', { config: this.config });
  }

  /**
   * Export configuration (without sensitive data)
   */
  exportConfig(includeSensitive = false): Partial<UnifiedPlatformConfig> {
    const exported = { ...this.config };
    
    if (!includeSensitive) {
      // Remove API keys and other sensitive data
      for (const platform of Object.values(exported.platforms)) {
        delete platform.apiKey;
      }
    }
    
    return exported;
  }

  /**
   * Import configuration
   */
  importConfig(config: Partial<UnifiedPlatformConfig>): void {
    this.config = { ...this.config, ...config };
    this.emit('configImported', { config: this.config });
  }

  /**
   * Cleanup resources
   */
  destroy(): void {
    // Clear all watchers
    for (const watcher of this.watchers.values()) {
      clearInterval(watcher);
    }
    this.watchers.clear();

    // Remove all listeners
    this.removeAllListeners();
  }
}

// Create singleton instance
const unifiedConfig = new UnifiedConfigManager();

export { 
  UnifiedConfigManager, 
  unifiedConfig,
  type UnifiedPlatformConfig,
  type CursorConfig,
  type BoltDiyConfig,
  type FirebaseConfig,
  type TraeAiConfig,
  type ConfigValidationResult
};