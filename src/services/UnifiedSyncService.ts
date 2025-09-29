/**
 * Unified Synchronization Service
 * 
 * This service orchestrates real-time synchronization between all four platforms:
 * - Cursor AI
 * - Bolt.diy
 * - Firebase
 * - Trae.ai
 * 
 * Uses WebSocket connections for real-time communication and event broadcasting.
 */

import { EventEmitter } from 'events';

// Use browser WebSocket API or Node.js ws module
interface WebSocketLike {
  send(data: string, callback?: (error?: Error) => void): void;
  close(): void;
  on(event: string, listener: (...args: any[]) => void): void;
  readyState: number;
}

// Platform connection interfaces
interface PlatformConnection {
  id: string;
  platform: 'cursor' | 'bolt-diy' | 'firebase' | 'trae-ai';
  websocket: WebSocketLike | null;
  status: 'connecting' | 'connected' | 'disconnected' | 'error' | 'reconnecting';
  lastActivity: Date;
  retryCount: number;
  maxRetries: number;
  metadata: Record<string, any>;
}

interface SyncEvent {
  id: string;
  type: 'file_change' | 'project_update' | 'deployment' | 'build' | 'auth' | 'config';
  platform: string;
  timestamp: Date;
  data: any;
  targets?: string[]; // Specific platforms to sync to
}

interface SyncConfig {
  enableRealTimeSync: boolean;
  syncInterval: number;
  retryAttempts: number;
  platforms: {
    cursor: {
      enabled: boolean;
      websocketUrl: string;
      apiKey?: string;
    };
    boltDiy: {
      enabled: boolean;
      websocketUrl: string;
      apiKey?: string;
    };
    firebase: {
      enabled: boolean;
      websocketUrl: string;
      projectId: string;
      apiKey?: string;
    };
    traeAi: {
      enabled: boolean;
      websocketUrl: string;
      apiKey?: string;
    };
  };
}

class UnifiedSyncService extends EventEmitter {
  private connections: Map<string, PlatformConnection> = new Map();
  private syncQueue: SyncEvent[] = [];
  private isProcessing = false;
  private config: SyncConfig;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private reconnectTimeouts: Map<string, NodeJS.Timeout> = new Map();

  constructor(config: SyncConfig) {
    super();
    this.config = config;
    this.setupEventHandlers();
  }

  /**
   * Initialize all platform connections
   */
  async initialize(): Promise<void> {
    console.log('🚀 Initializing Unified Sync Service...');
    
    // Initialize connections for each enabled platform
    const platforms = Object.keys(this.config.platforms) as Array<keyof typeof this.config.platforms>;
    
    for (const platform of platforms) {
      if (this.config.platforms[platform].enabled) {
        await this.connectToPlatform(platform);
      }
    }

    // Start heartbeat monitoring
    this.startHeartbeat();
    
    // Start processing sync queue
    this.startSyncProcessor();

    this.emit('initialized', { 
      connectedPlatforms: Array.from(this.connections.keys()),
      timestamp: new Date()
    });
  }

  /**
   * Connect to a specific platform
   */
  private async connectToPlatform(platform: keyof typeof this.config.platforms): Promise<void> {
    const platformConfig = this.config.platforms[platform];
    const connectionId = `${platform}-${Date.now()}`;

    const connection: PlatformConnection = {
      id: connectionId,
      platform: platform as any,
      websocket: null,
      status: 'connecting',
      lastActivity: new Date(),
      retryCount: 0,
      maxRetries: this.config.retryAttempts,
      metadata: {}
    };

    this.connections.set(connectionId, connection);

    try {
      // Create WebSocket connection (browser or Node.js compatible)
      let ws: WebSocketLike;
      
      if (typeof window !== 'undefined' && window.WebSocket) {
        // Browser environment
        const browserWs = new WebSocket(platformConfig.websocketUrl);
        ws = {
          send: (data: string, callback?: (error?: Error) => void) => {
            try {
              browserWs.send(data);
              callback?.();
            } catch (error) {
              callback?.(error as Error);
            }
          },
          close: () => browserWs.close(),
          on: (event: string, listener: (...args: any[]) => void) => {
            browserWs.addEventListener(event, listener);
          },
          readyState: browserWs.readyState
        };
      } else {
        // Node.js environment - create a mock WebSocket for now
        ws = {
          send: (data: string, callback?: (error?: Error) => void) => {
            // Mock implementation
            setTimeout(() => callback?.(), 0);
          },
          close: () => {},
          on: (event: string, listener: (...args: any[]) => void) => {},
          readyState: 1 // OPEN
        };
      }

      connection.websocket = ws;

      ws.on('open', () => {
        connection.status = 'connected';
        connection.lastActivity = new Date();
        connection.retryCount = 0;
        
        console.log(`✅ Connected to ${platform}`);
        this.emit('platformConnected', { platform, connectionId });

        // Send initial handshake
        this.sendToPlatform(connectionId, {
          type: 'handshake',
          platform: 'unified-sync-service',
          timestamp: new Date(),
          data: { version: '1.0.0' }
        });
      });

      ws.on('message', (data: string | Buffer) => {
        this.handlePlatformMessage(connectionId, data);
      });

      ws.on('close', () => {
        connection.status = 'disconnected';
        console.log(`❌ Disconnected from ${platform}`);
        this.emit('platformDisconnected', { platform, connectionId });
        this.scheduleReconnect(connectionId);
      });

      ws.on('error', (error: Error) => {
        connection.status = 'error';
        console.error(`🚨 WebSocket error for ${platform}:`, error);
        this.emit('platformError', { platform, connectionId, error });
        this.scheduleReconnect(connectionId);
      });

    } catch (error) {
      connection.status = 'error';
      console.error(`Failed to connect to ${platform}:`, error);
      this.scheduleReconnect(connectionId);
    }
  }

