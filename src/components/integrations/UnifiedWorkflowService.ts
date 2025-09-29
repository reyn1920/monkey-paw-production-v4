import { CursorService } from './CursorService';
import { BoltDiyService } from './BoltDiyService';
import { FirebaseService } from './FirebaseService';
import { TraeAIService } from './TraeAIService';
import { VSCodeService } from '../../services/VSCodeService';
import { WindsurfService } from '../../services/WindsurfService';
import toast from 'react-hot-toast';

export interface WorkflowConfig {
  id: string;
  name: string;
  description: string;
  platforms: ('cursor' | 'boltdiy' | 'firebase' | 'traeai' | 'vscode' | 'windsurf')[];
  triggers: WorkflowTrigger[];
  steps: WorkflowStep[];
  schedule?: string;
  enabled: boolean;
}

export interface WorkflowTrigger {
  type: 'file_change' | 'git_push' | 'manual' | 'schedule' | 'platform_event';
  platform?: string;
  conditions: { [key: string]: any };
}

export interface WorkflowStep {
  id: string;
  name: string;
  platform: 'cursor' | 'boltdiy' | 'firebase' | 'traeai' | 'vscode' | 'windsurf';
  action: string;
  config: { [key: string]: any };
  dependencies: string[];
  retryCount?: number;
  timeout?: number;
}

export interface WorkflowExecution {
  id: string;
  workflowId: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  startTime: string;
  endTime?: string;
  steps: WorkflowStepExecution[];
  logs: WorkflowLog[];
  error?: string;
}

export interface WorkflowStepExecution {
  stepId: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'skipped';
  startTime?: string;
  endTime?: string;
  output?: any;
  error?: string;
}

export interface WorkflowLog {
  timestamp: string;
  level: 'info' | 'warning' | 'error' | 'debug';
  message: string;
  stepId?: string;
  data?: any;
}

export interface CrossPlatformProject {
  id: string;
  name: string;
  description: string;
  platforms: {
    cursor?: { projectId: string; connected: boolean };
    boltdiy?: { projectId: string; connected: boolean };
    firebase?: { projectId: string; connected: boolean };
    traeai?: { projectId: string; connected: boolean };
    vscode?: { projectId: string; connected: boolean };
    windsurf?: { projectId: string; connected: boolean };
  };
  files: { [fileName: string]: string };
  metadata: {
    createdAt: string;
    updatedAt: string;
    owner: string;
    framework: string;
    language: string;
    version: string;
  };
  syncStatus: {
    lastSync: string;
    conflicts: string[];
    pendingChanges: { [platform: string]: string[] };
  };
}

export interface UnifiedWorkflowConfig {
  cursor?: {
    apiKey: string;
    projectPath?: string;
    workspaceId?: string;
    userId?: string;
  };
  boltdiy?: {
    apiKey: string;
    projectId?: string;
    organizationId?: string;
    deploymentRegion?: string;
  };
  firebase?: {
    apiKey: string;
    authDomain: string;
    projectId: string;
    storageBucket: string;
    messagingSenderId: string;
    appId: string;
    measurementId?: string;
  };
  traeai?: {
    apiKey: string;
    baseUrl?: string;
    organizationId?: string;
    projectId?: string;
    enableRealTimeAnalysis?: boolean;
    enableAutoOptimization?: boolean;
  };
}

export interface UnifiedIntegrationStatus {
  overall: {
    connected: boolean
    health: 'healthy' | 'warning' | 'error'
    lastSync?: string
    activeProjects: number
    totalPlatforms: number
    connectedPlatforms: number
  }
  platforms: {
    cursor?: { connected: boolean; health: string; lastSync?: string }
    boltdiy?: { connected: boolean; health: string; lastSync?: string }
    firebase?: { connected: boolean; health: string; lastSync?: string }
    traeai?: { connected: boolean; health: string; lastSync?: string }
    vscode?: { connected: boolean; health: string; lastSync?: string }
    windsurf?: { connected: boolean; health: string; lastSync?: string }
  }
  syncStatus: {
    inProgress: boolean
    pendingConflicts: number
    lastSuccessfulSync?: string
    failedSyncs: number
  }
}

export interface SyncOperation {
  id: string
  projectId: string
  platforms: string[]
  status: 'pending' | 'running' | 'completed' | 'failed'
  startTime: string
  endTime?: string
  results: { [platform: string]: { success: boolean; error?: string } }
  conflicts: string[]
  logs: string[]
}

export class UnifiedWorkflowService {
  private cursorService: CursorService;
  private boltDiyService: BoltDiyService;
  private firebaseService: FirebaseService;
  private traeAIService: TraeAIService;
  private vscodeService: VSCodeService;
  private windsurfService: WindsurfService;
  
