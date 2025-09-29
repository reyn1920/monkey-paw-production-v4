import { firebaseService } from './FirebaseService';
import { traeAIService } from './TraeAIService';

export interface SyncConfig {
  projectId: string;
  platforms: {
    cursor: { enabled: boolean; apiKey?: string; projectPath?: string };
    boltdiy: { enabled: boolean; token?: string; projectId?: string };
    firebase: { enabled: boolean; projectId?: string };
    traeai: { enabled: boolean; apiKey?: string; projectId?: string };
  };
  syncInterval: number; // in milliseconds
  conflictResolution: 'manual' | 'latest' | 'merge';
}

export interface SyncEvent {
  id: string;
  timestamp: string;
  platform: 'cursor' | 'boltdiy' | 'firebase' | 'traeai';
  type: 'file_change' | 'project_update' | 'config_change' | 'deployment';
  data: any;
  status: 'pending' | 'syncing' | 'completed' | 'failed' | 'conflict';
  error?: string;
}

export interface SyncStatus {
  isActive: boolean;
  lastSync: string;
  nextSync: string;
  conflicts: SyncConflict[];
  statistics: {
    totalSyncs: number;
    successfulSyncs: number;
    failedSyncs: number;
    conflictsResolved: number;
  };
}

export interface SyncConflict {
  id: string;
  timestamp: string;
  platforms: string[];
  type: 'file_conflict' | 'version_conflict' | 'config_conflict';
  description: string;
  data: {
    local: any;
    remote: any;
  };
  resolution?: 'use_local' | 'use_remote' | 'merge' | 'manual';
}

export interface ProjectSnapshot {
  id: string;
  timestamp: string;
  platform: string;
  files: { [key: string]: string };
  metadata: any;
  checksum: string;
}

export class SyncService {
  private config: SyncConfig | null = null;
  private isActive: boolean = false;
  private syncInterval: NodeJS.Timeout | null = null;
  private conflicts: SyncConflict[] = [];
  private listeners: ((event: SyncEvent) => void)[] = [];
  private snapshots: Map<string, ProjectSnapshot> = new Map();

  constructor() {}

  // Configuration and lifecycle
  async initialize(config: SyncConfig): Promise<boolean> {
    try {
      this.config = config;
      
      // Validate platform connections
      const validationResults = await this.validateConnections();
      
      if (validationResults.some(result => !result.success)) {
        console.warn('Some platform connections failed validation:', validationResults);
      }

      return true;
    } catch (error) {
      console.error('Failed to initialize sync service:', error);
      return false;
    }
  }

  async start(): Promise<boolean> {
    if (!this.config || this.isActive) return false;

    try {
      this.isActive = true;
      
      // Create initial snapshots
      await this.createSnapshots();
      
      // Start sync interval
      this.syncInterval = setInterval(() => {
        this.performSync();
      }, this.config.syncInterval);

      console.log('Sync service started');
      return true;
    } catch (error) {
      console.error('Failed to start sync service:', error);
      this.isActive = false;
      return false;
    }
  }

  stop(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
    this.isActive = false;
    console.log('Sync service stopped');
  }

  // Platform validation
  private async validateConnections(): Promise<{ platform: string; success: boolean; error?: string }[]> {
    const results = [];

    if (this.config?.platforms.cursor.enabled) {
      results.push({
        platform: 'cursor',
        success: await this.validateCursorConnection(),
        error: 'Cursor IDE connection validation'
      });
    }

    if (this.config?.platforms.boltdiy.enabled) {
      results.push({
        platform: 'boltdiy',
        success: await this.validateBoltDiyConnection(),
        error: 'Bolt.diy connection validation'
      });
    }

    if (this.config?.platforms.firebase.enabled) {
      results.push({
        platform: 'firebase',
        success: await firebaseService.testConnection(),
        error: 'Firebase connection validation'
      });
    }

    if (this.config?.platforms.traeai.enabled) {
      results.push({
        platform: 'traeai',
        success: await traeAIService.testConnection(),
        error: 'Trae.ai connection validation'
      });
    }

    return results;
  }

  private async validateCursorConnection(): Promise<boolean> {
    // Simulate Cursor IDE connection validation
    return new Promise(resolve => {
      setTimeout(() => resolve(Math.random() > 0.1), 500);
    });
  }

  private async validateBoltDiyConnection(): Promise<boolean> {
    // Simulate Bolt.diy connection validation
    return new Promise(resolve => {
      setTimeout(() => resolve(Math.random() > 0.1), 500);
    });
  }

