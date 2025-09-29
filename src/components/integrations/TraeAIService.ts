export interface TraeAIConfig {
  apiKey: string;
  baseUrl?: string;
  organizationId?: string;
  projectId?: string;
  enableRealTimeAnalysis?: boolean;
  enableAutoOptimization?: boolean;
}

export interface TraeAIProject {
  id: string;
  name: string;
  description: string;
  framework: string;
  files: { [key: string]: string };
  metadata: {
    createdAt: string;
    updatedAt: string;
    owner: string;
    collaborators: string[];
    tags: string[];
    status: 'active' | 'archived' | 'draft';
    version: string;
    language: string;
    dependencies: { [key: string]: string };
  };
  aiContext: {
    requirements: string[];
    suggestions: string[];
    codeReviews: TraeAICodeReview[];
    optimizations: TraeAIOptimization[];
    documentation: TraeAIDocumentation[];
    testCoverage: TraeAITestCoverage;
  };
  integrations: {
    cursor: boolean;
    boltdiy: boolean;
    firebase: boolean;
    github: boolean;
  };
}

export interface TraeAICodeReview {
  id: string;
  fileName: string;
  lineNumber: number;
  severity: 'info' | 'warning' | 'error' | 'critical';
  category: 'syntax' | 'logic' | 'performance' | 'security' | 'style' | 'accessibility';
  message: string;
  suggestion?: string;
  autoFixAvailable: boolean;
  timestamp: string;
  confidence: number;
}

export interface TraeAIOptimization {
  id: string;
  type: 'performance' | 'security' | 'maintainability' | 'accessibility' | 'bundle-size' | 'memory';
  description: string;
  impact: 'low' | 'medium' | 'high' | 'critical';
  effort: 'low' | 'medium' | 'high';
  implementation: string;
  beforeCode?: string;
  afterCode?: string;
  metrics: {
    performanceGain?: number;
    bundleSizeReduction?: number;
    memoryImprovement?: number;
  };
  timestamp: string;
  applied: boolean;
}

export interface TraeAIDocumentation {
  id: string;
  type: 'function' | 'class' | 'module' | 'api' | 'readme';
  fileName: string;
  content: string;
  generatedAt: string;
  quality: 'excellent' | 'good' | 'fair' | 'poor';
  completeness: number;
}

export interface TraeAITestCoverage {
  overall: number;
  byFile: { [fileName: string]: number };
  uncoveredLines: { [fileName: string]: number[] };
  suggestions: string[];
  missingTests: string[];
}

export interface TraeAIWorkflow {
  id: string;
  name: string;
  description: string;
  steps: TraeAIWorkflowStep[];
  triggers: string[];
  status: 'active' | 'paused' | 'completed' | 'failed';
  schedule?: string;
  lastRun?: string;
  nextRun?: string;
}

export interface TraeAIWorkflowStep {
  id: string;
  name: string;
  type: 'code_generation' | 'code_review' | 'testing' | 'deployment' | 'optimization' | 'documentation' | 'security_scan';
  config: { [key: string]: any };
  dependencies: string[];
  status: 'pending' | 'running' | 'completed' | 'failed' | 'skipped';
  output?: any;
  duration?: number;
}

export interface TraeAIAnalytics {
  projectId: string;
  codeQuality: {
    score: number;
    trends: { date: string; score: number }[];
    issues: { type: string; count: number; severity: string }[];
    improvements: { date: string; description: string }[];
  };
  productivity: {
    linesOfCode: number;
    filesModified: number;
    commitsToday: number;
    aiSuggestions: number;
    aiSuggestionsAccepted: number;
    timeSpentCoding: number;
  };
  performance: {
    buildTime: number;
    testCoverage: number;
    bundleSize: number;
    loadTime: number;
    memoryUsage: number;
    apiResponseTime: number;
  };
  security: {
    vulnerabilities: { severity: string; count: number }[];
    securityScore: number;
    lastScan: string;
    fixedIssues: number;
  };
}

