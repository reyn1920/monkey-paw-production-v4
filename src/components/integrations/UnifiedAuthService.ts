import { BoltDiyConfig, boltDiyService } from './BoltDiyService';
import { CursorConfig, cursorService } from './CursorService';
import { FirebaseConfig, firebaseService } from './FirebaseService';
import { TraeAIConfig, traeAIService } from './TraeAIService';
import { TraeAIUpgradeService } from './TraeAIUpgradeService';
import { VSCodeConfig, vsCodeService } from './VSCodeService';
import { WindsurfConfig, windsurfService } from './WindsurfService';

// (Removed stray method definition at file top)

export interface UnifiedAuthConfig {
  cursor?: CursorConfig;
  boltdiy?: BoltDiyConfig;
  firebase?: FirebaseConfig;
  traeai?: TraeAIConfig;
  vscode?: VSCodeConfig;
  windsurf?: WindsurfConfig;
}

export interface AuthStatus {
  platform:
    | 'cursor'
    | 'boltdiy'
    | 'firebase'
    | 'traeai'
    | 'vscode'
    | 'windsurf';
  authenticated: boolean;
  user?: any;
  error?: string;
  lastAuthenticated?: string;
}

export interface UnifiedUser {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  platforms: {
    cursor?: { userId: string; workspaceId?: string };
    boltdiy?: { organizationId?: string; projectId?: string };
    firebase?: { uid: string; displayName?: string };
    traeai?: { organizationId?: string; projectId?: string };
    vscode?: { workspaceId?: string; extensionSyncEnabled?: boolean };
    windsurf?: { workspaceId?: string; collaborationEnabled?: boolean };
  };
  preferences: {
    defaultPlatform:
      | 'cursor'
      | 'boltdiy'
      | 'firebase'
      | 'traeai'
      | 'vscode'
      | 'windsurf';
    autoSync: boolean;
    notifications: boolean;
  };
}

export interface AuthEvent {
  type:
    | 'login'
    | 'logout'
    | 'error'
    | 'sync'
    | 'platformConnected'
    | 'platformDisconnected';
  platform?: string;
  user?: UnifiedUser;
  error?: string;
  timestamp: string;
}

// Browser-compatible EventEmitter replacement
class BrowserEventEmitter {
  private listeners: Map<string, Function[]> = new Map();

  on(event: string, listener: Function): this {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(listener);
    return this;
  }

  emit(event: string, ...args: any[]): boolean {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.forEach(listener => listener(...args));
      return true;
    }
    return false;
  }

  off(event: string, listener: Function): this {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      const index = eventListeners.indexOf(listener);
      if (index > -1) {
        eventListeners.splice(index, 1);
      }
    }
    return this;
  }

  removeAllListeners(event?: string): this {
    if (event) {
      this.listeners.delete(event);
    } else {
      this.listeners.clear();
    }
    return this;
  }
}

export class UnifiedAuthService extends BrowserEventEmitter {
  private authStatuses: Map<string, AuthStatus> = new Map();
  private currentUser: UnifiedUser | null = null;
  private authConfig: UnifiedAuthConfig = {};
  private syncInterval: NodeJS.Timeout | null = null;
  // private isInitialized: boolean = false; // Removed unused property

  constructor() {
    super();
    this.initializeAuthStatuses();
    this.setupPlatformListeners();
  }

  private initializeAuthStatuses(): void {
    const platforms = [
      'cursor',
      'boltdiy',
      'firebase',
      'traeai',
      'vscode',
      'windsurf',
    ] as const;
    platforms.forEach(platform => {
      this.authStatuses.set(platform, {
        platform,
        authenticated: false,
      });
    });
  }

  private setupPlatformListeners(): void {
    // Firebase auth state listener
    firebaseService.onAuthStateChanged(user => {
      this.updateAuthStatus('firebase', {
        authenticated: !!user,
        user,
        lastAuthenticated: user ? new Date().toISOString() : undefined,
      });
    });

    // Setup listeners for other platforms
    this.setupCursorListener();
    this.setupBoltDiyListener();
    this.setupTraeAIListener();
    this.setupVSCodeListener();
    this.setupWindsurfListener();
  }

  private setupCursorListener(): void {
    cursorService.on('authenticated', (user: any) => {
      this.updateAuthStatus('cursor', {
        authenticated: true,
        user,
        lastAuthenticated: new Date().toISOString(),
      });
    });

    cursorService.on('disconnected', () => {
      this.updateAuthStatus('cursor', {
        authenticated: false,
      });
    });
  }

