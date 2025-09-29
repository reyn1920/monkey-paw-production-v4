import { BrowserEventEmitter } from './BrowserEventEmitter';
import { toast } from 'react-hot-toast';

export interface VSCodeProject {
  id: string;
  name: string;
  path: string;
  workspace?: string;
  extensions: string[];
  settings: Record<string, any>;
  lastModified: Date;
  status: 'active' | 'inactive' | 'syncing';
  integrations?: {
    cursor?: boolean;
    boltdiy?: boolean;
    firebase?: boolean;
    traeai?: boolean;
    windsurf?: boolean;
  };
}

export interface VSCodeExtension {
  id: string;
  name: string;
  version: string;
  enabled: boolean;
  category: string;
  description?: string;
  publisher?: string;
  installDate?: Date;
  updateAvailable?: boolean;
}

export interface VSCodeSettings {
  theme: string;
  fontSize: number;
  tabSize: number;
  autoSave: boolean;
  formatOnSave: boolean;
  extensions: VSCodeExtension[];
  workbench?: Record<string, any>;
  editor?: Record<string, any>;
}

export interface VSCodeConfig {
  apiKey?: string;
  serverUrl?: string;
  workspacePath?: string;
  autoSync?: boolean;
  syncInterval?: number;
}

export interface VSCodeIntegrationStatus {
  connected: boolean;
  lastSync?: Date;
  projectCount: number;
  activeExtensions: number;
  syncStatus: 'idle' | 'syncing' | 'error';
  integrations: {
    cursor: boolean;
    boltdiy: boolean;
    firebase: boolean;
    traeai: boolean;
    windsurf: boolean;
  };
}

export interface VSCodeApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: Date;
}

export class VSCodeService extends BrowserEventEmitter {
  private projects: Map<string, VSCodeProject> = new Map();
  private extensions: Map<string, VSCodeExtension> = new Map();
  private isConnected = false;
  private connectionStatus: 'connected' | 'disconnected' | 'connecting' = 'disconnected';
  private config: VSCodeConfig | null = null;
  private baseUrl = 'http://localhost:3001/api/vscode';
  private wsUrl = 'ws://localhost:3001/ws/vscode';
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private syncInterval: NodeJS.Timeout | null = null;

  constructor() {
    super();
    this.initializeService();
    this.setupErrorHandling();
  }

  private setupErrorHandling(): void {
    this.on('error', (error: any) => {
      console.error('VS Code Service Error:', error);
      toast.error(`VS Code Error: ${error.message || 'Unknown error'}`);
    });
  }

  private async initializeService(): Promise<void> {
    try {
      await this.loadStoredConfig();
      await this.simulateConnection();
      this.loadMockProjects();
      this.loadMockExtensions();
      this.emit('initialized');
      toast.success('VS Code service initialized successfully');
    } catch (error) {
      console.error('Failed to initialize VS Code service:', error);
      this.emit('error', error);
      toast.error('Failed to initialize VS Code service');
    }
  }

  private async loadStoredConfig(): Promise<void> {
    try {
      const stored = localStorage.getItem('vscode-config');
      if (stored) {
        this.config = JSON.parse(stored);
      }
    } catch (error) {
      console.warn('Failed to load stored VS Code config:', error);
    }
  }

  private async simulateConnection(): Promise<void> {
    return new Promise((resolve) => {
      setTimeout(() => {
        this.isConnected = true;
        this.connectionStatus = 'connected';
        resolve();
      }, 1000);
    });
  }

  private loadMockProjects(): void {
    const mockProjects: VSCodeProject[] = [
      {
        id: 'vscode-project-1',
        name: 'React Dashboard',
        path: '/Users/dev/projects/react-dashboard',
        workspace: 'dashboard.code-workspace',
        extensions: ['ms-vscode.vscode-typescript-next', 'bradlc.vscode-tailwindcss'],
        settings: {
          'editor.fontSize': 14,
          'editor.tabSize': 2,
          'files.autoSave': 'afterDelay'
        },
        lastModified: new Date(),
        status: 'active',
        integrations: {
          cursor: true,
          boltdiy: false,
          firebase: true,
          traeai: true,
          windsurf: false
        }
      },
      {
        id: 'vscode-project-2',
        name: 'Node.js API',
        path: '/Users/dev/projects/nodejs-api',
        extensions: ['ms-vscode.vscode-json', 'ms-vscode.vscode-eslint'],
        settings: {
          'editor.fontSize': 12,
          'editor.tabSize': 4,
          'files.autoSave': 'off'
        },
        lastModified: new Date(Date.now() - 86400000),
        status: 'inactive',
        integrations: {
          cursor: false,
          boltdiy: true,
          firebase: false,
          traeai: false,
          windsurf: true
        }
      }
    ];

    mockProjects.forEach(project => {
      this.projects.set(project.id, project);
    });
  }