export interface TraeAIInsight {
  id: string;
  type: 'suggestion' | 'warning' | 'opportunity' | 'achievement';
  title: string;
  description: string;
  actionable: boolean;
  priority: 'low' | 'medium' | 'high' | 'critical';
  category: 'performance' | 'security' | 'maintainability' | 'productivity';
  timestamp: string;
  data?: any;
}

export interface TraeAISyncResult {
  success: boolean;
  platform: 'cursor' | 'boltdiy' | 'firebase';
  syncedFiles: string[];
  conflicts: string[];
  errors: string[];
  timestamp: string;
}

export interface TraeAIIntegrationStatus {
  connected: boolean
  authenticated: boolean
  lastAnalysis?: string
  projectsCount: number
  activeWorkflows: number
  apiVersion: string
  health: 'healthy' | 'warning' | 'error'
  features: {
    codeAnalysis: boolean
    autoOptimization: boolean
    realTimeSync: boolean
    workflowAutomation: boolean
  }
}

export class TraeAIService {
  private config: TraeAIConfig | null = null;
  private isConnected: boolean = false;
  private baseUrl: string = 'https://api.trae.ai/v1';
  private websocket: WebSocket | null = null;
  private eventListeners: Map<string, Function[]> = new Map();
  private analysisQueue: Array<{ projectId: string; files: string[] }> = [];
  private isProcessingQueue: boolean = false;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;

  constructor() {
    this.setupEventHandlers();
  }