  private workflows: Map<string, WorkflowConfig> = new Map();
  private executions: Map<string, WorkflowExecution> = new Map();
  private eventListeners: Map<string, Function[]> = new Map();
  private isInitialized: boolean = false;
  private config: UnifiedWorkflowConfig | null = null;
  private activeSyncs: Map<string, SyncOperation> = new Map();
  private syncQueue: string[] = [];
  private isProcessingQueue: boolean = false;

  constructor() {
    this.cursorService = new CursorService();
    this.boltDiyService = new BoltDiyService();
    this.firebaseService = new FirebaseService();
    this.traeAIService = new TraeAIService();
    this.vscodeService = new VSCodeService();
    this.windsurfService = new WindsurfService();
    this.setupCrossPlatformEventHandlers();
  }

  async initialize(config?: UnifiedWorkflowConfig): Promise<{ success: boolean; errors: string[] }> {
    if (this.isInitialized) {
      return { success: true, errors: [] };
    }

    const errors: string[] = [];
    
    if (config) {
      this.config = config;
    }

    try {
      // Initialize all platform services that have initialization methods
      const initPromises: Promise<any>[] = [];
      
      // Only initialize services that have public initialization methods
      if (typeof (this.vscodeService as any).initialize === 'function') {
        initPromises.push((this.vscodeService as any).initialize());
      }
      
      if (typeof (this.windsurfService as any).initialize === 'function') {
        initPromises.push((this.windsurfService as any).initialize());
      }

      await Promise.all(initPromises);

      this.isInitialized = true;
      this.emit('initialized');
      
      return { success: true, errors };
    } catch (error: any) {
      errors.push(`Failed to initialize workflow service: ${error.message}`);
      return { success: false, errors };
    }
  }

