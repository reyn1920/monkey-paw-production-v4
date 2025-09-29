import { firebaseService, FirebaseConfig } from './FirebaseService';
import { traeAIService, TraeAIConfig } from './TraeAIService';
import { syncService, SyncConfig } from './SyncService';
import toast from 'react-hot-toast';

export interface IntegrationConfig {
  cursor?: {
    apiKey: string;
    projectPath?: string;
  };
  boltdiy?: {
    token: string;
    projectId?: string;
  };
  firebase?: FirebaseConfig;
  traeai?: TraeAIConfig;
}

export interface SyncResult {
  success: boolean;
  message: string;
  timestamp: string;
  details?: any;
}

export interface IntegrationStatus {
  connected: boolean;
  lastSync?: string;
  error?: string;
  config?: any;
  health?: 'healthy' | 'warning' | 'error';
  version?: string;
}

export class IntegrationService {
  private integrations: Map<string, IntegrationStatus> = new Map();
  private syncEnabled: boolean = false;

  constructor() {
    // Initialize with default statuses
    this.integrations.set('cursor', { connected: false });
    this.integrations.set('boltdiy', { connected: false });
    this.integrations.set('firebase', { connected: false });
    this.integrations.set('traeai', { connected: false });
  }

  // Connection management with enhanced error handling
  async connect(platform: string, config: any): Promise<SyncResult> {
    const loadingToast = toast.loading(`Connecting to ${platform}...`);
    
    try {
      let result: { success: boolean; error?: string } = { success: false };

      switch (platform) {
        case 'cursor':
          result = await this.connectCursor(config);
          break;
        case 'boltdiy':
          result = await this.connectBoltDiy(config);
          break;
        case 'firebase':
          result = await this.connectFirebase(config);
          break;
        case 'traeai':
          result = await this.connectTraeAI(config);
          break;
        default:
          toast.dismiss(loadingToast);
          toast.error(`Unknown platform: ${platform}`);
          return {
            success: false,
            message: `Unknown platform: ${platform}`,
            timestamp: new Date().toISOString()
          };
      }

      if (result.success) {
        this.integrations.set(platform, {
          connected: true,
          lastSync: new Date().toISOString(),
          config,
          health: 'healthy'
        });

        // Initialize sync service if multiple platforms are connected
        await this.initializeSyncIfReady();

        toast.dismiss(loadingToast);
        toast.success(`Successfully connected to ${platform}`);

        return {
          success: true,
          message: `Successfully connected to ${platform}`,
          timestamp: new Date().toISOString()
        };
      } else {
        this.integrations.set(platform, {
          connected: false,
          error: result.error || 'Connection failed',
          health: 'error'
        });

        toast.dismiss(loadingToast);
        toast.error(`Failed to connect to ${platform}: ${result.error || 'Unknown error'}`);

        return {
          success: false,
          message: result.error || `Failed to connect to ${platform}`,
          timestamp: new Date().toISOString()
        };
      }
    } catch (error: any) {
      toast.dismiss(loadingToast);
      toast.error(`Connection error: ${error.message || 'Unknown error'}`);
      
      this.integrations.set(platform, {
        connected: false,
        error: error.message || 'Connection failed',
        health: 'error'
      });

      return {
        success: false,
        message: error.message || `Failed to connect to ${platform}`,
        timestamp: new Date().toISOString(),
        details: error
      };
    }
  }

  async disconnect(platform: string): Promise<SyncResult> {
    const loadingToast = toast.loading(`Disconnecting from ${platform}...`);
    
    try {
      this.integrations.set(platform, { connected: false });
      
      toast.dismiss(loadingToast);
      toast.success(`Disconnected from ${platform}`);

      return {
        success: true,
        message: `Successfully disconnected from ${platform}`,
        timestamp: new Date().toISOString()
      };
    } catch (error: any) {
      toast.dismiss(loadingToast);
      toast.error(`Failed to disconnect from ${platform}: ${error.message}`);

      return {
        success: false,
        message: error.message || `Failed to disconnect from ${platform}`,
        timestamp: new Date().toISOString()
      };
    }
  }