  async connect(config: TraeAIConfig): Promise<{ success: boolean; error?: string }> {
    try {
      this.config = config;
      this.baseUrl = config.baseUrl || this.baseUrl;
      
      // Test the connection
      const connectionTest = await this.testConnection();
      if (!connectionTest) {
        throw new Error('Failed to connect to Trae.ai API');
      }
      
      this.isConnected = true;
      
      // Initialize WebSocket if real-time analysis is enabled
      if (config.enableRealTimeAnalysis) {
        await this.initializeWebSocket();
      }
      
      // Start auto-optimization if enabled
      if (config.enableAutoOptimization) {
        this.startAutoOptimization();
      }
      
      this.emit('connected', { config });
      return { success: true };
    } catch (error: any) {
      this.isConnected = false;
      this.emit('connectionError', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  async getIntegrationStatus(): Promise<TraeAIIntegrationStatus> {
    try {
      if (!this.isConnected) {
        return {
          connected: false,
          authenticated: false,
          projectsCount: 0,
          activeWorkflows: 0,
          apiVersion: '1.0',
          health: 'error',
          features: {
            codeAnalysis: false,
            autoOptimization: false,
            realTimeSync: false,
            workflowAutomation: false
          }
        }
      }

      const response = await this.makeRequest('/status', 'GET')
      return {
        connected: true,
        authenticated: true,
        lastAnalysis: response.lastAnalysis,
        projectsCount: response.projectsCount || 0,
        activeWorkflows: response.activeWorkflows || 0,
        apiVersion: response.apiVersion || '1.0',
        health: response.health || 'healthy',
        features: {
          codeAnalysis: response.features?.codeAnalysis || true,
          autoOptimization: response.features?.autoOptimization || true,
          realTimeSync: response.features?.realTimeSync || true,
          workflowAutomation: response.features?.workflowAutomation || true
        }
      }
    } catch (error) {
      return {
        connected: false,
        authenticated: false,
        projectsCount: 0,
        activeWorkflows: 0,
        apiVersion: '1.0',
        health: 'error',
        features: {
          codeAnalysis: false,
          autoOptimization: false,
          realTimeSync: false,
          workflowAutomation: false
        }
      }
    }
  }

  async syncWithAllPlatforms(projectId: string): Promise<{ success: boolean; results: TraeAISyncResult[] }> {
    const results: TraeAISyncResult[] = []
    
    try {
      // Get project data
      const project = await this.getProject(projectId)
      if (!project) {
        throw new Error('Project not found')
      }

      // Sync with Cursor
      if (project.integrations.cursor) {
        const cursorResult = await this.syncWithCursor(projectId, {
          files: project.files,
          metadata: project.metadata
        })
        results.push({
          success: cursorResult,
          platform: 'cursor',
          syncedFiles: Object.keys(project.files),
          conflicts: [],
          errors: cursorResult ? [] : ['Cursor sync failed'],
          timestamp: new Date().toISOString()
        })
      }

      // Sync with Bolt.diy
      if (project.integrations.boltdiy) {
        const boltResult = await this.syncWithBoltDiy(projectId, {
          files: project.files,
          components: project.aiContext.suggestions
        })
        results.push({
          success: boltResult,
          platform: 'boltdiy',
          syncedFiles: Object.keys(project.files),
          conflicts: [],
          errors: boltResult ? [] : ['Bolt.diy sync failed'],
          timestamp: new Date().toISOString()
        })
      }

      // Sync with Firebase
      if (project.integrations.firebase) {
        const firebaseResult = await this.syncWithFirebase(projectId, {
          files: project.files,
          config: project.metadata
        })
        results.push({
          success: firebaseResult,
          platform: 'firebase',
          syncedFiles: Object.keys(project.files),
          conflicts: [],
          errors: firebaseResult ? [] : ['Firebase sync failed'],
          timestamp: new Date().toISOString()
        })
      }

      return { success: true, results }
    } catch (error: any) {
      return { 
        success: false, 
        results: [...results, {
          success: false,
          platform: 'cursor',
          syncedFiles: [],
          conflicts: [],
          errors: [error.message],
          timestamp: new Date().toISOString()
        }]
      }
    }
  }

  async enableCrossPlatformSync(projectId: string, platforms: ('cursor' | 'boltdiy' | 'firebase')[]): Promise<boolean> {
    try {
      const response = await this.makeRequest(`/projects/${projectId}/integrations`, 'PUT', {
        integrations: platforms.reduce((acc, platform) => {
          acc[platform] = true
          return acc
        }, {} as any)
      })

      this.emit('integrationsUpdated', { projectId, platforms })
      return response.success
    } catch (error: any) {
      this.emit('integrationError', { projectId, error: error.message })
      return false
    }
  }

  async generateProjectInsights(projectId: string): Promise<TraeAIInsight[]> {
    try {
      const response = await this.makeRequest(`/projects/${projectId}/insights`, 'GET')
      return response.insights || []
    } catch (error: any) {
      this.emit('insightError', { projectId, error: error.message })
      return []
    }
  }

  disconnect(): void {
    this.isConnected = false;
    this.config = null;
    
    if (this.websocket) {
      this.websocket.close();
      this.websocket = null;
    }
    
    this.stopAutoOptimization();
    this.emit('disconnected');
  }

  isAuthenticated(): boolean {
    return this.isConnected && this.config !== null;
  }

  // Enhanced project management
  async createProject(projectData: Omit<TraeAIProject, 'id' | 'metadata' | 'aiContext' | 'integrations'>): Promise<string | null> {
    if (!this.isConnected) return null;

    try {
      const response = await this.makeRequest('/projects', 'POST', {
        ...projectData,
        metadata: {
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          owner: this.config?.organizationId || 'unknown',
          collaborators: [],
          tags: [],
          status: 'active',
          version: '1.0.0',
          language: this.detectLanguage(projectData.files),
          dependencies: this.extractDependencies(projectData.files)
        },
        aiContext: {
          requirements: [],
          suggestions: [],
          codeReviews: [],
          optimizations: [],
          documentation: [],
          testCoverage: {
            overall: 0,
            byFile: {},
            uncoveredLines: {},
            suggestions: [],
            missingTests: []
          }
        },
        integrations: {
          cursor: false,
          boltdiy: false,
          firebase: false,
          github: false
        }
      });

      if (response.success) {
        const projectId = response.data.id;
        
        // Start initial analysis
        await this.analyzeProject(projectId);
        
        this.emit('projectCreated', { projectId, data: response.data });
        return projectId;
      }
      return null;
    } catch (error: any) {
      console.error('Failed to create project:', error);
      this.emit('projectCreationError', { error });
      return null;
    }
  }

  async getProject(projectId: string): Promise<TraeAIProject | null> {
    if (!this.isAuthenticated()) return null;

    try {
      const response = await this.makeRequest(`/projects/${projectId}`, 'GET');
      return response.data || null;
    } catch (error) {
      console.error('Failed to get Trae.ai project:', error);
      return null;
    }
  }

  async updateProject(projectId: string, updates: Partial<TraeAIProject>): Promise<boolean> {
    if (!this.isAuthenticated()) return false;

    try {
      const response = await this.makeRequest(`/projects/${projectId}`, 'PUT', {
        ...updates,
        'metadata.updatedAt': new Date().toISOString()
      });
      return response.success;
    } catch (error) {
      console.error('Failed to update Trae.ai project:', error);
      return false;
    }
  }

  async deleteProject(projectId: string): Promise<boolean> {
    if (!this.isAuthenticated()) return false;

    try {
      const response = await this.makeRequest(`/projects/${projectId}`, 'DELETE');
      return response.success;
    } catch (error) {
      console.error('Failed to delete Trae.ai project:', error);
      return false;
    }
  }

  async listProjects(): Promise<TraeAIProject[]> {
    if (!this.isAuthenticated()) return [];

    try {
      const response = await this.makeRequest('/projects', 'GET');
      return response.data || [];
    } catch (error) {
      console.error('Failed to list Trae.ai projects:', error);
      return [];
    }
  }

  // AI-powered code analysis
  async analyzeCode(projectId: string, code: string, fileName: string): Promise<TraeAICodeReview[]> {
    if (!this.isAuthenticated()) return [];

    try {
      const response = await this.makeRequest('/ai/analyze', 'POST', {
        projectId,
        code,
        fileName,
        analysisType: 'comprehensive'
      });

      return response.data?.reviews || [];
    } catch (error) {
      console.error('Failed to analyze code:', error);
      return [];
    }
  }

  async generateCode(projectId: string, prompt: string, context?: any): Promise<string | null> {
    if (!this.isAuthenticated()) return null;

    try {
      const response = await this.makeRequest('/ai/generate', 'POST', {
        projectId,
        prompt,
        context,
        model: 'trae-codegen-v2'
      });

      return response.data?.code || null;
    } catch (error) {
      console.error('Failed to generate code:', error);
      return null;
    }
  }

  async optimizeCode(projectId: string, code: string, optimizationType: string): Promise<TraeAIOptimization[]> {
    if (!this.isAuthenticated()) return [];

    try {
      const response = await this.makeRequest('/ai/optimize', 'POST', {
        projectId,
        code,
        optimizationType,
        includeExplanation: true
      });

      return response.data?.optimizations || [];
    } catch (error) {
      console.error('Failed to optimize code:', error);
      return [];
    }
  }

  // Workflow management
  async createWorkflow(workflow: Omit<TraeAIWorkflow, 'id' | 'status'>): Promise<string | null> {
    if (!this.isAuthenticated()) return null;

    try {
      const response = await this.makeRequest('/workflows', 'POST', {
        ...workflow,
        status: 'active'
      });

      return response.data?.id || null;
    } catch (error) {
      console.error('Failed to create workflow:', error);
      return null;
    }
  }

  async executeWorkflow(workflowId: string, projectId: string): Promise<boolean> {
    if (!this.isAuthenticated()) return false;

    try {
      const response = await this.makeRequest(`/workflows/${workflowId}/execute`, 'POST', {
        projectId
      });
      return response.success;
    } catch (error) {
      console.error('Failed to execute workflow:', error);
      return false;
    }
  }

  async getWorkflowStatus(workflowId: string): Promise<TraeAIWorkflow | null> {
    if (!this.isAuthenticated()) return null;

    try {
      const response = await this.makeRequest(`/workflows/${workflowId}`, 'GET');
      return response.data || null;
    } catch (error) {
      console.error('Failed to get workflow status:', error);
      return null;
    }
  }

  // Analytics and insights
  async getProjectAnalytics(projectId: string): Promise<TraeAIAnalytics | null> {
    if (!this.isAuthenticated()) return null;

    try {
      const response = await this.makeRequest(`/analytics/projects/${projectId}`, 'GET');
      return response.data || null;
    } catch (error) {
      console.error('Failed to get project analytics:', error);
      return null;
    }
  }

  async getCodeSuggestions(projectId: string, context: any): Promise<string[]> {
    if (!this.isAuthenticated()) return [];

    try {
      const response = await this.makeRequest('/ai/suggestions', 'POST', {
        projectId,
        context,
        maxSuggestions: 5
      });

      return response.data?.suggestions || [];
    } catch (error) {
      console.error('Failed to get code suggestions:', error);
      return [];
    }
  }

  // Integration synchronization
  async syncWithCursor(projectId: string, cursorData: any): Promise<boolean> {
    if (!this.isAuthenticated()) return false;

    try {
      const response = await this.makeRequest('/integrations/cursor/sync', 'POST', {
        projectId,
        data: cursorData,
        timestamp: new Date().toISOString()
      });
      return response.success;
    } catch (error) {
      console.error('Failed to sync with Cursor:', error);
      return false;
    }
  }

  async syncWithBoltDiy(projectId: string, boltData: any): Promise<boolean> {
    if (!this.isAuthenticated()) return false;

    try {
      const response = await this.makeRequest('/integrations/boltdiy/sync', 'POST', {
        projectId,
        data: boltData,
        timestamp: new Date().toISOString()
      });
      return response.success;
    } catch (error) {
      console.error('Failed to sync with Bolt.diy:', error);
      return false;
    }
  }

  async syncWithFirebase(projectId: string, firebaseData: any): Promise<boolean> {
    if (!this.isAuthenticated()) return false;

    try {
      const response = await this.makeRequest('/integrations/firebase/sync', 'POST', {
        projectId,
        data: firebaseData,
        timestamp: new Date().toISOString()
      });
      return response.success;
    } catch (error) {
      console.error('Failed to sync with Firebase:', error);
      return false;
    }
  }

  // Real-time collaboration
  async subscribeToProject(projectId: string, callback: (data: any) => void): Promise<() => void> {
    if (!this.isAuthenticated()) return () => {};

    // Simulate WebSocket connection for real-time updates
    const interval = setInterval(async () => {
      try {
        const project = await this.getProject(projectId);
        if (project) {
          callback(project);
        }
      } catch (error) {
        console.error('Failed to get real-time updates:', error);
      }
    }, 5000);

    return () => clearInterval(interval);
  }

  // Event handling system
  private setupEventHandlers(): void {
    this.eventListeners = new Map();
  }

  private emit(event: string, data?: any): void {
    const listeners = this.eventListeners.get(event) || [];
    listeners.forEach(listener => {
      try {
        listener(data);
      } catch (error) {
        console.error(`Error in event listener for ${event}:`, error);
      }
    });
  }

  on(event: string, listener: Function): () => void {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }
    this.eventListeners.get(event)!.push(listener);
    
    // Return unsubscribe function
    return () => {
      const listeners = this.eventListeners.get(event) || [];
      const index = listeners.indexOf(listener);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    };
  }

  // Enhanced utility methods
  private async initializeWebSocket(): Promise<void> {
    if (!this.config) return;
    
    try {
      const wsUrl = this.baseUrl.replace('http', 'ws') + '/ws';
      this.websocket = new WebSocket(wsUrl);
      
      this.websocket.onopen = () => {
        this.reconnectAttempts = 0; // Reset reconnect attempts on successful connection
        this.emit('websocketConnected');
      };

      this.websocket.onclose = () => {
        this.emit('websocketDisconnected');
        // Attempt to reconnect if we haven't exceeded max attempts
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          setTimeout(() => this.initializeWebSocket(), 1000 * this.reconnectAttempts);
        }
      };

      this.websocket.onerror = (error) => {
        this.emit('websocketError', { error });
      };

      this.websocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.emit('realtimeUpdate', data);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };
    } catch (error) {
      console.error('Failed to initialize WebSocket:', error);
      this.emit('websocketError', { error });
    }
  }