  private setupBoltDiyListener(): void {
    boltDiyService.on('authenticated', (user: any) => {
      this.updateAuthStatus('boltdiy', {
        authenticated: true,
        user,
        lastAuthenticated: new Date().toISOString(),
      });
    });

    boltDiyService.on('disconnected', () => {
      this.updateAuthStatus('boltdiy', {
        authenticated: false,
      });
    });
  }

  private setupTraeAIListener(): void {
    traeAIService.on('connected', (data: any) => {
      this.updateAuthStatus('traeai', {
        authenticated: true,
        user: data.user,
        lastAuthenticated: new Date().toISOString(),
      });
    });

    traeAIService.on('disconnected', () => {
      this.updateAuthStatus('traeai', {
        authenticated: false,
      });
    });
  }

  private setupVSCodeListener(): void {
    vsCodeService.on('connected', () => {
      this.updateAuthStatus('vscode', {
        authenticated: true,
        lastAuthenticated: new Date().toISOString(),
      });
    });

    vsCodeService.on('disconnected', () => {
      this.updateAuthStatus('vscode', {
        authenticated: false,
      });
    });
  }

  private setupWindsurfListener(): void {
    windsurfService.on('connected', () => {
      this.updateAuthStatus('windsurf', {
        authenticated: true,
        lastAuthenticated: new Date().toISOString(),
      });
    });

    windsurfService.on('disconnected', () => {
      this.updateAuthStatus('windsurf', {
        authenticated: false,
      });
    });
  }

  private updateAuthStatus(
    platform: string,
    status: Partial<AuthStatus>
  ): void {
    const currentStatus = this.authStatuses.get(platform);
    if (currentStatus) {
      const updatedStatus = { ...currentStatus, ...status };
      this.authStatuses.set(platform, updatedStatus);

      this.emit('authStatusChanged', {
        type: status.authenticated
          ? 'platformConnected'
          : 'platformDisconnected',
        platform,
        timestamp: new Date().toISOString(),
      });

      // Update unified user if needed
      this.updateUnifiedUser();
    }
  }

  private updateUnifiedUser(): void {
    const authenticatedPlatforms = Array.from(
      this.authStatuses.values()
    ).filter(status => status.authenticated);

    if (authenticatedPlatforms.length === 0) {
      this.currentUser = null;
      this.emit('logout', {
        type: 'logout',
        timestamp: new Date().toISOString(),
      });
      return;
    }

    // Create or update unified user from authenticated platforms
    const firebaseStatus = this.authStatuses.get('firebase');
    const primaryUser = firebaseStatus?.authenticated
      ? firebaseStatus.user
      : authenticatedPlatforms[0].user;

    if (primaryUser) {
      this.currentUser = {
        id: primaryUser.uid || primaryUser.id || 'unified-user',
        email: primaryUser.email || 'user@example.com',
        name: primaryUser.displayName || primaryUser.name || 'User',
        avatar: primaryUser.photoURL || primaryUser.avatar,
        platforms: this.buildPlatformData(),
        preferences: {
          defaultPlatform: 'firebase',
          autoSync: true,
          notifications: true,
        },
      };

      this.emit('login', {
        type: 'login',
        user: this.currentUser,
        timestamp: new Date().toISOString(),
      });
    }
  }

  private buildPlatformData(): UnifiedUser['platforms'] {
    const platforms: UnifiedUser['platforms'] = {};

    const cursorStatus = this.authStatuses.get('cursor');
    if (cursorStatus?.authenticated && cursorStatus.user) {
      platforms.cursor = {
        userId: cursorStatus.user.id,
        workspaceId: cursorStatus.user.workspaceId,
      };
    }

    const boltdiyStatus = this.authStatuses.get('boltdiy');
    if (boltdiyStatus?.authenticated && boltdiyStatus.user) {
      platforms.boltdiy = {
        organizationId: boltdiyStatus.user.organizationId,
        projectId: boltdiyStatus.user.projectId,
      };
    }

    const firebaseStatus = this.authStatuses.get('firebase');
    if (firebaseStatus?.authenticated && firebaseStatus.user) {
      platforms.firebase = {
        uid: firebaseStatus.user.uid,
        displayName: firebaseStatus.user.displayName,
      };
    }

    const traeaiStatus = this.authStatuses.get('traeai');
    if (traeaiStatus?.authenticated && traeaiStatus.user) {
      platforms.traeai = {
        organizationId: traeaiStatus.user.organizationId,
        projectId: traeaiStatus.user.projectId,
      };
    }

    return platforms;
  }