  private loadMockExtensions(): void {
    const mockExtensions: VSCodeExtension[] = [
      {
        id: 'ms-vscode.vscode-typescript-next',
        name: 'TypeScript Importer',
        version: '4.2.0',
        enabled: true,
        category: 'Programming Languages',
        description: 'TypeScript language support',
        publisher: 'Microsoft',
        installDate: new Date(Date.now() - 86400000 * 7),
        updateAvailable: false
      },
      {
        id: 'bradlc.vscode-tailwindcss',
        name: 'Tailwind CSS IntelliSense',
        version: '0.9.11',
        enabled: true,
        category: 'Other',
        description: 'Intelligent Tailwind CSS tooling',
        publisher: 'Brad Cornes',
        installDate: new Date(Date.now() - 86400000 * 14),
        updateAvailable: true
      },
      {
        id: 'ms-vscode.vscode-eslint',
        name: 'ESLint',
        version: '2.4.2',
        enabled: true,
        category: 'Linters',
        description: 'Integrates ESLint JavaScript',
        publisher: 'Microsoft',
        installDate: new Date(Date.now() - 86400000 * 21),
        updateAvailable: false
      }
    ];

    mockExtensions.forEach(ext => {
      this.extensions.set(ext.id, ext);
    });
  }

  async connect(config?: VSCodeConfig): Promise<boolean> {
    try {
      this.connectionStatus = 'connecting';
      this.emit('connectionStatusChanged', this.connectionStatus);
      toast.loading('Connecting to VS Code...', { id: 'vscode-connect' });

      if (config) {
        this.config = config;
        localStorage.setItem('vscode-config', JSON.stringify(config));
      }

      // Simulate connection process
      await new Promise(resolve => setTimeout(resolve, 2000));

      this.isConnected = true;
      this.connectionStatus = 'connected';
      this.reconnectAttempts = 0;
      
      if (this.config?.autoSync) {
        this.startPeriodicSync();
      }

      this.emit('connected');
      this.emit('connectionStatusChanged', this.connectionStatus);
      
      toast.success('Successfully connected to VS Code!', { id: 'vscode-connect' });
      return true;
    } catch (error) {
      this.connectionStatus = 'disconnected';
      this.emit('connectionError', error);
      this.emit('connectionStatusChanged', this.connectionStatus);
      toast.error('Failed to connect to VS Code', { id: 'vscode-connect' });
      return false;
    }
  }

  async disconnect(): Promise<void> {
    try {
      this.isConnected = false;
      this.connectionStatus = 'disconnected';
      
      if (this.syncInterval) {
        clearInterval(this.syncInterval);
        this.syncInterval = null;
      }

      if (this.ws) {
        this.ws.close();
        this.ws = null;
      }

      this.emit('disconnected');
      this.emit('connectionStatusChanged', this.connectionStatus);
      toast.success('Disconnected from VS Code');
    } catch (error) {
      console.error('Error disconnecting from VS Code:', error);
      toast.error('Error disconnecting from VS Code');
    }
  }

  getConnectionStatus(): 'connected' | 'disconnected' | 'connecting' {
    return this.connectionStatus;
  }

  isServiceConnected(): boolean {
    return this.isConnected;
  }

  async getIntegrationStatus(): Promise<VSCodeIntegrationStatus> {
    const projects = await this.getProjects();
    const extensions = await this.getExtensions();
    
    return {
      connected: this.isConnected,
      lastSync: projects.length > 0 ? new Date() : undefined,
      projectCount: projects.length,
      activeExtensions: extensions.filter(ext => ext.enabled).length,
      syncStatus: 'idle',
      integrations: {
        cursor: projects.some(p => p.integrations?.cursor),
        boltdiy: projects.some(p => p.integrations?.boltdiy),
        firebase: projects.some(p => p.integrations?.firebase),
        traeai: projects.some(p => p.integrations?.traeai),
        windsurf: projects.some(p => p.integrations?.windsurf)
      }
    };
  }