  // Platform-specific connection methods
  // Connection methods - made public for external access
  async connectCursor(config: any): Promise<SyncResult> {
    // Simulate Cursor IDE connection
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    if (!config.apiKey) {
      return { 
        success: false, 
        message: 'API Key is required for Cursor IDE',
        timestamp: new Date().toISOString()
      };
    }

    // Simulate API validation
    if (config.apiKey.length < 10) {
      return { 
        success: false, 
        message: 'Invalid API Key format',
        timestamp: new Date().toISOString()
      };
    }

    return { 
      success: true,
      message: 'Successfully connected to Cursor IDE',
      timestamp: new Date().toISOString()
    };
  }

  async connectBoltDiy(config: any): Promise<SyncResult> {
    // Simulate Bolt.diy connection
    await new Promise(resolve => setTimeout(resolve, 800));
    
    if (!config.token) {
      return { 
        success: false, 
        message: 'Auth Token is required for Bolt.diy',
        timestamp: new Date().toISOString()
      };
    }

    // Simulate token validation
    if (config.token.length < 20) {
      return { 
        success: false, 
        message: 'Invalid Auth Token format',
        timestamp: new Date().toISOString()
      };
    }

    return { 
      success: true,
      message: 'Successfully connected to Bolt.diy',
      timestamp: new Date().toISOString()
    };
  }

  async connectFirebase(config: FirebaseConfig): Promise<SyncResult> {
    try {
      const success = await firebaseService.initialize(config);
      if (success) {
        return { 
          success: true,
          message: 'Successfully connected to Firebase',
          timestamp: new Date().toISOString()
        };
      } else {
        return { 
          success: false, 
          message: 'Firebase initialization failed',
          timestamp: new Date().toISOString()
        };
      }
    } catch (error: any) {
      return { 
        success: false, 
        message: error.message || 'Firebase connection failed',
        timestamp: new Date().toISOString()
      };
    }
  }

  // Add missing connectTraeAi method (note the lowercase 'i' to match usage)
  async connectTraeAi(config: TraeAIConfig): Promise<SyncResult> {
    return this.connectTraeAI(config);
  }

  async connectTraeAI(config: TraeAIConfig): Promise<SyncResult> {
    try {
      const result = await traeAIService.connect(config);
      if (result.success) {
        return {
          success: true,
          message: 'Successfully connected to Trae.ai',
          timestamp: new Date().toISOString()
        };
      } else {
        return {
          success: false,
          message: result.error || 'Failed to connect to Trae.ai',
          timestamp: new Date().toISOString()
        };
      }
    } catch (error: any) {
      return { 
        success: false, 
        message: error.message || 'Trae.ai connection failed',
        timestamp: new Date().toISOString()
      };
    }
  }

  // Synchronization
  // Sync operations with enhanced error handling
  async sync(platform: string): Promise<SyncResult> {
    const loadingToast = toast.loading(`Syncing ${platform}...`);
    
    try {
      const status = this.integrations.get(platform);
      if (!status?.connected) {
        toast.dismiss(loadingToast);
        toast.error(`${platform} is not connected`);
        return {
          success: false,
          message: `${platform} is not connected`,
          timestamp: new Date().toISOString()
        };
      }

      let syncSuccess = false;
      let errorMessage = '';

      switch (platform) {
        case 'cursor':
          syncSuccess = await this.syncCursor();
          break;
        case 'boltdiy':
          syncSuccess = await this.syncBoltDiy();
          break;
        case 'firebase':
          syncSuccess = await this.syncFirebase();
          break;
        case 'traeai':
          syncSuccess = await this.syncTraeAI();
          break;
        default:
          toast.dismiss(loadingToast);
          toast.error(`Unknown platform: ${platform}`);
          return {
            success: false,
            message: `Unknown platform: ${platform}`,
            timestamp: new Date().toISOString()
          };
      }

      if (syncSuccess) {
        this.integrations.set(platform, {
          ...status,
          lastSync: new Date().toISOString(),
          health: 'healthy',
          error: undefined
        });

        toast.dismiss(loadingToast);
        toast.success(`Successfully synced ${platform}`);

        return {
          success: true,
          message: `Successfully synced ${platform}`,
          timestamp: new Date().toISOString()
        };
      } else {
        this.integrations.set(platform, {
          ...status,
          health: 'warning',
          error: 'Sync failed'
        });

        toast.dismiss(loadingToast);
        toast.error(`Failed to sync ${platform}`);

        return {
          success: false,
          message: `Failed to sync ${platform}`,
          timestamp: new Date().toISOString()
        };
      }
    } catch (error: any) {
      const status = this.integrations.get(platform);
      if (status) {
        this.integrations.set(platform, {
          ...status,
          health: 'error',
          error: error.message || 'Sync error'
        });
      }

      toast.dismiss(loadingToast);
      toast.error(`Sync error for ${platform}: ${error.message || 'Unknown error'}`);

      return {
        success: false,
        message: error.message || `Sync failed for ${platform}`,
        timestamp: new Date().toISOString(),
        details: error
      };
    }
  }