  async initialize(
    config: UnifiedAuthConfig
  ): Promise<{ success: boolean; errors: string[] }> {
    this.authConfig = config;
    const errors: string[] = [];

    // Initialize Firebase first (primary auth provider)
    if (config.firebase) {
      try {
        const result = await firebaseService.initialize(config.firebase);
        if (!result.success) {
          errors.push(`Firebase: ${result.error}`);
        }
      } catch (error: any) {
        errors.push(`Firebase: ${error.message}`);
      }
    }

    // Initialize other platforms
    if (config.cursor) {
      try {
        const result = await cursorService.connect(config.cursor);
        if (!result.success) {
          errors.push(`Cursor: ${result.error}`);
        }
      } catch (error: any) {
        errors.push(`Cursor: ${error.message}`);
      }
    }

    if (config.boltdiy) {
      try {
        const result = await boltDiyService.connect(config.boltdiy);
        if (!result.success) {
          errors.push(`Bolt.diy: ${result.error}`);
        }
      } catch (error: any) {
        errors.push(`Bolt.diy: ${error.message}`);
      }
    }

    if (config.traeai) {
      try {
        const result = await traeAIService.connect(config.traeai);
        if (!result.success) {
          errors.push(`Trae.AI: ${result.error}`);
        }
      } catch (error: any) {
        errors.push(`Trae.AI: ${error.message}`);
      }
    }

    // this.isInitialized = true; // Removed unused property
    this.startAuthSync();

    return {
      success: errors.length === 0,
      errors,
    };
  }