  private startAutoOptimization(): void {
    if (this.isProcessingQueue) return;
    
    this.isProcessingQueue = true;
    this.processAnalysisQueue();
  }

  private stopAutoOptimization(): void {
    this.isProcessingQueue = false;
    this.analysisQueue = [];
  }

  private async processAnalysisQueue(): Promise<void> {
    while (this.isProcessingQueue && this.analysisQueue.length > 0) {
      const item = this.analysisQueue.shift();
      if (item) {
        try {
          await this.analyzeProject(item.projectId);
          this.emit('autoAnalysisCompleted', { projectId: item.projectId });
        } catch (error) {
          this.emit('autoAnalysisError', { projectId: item.projectId, error });
        }
      }
      
      // Wait before processing next item
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }

  private detectLanguage(files: { [key: string]: string }): string {
    const extensions = Object.keys(files).map(file => {
      const parts = file.split('.');
      return parts.length > 1 ? parts[parts.length - 1] : '';
    });
    
    if (extensions.includes('ts') || extensions.includes('tsx')) return 'typescript';
    if (extensions.includes('js') || extensions.includes('jsx')) return 'javascript';
    if (extensions.includes('py')) return 'python';
    if (extensions.includes('java')) return 'java';
    if (extensions.includes('cpp') || extensions.includes('cc')) return 'cpp';
    
    return 'unknown';
  }

  private extractDependencies(files: { [key: string]: string }): { [key: string]: string } {
    const dependencies: { [key: string]: string } = {};
    
    // Look for package.json
    const packageJson = files['package.json'];
    if (packageJson) {
      try {
        const parsed = JSON.parse(packageJson);
        Object.assign(dependencies, parsed.dependencies || {});
        Object.assign(dependencies, parsed.devDependencies || {});
      } catch (error) {
        console.error('Failed to parse package.json:', error);
      }
    }
    
    return dependencies;
  }

  private async analyzeProject(projectId: string): Promise<void> {
    try {
      const project = await this.getProject(projectId);
      if (!project) return;
      
      // Analyze each file
      for (const [fileName, content] of Object.entries(project.files)) {
        await this.analyzeCode(projectId, content, fileName);
      }
      
      this.emit('projectAnalysisCompleted', { projectId });
    } catch (error) {
      console.error('Failed to analyze project:', error);
      this.emit('projectAnalysisError', { projectId, error });
    }
  }

  private async makeRequest(endpoint: string, method: string, data?: any): Promise<any> {
    if (!this.config) {
      throw new Error('Trae.ai not configured');
    }

    // Simulate API calls for demo purposes
    await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 1000));