  // Snapshot management
  private async createSnapshots(): Promise<void> {
    if (!this.config) return;

    const timestamp = new Date().toISOString();

    if (this.config.platforms.cursor.enabled) {
      const snapshot = await this.createCursorSnapshot(timestamp);
      if (snapshot) this.snapshots.set('cursor', snapshot);
    }

    if (this.config.platforms.boltdiy.enabled) {
      const snapshot = await this.createBoltDiySnapshot(timestamp);
      if (snapshot) this.snapshots.set('boltdiy', snapshot);
    }

    if (this.config.platforms.firebase.enabled) {
      const snapshot = await this.createFirebaseSnapshot(timestamp);
      if (snapshot) this.snapshots.set('firebase', snapshot);
    }

    if (this.config.platforms.traeai.enabled) {
      const snapshot = await this.createTraeAISnapshot(timestamp);
      if (snapshot) this.snapshots.set('traeai', snapshot);
    }
  }

  private async createCursorSnapshot(timestamp: string): Promise<ProjectSnapshot | null> {
    try {
      // Simulate getting project data from Cursor IDE
      const files = {
        'src/App.tsx': '// Cursor IDE version',
        'package.json': '{ "name": "cursor-project" }'
      };

      return {
        id: `cursor_${Date.now()}`,
        timestamp,
        platform: 'cursor',
        files,
        metadata: { version: '1.0.0', lastModified: timestamp },
        checksum: this.calculateChecksum(files)
      };
    } catch (error) {
      console.error('Failed to create Cursor snapshot:', error);
      return null;
    }
  }

  private async createBoltDiySnapshot(timestamp: string): Promise<ProjectSnapshot | null> {
    try {
      // Simulate getting project data from Bolt.diy
      const files = {
        'src/App.tsx': '// Bolt.diy version',
        'package.json': '{ "name": "boltdiy-project" }'
      };

      return {
        id: `boltdiy_${Date.now()}`,
        timestamp,
        platform: 'boltdiy',
        files,
        metadata: { version: '1.0.0', lastModified: timestamp },
        checksum: this.calculateChecksum(files)
      };
    } catch (error) {
      console.error('Failed to create Bolt.diy snapshot:', error);
      return null;
    }
  }

  private async createFirebaseSnapshot(timestamp: string): Promise<ProjectSnapshot | null> {
    try {
      if (!this.config?.projectId) return null;

      const project = await firebaseService.getProject(this.config.projectId);
      if (!project) return null;

      return {
        id: `firebase_${Date.now()}`,
        timestamp,
        platform: 'firebase',
        files: project.files,
        metadata: project.metadata,
        checksum: this.calculateChecksum(project.files)
      };
    } catch (error) {
      console.error('Failed to create Firebase snapshot:', error);
      return null;
    }
  }

  private async createTraeAISnapshot(timestamp: string): Promise<ProjectSnapshot | null> {
    try {
      if (!this.config?.platforms.traeai.projectId) return null;

      const project = await traeAIService.getProject(this.config.platforms.traeai.projectId);
      if (!project) return null;

      return {
        id: `traeai_${Date.now()}`,
        timestamp,
        platform: 'traeai',
        files: project.files,
        metadata: project.metadata,
        checksum: this.calculateChecksum(project.files)
      };
    } catch (error) {
      console.error('Failed to create Trae.ai snapshot:', error);
      return null;
    }
  }

  // Synchronization logic
  private async performSync(): Promise<void> {
    if (!this.isActive || !this.config) return;

    try {
      console.log('Starting sync cycle...');

      // Create new snapshots
      const newSnapshots = new Map<string, ProjectSnapshot>();
      
      if (this.config.platforms.cursor.enabled) {
        const snapshot = await this.createCursorSnapshot(new Date().toISOString());
        if (snapshot) newSnapshots.set('cursor', snapshot);
      }

      if (this.config.platforms.boltdiy.enabled) {
        const snapshot = await this.createBoltDiySnapshot(new Date().toISOString());
        if (snapshot) newSnapshots.set('boltdiy', snapshot);
      }

      if (this.config.platforms.firebase.enabled) {
        const snapshot = await this.createFirebaseSnapshot(new Date().toISOString());
        if (snapshot) newSnapshots.set('firebase', snapshot);
      }

      if (this.config.platforms.traeai.enabled) {
        const snapshot = await this.createTraeAISnapshot(new Date().toISOString());
        if (snapshot) newSnapshots.set('traeai', snapshot);
      }

      // Detect changes and conflicts
      const changes = this.detectChanges(newSnapshots);
      const conflicts = this.detectConflicts(changes);

      // Handle conflicts
      if (conflicts.length > 0) {
        await this.handleConflicts(conflicts);
      }

      // Apply changes
      await this.applyChanges(changes);

      // Update snapshots
      this.snapshots = newSnapshots;

      console.log('Sync cycle completed');
    } catch (error) {
      console.error('Sync cycle failed:', error);
    }
  }