  async syncAll(): Promise<SyncResult[]> {
    const loadingToast = toast.loading('Syncing all platforms...');
    
    try {
      const connectedPlatforms = this.getConnectedPlatforms();
      
      if (connectedPlatforms.length === 0) {
        toast.dismiss(loadingToast);
        toast.error('No platforms connected');
        return [{
          success: false,
          message: 'No platforms connected',
          timestamp: new Date().toISOString()
        }];
      }

      const results = await Promise.allSettled(
        connectedPlatforms.map(platform => this.sync(platform))
      );

      const syncResults = results.map((result, index) => {
        if (result.status === 'fulfilled') {
          return result.value;
        } else {
          return {
            success: false,
            message: `Failed to sync ${connectedPlatforms[index]}: ${result.reason}`,
            timestamp: new Date().toISOString(),
            details: result.reason
          };
        }
      });

      const successCount = syncResults.filter(r => r.success).length;
      const totalCount = syncResults.length;

      toast.dismiss(loadingToast);
      
      if (successCount === totalCount) {
        toast.success(`Successfully synced all ${totalCount} platforms`);
      } else if (successCount > 0) {
        toast.success(`Synced ${successCount}/${totalCount} platforms`, {
          icon: '⚠️'
        });
      } else {
        toast.error('Failed to sync all platforms');
      }

      return syncResults;
    } catch (error: any) {
      toast.dismiss(loadingToast);
      toast.error(`Sync all failed: ${error.message || 'Unknown error'}`);
      
      return [{
        success: false,
        message: error.message || 'Sync all failed',
        timestamp: new Date().toISOString(),
        details: error
      }];
    }
  }

  // Platform-specific sync methods
  private async syncCursor(): Promise<boolean> {
    // Simulate Cursor IDE sync
    await new Promise(resolve => setTimeout(resolve, 500));
    return Math.random() > 0.1; // 90% success rate
  }

  private async syncBoltDiy(): Promise<boolean> {
    // Simulate Bolt.diy sync
    await new Promise(resolve => setTimeout(resolve, 600));
    return Math.random() > 0.1; // 90% success rate
  }

  private async syncFirebase(): Promise<boolean> {
    try {
      return await firebaseService.testConnection();
    } catch (error) {
      return false;
    }
  }

  private async syncTraeAI(): Promise<boolean> {
    try {
      return await traeAIService.testConnection();
    } catch (error) {
      return false;
    }
  }