    // Mock responses based on endpoint
    if (endpoint === '/auth/validate') {
      return { success: true, data: { authenticated: true } };
    }

    if (endpoint === '/projects' && method === 'POST') {
      return {
        success: true,
        data: {
          id: `trae_project_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
        }
      };
    }

    if (endpoint.startsWith('/projects/') && method === 'GET') {
      const projectId = endpoint.split('/')[2];
      return {
        success: true,
        data: {
          id: projectId,
          name: 'Sample Project',
          description: 'A sample project managed by Trae.ai',
          framework: 'react',
          files: {},
          metadata: {
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            owner: 'current_user',
            collaborators: [],
            tags: ['ai-generated'],
            status: 'active',
            version: '1.0.0',
            language: 'javascript',
            dependencies: {}
          },
          aiContext: {
            requirements: ['Build a modern web application'],
            suggestions: ['Consider using TypeScript', 'Add error boundaries'],
            codeReviews: [],
            optimizations: [],
            documentation: [],
            testCoverage: {
              overall: 0,
              byFile: {},
              uncoveredLines: {},
              suggestions: [],
              missingTests: []
            }
          },
          integrations: {
            cursor: false,
            boltdiy: false,
            firebase: false,
            github: false
          }
        }
      };
    }

    if (endpoint === '/ai/analyze') {
      return {
        success: true,
        data: {
          reviews: [
            {
              id: 'review_1',
              fileName: data.fileName,
              lineNumber: 10,
              severity: 'warning',
              category: 'style',
              message: 'Consider using const instead of let for immutable variables',
              suggestion: 'const myVariable = value;',
              autoFixAvailable: true,
              timestamp: new Date().toISOString(),
              confidence: 0.85
            }
          ]
        }
      };
    }

    if (endpoint === '/ai/generate') {
      return {
        success: true,
        data: {
          code: `// Generated by Trae.ai\n// ${data.prompt}\n\nfunction generatedFunction() {\n  // Implementation here\n  return true;\n}`
        }
      };
    }