  private detectChanges(newSnapshots: Map<string, ProjectSnapshot>): { platform: string; changes: any[] }[] {
    const allChanges: { platform: string; changes: any[] }[] = [];

    for (const [platform, newSnapshot] of newSnapshots) {
      const oldSnapshot = this.snapshots.get(platform);
      
      if (!oldSnapshot) {
        // New platform, all files are changes
        allChanges.push({
          platform,
          changes: Object.keys(newSnapshot.files).map(file => ({
            type: 'added',
            file,
            content: newSnapshot.files[file]
          }))
        });
        continue;
      }

      if (oldSnapshot.checksum !== newSnapshot.checksum) {
        const changes = this.compareFiles(oldSnapshot.files, newSnapshot.files);
        if (changes.length > 0) {
          allChanges.push({ platform, changes });
        }
      }
    }

    return allChanges;
  }

  private compareFiles(oldFiles: { [key: string]: string }, newFiles: { [key: string]: string }): any[] {
    const changes = [];

    // Check for added and modified files
    for (const [file, content] of Object.entries(newFiles)) {
      if (!oldFiles[file]) {
        changes.push({ type: 'added', file, content });
      } else if (oldFiles[file] !== content) {
        changes.push({ type: 'modified', file, content, oldContent: oldFiles[file] });
      }
    }

    // Check for deleted files
    for (const file of Object.keys(oldFiles)) {
      if (!newFiles[file]) {
        changes.push({ type: 'deleted', file });
      }
    }

    return changes;
  }