  // Sync service initialization
  private async initializeSyncIfReady(): Promise<void> {
    const connectedPlatforms = Array.from(this.integrations.entries())
      .filter(([_, status]) => status.connected);

    if (connectedPlatforms.length >= 2 && !this.syncEnabled) {
      try {
        // Create sync configuration
        const syncConfig: SyncConfig = {
          projectId: 'stackbuilder_project',
          platforms: {
            cursor: {
              enabled: this.integrations.get('cursor')?.connected || false,
              apiKey: this.integrations.get('cursor')?.config?.apiKey,
              projectPath: this.integrations.get('cursor')?.config?.projectPath
            },
            boltdiy: {
              enabled: this.integrations.get('boltdiy')?.connected || false,
              token: this.integrations.get('boltdiy')?.config?.token,
              projectId: this.integrations.get('boltdiy')?.config?.projectId
            },
            firebase: {
              enabled: this.integrations.get('firebase')?.connected || false,
              projectId: this.integrations.get('firebase')?.config?.projectId
            },
            traeai: {
              enabled: this.integrations.get('traeai')?.connected || false,
              apiKey: this.integrations.get('traeai')?.config?.apiKey,
              projectId: this.integrations.get('traeai')?.config?.organizationId
            }
          },
          syncInterval: 30000, // 30 seconds
          conflictResolution: 'latest'
        };

        const initialized = await syncService.initialize(syncConfig);
        if (initialized) {
          await syncService.start();
          this.syncEnabled = true;
          console.log('Sync service initialized and started');
        }
      } catch (error) {
        console.error('Failed to initialize sync service:', error);
      }
    }
  }

  // Status and monitoring
  // Add missing methods for external access
  async disconnectIntegration(platform: string): Promise<SyncResult> {
    return this.disconnect(platform);
  }

  async syncIntegration(platform: string): Promise<SyncResult> {
    return this.sync(platform);
  }

  async syncAllIntegrations(): Promise<SyncResult[]> {
    return this.syncAll();
  }

  getStatus(platform: string): IntegrationStatus {
    return this.integrations.get(platform) || { connected: false };
  }

  getAllStatuses(): Map<string, IntegrationStatus> {
    return new Map(this.integrations);
  }

  getConnectedPlatforms(): string[] {
    return Array.from(this.integrations.entries())
      .filter(([_, status]) => status.connected)
      .map(([platform, _]) => platform);
  }

  isSyncEnabled(): boolean {
    return this.syncEnabled;
  }

  getSyncStatus() {
    return syncService.getStatus();
  }

  // Configuration management
  async updateConfig(platform: string, config: any): Promise<SyncResult> {
    const status = this.integrations.get(platform);
    
    if (!status?.connected) {
      return {
        success: false,
        message: `${platform} is not connected`,
        timestamp: new Date().toISOString()
      };
    }

    try {
      // Update the configuration
      this.integrations.set(platform, {
        ...status,
        config: { ...status.config, ...config }
      });

      return {
        success: true,
        message: `Configuration updated for ${platform}`,
        timestamp: new Date().toISOString()
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.message || 'Configuration update failed',
        timestamp: new Date().toISOString()
      };
    }
  }

  // Cross-platform project management
  async createProject(name: string, description: string, framework: string): Promise<{ success: boolean; projectIds: { [platform: string]: string } }> {
    const connectedPlatforms = this.getConnectedPlatforms();
    const projectIds: { [platform: string]: string } = {};
    
    for (const platform of connectedPlatforms) {
      try {
        let projectId: string | null = null;

        switch (platform) {
          case 'firebase':
            if (firebaseService.isAuthenticated()) {
              projectId = await firebaseService.createProject({
                name,
                description,
                files: {},
                integrations: {
                  cursor: connectedPlatforms.includes('cursor'),
                  boltdiy: connectedPlatforms.includes('boltdiy'),
                  traeai: connectedPlatforms.includes('traeai'),
                  firebase: connectedPlatforms.includes('firebase'),
                  vscode: connectedPlatforms.includes('vscode'),
                  windsurf: connectedPlatforms.includes('windsurf')
                }
              });
            }
            break;
          case 'traeai':
            if (traeAIService.isAuthenticated()) {
              projectId = await traeAIService.createProject({
                name,
                description,
                framework,
                files: {}
              });
            }
            break;
        }

        if (projectId) {
          projectIds[platform] = projectId;
        }
      } catch (error) {
        console.error(`Failed to create project in ${platform}:`, error);
      }
    }

    return {
      success: Object.keys(projectIds).length > 0,
      projectIds
    };
  }
}

// Export singleton instance
export const integrationService = new IntegrationService();