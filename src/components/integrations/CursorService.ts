export interface CursorConfig {
  apiKey: string
  projectPath?: string
  workspaceId?: string
  userId?: string
  serverUrl?: string
  enableRealTimeSync?: boolean
  syncInterval?: number
}

export interface CursorProject {
  id: string
  name: string
  path: string
  files: CursorFile[]
  collaborators: CursorUser[]
  settings: CursorProjectSettings
  metadata: {
    createdAt: string
    updatedAt: string
    version: string
    framework?: string
    language?: string
  }
}

export interface CursorFile {
  path: string
  content: string
  language: string
  lastModified: string
  author: string
  size: number
  checksum?: string
}

export interface CursorUser {
  id: string
  name: string
  email: string
  avatar?: string
  status: 'online' | 'offline' | 'away'
  permissions: string[]
}

export interface CursorProjectSettings {
  aiCompletionEnabled: boolean
  collaborationEnabled: boolean
  autoSave: boolean
  linting: boolean
  formatting: boolean
  extensions: string[]
  theme: string
  fontSize: number
}

export interface CursorCompletion {
  id: string
  text: string
  confidence: number
  context: string
  language: string
  suggestions: string[]
  metadata: {
    model: string
    tokens: number
    latency: number
  }
}

export interface CursorSyncResult {
  success: boolean
  filesUpdated: number
  conflicts: string[]
  timestamp: string
  changes?: string[]
  errors?: string[]
  syncId: string
}

export interface CursorIntegrationStatus {
  connected: boolean
  authenticated: boolean
  lastSync?: string
  projectsCount: number
  activeCollaborators: number
  apiVersion: string
  health: 'healthy' | 'warning' | 'error'
}

// Browser-compatible EventEmitter replacement
class BrowserEventEmitter {
  private listeners: Map<string, Function[]> = new Map()

  on(event: string, listener: Function): this {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event)!.push(listener)
    return this
  }

  emit(event: string, ...args: any[]): boolean {
    const eventListeners = this.listeners.get(event)
    if (eventListeners) {
      eventListeners.forEach(listener => listener(...args))
      return true
    }
    return false
  }

  off(event: string, listener: Function): this {
    const eventListeners = this.listeners.get(event)
    if (eventListeners) {
      const index = eventListeners.indexOf(listener)
      if (index > -1) {
        eventListeners.splice(index, 1)
      }
    }
    return this
  }

  removeAllListeners(event?: string): this {
    if (event) {
      this.listeners.delete(event)
    } else {
      this.listeners.clear()
    }
    return this
  }
}

export class CursorService extends BrowserEventEmitter {
  private config: CursorConfig | null = null
  private authenticated: boolean = false
  private websocket: WebSocket | null = null
  private currentProject: CursorProject | null = null
  private syncInterval: NodeJS.Timeout | null = null
  private reconnectAttempts: number = 0
  private maxReconnectAttempts: number = 5
  private baseUrl: string = 'https://api.cursor.sh/v1'
  private wsUrl: string = 'wss://ws.cursor.sh/v1'

  constructor() {
    super()
    this.setupErrorHandling()
  }

  private setupErrorHandling(): void {
    window.addEventListener('beforeunload', () => {
      this.disconnect()
    })
  }

  async connect(config: CursorConfig): Promise<{ success: boolean; error?: string }> {
    try {
      this.config = {
        ...config,
        serverUrl: config.serverUrl || this.baseUrl,
        enableRealTimeSync: config.enableRealTimeSync ?? true,
        syncInterval: config.syncInterval || 30000
      }

      // Authenticate with Cursor API
      const authResult = await this.authenticateWithCursor(config.apiKey)
      if (!authResult.success) {
        return { success: false, error: authResult.error }
      }

      this.authenticated = true

      // Initialize WebSocket for real-time updates
      if (this.config.enableRealTimeSync) {
        await this.initializeWebSocket()
      }

      // Start periodic sync
      this.startPeriodicSync()

      this.emit('connected', { config: this.config })
      return { success: true }
    } catch (error: any) {
      this.emit('connectionError', { error: error.message })
      return { success: false, error: error.message }
    }
  }