  private detectConflicts(allChanges: { platform: string; changes: any[] }[]): SyncConflict[] {
    const conflicts: SyncConflict[] = [];
    const fileChanges = new Map<string, { platform: string; change: any }[]>();

    // Group changes by file
    for (const { platform, changes } of allChanges) {
      for (const change of changes) {
        if (!fileChanges.has(change.file)) {
          fileChanges.set(change.file, []);
        }
        fileChanges.get(change.file)!.push({ platform, change });
      }
    }

    // Detect conflicts (same file changed in multiple platforms)
    for (const [file, platformChanges] of fileChanges) {
      if (platformChanges.length > 1) {
        conflicts.push({
          id: `conflict_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          timestamp: new Date().toISOString(),
          platforms: platformChanges.map(pc => pc.platform),
          type: 'file_conflict',
          description: `File ${file} was modified in multiple platforms`,
          data: {
            local: platformChanges[0].change,
            remote: platformChanges.slice(1)
          }
        });
      }
    }

    return conflicts;
  }

  private async handleConflicts(conflicts: SyncConflict[]): Promise<void> {
    for (const conflict of conflicts) {
      switch (this.config?.conflictResolution) {
        case 'latest':
          conflict.resolution = 'use_remote';
          break;
        case 'merge':
          conflict.resolution = 'merge';
          break;
        default:
          conflict.resolution = 'manual';
          this.conflicts.push(conflict);
          break;
      }
    }
  }

  private async applyChanges(allChanges: { platform: string; changes: any[] }[]): Promise<void> {
    for (const { platform, changes } of allChanges) {
      for (const change of changes) {
        await this.applySingleChange(platform, change);
      }
    }
  }

  private async applySingleChange(sourcePlatform: string, change: any): Promise<void> {
    if (!this.config) return;

    // Apply change to all other enabled platforms
    const targetPlatforms = Object.keys(this.config.platforms).filter(
      p => p !== sourcePlatform && (this.config!.platforms as any)[p].enabled
    );

    for (const targetPlatform of targetPlatforms) {
      try {
        await this.syncChangeToPlatform(targetPlatform, change);
      } catch (error) {
        console.error(`Failed to sync change to ${targetPlatform}:`, error);
      }
    }
  }

  private async syncChangeToPlatform(platform: string, change: any): Promise<void> {
    switch (platform) {
      case 'cursor':
        await this.syncToCursor(change);
        break;
      case 'boltdiy':
        await this.syncToBoltDiy(change);
        break;
      case 'firebase':
        await this.syncToFirebase(change);
        break;
      case 'traeai':
        await this.syncToTraeAI(change);
        break;
    }
  }

  private async syncToCursor(change: any): Promise<void> {
    // Simulate syncing to Cursor IDE
    console.log('Syncing to Cursor:', change);
    await new Promise(resolve => setTimeout(resolve, 200));
  }

  private async syncToBoltDiy(change: any): Promise<void> {
    // Simulate syncing to Bolt.diy
    console.log('Syncing to Bolt.diy:', change);
    await new Promise(resolve => setTimeout(resolve, 200));
  }

  private async syncToFirebase(change: any): Promise<void> {
    if (!this.config?.projectId) return;

    try {
      const project = await firebaseService.getProject(this.config.projectId);
      if (project) {
        const updatedFiles = { ...project.files };
        
        switch (change.type) {
          case 'added':
          case 'modified':
            updatedFiles[change.file] = change.content;
            break;
          case 'deleted':
            delete updatedFiles[change.file];
            break;
        }

        await firebaseService.updateProject(this.config.projectId, { files: updatedFiles });
      }
    } catch (error) {
      console.error('Failed to sync to Firebase:', error);
    }
  }

  private async syncToTraeAI(change: any): Promise<void> {
    if (!this.config?.platforms.traeai.projectId) return;

    try {
      const project = await traeAIService.getProject(this.config.platforms.traeai.projectId);
      if (project) {
        const updatedFiles = { ...project.files };
        
        switch (change.type) {
          case 'added':
          case 'modified':
            updatedFiles[change.file] = change.content;
            break;
          case 'deleted':
            delete updatedFiles[change.file];
            break;
        }

        await traeAIService.updateProject(this.config.platforms.traeai.projectId, { files: updatedFiles });
      }
    } catch (error) {
      console.error('Failed to sync to Trae.ai:', error);
    }
  }

  // Event management
  addEventListener(listener: (event: SyncEvent) => void): () => void {
    this.listeners.push(listener);
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  // Status and monitoring
  getStatus(): SyncStatus {
    return {
      isActive: this.isActive,
      lastSync: this.snapshots.size > 0 ? 
        Math.max(...Array.from(this.snapshots.values()).map(s => new Date(s.timestamp).getTime())).toString() : 
        'Never',
      nextSync: this.isActive && this.config ? 
        new Date(Date.now() + this.config.syncInterval).toISOString() : 
        'Not scheduled',
      conflicts: this.conflicts,
      statistics: {
        totalSyncs: 0, // TODO: Implement proper tracking
        successfulSyncs: 0,
        failedSyncs: 0,
        conflictsResolved: 0
      }
    };
  }

  getConflicts(): SyncConflict[] {
    return [...this.conflicts];
  }

  async resolveConflict(conflictId: string, resolution: 'use_local' | 'use_remote' | 'merge'): Promise<boolean> {
    const conflictIndex = this.conflicts.findIndex(c => c.id === conflictId);
    if (conflictIndex === -1) return false;

    const conflict = this.conflicts[conflictIndex];
    conflict.resolution = resolution;

    // Apply resolution
    try {
      await this.applyConflictResolution(conflict);
      this.conflicts.splice(conflictIndex, 1);
      return true;
    } catch (error) {
      console.error('Failed to resolve conflict:', error);
      return false;
    }
  }

  private async applyConflictResolution(conflict: SyncConflict): Promise<void> {
    // Implementation depends on the specific conflict resolution strategy
    console.log('Applying conflict resolution:', conflict);
  }

  // Utility methods
  private calculateChecksum(files: { [key: string]: string }): string {
    const content = Object.keys(files).sort().map(key => `${key}:${files[key]}`).join('|');
    return btoa(content).slice(0, 16); // Simple checksum
  }

  async forcSync(): Promise<boolean> {
    if (!this.isActive) return false;

    try {
      await this.performSync();
      return true;
    } catch (error) {
      console.error('Force sync failed:', error);
      return false;
    }
  }

  updateConfig(newConfig: Partial<SyncConfig>): boolean {
    if (!this.config) return false;

    this.config = { ...this.config, ...newConfig };
    
    // Restart sync if interval changed
    if (newConfig.syncInterval && this.isActive) {
      this.stop();
      this.start();
    }

    return true;
  }
}

// Export singleton instance
export const syncService = new SyncService();