  on(event: string, listener: Function): void {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }
    this.eventListeners.get(event)!.push(listener);
  }

  off(event: string, listener: Function): void {
    const listeners = this.eventListeners.get(event);
    if (listeners) {
      const index = listeners.indexOf(listener);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
  }

  async getUnifiedIntegrationStatus(): Promise<UnifiedIntegrationStatus> {
    const platformStatuses = {
      cursor: null as any,
      boltdiy: null as any,
      firebase: null as any,
      traeai: null as any,
      vscode: null as any,
      windsurf: null as any
    }

    let connectedCount = 0
    let totalPlatforms = 0

    // Check each platform status
    try {
      if (this.cursorService.isAuthenticated()) {
        platformStatuses.cursor = await this.cursorService.getIntegrationStatus()
        totalPlatforms++
        if (platformStatuses.cursor.connected) connectedCount++
      }
    } catch (error) {
      platformStatuses.cursor = { connected: false, health: 'error' }
    }

    try {
      if (this.boltDiyService.isAuthenticated()) {
        platformStatuses.boltdiy = await this.boltDiyService.getIntegrationStatus()
        totalPlatforms++
        if (platformStatuses.boltdiy.connected) connectedCount++
      }
    } catch (error) {
      platformStatuses.boltdiy = { connected: false, health: 'error' }
    }

    try {
      if (this.firebaseService.isAuthenticated()) {
        // Firebase doesn't have getIntegrationStatus method yet, so we'll create a basic status
        platformStatuses.firebase = { 
          connected: true, 
          health: 'healthy',
          lastSync: new Date().toISOString()
        }
        totalPlatforms++
        if (platformStatuses.firebase.connected) connectedCount++
      }
    } catch (error) {
      platformStatuses.firebase = { connected: false, health: 'error' }
    }

    try {
      if (this.traeAIService.isAuthenticated()) {
        platformStatuses.traeai = await this.traeAIService.getIntegrationStatus()
        totalPlatforms++
        if (platformStatuses.traeai.connected) connectedCount++
      }
    } catch (error) {
      platformStatuses.traeai = { connected: false, health: 'error' }
    }

    const projects = await this.getUnifiedProjects()
    const pendingConflicts = projects.reduce((sum, p) => sum + p.syncStatus.conflicts.length, 0)
    const failedSyncs = Array.from(this.activeSyncs.values()).filter(s => s.status === 'failed').length

    return {
      overall: {
        connected: connectedCount > 0,
        health: connectedCount === totalPlatforms ? 'healthy' : connectedCount > 0 ? 'warning' : 'error',
        activeProjects: projects.length,
        totalPlatforms,
        connectedPlatforms: connectedCount,
        lastSync: this.getLastSyncTime()
      },
      platforms: platformStatuses,
      syncStatus: {
        inProgress: this.isProcessingQueue || this.activeSyncs.size > 0,
        pendingConflicts,
        lastSuccessfulSync: this.getLastSuccessfulSync(),
        failedSyncs
      }
    }
  }

  async performUnifiedSync(projectId: string, platforms?: string[]): Promise<SyncOperation> {
    const syncId = `sync_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    const project = await this.getUnifiedProject(projectId)
    
    if (!project) {
      throw new Error('Project not found')
    }

    const targetPlatforms = platforms || Object.keys(project.platforms)
    const syncOperation: SyncOperation = {
      id: syncId,
      projectId,
      platforms: targetPlatforms,
      status: 'pending',
      startTime: new Date().toISOString(),
      results: {},
      conflicts: [],
      logs: []
    }

    this.activeSyncs.set(syncId, syncOperation)
    this.emit('syncStarted', { syncId, projectId, platforms: targetPlatforms })

    try {
      syncOperation.status = 'running'
      syncOperation.logs.push(`Starting sync for project ${projectId} across ${targetPlatforms.length} platforms`)

      // Perform sync for each platform
      for (const platform of targetPlatforms) {
        try {
          const result = await this.syncPlatform(platform, project)
          syncOperation.results[platform] = { success: result }
          syncOperation.logs.push(`${platform}: ${result ? 'Success' : 'Failed'}`)
        } catch (error: any) {
          syncOperation.results[platform] = { success: false, error: error.message }
          syncOperation.logs.push(`${platform}: Error - ${error.message}`)
        }
      }

      // Check for conflicts
      syncOperation.conflicts = await this.detectAllConflicts(project)
      
      const successCount = Object.values(syncOperation.results).filter(r => r.success).length
      syncOperation.status = successCount === targetPlatforms.length ? 'completed' : 'failed'
      syncOperation.endTime = new Date().toISOString()

      this.emit('syncCompleted', { syncId, success: syncOperation.status === 'completed' })
      
    } catch (error: any) {
      syncOperation.status = 'failed'
      syncOperation.endTime = new Date().toISOString()
      syncOperation.logs.push(`Sync failed: ${error.message}`)
      this.emit('syncFailed', { syncId, error: error.message })
    }

    return syncOperation
  }

  private async syncPlatform(platform: string, project: CrossPlatformProject): Promise<boolean> {
    switch (platform) {
      case 'cursor':
        return await this.cursorService.syncProject()
          .then(result => result.success)
          .catch(() => false)
      
      case 'boltdiy':
        return await this.boltDiyService.syncWithAllPlatforms()
          .then(result => result.success)
          .catch(() => false)
      
      case 'firebase':
        const firebaseResult = await this.firebaseService.syncAllPlatforms(project.id)
        return firebaseResult.cursor && firebaseResult.boltdiy && firebaseResult.traeai
      
      case 'traeai':
        return await this.traeAIService.syncWithAllPlatforms(project.id)
          .then(result => result.success)
          .catch(() => false)
      
      default:
        return false
    }
  }

  private async detectAllConflicts(project: CrossPlatformProject): Promise<string[]> {
    const conflicts: string[] = []
    
    // Check for file conflicts across platforms
    for (const [fileName, content] of Object.entries(project.files)) {
      const platformVersions = new Map<string, string>()
      
      // Get file versions from each platform
      for (const platform of Object.keys(project.platforms)) {
        try {
          const platformContent = await this.getPlatformFileContent(platform, project.id, fileName)
          if (platformContent && platformContent !== content) {
            platformVersions.set(platform, platformContent)
          }
        } catch (error) {
          // Platform might not have this file
        }
      }
      
      if (platformVersions.size > 1) {
        conflicts.push(`File ${fileName} has different versions across platforms: ${Array.from(platformVersions.keys()).join(', ')}`)
      }
    }
    
    return conflicts
  }

  private async getPlatformFileContent(platform: string, projectId: string, fileName: string): Promise<string | null> {
    // This would be implemented to fetch file content from specific platforms
    // For now, return null as a placeholder
    return null
  }

  private getLastSyncTime(): string | undefined {
    const syncs = Array.from(this.activeSyncs.values())
    const completedSyncs = syncs.filter(s => s.status === 'completed')
    if (completedSyncs.length === 0) return undefined
    
    return completedSyncs
      .sort((a, b) => new Date(b.endTime!).getTime() - new Date(a.endTime!).getTime())[0]
      .endTime
  }

  private getLastSuccessfulSync(): string | undefined {
    return this.getLastSyncTime()
  }

  getSyncOperation(syncId: string): SyncOperation | null {
    return this.activeSyncs.get(syncId) || null
  }

  getAllSyncOperations(): SyncOperation[] {
    return Array.from(this.activeSyncs.values())
  }

  private setupCrossPlatformEventHandlers(): void {
    // Setup event handlers for cross-platform communication
    // This would be implemented to listen to platform events
  }

  private emit(event: string, data?: any): void {
    const listeners = this.eventListeners.get(event) || []
    listeners.forEach(listener => {
      try {
        listener(data)
      } catch (error) {
        console.error(`Error in event listener for ${event}:`, error)
      }
    })
  }

  async getUnifiedProjects(): Promise<CrossPlatformProject[]> {
    // This would fetch all unified projects from storage
    return []
  }

  async getUnifiedProject(projectId: string): Promise<CrossPlatformProject | null> {
    // This would fetch a specific project from storage
    return null
  }
}

// Export singleton instance
export const unifiedWorkflowService = new UnifiedWorkflowService();