  async disconnect(): Promise<void> {
    this.authenticated = false
    
    if (this.websocket) {
      this.websocket.close()
      this.websocket = null
    }

    if (this.syncInterval) {
      clearInterval(this.syncInterval)
      this.syncInterval = null
    }

    this.emit('disconnected')
  }

  isAuthenticated(): boolean {
    return this.authenticated
  }

  async getIntegrationStatus(): Promise<CursorIntegrationStatus> {
    if (!this.authenticated) {
      return {
        connected: false,
        authenticated: false,
        projectsCount: 0,
        activeCollaborators: 0,
        apiVersion: 'unknown',
        health: 'error'
      }
    }

    try {
      const response = await this.makeRequest('/status', 'GET')
      return {
        connected: true,
        authenticated: true,
        lastSync: response.lastSync,
        projectsCount: response.projectsCount || 0,
        activeCollaborators: response.activeCollaborators || 0,
        apiVersion: response.apiVersion || '1.0',
        health: response.health || 'healthy'
      }
    } catch (error) {
      return {
        connected: true,
        authenticated: true,
        projectsCount: 0,
        activeCollaborators: 0,
        apiVersion: '1.0',
        health: 'error'
      }
    }
  }

  async getCodeCompletion(
    code: string, 
    cursorPosition: number, 
    language: string,
    context?: string
  ): Promise<CursorCompletion[]> {
    if (!this.authenticated) {
      throw new Error('Not authenticated with Cursor')
    }

    try {
      const response = await this.makeRequest('/completions', 'POST', {
        code,
        position: cursorPosition,
        language,
        context: context || this.getFileContext(),
        maxSuggestions: 5,
        temperature: 0.7
      })

      return response.completions.map((comp: any) => ({
        id: comp.id,
        text: comp.text,
        confidence: comp.confidence,
        context: comp.context,
        language,
        suggestions: comp.alternatives || [],
        metadata: {
          model: comp.model || 'cursor-default',
          tokens: comp.tokens || 0,
          latency: comp.latency || 0
        }
      }))
    } catch (error: any) {
      this.emit('completionError', { error: error.message })
      return []
    }
  }

  async acceptCompletion(completionId: string): Promise<boolean> {
    try {
      await this.makeRequest(`/completions/${completionId}/accept`, 'POST')
      await this.trackCompletionUsage(completionId, 'accepted')
      return true
    } catch (error) {
      return false
    }
  }

  async createProject(name: string, path: string, template?: string): Promise<CursorProject> {
    if (!this.authenticated) {
      throw new Error('Not authenticated with Cursor')
    }

    try {
      const response = await this.makeRequest('/projects', 'POST', {
        name,
        path,
        template,
        settings: {
          aiCompletionEnabled: true,
          collaborationEnabled: true,
          autoSave: true,
          linting: true,
          formatting: true,
          extensions: ['typescript', 'react', 'tailwindcss'],
          theme: 'dark',
          fontSize: 14
        }
      })

      const project: CursorProject = {
        id: response.id,
        name: response.name,
        path: response.path,
        files: response.files || [],
        collaborators: response.collaborators || [],
        settings: response.settings,
        metadata: {
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          version: '1.0.0',
          framework: template,
          language: 'typescript'
        }
      }

      this.currentProject = project
      this.emit('projectCreated', { project })
      return project
    } catch (error: any) {
      throw new Error(`Failed to create project: ${error.message}`)
    }
  }

  async loadProject(path: string): Promise<CursorProject> {
    if (!this.authenticated) {
      throw new Error('Not authenticated with Cursor')
    }

    try {
      const project = await this.fetchProjectData(path)
      this.currentProject = project
      this.emit('projectLoaded', { project })
      return project
    } catch (error: any) {
      throw new Error(`Failed to load project: ${error.message}`)
    }
  }