  async signInWithEmail(
    email: string,
    password: string
  ): Promise<{ success: boolean; user?: UnifiedUser; error?: string }> {
    if (!this.authConfig.firebase) {
      return { success: false, error: 'Firebase not configured' };
    }

    try {
      const result = await firebaseService.signIn(email, password);
      if (result.success && result.user) {
        // Firebase auth will trigger the auth state listener
        return { success: true, user: this.currentUser || undefined };
      }
      return { success: false, error: result.error };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  async signInWithGoogle(): Promise<{
    success: boolean;
    user?: UnifiedUser;
    error?: string;
  }> {
    if (!this.authConfig.firebase) {
      return { success: false, error: 'Firebase not configured' };
    }

    try {
      const result = await firebaseService.signInWithGoogle();
      if (result.success && result.user) {
        return { success: true, user: this.currentUser || undefined };
      }
      return { success: false, error: result.error };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  async signUp(
    email: string,
    password: string,
    displayName?: string
  ): Promise<{ success: boolean; user?: UnifiedUser; error?: string }> {
    if (!this.authConfig.firebase) {
      return { success: false, error: 'Firebase not configured' };
    }

    try {
      const result = await firebaseService.signUp(email, password, displayName);
      if (result.success && result.user) {
        return { success: true, user: this.currentUser || undefined };
      }
      return { success: false, error: result.error };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  async signOut(): Promise<{ success: boolean; error?: string }> {
    try {
      // Sign out from all platforms
      const promises = [];

      if (this.authStatuses.get('firebase')?.authenticated) {
        promises.push(firebaseService.signOutUser());
      }

      if (this.authStatuses.get('cursor')?.authenticated) {
        promises.push(cursorService.disconnect());
      }

      if (this.authStatuses.get('boltdiy')?.authenticated) {
        promises.push(boltDiyService.disconnect());
      }

      if (this.authStatuses.get('traeai')?.authenticated) {
        promises.push(traeAIService.disconnect());
      }

      await Promise.all(promises);

      this.currentUser = null;
      this.stopAuthSync();

      this.emit('logout', {
        type: 'logout',
        timestamp: new Date().toISOString(),
      });

      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  async connectPlatform(
    platform: 'cursor' | 'boltdiy' | 'traeai',
    config: any
  ): Promise<{ success: boolean; error?: string }> {
    try {
      let result;

      switch (platform) {
        case 'cursor':
          result = await cursorService.connect(config);
          break;
        case 'boltdiy':
          result = await boltDiyService.connect(config);
          break;
        case 'traeai':
          result = await traeAIService.connect(config);
          break;
        default:
          return { success: false, error: 'Unsupported platform' };
      }

      if (result.success) {
        this.authConfig[platform] = config;
      }

      return result;
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  async disconnectPlatform(
    platform: 'cursor' | 'boltdiy' | 'firebase' | 'traeai'
  ): Promise<{ success: boolean; error?: string }> {
    try {
      switch (platform) {
        case 'cursor':
          await cursorService.disconnect();
          break;
        case 'boltdiy':
          await boltDiyService.disconnect();
          break;
        case 'firebase':
          await firebaseService.signOut();
          break;
        case 'traeai':
          traeAIService.disconnect();
          break;
        default:
          return { success: false, error: 'Unsupported platform' };
      }

      delete this.authConfig[platform];
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  getCurrentUser(): UnifiedUser | null {
    return this.currentUser;
  }

  isAuthenticated(): boolean {
    return this.currentUser !== null;
  }

  getAuthStatus(platform?: string): AuthStatus | AuthStatus[] {
    if (platform) {
      return (
        this.authStatuses.get(platform) || {
          platform: platform as any,
          authenticated: false,
        }
      );
    }
    return Array.from(this.authStatuses.values());
  }

  getConnectedPlatforms(): string[] {
    return Array.from(this.authStatuses.entries())
      .filter(([_, status]) => status.authenticated)
      .map(([platform, _]) => platform);
  }

  async syncAuthAcrossPlatforms(): Promise<{
    success: boolean;
    errors: string[];
  }> {
    const errors: string[] = [];

    if (!this.currentUser) {
      return { success: false, errors: ['No authenticated user'] };
    }

    // Sync user data across platforms
    const syncPromises = [];

    if (this.authStatuses.get('cursor')?.authenticated) {
      syncPromises.push(
        this.syncUserToCursor().catch(err =>
          errors.push(`Cursor sync: ${err.message}`)
        )
      );
    }

    if (this.authStatuses.get('boltdiy')?.authenticated) {
      syncPromises.push(
        this.syncUserToBoltDiy().catch(err =>
          errors.push(`Bolt.diy sync: ${err.message}`)
        )
      );
    }

    if (this.authStatuses.get('traeai')?.authenticated) {
      syncPromises.push(
        this.syncUserToTraeAI().catch(err =>
          errors.push(`Trae.AI sync: ${err.message}`)
        )
      );
    }

    await Promise.all(syncPromises);

    this.emit('sync', {
      type: 'sync',
      user: this.currentUser,
      timestamp: new Date().toISOString(),
    });

    return {
      success: errors.length === 0,
      errors,
    };
  }

  private async syncUserToCursor(): Promise<void> {
    // Implement cursor-specific user sync logic
    console.log('Syncing user to Cursor...');
  }

  private async syncUserToBoltDiy(): Promise<void> {
    // Implement bolt.diy-specific user sync logic
    console.log('Syncing user to Bolt.diy...');
  }

  private async syncUserToTraeAI(): Promise<void> {
    // Implement trae.ai-specific user sync logic
    console.log('Syncing user to Trae.AI...');
  }

  private startAuthSync(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
    }

    // Sync auth status every 5 minutes
    this.syncInterval = setInterval(() => {
      this.syncAuthAcrossPlatforms();
    }, 5 * 60 * 1000);
  }

  private stopAuthSync(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
  }

  async testConnection(
    platform: 'firebase' | 'cursor' | 'boltdiy' | 'traeai'
  ): Promise<boolean> {
    try {
      switch (platform) {
        case 'firebase':
          return await firebaseService.testConnection();
        case 'cursor':
          return cursorService.isAuthenticated();
        case 'boltdiy':
          return boltDiyService.isAuthenticated();
        case 'traeai':
          return await traeAIService.testConnection();
        default:
          return false;
      }
    } catch (error) {
      console.error(`Test connection failed for ${platform}:`, error);
      return false;
    }
  }

  // Fetch and integrate all available upgrades from trai.ai
  async fetchAndIntegrateTraeAIUpgrades(): Promise<void> {
    await TraeAIUpgradeService.fetchAndIntegrateAll();
  }
  async testConnections(): Promise<{ [platform: string]: boolean }> {
    const results: { [platform: string]: boolean } = {};

    const testPromises = [
      firebaseService.testConnection().then(result => {
        results.firebase = result;
      }),
      cursorService.isAuthenticated()
        ? Promise.resolve((results.cursor = true))
        : Promise.resolve((results.cursor = false)),
      boltDiyService.isAuthenticated()
        ? Promise.resolve((results.boltdiy = true))
        : Promise.resolve((results.boltdiy = false)),
      traeAIService.testConnection().then(result => {
        results.traeai = result;
      }),
    ];

    await Promise.all(testPromises);
    return results;
  }

  destroy(): void {
    this.stopAuthSync();
    this.removeAllListeners();
    this.authStatuses.clear();
    this.currentUser = null;
    // this.isInitialized = false; // Removed unused property
  }
}

// Export singleton instance
export const unifiedAuthService = new UnifiedAuthService();