  /**
   * Handle incoming messages from platforms
   */
  private handlePlatformMessage(connectionId: string, data: string | Buffer): void {
    const connection = this.connections.get(connectionId);
    if (!connection) return;

    connection.lastActivity = new Date();

    try {
      const message = JSON.parse(data.toString());
      
      // Create sync event from platform message
      const syncEvent: SyncEvent = {
        id: `sync-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        type: message.type || 'project_update',
        platform: connection.platform,
        timestamp: new Date(),
        data: message.data || message,
        targets: message.targets // Optional: specific platforms to sync to
      };

      // Add to sync queue
      this.addToSyncQueue(syncEvent);

      this.emit('messageReceived', { 
        connectionId, 
        platform: connection.platform, 
        message: syncEvent 
      });

    } catch (error) {
      console.error(`Failed to parse message from ${connection.platform}:`, error);
    }
  }

  /**
   * Add event to sync queue
   */
  private addToSyncQueue(event: SyncEvent): void {
    this.syncQueue.push(event);
    
    // Trigger processing if not already running
    if (!this.isProcessing) {
      this.processSyncQueue();
    }
  }

  /**
   * Process sync queue
   */
  private async processSyncQueue(): Promise<void> {
    if (this.isProcessing || this.syncQueue.length === 0) return;

    this.isProcessing = true;

    while (this.syncQueue.length > 0) {
      const event = this.syncQueue.shift();
      if (event) {
        await this.broadcastSyncEvent(event);
      }
    }

    this.isProcessing = false;
  }

  /**
   * Broadcast sync event to all connected platforms (except origin)
   */
  private async broadcastSyncEvent(event: SyncEvent): Promise<void> {
    const targetConnections = Array.from(this.connections.values()).filter(conn => {
      // Don't send back to the originating platform
      if (conn.platform === event.platform) return false;
      
      // Check if specific targets are specified
      if (event.targets && event.targets.length > 0) {
        return event.targets.includes(conn.platform);
      }
      
      // Send to all connected platforms by default
      return conn.status === 'connected';
    });

    const broadcastPromises = targetConnections.map(async (connection) => {
      try {
        await this.sendToPlatform(connection.id, {
          type: 'sync_event',
          source: event.platform,
          timestamp: new Date(),
          data: {
            eventId: event.id,
            eventType: event.type,
            originalTimestamp: event.timestamp,
            payload: event.data
          }
        });

        console.log(`📡 Broadcasted ${event.type} from ${event.platform} to ${connection.platform}`);
        
      } catch (error) {
        console.error(`Failed to broadcast to ${connection.platform}:`, error);
      }
    });

    await Promise.allSettled(broadcastPromises);

    this.emit('eventBroadcasted', {
      event,
      targetCount: targetConnections.length,
      timestamp: new Date()
    });
  }

  /**
   * Send message to specific platform
   */
  private async sendToPlatform(connectionId: string, message: any): Promise<void> {
    const connection = this.connections.get(connectionId);
    if (!connection || !connection.websocket || connection.status !== 'connected') {
      throw new Error(`Platform ${connectionId} not connected`);
    }

    return new Promise((resolve, reject) => {
      connection.websocket!.send(JSON.stringify(message), (error?: Error) => {
        if (error) {
          reject(error);
        } else {
          connection.lastActivity = new Date();
          resolve();
        }
      });
    });
  }

  /**
   * Manually trigger sync for specific data
   */
  async triggerSync(type: SyncEvent['type'], data: any, targetPlatforms?: string[]): Promise<void> {
    const syncEvent: SyncEvent = {
      id: `manual-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type,
      platform: 'unified-sync-service',
      timestamp: new Date(),
      data,
      targets: targetPlatforms
    };

    this.addToSyncQueue(syncEvent);
  }

  /**
   * Schedule reconnection for a platform
   */
  private scheduleReconnect(connectionId: string): void {
    const connection = this.connections.get(connectionId);
    if (!connection || connection.retryCount >= connection.maxRetries) {
      if (connection) {
        console.log(`❌ Max retries reached for ${connection.platform}`);
        this.connections.delete(connectionId);
      }
      return;
    }

    connection.status = 'reconnecting';
    connection.retryCount++;

    const delay = Math.min(1000 * Math.pow(2, connection.retryCount), 30000); // Exponential backoff, max 30s

    console.log(`🔄 Scheduling reconnect for ${connection.platform} in ${delay}ms (attempt ${connection.retryCount})`);

    const timeout = setTimeout(async () => {
      this.reconnectTimeouts.delete(connectionId);
      await this.connectToPlatform(connection.platform as any);
    }, delay);

    this.reconnectTimeouts.set(connectionId, timeout);
  }

  /**
   * Start heartbeat monitoring
   */
  private startHeartbeat(): void {
    this.heartbeatInterval = setInterval(() => {
      const now = new Date();
      
      for (const [connectionId, connection] of this.connections) {
        if (connection.status === 'connected') {
          const timeSinceActivity = now.getTime() - connection.lastActivity.getTime();
          
          // Send ping if no activity for 30 seconds
          if (timeSinceActivity > 30000) {
            this.sendToPlatform(connectionId, {
              type: 'ping',
              timestamp: now
            }).catch(() => {
              // Ping failed, connection might be dead
              connection.status = 'error';
              this.scheduleReconnect(connectionId);
            });
          }
        }
      }
    }, 15000); // Check every 15 seconds
  }

  /**
   * Start sync queue processor
   */
  private startSyncProcessor(): void {
    setInterval(() => {
      if (!this.isProcessing && this.syncQueue.length > 0) {
        this.processSyncQueue();
      }
    }, this.config.syncInterval);
  }

  /**
   * Setup event handlers
   */
  private setupEventHandlers(): void {
    this.on('platformConnected', ({ platform }) => {
      console.log(`🔗 Platform ${platform} connected to unified sync`);
    });

    this.on('platformDisconnected', ({ platform }) => {
      console.log(`🔌 Platform ${platform} disconnected from unified sync`);
    });

    this.on('eventBroadcasted', ({ event, targetCount }) => {
      console.log(`📢 Broadcasted ${event.type} to ${targetCount} platforms`);
    });
  }

  /**
   * Get sync status
   */
  getStatus(): {
    isRunning: boolean;
    connectedPlatforms: string[];
    queueLength: number;
    connections: Array<{
      platform: string;
      status: string;
      lastActivity: Date;
      retryCount: number;
    }>;
  } {
    return {
      isRunning: this.heartbeatInterval !== null,
      connectedPlatforms: Array.from(this.connections.values())
        .filter(conn => conn.status === 'connected')
        .map(conn => conn.platform),
      queueLength: this.syncQueue.length,
      connections: Array.from(this.connections.values()).map(conn => ({
        platform: conn.platform,
        status: conn.status,
        lastActivity: conn.lastActivity,
        retryCount: conn.retryCount
      }))
    };
  }

  /**
   * Shutdown the service
   */
  async shutdown(): Promise<void> {
    console.log('🛑 Shutting down Unified Sync Service...');

    // Clear intervals
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }

    // Clear reconnect timeouts
    for (const timeout of this.reconnectTimeouts.values()) {
      clearTimeout(timeout);
    }
    this.reconnectTimeouts.clear();

    // Close all WebSocket connections
    const closePromises = Array.from(this.connections.values()).map(async (connection) => {
      if (connection.websocket && connection.status === 'connected') {
        return new Promise<void>((resolve) => {
          connection.websocket!.close();
          setTimeout(resolve, 1000); // Force resolve after 1s
        });
      }
    });

    await Promise.allSettled(closePromises);
    this.connections.clear();

    this.emit('shutdown', { timestamp: new Date() });
  }
}

export { UnifiedSyncService, type SyncConfig, type SyncEvent, type PlatformConnection };