  async syncProject(): Promise<CursorSyncResult> {
    if (!this.currentProject) {
      throw new Error('No active project to sync')
    }

    try {
      const result = await this.performProjectSync(this.currentProject)
      this.emit('projectSynced', { result })
      return result
    } catch (error: any) {
      const errorResult: CursorSyncResult = {
        success: false,
        filesUpdated: 0,
        conflicts: [],
        timestamp: new Date().toISOString(),
        errors: [error.message],
        syncId: this.generateSyncId()
      }
      this.emit('syncError', { error: errorResult })
      return errorResult
    }
  }

  async inviteCollaborator(email: string, role: 'viewer' | 'editor' | 'admin' = 'editor'): Promise<boolean> {
    if (!this.authenticated || !this.currentProject) {
      throw new Error('No active project for collaboration')
    }

    try {
      const invitation = await this.sendCollaborationInvite(email, role, this.currentProject.id)
      this.emit('collaboratorInvited', { email, role, projectId: this.currentProject.id })
      return invitation.success
    } catch (error: any) {
      throw new Error(`Failed to invite collaborator: ${error.message}`)
    }
  }

  async getActiveCollaborators(): Promise<CursorUser[]> {
    if (!this.currentProject) return []
    
    return this.currentProject.collaborators.filter(user => user.status === 'online')
  }

  async saveFile(filePath: string, content: string): Promise<boolean> {
    if (!this.authenticated || !this.currentProject) {
      throw new Error('No active project')
    }

    try {
      // Update local file
      const fileIndex = this.currentProject.files.findIndex(f => f.path === filePath)
      const fileData: CursorFile = {
        path: filePath,
        content,
        language: this.detectLanguage(filePath),
        lastModified: new Date().toISOString(),
        author: this.config?.userId || 'current_user'
      }

      if (fileIndex >= 0) {
        this.currentProject.files[fileIndex] = fileData
      } else {
        this.currentProject.files.push(fileData)
      }

      // Sync with Cursor servers
      await this.syncFileToServer(fileData)
      
      // Notify collaborators via WebSocket
      this.broadcastFileChange(fileData)
      
      this.emit('fileSaved', fileData)
      return true
    } catch (error: any) {
      throw new Error(`Failed to save file: ${error.message}`)
    }
  }

  async getFile(filePath: string): Promise<CursorFile | null> {
    if (!this.currentProject) return null
    
    return this.currentProject.files.find(f => f.path === filePath) || null
  }

  async exportToFirebase(firebaseProjectId: string): Promise<boolean> {
    if (!this.currentProject) {
      throw new Error('No active project to export')
    }

    try {
      // Export project structure and files to Firebase
      const exportData = {
        projectId: this.currentProject.id,
        name: this.currentProject.name,
        files: this.currentProject.files,
        settings: this.currentProject.settings,
        exportedAt: new Date().toISOString()
      }

      // This would integrate with FirebaseService
      this.emit('exportedToFirebase', { firebaseProjectId, data: exportData })
      return true
    } catch (error: any) {
      throw new Error(`Firebase export failed: ${error.message}`)
    }
  }

  async syncWithTraeAI(traeProjectId: string): Promise<boolean> {
    if (!this.currentProject) {
      throw new Error('No active project to sync')
    }

    try {
      // Sync code analysis and suggestions with Trae.AI
      const analysisData = {
        projectId: this.currentProject.id,
        files: this.currentProject.files.map(f => ({
          path: f.path,
          content: f.content,
          language: f.language
        })),
        syncedAt: new Date().toISOString()
      }

      this.emit('syncedWithTraeAI', { traeProjectId, data: analysisData })
      return true
    } catch (error: any) {
      throw new Error(`Trae.AI sync failed: ${error.message}`)
    }
  }

  async getRecentChanges(since?: string): Promise<CursorFile[]> {
    if (!this.currentProject) {
      throw new Error('No active project')
    }

    const sinceDate = since ? new Date(since) : new Date(Date.now() - 24 * 60 * 60 * 1000) // Default to last 24 hours
    
    return this.currentProject.files.filter(file => 
      new Date(file.lastModified) > sinceDate
    )
  }