    // Default success response
    return { success: true, data: {} };
  }

  async testConnection(): Promise<boolean> {
    if (!this.config) return false;

    try {
      const response = await this.makeRequest('/health', 'GET');
      return response.success;
    } catch (error) {
      return false;
    }
  }

  // Queue management for auto-optimization
  queueProjectForAnalysis(projectId: string, files: string[]): void {
    if (!this.config?.enableAutoOptimization) return;
    
    // Remove existing entry for this project
    this.analysisQueue = this.analysisQueue.filter(item => item.projectId !== projectId);
    
    // Add new entry
    this.analysisQueue.push({ projectId, files });
    
    // Start processing if not already running
    if (!this.isProcessingQueue) {
      this.startAutoOptimization();
    }
  }
}

// Export singleton instance with enhanced capabilities
export const traeAIService = new TraeAIService();

// Export additional utility types
export type TraeAIEventType = 'connected' | 'disconnected' | 'connectionError' | 'projectCreated' | 'projectCreationError' | 'websocketConnected' | 'websocketDisconnected' | 'websocketError' | 'realtimeUpdate' | 'autoAnalysisCompleted' | 'autoAnalysisError' | 'projectAnalysisCompleted' | 'projectAnalysisError';

export interface TraeAIEventData {
  [key: string]: any;
}