  private async makeRequest<T>(endpoint: string, options: RequestInit = {}): Promise<VSCodeApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': this.config?.apiKey ? `Bearer ${this.config.apiKey}` : '',
          ...options.headers,
        },
      });

      const data = await response.json();
      
      return {
        success: response.ok,
        data: response.ok ? data : undefined,
        error: response.ok ? undefined : data.message || 'Request failed',
        timestamp: new Date()
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
        timestamp: new Date()
      };
    }
  }

  private startPeriodicSync(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
    }

    const interval = this.config?.syncInterval || 300000; // 5 minutes default
    this.syncInterval = setInterval(() => {
      this.syncAllProjects();
    }, interval);
  }

  async getProjects(): Promise<VSCodeProject[]> {
    return Array.from(this.projects.values());
  }

  async getProject(projectId: string): Promise<VSCodeProject | null> {
    return this.projects.get(projectId) || null;
  }

  async getExtensions(): Promise<VSCodeExtension[]> {
    return Array.from(this.extensions.values());
  }

  async getExtension(extensionId: string): Promise<VSCodeExtension | null> {
    return this.extensions.get(extensionId) || null;
  }

  async createProject(projectData: Omit<VSCodeProject, 'id' | 'lastModified'>): Promise<VSCodeProject> {
    try {
      const project: VSCodeProject = {
        ...projectData,
        id: `vscode-${Date.now()}`,
        lastModified: new Date(),
        status: 'active'
      };

      this.projects.set(project.id, project);
      this.emit('projectCreated', project);
      toast.success(`VS Code project "${project.name}" created successfully`);
      
      return project;
    } catch (error) {
      console.error('Error creating VS Code project:', error);
      toast.error('Failed to create VS Code project');
      throw error;
    }
  }

  async updateProject(projectId: string, updates: Partial<VSCodeProject>): Promise<VSCodeProject> {
    try {
      const project = this.projects.get(projectId);
      if (!project) {
        throw new Error(`VS Code project ${projectId} not found`);
      }

      const updatedProject = {
        ...project,
        ...updates,
        lastModified: new Date()
      };

      this.projects.set(projectId, updatedProject);
      this.emit('projectUpdated', updatedProject);
      toast.success(`VS Code project "${updatedProject.name}" updated successfully`);
      
      return updatedProject;
    } catch (error) {
      console.error('Error updating VS Code project:', error);
      toast.error('Failed to update VS Code project');
      throw error;
    }
  }

  async deleteProject(projectId: string): Promise<void> {
    try {
      const project = this.projects.get(projectId);
      if (!project) {
        throw new Error(`VS Code project ${projectId} not found`);
      }

      this.projects.delete(projectId);
      this.emit('projectDeleted', projectId);
      toast.success(`VS Code project "${project.name}" deleted successfully`);
    } catch (error) {
      console.error('Error deleting VS Code project:', error);
      toast.error('Failed to delete VS Code project');
      throw error;
    }
  }

  async syncProject(projectId: string): Promise<void> {
    try {
      const project = this.projects.get(projectId);
      if (!project) {
        throw new Error(`VS Code project ${projectId} not found`);
      }

      await this.updateProject(projectId, { status: 'syncing' });
      
      toast.loading(`Syncing VS Code project "${project.name}"...`, { id: `vscode-sync-${projectId}` });

      // Simulate sync process
      await new Promise(resolve => setTimeout(resolve, 3000));

      await this.updateProject(projectId, { status: 'active' });
      
      this.emit('projectSynced', project);
      toast.success(`VS Code project "${project.name}" synced successfully`, { id: `vscode-sync-${projectId}` });
    } catch (error) {
      console.error('Error syncing VS Code project:', error);
      toast.error('Failed to sync VS Code project', { id: `vscode-sync-${projectId}` });
      throw error;
    }
  }

  async syncAllProjects(): Promise<void> {
    const projects = await this.getProjects();
    const activeProjects = projects.filter(p => p.status === 'active');
    
    for (const project of activeProjects) {
      try {
        await this.syncProject(project.id);
      } catch (error) {
        console.error(`Failed to sync project ${project.id}:`, error);
      }
    }
  }

  // Cross-platform sync methods
  async syncWithCursor(projectId: string): Promise<boolean> {
    try {
      const project = this.projects.get(projectId);
      if (!project) return false;

      // Simulate cursor sync
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      await this.updateProject(projectId, {
        integrations: { ...project.integrations, cursor: true }
      });
      
      this.emit('cursorSyncCompleted', { projectId, success: true });
      return true;
    } catch (error) {
      this.emit('cursorSyncCompleted', { projectId, success: false, error });
      return false;
    }
  }

  async syncWithBoltDiy(projectId: string): Promise<boolean> {
    try {
      const project = this.projects.get(projectId);
      if (!project) return false;

      // Simulate bolt.diy sync
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      await this.updateProject(projectId, {
        integrations: { ...project.integrations, boltdiy: true }
      });
      
      this.emit('boltdiySyncCompleted', { projectId, success: true });
      return true;
    } catch (error) {
      this.emit('boltdiySyncCompleted', { projectId, success: false, error });
      return false;
    }
  }

  async syncWithFirebase(projectId: string): Promise<boolean> {
    try {
      const project = this.projects.get(projectId);
      if (!project) return false;

      // Simulate firebase sync
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      await this.updateProject(projectId, {
        integrations: { ...project.integrations, firebase: true }
      });
      
      this.emit('firebaseSyncCompleted', { projectId, success: true });
      return true;
    } catch (error) {
      this.emit('firebaseSyncCompleted', { projectId, success: false, error });
      return false;
    }
  }

  async syncWithTraeAI(projectId: string): Promise<boolean> {
    try {
      const project = this.projects.get(projectId);
      if (!project) return false;

      // Simulate trae.ai sync
      await new Promise(resolve => setTimeout(resolve, 1200));
      
      await this.updateProject(projectId, {
        integrations: { ...project.integrations, traeai: true }
      });
      
      this.emit('traeaiSyncCompleted', { projectId, success: true });
      return true;
    } catch (error) {
      this.emit('traeaiSyncCompleted', { projectId, success: false, error });
      return false;
    }
  }

  async getSettings(): Promise<VSCodeSettings> {
    const extensions = await this.getExtensions();
    return {
      theme: 'Dark+ (default dark)',
      fontSize: 14,
      tabSize: 2,
      autoSave: true,
      formatOnSave: true,
      extensions,
      workbench: {
        'colorTheme': 'Default Dark+',
        'iconTheme': 'vs-seti'
      },
      editor: {
        'fontSize': 14,
        'tabSize': 2,
        'insertSpaces': true,
        'formatOnSave': true
      }
    };
  }

  async updateSettings(settings: Partial<VSCodeSettings>): Promise<void> {
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      this.emit('settingsUpdated', settings);
      toast.success('VS Code settings updated successfully');
    } catch (error) {
      console.error('Error updating VS Code settings:', error);
      toast.error('Failed to update VS Code settings');
      throw error;
    }
  }

  async openProject(projectId: string): Promise<void> {
    try {
      const project = this.projects.get(projectId);
      if (!project) {
        throw new Error(`VS Code project ${projectId} not found`);
      }

      await new Promise(resolve => setTimeout(resolve, 1500));
      
      this.emit('projectOpened', project);
      toast.success(`Opened "${project.name}" in VS Code`);
    } catch (error) {
      console.error('Error opening VS Code project:', error);
      toast.error('Failed to open project in VS Code');
      throw error;
    }
  }

  async installExtension(extensionId: string): Promise<void> {
    try {
      toast.loading(`Installing VS Code extension: ${extensionId}...`, { id: `vscode-ext-${extensionId}` });
      
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Add to extensions map if not exists
      if (!this.extensions.has(extensionId)) {
        const newExtension: VSCodeExtension = {
          id: extensionId,
          name: extensionId.split('.').pop() || extensionId,
          version: '1.0.0',
          enabled: true,
          category: 'Other',
          installDate: new Date()
        };
        this.extensions.set(extensionId, newExtension);
      }
      
      this.emit('extensionInstalled', extensionId);
      toast.success(`VS Code extension "${extensionId}" installed successfully`, { id: `vscode-ext-${extensionId}` });
    } catch (error) {
      console.error('Error installing VS Code extension:', error);
      toast.error('Failed to install VS Code extension', { id: `vscode-ext-${extensionId}` });
      throw error;
    }
  }

  async uninstallExtension(extensionId: string): Promise<void> {
    try {
      toast.loading(`Uninstalling VS Code extension: ${extensionId}...`, { id: `vscode-ext-${extensionId}` });
      
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      this.extensions.delete(extensionId);
      
      this.emit('extensionUninstalled', extensionId);
      toast.success(`VS Code extension "${extensionId}" uninstalled successfully`, { id: `vscode-ext-${extensionId}` });
    } catch (error) {
      console.error('Error uninstalling VS Code extension:', error);
      toast.error('Failed to uninstall VS Code extension', { id: `vscode-ext-${extensionId}` });
      throw error;
    }
  }

  async enableExtension(extensionId: string): Promise<void> {
    try {
      const extension = this.extensions.get(extensionId);
      if (!extension) {
        throw new Error(`Extension ${extensionId} not found`);
      }

      extension.enabled = true;
      this.extensions.set(extensionId, extension);
      
      this.emit('extensionEnabled', extensionId);
      toast.success(`VS Code extension "${extension.name}" enabled`);
    } catch (error) {
      console.error('Error enabling VS Code extension:', error);
      toast.error('Failed to enable VS Code extension');
      throw error;
    }
  }

  async disableExtension(extensionId: string): Promise<void> {
    try {
      const extension = this.extensions.get(extensionId);
      if (!extension) {
        throw new Error(`Extension ${extensionId} not found`);
      }

      extension.enabled = false;
      this.extensions.set(extensionId, extension);
      
      this.emit('extensionDisabled', extensionId);
      toast.success(`VS Code extension "${extension.name}" disabled`);
    } catch (error) {
      console.error('Error disabling VS Code extension:', error);
      toast.error('Failed to disable VS Code extension');
      throw error;
    }
  }

  async updateExtension(extensionId: string): Promise<void> {
    try {
      const extension = this.extensions.get(extensionId);
      if (!extension) {
        throw new Error(`Extension ${extensionId} not found`);
      }

      toast.loading(`Updating VS Code extension: ${extension.name}...`, { id: `vscode-ext-update-${extensionId}` });
      
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      extension.updateAvailable = false;
      extension.version = '1.0.1'; // Simulate version update
      this.extensions.set(extensionId, extension);
      
      this.emit('extensionUpdated', extensionId);
      toast.success(`VS Code extension "${extension.name}" updated successfully`, { id: `vscode-ext-update-${extensionId}` });
    } catch (error) {
      console.error('Error updating VS Code extension:', error);
      toast.error('Failed to update VS Code extension', { id: `vscode-ext-update-${extensionId}` });
      throw error;
    }
  }

  async getStatus(): Promise<{
    connected: boolean;
    projectCount: number;
    activeProjects: number;
    lastSync: Date | null;
    extensionCount: number;
    enabledExtensions: number;
  }> {
    const projects = await this.getProjects();
    const extensions = await this.getExtensions();
    const activeProjects = projects.filter(p => p.status === 'active').length;
    const enabledExtensions = extensions.filter(e => e.enabled).length;
    
    return {
      connected: this.isConnected,
      projectCount: projects.length,
      activeProjects,
      lastSync: projects.length > 0 ? new Date() : null,
      extensionCount: extensions.length,
      enabledExtensions
    };
  }

  // Methods needed by UnifiedWorkflowService
  async getChangedFiles(projectId: string, since?: string): Promise<string[]> {
    const project = this.projects.get(projectId);
    if (!project) {
      throw new Error(`Project ${projectId} not found`);
    }

    // Simulate getting changed files
    return [`${project.path}/src/main.ts`, `${project.path}/package.json`];
  }

  async updateFiles(projectId: string, files: { path: string; content: string }[]): Promise<boolean> {
    const project = this.projects.get(projectId);
    if (!project) {
      throw new Error(`Project ${projectId} not found`);
    }

    try {
      project.lastModified = new Date();
      this.emit('filesUpdated', { projectId, files });
      return true;
    } catch (error) {
      return false;
    }
  }

  async getFileContent(projectId: string, filePath: string): Promise<string | null> {
    const project = this.projects.get(projectId);
    if (!project) {
      return null;
    }

    // Simulate file content retrieval
    return `// Content of ${filePath}\n// Project: ${project.name}`;
  }
}

export const vscodeService = new VSCodeService();