  async updateFiles(files: { path: string; content: string }[]): Promise<boolean> {
    if (!this.currentProject) {
      throw new Error('No active project')
    }

    try {
      for (const file of files) {
        await this.saveFile(file.path, file.content)
      }
      return true
    } catch (error) {
      return false
    }
  }

  async deleteProject(projectId: string): Promise<boolean> {
    try {
      // Simulate project deletion
      if (this.currentProject?.id === projectId) {
        this.currentProject = null
      }
      this.emit('projectDeleted', { projectId })
      return true
    } catch (error) {
      return false
    }
  }

  private async makeRequest(endpoint: string, method: string, data?: any): Promise<any> {
    if (!this.config) {
      throw new Error('Service not configured')
    }

    const url = `${this.config.serverUrl}${endpoint}`
    const options: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
        'X-Cursor-Version': '1.0'
      }
    }

    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
      options.body = JSON.stringify(data)
    }

    const response = await fetch(url, options)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`)
    }

    return response.json()
  }

  private generateSyncId(): string {
    return `sync_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  private async authenticateWithCursor(apiKey: string): Promise<{ success: boolean; error?: string }> {
    try {
      const response = await this.makeRequest('/auth', 'POST', { apiKey })
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  }

  private async initializeWebSocket(): Promise<void> {
    if (!this.config) return

    try {
      this.websocket = new WebSocket(`${this.wsUrl}?token=${this.config.apiKey}`)
      
      this.websocket.onopen = () => {
        this.reconnectAttempts = 0
        this.emit('websocketConnected')
      }

      this.websocket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        this.handleWebSocketMessage(data)
      }

      this.websocket.onclose = () => {
        this.emit('websocketDisconnected')
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++
          setTimeout(() => this.initializeWebSocket(), 5000 * this.reconnectAttempts)
        }
      }
    } catch (error) {
      console.error('WebSocket initialization failed:', error)
    }
  }

  private handleWebSocketMessage(data: any): void {
    switch (data.type) {
      case 'file_changed':
        this.emit('fileChanged', data.file)
        break
      case 'collaborator_joined':
        this.emit('collaboratorJoined', data.user)
        break
      case 'collaborator_left':
        this.emit('collaboratorLeft', data.user)
        break
      case 'cursor_moved':
        this.emit('cursorMoved', data.cursor)
        break
    }
  }

  private startPeriodicSync(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval)
    }

    if (this.config?.syncInterval) {
      this.syncInterval = setInterval(async () => {
        if (this.currentProject) {
          try {
            await this.syncProject()
          } catch (error) {
            console.error('Periodic sync failed:', error)
          }
        }
      }, this.config.syncInterval)
    }
  }

  private async trackCompletionUsage(completionId: string, action: string): Promise<void> {
    try {
      await this.makeRequest('/completions/usage', 'POST', {
        completionId,
        action,
        timestamp: new Date().toISOString()
      })
    } catch (error) {
      console.error('Failed to track completion usage:', error)
    }
  }

  private getFileContext(): string {
    if (!this.currentProject) return ''
    
    return this.currentProject.files
      .map(f => `${f.path}: ${f.language}`)
      .join(', ')
  }

  private async fetchProjectData(path: string): Promise<CursorProject> {
    const response = await this.makeRequest(`/projects?path=${encodeURIComponent(path)}`, 'GET')
    return response.project
  }

  private async performProjectSync(project: CursorProject): Promise<CursorSyncResult> {
    const syncId = this.generateSyncId()
    
    try {
      const response = await this.makeRequest('/projects/sync', 'POST', {
        projectId: project.id,
        syncId,
        files: project.files.map(f => ({
          path: f.path,
          checksum: f.checksum,
          lastModified: f.lastModified
        }))
      })

      return {
        success: true,
        filesUpdated: response.filesUpdated || 0,
        conflicts: response.conflicts || [],
        timestamp: new Date().toISOString(),
        changes: response.changes || [],
        syncId
      }
    } catch (error: any) {
      return {
        success: false,
        filesUpdated: 0,
        conflicts: [],
        timestamp: new Date().toISOString(),
        errors: [error.message],
        syncId
      }
    }
  }
}

// Export singleton instance
export const cursorService = new CursorService()