// Helper functions for common operations
export const TraeAIHelpers = {
  formatCodeReview: (review: TraeAICodeReview): string => {
    return `${review.severity.toUpperCase()}: ${review.message} (${review.fileName}:${review.lineNumber})`;
  },
  
  calculateProjectHealth: (project: TraeAIProject): number => {
    const reviews = project.aiContext.codeReviews;
    const criticalIssues = reviews.filter(r => r.severity === 'critical').length;
    const errorIssues = reviews.filter(r => r.severity === 'error').length;
    const warningIssues = reviews.filter(r => r.severity === 'warning').length;
    
    const totalFiles = Object.keys(project.files).length;
    
    if (totalFiles === 0) return 100;
    
    const healthScore = Math.max(0, 100 - (criticalIssues * 20 + errorIssues * 10 + warningIssues * 5));
    return Math.round(healthScore);
  },
  
  prioritizeOptimizations: (optimizations: TraeAIOptimization[]): TraeAIOptimization[] => {
    return optimizations.sort((a, b) => {
      const impactWeight = { critical: 4, high: 3, medium: 2, low: 1 };
      const effortWeight = { low: 3, medium: 2, high: 1 };
      
      const scoreA = impactWeight[a.impact] * effortWeight[a.effort];
      const scoreB = impactWeight[b.impact] * effortWeight[b.effort];
      
      return scoreB - scoreA;
    });
  },

  // Additional method needed by UnifiedWorkflowService
  getProjectFiles: async (projectId: string): Promise<{ [key: string]: string }> => {
    const project = await traeAIService.getProject(projectId);
    return project?.files || {};
  }
};