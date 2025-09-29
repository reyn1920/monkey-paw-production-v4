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

export interface BoltDiyConfig {
  apiKey: string
  projectId?: string
  organizationId?: string
  deploymentRegion?: string
}

export interface BoltDiyProject {
  id: string
  name: string
  description: string
  framework: string
  status: 'active' | 'building' | 'deployed' | 'error'
  url?: string
  previewUrl?: string
  files: BoltDiyFile[]
  components: BoltDiyComponent[]
  deployments: BoltDiyDeployment[]
  settings: BoltDiyProjectSettings
}

export interface BoltDiyFile {
  path: string
  content: string
  type: 'component' | 'page' | 'asset' | 'config'
  lastModified: string
  size: number
}

export interface BoltDiyComponent {
  id: string
  name: string
  category: string
  description: string
  props: BoltDiyComponentProp[]
  code: string
  preview: string
  tags: string[]
  version: string
}

export interface BoltDiyComponentProp {
  name: string
  type: string
  required: boolean
  default?: any
  description: string
}

export interface BoltDiyDeployment {
  id: string
  version: string
  status: 'pending' | 'building' | 'success' | 'failed'
  url?: string
  createdAt: string
  buildTime?: number
  logs: string[]
}

export interface BoltDiyProjectSettings {
  autoDeployment: boolean
  previewMode: boolean
  componentLibraryEnabled: boolean
  hotReload: boolean
  buildOptimization: boolean
  environmentVariables: { [key: string]: string }
}

export interface BoltDiyBuildResult {
  success: boolean
  deploymentId: string
  url?: string
  buildTime: number
  errors: string[]
  warnings: string[]
  files?: string[]
}

export interface BoltDiyIntegrationStatus {
  connected: boolean
  authenticated: boolean
  lastDeployment?: string
  projectsCount: number
  activeBuilds: number
  apiVersion: string
  health: 'healthy' | 'warning' | 'error'
  deploymentRegion: string
}

export interface BoltDiyApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
  timestamp: string
}

export class BoltDiyService extends BrowserEventEmitter {
  private config: BoltDiyConfig | null = null
  private authenticated: boolean = false
  private currentProject: BoltDiyProject | null = null
  private websocket: WebSocket | null = null
  private buildQueue: string[] = []
  private isBuilding: boolean = false
  private baseUrl: string = 'https://api.bolt.diy/v1'
  private wsUrl: string = 'wss://ws.bolt.diy/v1'
  private reconnectAttempts: number = 0
  private maxReconnectAttempts: number = 5

  constructor() {
    super()
    this.setupErrorHandling()
  }

  private setupErrorHandling(): void {
    this.on('error', (error: any) => {
      console.error('BoltDiyService error:', error)
    })
  }

  async connect(config: BoltDiyConfig): Promise<{ success: boolean; error?: string }> {
    try {
      this.config = config
      
      const authResult = await this.authenticateWithBoltDiy(config.apiKey)
      if (!authResult.success) {
        return authResult
      }

      this.authenticated = true
      await this.initializeWebSocket()
      
      this.emit('connected')
      return { success: true }
    } catch (error: any) {
      this.emit('error', error)
      return { success: false, error: error.message }
    }
  }

  async getIntegrationStatus(): Promise<BoltDiyIntegrationStatus> {
    try {
      if (!this.authenticated) {
        return {
          connected: false,
          authenticated: false,
          projectsCount: 0,
          activeBuilds: 0,
          apiVersion: '1.0',
          health: 'error',
          deploymentRegion: 'unknown'
        }
      }

      const response = await this.makeRequest('/status', 'GET')
      return {
        connected: true,
        authenticated: true,
        lastDeployment: response.lastDeployment,
        projectsCount: response.projectsCount || 0,
        activeBuilds: response.activeBuilds || 0,
        apiVersion: response.apiVersion || '1.0',
        health: response.health || 'healthy',
        deploymentRegion: this.config?.deploymentRegion || 'us-east-1'
      }
    } catch (error) {
      return {
        connected: false,
        authenticated: false,
        projectsCount: 0,
        activeBuilds: 0,
        apiVersion: '1.0',
        health: 'error',
        deploymentRegion: 'unknown'
      }
    }
  }

  private async makeRequest(endpoint: string, method: string, data?: any): Promise<any> {
    if (!this.config) {
      throw new Error('Service not configured')
    }

    const url = `${this.baseUrl}${endpoint}`
    const options: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
        'X-Bolt-Version': '1.0'
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

  async syncWithAllPlatforms(): Promise<{ success: boolean; results: any[] }> {
    const results = []
    
    try {
      // Sync with Firebase
      if (this.currentProject) {
        const firebaseResult = await this.deployToFirebase({
          projectId: 'default',
          hosting: true,
          functions: false
        })
        results.push({ platform: 'firebase', success: firebaseResult })
      }

      // Sync with Cursor
      if (this.currentProject) {
        const cursorResult = await this.syncWithCursor(this.currentProject.id, {})
        results.push({ platform: 'cursor', success: cursorResult })
      }

      // Sync with Trae.ai
      if (this.currentProject) {
        const traeResult = await this.syncWithTraeAI(this.currentProject.id, {})
        results.push({ platform: 'traeai', success: traeResult })
      }

      return { success: true, results }
    } catch (error: any) {
      return { success: false, results: [...results, { error: error.message }] }
    }
  }



  async disconnect(): Promise<void> {
    this.authenticated = false
    
    if (this.websocket) {
      this.websocket.close()
      this.websocket = null
    }

    this.currentProject = null
    this.config = null
    this.buildQueue = []
    this.isBuilding = false
    this.emit('disconnected')
  }

  isAuthenticated(): boolean {
    return this.authenticated
  }

  // Project Management
  async createProject(
    name: string, 
    framework: string, 
    template?: string
  ): Promise<BoltDiyProject> {
    if (!this.authenticated) {
      throw new Error('Not authenticated with Bolt.diy')
    }

    try {
      const projectData = await this.createProjectOnServer({
        name,
        framework,
        template,
        organizationId: this.config?.organizationId
      })

      this.currentProject = projectData
      this.emit('projectCreated', projectData)
      return projectData
    } catch (error: any) {
      throw new Error(`Failed to create project: ${error.message}`)
    }
  }

  async loadProject(projectId: string): Promise<BoltDiyProject> {
    if (!this.authenticated) {
      throw new Error('Not authenticated with Bolt.diy')
    }

    try {
      const projectData = await this.fetchProjectData(projectId)
      this.currentProject = projectData
      this.emit('projectLoaded', projectData)
      return projectData
    } catch (error: any) {
      throw new Error(`Failed to load project: ${error.message}`)
    }
  }

  async updateProject(updates: Partial<BoltDiyProject>): Promise<BoltDiyProject> {
    if (!this.authenticated || !this.currentProject) {
      throw new Error('No active project')
    }

    try {
      const updatedProject = { ...this.currentProject, ...updates }
      await this.updateProjectOnServer(updatedProject)
      this.currentProject = updatedProject
      this.emit('projectUpdated', updatedProject)
      return updatedProject
    } catch (error: any) {
      throw new Error(`Failed to update project: ${error.message}`)
    }
  }

  // Instant Deployment
  async deployProject(options?: { 
    environment?: 'preview' | 'production'
    buildCommand?: string
    outputDirectory?: string
  }): Promise<BoltDiyBuildResult> {
    if (!this.authenticated || !this.currentProject) {
      throw new Error('No active project to deploy')
    }

    try {
      this.isBuilding = true
      this.emit('deploymentStarted', { projectId: this.currentProject.id })

      const buildResult = await this.performDeployment({
        projectId: this.currentProject.id,
        environment: options?.environment || 'preview',
        buildCommand: options?.buildCommand,
        outputDirectory: options?.outputDirectory
      })

      // Update project status
      if (this.currentProject) {
        this.currentProject.status = buildResult.success ? 'deployed' : 'error'
        if (buildResult.url) {
          if (options?.environment === 'production') {
            this.currentProject.url = buildResult.url
          } else {
            this.currentProject.previewUrl = buildResult.url
          }
        }
      }

      this.isBuilding = false
      this.emit('deploymentCompleted', buildResult)
      return buildResult
    } catch (error: any) {
      this.isBuilding = false
      throw new Error(`Deployment failed: ${error.message}`)
    }
  }

  async getDeploymentStatus(deploymentId: string): Promise<BoltDiyDeployment> {
    if (!this.authenticated) {
      throw new Error('Not authenticated with Bolt.diy')
    }

    try {
      return await this.fetchDeploymentStatus(deploymentId)
    } catch (error: any) {
      throw new Error(`Failed to get deployment status: ${error.message}`)
    }
  }

  async rollbackDeployment(deploymentId: string): Promise<boolean> {
    if (!this.authenticated || !this.currentProject) {
      throw new Error('No active project')
    }

    try {
      await this.performRollback(this.currentProject.id, deploymentId)
      this.emit('deploymentRolledBack', { projectId: this.currentProject.id, deploymentId })
      return true
    } catch (error: any) {
      throw new Error(`Rollback failed: ${error.message}`)
    }
  }

  // Component Library
  async getComponentLibrary(): Promise<BoltDiyComponent[]> {
    if (!this.authenticated) {
      throw new Error('Not authenticated with Bolt.diy')
    }

    try {
      return await this.fetchComponentLibrary()
    } catch (error: any) {
      throw new Error(`Failed to fetch component library: ${error.message}`)
    }
  }

  async searchComponents(query: string, category?: string): Promise<BoltDiyComponent[]> {
    if (!this.authenticated) {
      throw new Error('Not authenticated with Bolt.diy')
    }

    try {
      return await this.searchComponentLibrary(query, category)
    } catch (error: any) {
      throw new Error(`Component search failed: ${error.message}`)
    }
  }

  async addComponentToProject(componentId: string, customization?: any): Promise<boolean> {
    if (!this.authenticated || !this.currentProject) {
      throw new Error('No active project')
    }

    try {
      const component = await this.fetchComponent(componentId)
      
      // Apply customizations if provided
      if (customization) {
        component.code = this.applyComponentCustomization(component.code, customization)
      }

      // Add component to project
      this.currentProject.components.push(component)
      
      // Create component file
      const componentFile: BoltDiyFile = {
        path: `src/components/${component.name}.tsx`,
        content: component.code,
        type: 'component',
        lastModified: new Date().toISOString(),
        size: component.code.length
      }

      this.currentProject.files.push(componentFile)
      
      await this.updateProjectOnServer(this.currentProject)
      this.emit('componentAdded', { component, file: componentFile })
      return true
    } catch (error: any) {
      throw new Error(`Failed to add component: ${error.message}`)
    }
  }

  async createCustomComponent(
    name: string, 
    code: string, 
    props: BoltDiyComponentProp[]
  ): Promise<BoltDiyComponent> {
    if (!this.authenticated || !this.currentProject) {
      throw new Error('No active project')
    }

    try {
      const component: BoltDiyComponent = {
        id: `custom_${Date.now()}`,
        name,
        category: 'custom',
        description: `Custom component: ${name}`,
        props,
        code,
        preview: await this.generateComponentPreview(code),
        tags: ['custom'],
        version: '1.0.0'
      }

      this.currentProject.components.push(component)
      await this.updateProjectOnServer(this.currentProject)
      this.emit('customComponentCreated', component)
      return component
    } catch (error: any) {
      throw new Error(`Failed to create custom component: ${error.message}`)
    }
  }

  // Real-time Preview
  async enablePreviewMode(): Promise<string> {
    if (!this.authenticated || !this.currentProject) {
      throw new Error('No active project')
    }

    try {
      const previewUrl = await this.createPreviewEnvironment(this.currentProject.id)
      
      if (this.currentProject) {
        this.currentProject.previewUrl = previewUrl
        this.currentProject.settings.previewMode = true
      }

      this.emit('previewModeEnabled', { url: previewUrl })
      return previewUrl
    } catch (error: any) {
      throw new Error(`Failed to enable preview mode: ${error.message}`)
    }
  }

  async updatePreview(files: BoltDiyFile[]): Promise<boolean> {
    if (!this.authenticated || !this.currentProject?.settings.previewMode) {
      throw new Error('Preview mode not enabled')
    }

    try {
      await this.updatePreviewEnvironment(this.currentProject.id, files)
      this.emit('previewUpdated', { files })
      return true
    } catch (error: any) {
      throw new Error(`Failed to update preview: ${error.message}`)
    }
  }

  async disablePreviewMode(): Promise<boolean> {
    if (!this.authenticated || !this.currentProject) {
      throw new Error('No active project')
    }

    try {
      await this.destroyPreviewEnvironment(this.currentProject.id)
      
      if (this.currentProject) {
        this.currentProject.settings.previewMode = false
        this.currentProject.previewUrl = undefined
      }

      this.emit('previewModeDisabled')
      return true
    } catch (error: any) {
      throw new Error(`Failed to disable preview mode: ${error.message}`)
    }
  }

  // File Management
  async uploadFile(file: File, path: string): Promise<BoltDiyFile> {
    if (!this.authenticated || !this.currentProject) {
      throw new Error('No active project')
    }

    try {
      const content = await this.readFileContent(file)
      const boltFile: BoltDiyFile = {
        path,
        content,
        type: this.determineFileType(path),
        lastModified: new Date().toISOString(),
        size: file.size
      }

      // Add to project files
      const existingIndex = this.currentProject.files.findIndex(f => f.path === path)
      if (existingIndex >= 0) {
        this.currentProject.files[existingIndex] = boltFile
      } else {
        this.currentProject.files.push(boltFile)
      }

      await this.updateProjectOnServer(this.currentProject)
      
      // Update preview if enabled
      if (this.currentProject.settings.previewMode) {
        await this.updatePreview([boltFile])
      }

      this.emit('fileUploaded', boltFile)
      return boltFile
    } catch (error: any) {
      throw new Error(`File upload failed: ${error.message}`)
    }
  }

  async deleteFile(path: string): Promise<boolean> {
    if (!this.authenticated || !this.currentProject) {
      throw new Error('No active project')
    }

    try {
      this.currentProject.files = this.currentProject.files.filter(f => f.path !== path)
      await this.updateProjectOnServer(this.currentProject)
      this.emit('fileDeleted', { path })
      return true
    } catch (error: any) {
      throw new Error(`File deletion failed: ${error.message}`)
    }
  }

  // Integration with other platforms
  async syncWithCursorUnified(projectId: string, cursorData: any): Promise<boolean> {
    if (!this.currentProject) {
      throw new Error('No active project to sync')
    }

    try {
      const syncData = {
        projectId: this.currentProject.id,
        files: this.currentProject.files,
        components: this.currentProject.components,
        syncedAt: new Date().toISOString(),
        cursorData
      }

      this.emit('syncedWithCursor', { cursorProjectId: projectId, data: syncData })
      return true
    } catch (error: any) {
      throw new Error(`Cursor sync failed: ${error.message}`)
    }
  }

  async deployToFirebase(firebaseConfig: any): Promise<boolean> {
    if (!this.currentProject) {
      throw new Error('No active project to deploy')
    }

    try {
      // Build project for Firebase deployment
      const buildResult = await this.buildForFirebase(this.currentProject)
      
      if (buildResult.success) {
        this.emit('deployedToFirebase', { 
          projectId: this.currentProject.id, 
          firebaseConfig,
          buildResult 
        })
        return true
      }
      
      return false
    } catch (error: any) {
      throw new Error(`Firebase deployment failed: ${error.message}`)
    }
  }

  // Private helper methods
  private async authenticateWithBoltDiy(apiKey: string): Promise<{ success: boolean; error?: string }> {
    // Simulate API authentication
    await new Promise(resolve => setTimeout(resolve, 800))
    
    if (apiKey.startsWith('bolt_') && apiKey.length >= 32) {
      return { success: true }
    } else {
      return { success: false, error: 'Invalid API key format. Must start with "bolt_" and be at least 32 characters.' }
    }
  }

  private async initializeWebSocket(): Promise<void> {
    if (!this.config) return

    try {
      this.websocket = new WebSocket(`wss://api.bolt.diy/ws?token=${this.config.apiKey}`)
      
      this.websocket.onopen = () => {
        this.emit('websocketConnected')
      }

      this.websocket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        this.handleWebSocketMessage(data)
      }

      this.websocket.onclose = () => {
        this.emit('websocketDisconnected')
        setTimeout(() => this.initializeWebSocket(), 5000)
      }
    } catch (error) {
      console.error('WebSocket initialization failed:', error)
    }
  }

  private handleWebSocketMessage(data: any): void {
    switch (data.type) {
      case 'build_started':
        this.emit('buildStarted', data)
        break
      case 'build_progress':
        this.emit('buildProgress', data)
        break
      case 'build_completed':
        this.emit('buildCompleted', data)
        break
      case 'deployment_ready':
        this.emit('deploymentReady', data)
        break
    }
  }

  private async createProjectOnServer(projectData: any): Promise<BoltDiyProject> {
    // Simulate project creation
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    return {
      id: `bolt_${Date.now()}`,
      name: projectData.name,
      description: `${projectData.framework} project created with Bolt.diy`,
      framework: projectData.framework,
      status: 'active',
      files: [],
      components: [],
      deployments: [],
      settings: {
        autoDeployment: true,
        previewMode: false,
        componentLibraryEnabled: true,
        hotReload: true,
        buildOptimization: true,
        environmentVariables: {}
      }
    }
  }

  private async fetchProjectData(projectId: string): Promise<BoltDiyProject> {
    // Simulate fetching project data
    await new Promise(resolve => setTimeout(resolve, 600))
    
    return {
      id: projectId,
      name: 'Loaded Project',
      description: 'Project loaded from Bolt.diy',
      framework: 'react',
      status: 'active',
      files: [],
      components: [],
      deployments: [],
      settings: {
        autoDeployment: true,
        previewMode: false,
        componentLibraryEnabled: true,
        hotReload: true,
        buildOptimization: true,
        environmentVariables: {}
      }
    }
  }

  private async updateProjectOnServer(_project: BoltDiyProject): Promise<void> {
    // Implementation would update project on server
    // For now, just simulate the operation
    // Implementation would update project on server
    // For now, just simulate the operation
  }

  private async performDeployment(options: any): Promise<BoltDiyBuildResult> {
    // Simulate deployment process
    const startTime = Date.now()
    await new Promise(resolve => setTimeout(resolve, 3000))
    const buildTime = Date.now() - startTime

    return {
      success: true,
      deploymentId: `deploy_${Date.now()}`,
      url: `https://${options.projectId}.bolt.diy`,
      buildTime,
      errors: [],
      warnings: []
    }
  }

  private async fetchDeploymentStatus(deploymentId: string): Promise<BoltDiyDeployment> {
    // Simulate fetching deployment status
    await new Promise(resolve => setTimeout(resolve, 200))
    
    return {
      id: deploymentId,
      version: '1.0.0',
      status: 'success',
      url: `https://deploy-${deploymentId}.bolt.diy`,
      createdAt: new Date().toISOString(),
      buildTime: 2500,
      logs: ['Build started', 'Dependencies installed', 'Build completed', 'Deployment successful']
    }
  }

  private async performRollback(_projectId: string, _deploymentId: string): Promise<void> {
    // Implementation would perform rollback
    // For now, just simulate the operation
  }

  private async fetchComponentLibrary(): Promise<BoltDiyComponent[]> {
    // Simulate fetching component library
    await new Promise(resolve => setTimeout(resolve, 400))
    
    return [
      {
        id: 'button-primary',
        name: 'PrimaryButton',
        category: 'buttons',
        description: 'Primary action button with hover effects',
        props: [
          { name: 'children', type: 'ReactNode', required: true, description: 'Button content' },
          { name: 'onClick', type: 'function', required: false, description: 'Click handler' },
          { name: 'disabled', type: 'boolean', required: false, default: false, description: 'Disabled state' }
        ],
        code: 'export const PrimaryButton = ({ children, onClick, disabled }) => {\n  return (\n    <button \n      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"\n      onClick={onClick}\n      disabled={disabled}\n    >\n      {children}\n    </button>\n  );\n};',
        preview: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIiBmaWxsPSIjMzB4NkY5IiByeD0iNCIvPjx0ZXh0IHg9IjUwIiB5PSIyNSIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPkJ1dHRvbjwvdGV4dD48L3N2Zz4=',
        tags: ['button', 'primary', 'action'],
        version: '1.0.0'
      }
    ]
  }

  private async searchComponentLibrary(query: string, category?: string): Promise<BoltDiyComponent[]> {
    const allComponents = await this.fetchComponentLibrary()
    return allComponents.filter(component => 
      component.name.toLowerCase().includes(query.toLowerCase()) ||
      component.description.toLowerCase().includes(query.toLowerCase()) ||
      (category && component.category === category)
    )
  }

  private async fetchComponent(componentId: string): Promise<BoltDiyComponent> {
    const components = await this.fetchComponentLibrary()
    const component = components.find(c => c.id === componentId)
    if (!component) {
      throw new Error(`Component ${componentId} not found`)
    }
    return component
  }

  private applyComponentCustomization(code: string, customization: any): string {
    // Apply customizations to component code
    let customizedCode = code
    
    if (customization.className) {
      customizedCode = customizedCode.replace(/className="[^"]*"/, `className="${customization.className}"`)
    }
    
    if (customization.styles) {
      // Apply inline styles or CSS modifications
      Object.entries(customization.styles).forEach(([property, value]) => {
        // Simple style replacement logic
        customizedCode = customizedCode.replace(
          new RegExp(`${property}:\\s*[^;]+`, 'g'),
          `${property}: ${value}`
        )
      })
    }
    
    return customizedCode
  }

  private async generateComponentPreview(code: string): Promise<string> {
    // Generate a base64 SVG preview of the component
    return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIiBmaWxsPSIjZjNmNGY2IiByeD0iNCIvPjx0ZXh0IHg9IjUwIiB5PSIyNSIgZmlsbD0iIzM3NDE1MSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+Q29tcG9uZW50PC90ZXh0Pjwvc3ZnPg=='
  }

  private async createPreviewEnvironment(projectId: string): Promise<string> {
    // Simulate creating preview environment
    await new Promise(resolve => setTimeout(resolve, 1000))
    return `https://preview-${projectId}.bolt.diy`
  }

  private async updatePreviewEnvironment(projectId: string, files: BoltDiyFile[]): Promise<void> {
    // Implementation would update preview environment
    // For now, just simulate the operation
  }

  private async destroyPreviewEnvironment(projectId: string): Promise<void> {
    // Implementation would destroy preview environment
    // For now, just simulate the operation
  }

  private async readFileContent(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => resolve(reader.result as string)
      reader.onerror = reject
      reader.readAsText(file)
    })
  }

  private determineFileType(path: string): 'component' | 'page' | 'asset' | 'config' {
    if (path.includes('/components/')) return 'component'
    if (path.includes('/pages/') || path.includes('/routes/')) return 'page'
    if (path.match(/\.(png|jpg|jpeg|gif|svg|css|scss|less)$/)) return 'asset'
    if (path.match(/\.(json|yaml|yml|toml|env)$/)) return 'config'
    return 'component'
  }

  private async buildForFirebase(project: BoltDiyProject): Promise<BoltDiyBuildResult> {
    // Simulate Firebase-specific build process
    return {
      success: true,
      deploymentId: `firebase-${Date.now()}`,
      url: `https://${project.name.toLowerCase()}.web.app`,
      buildTime: 45000,
      errors: [],
      warnings: []
    }
  }

  // Enhanced cross-platform integration methods
  async syncWithFirebase(projectId: string, firebaseData: any): Promise<boolean> {
    if (!this.authenticated) return false;

    try {
      // Sync project data with Firebase
      const syncPayload = {
        projectId,
        platform: 'boltdiy',
        data: {
          files: this.currentProject?.files || [],
          deployments: this.currentProject?.deployments || [],
          settings: this.currentProject?.settings,
          lastSync: new Date().toISOString()
        },
        firebaseData
      };

      // Simulate Firebase sync
      await new Promise(resolve => setTimeout(resolve, 500));
      
      this.emit('firebase-sync', syncPayload);
      console.log('Successfully synced Bolt.diy project with Firebase:', projectId);
      return true;
    } catch (error) {
      console.error('Failed to sync with Firebase:', error);
      return false;
    }
  }

  async syncWithCursor(projectId: string, cursorData: any): Promise<boolean> {
    if (!this.authenticated) return false;

    try {
      // Sync with Cursor IDE
      const syncPayload = {
        projectId,
        platform: 'boltdiy',
        files: this.currentProject?.files || [],
        cursorData,
        timestamp: new Date().toISOString()
      };

      // Update current project with Cursor data if provided
      if (cursorData.files && this.currentProject) {
        Object.entries(cursorData.files).forEach(([path, content]) => {
          const existingFileIndex = this.currentProject!.files.findIndex(f => f.path === path);
          const fileData: BoltDiyFile = {
            path,
            content: content as string,
            type: this.determineFileType(path),
            lastModified: new Date().toISOString(),
            size: (content as string).length
          };

          if (existingFileIndex >= 0) {
            this.currentProject!.files[existingFileIndex] = fileData;
          } else {
            this.currentProject!.files.push(fileData);
          }
        });
      }

      this.emit('cursor-sync', syncPayload);
      console.log('Successfully synced Bolt.diy project with Cursor:', projectId);
      return true;
    } catch (error) {
      console.error('Failed to sync with Cursor:', error);
      return false;
    }
  }

  async syncWithTraeAI(projectId: string, traeData: any): Promise<boolean> {
    if (!this.authenticated) return false;

    try {
      // Sync with Trae.AI
      const syncPayload = {
        projectId,
        platform: 'boltdiy',
        analysisData: traeData.analysis || {},
        recommendations: traeData.recommendations || [],
        codeQuality: traeData.codeQuality || {},
        timestamp: new Date().toISOString()
      };

      // Apply Trae.AI recommendations if available
      if (traeData.recommendations && this.currentProject) {
        traeData.recommendations.forEach((rec: any) => {
          if (rec.type === 'code_improvement' && rec.filePath) {
            const fileIndex = this.currentProject!.files.findIndex(f => f.path === rec.filePath);
            if (fileIndex >= 0 && rec.suggestedCode) {
              this.currentProject!.files[fileIndex].content = rec.suggestedCode;
              this.currentProject!.files[fileIndex].lastModified = new Date().toISOString();
            }
          }
        });
      }

      this.emit('traeai-sync', syncPayload);
      console.log('Successfully synced Bolt.diy project with Trae.AI:', projectId);
      return true;
    } catch (error) {
      console.error('Failed to sync with Trae.AI:', error);
      return false;
    }
  }

  // Unified synchronization orchestrator
  async syncAllPlatformsUnified(projectId: string, platformData: {
    cursor?: any;
    firebase?: any;
    traeai?: any;
  }): Promise<{
    cursor: boolean;
    firebase: boolean;
    traeai: boolean;
    boltdiy: boolean;
    errors: string[];
  }> {
    const results = {
      cursor: false,
      firebase: false,
      traeai: false,
      boltdiy: true, // Bolt.diy is the source platform
      errors: [] as string[]
    };

    try {
      // Execute all syncs in parallel
      const syncPromises = [];

      if (platformData.cursor) {
        syncPromises.push(
          this.syncWithCursor(projectId, platformData.cursor)
            .then(success => { results.cursor = success; })
            .catch(error => { results.errors.push(`Cursor sync failed: ${error.message}`); })
        );
      }

      if (platformData.firebase) {
        syncPromises.push(
          this.syncWithFirebase(projectId, platformData.firebase)
            .then(success => { results.firebase = success; })
            .catch(error => { results.errors.push(`Firebase sync failed: ${error.message}`); })
        );
      }

      if (platformData.traeai) {
        syncPromises.push(
          this.syncWithTraeAI(projectId, platformData.traeai)
            .then(success => { results.traeai = success; })
            .catch(error => { results.errors.push(`Trae.AI sync failed: ${error.message}`); })
        );
      }

      await Promise.allSettled(syncPromises);

      this.emit('allPlatformsSyncedUnified', { projectId, results });
      return results;
    } catch (error: any) {
      results.errors.push(`Unified sync orchestration failed: ${error.message}`);
      this.emit('allPlatformsSyncError', { projectId, error });
      return results;
    }
  }

  // Real-time event broadcasting to other platforms
  async broadcastToAllPlatforms(projectId: string, event: {
    type: 'file_change' | 'deployment' | 'build_complete' | 'component_added';
    data: any;
    source: 'boltdiy';
  }): Promise<boolean> {
    try {
      const broadcastPayload = {
        projectId,
        event,
        timestamp: new Date().toISOString(),
        source: 'boltdiy'
      };

      // Emit to all connected platforms
      this.emit('broadcast-to-cursor', broadcastPayload);
      this.emit('broadcast-to-firebase', broadcastPayload);
      this.emit('broadcast-to-traeai', broadcastPayload);

      console.log('Successfully broadcasted event to all platforms:', event.type);
      return true;
    } catch (error) {
      console.error('Failed to broadcast to all platforms:', error);
      return false;
    }
  }

  // Get unified integration status for all connected platforms
  async getUnifiedIntegrationStatus(projectId: string): Promise<{
    platforms: {
      boltdiy: { connected: boolean; lastSync?: string; deploymentUrl?: string };
      cursor: { connected: boolean; lastSync?: string; status?: string };
      firebase: { connected: boolean; lastSync?: string };
      traeai: { connected: boolean; lastSync?: string; analysisStatus?: string };
    };
    overallHealth: 'healthy' | 'warning' | 'error';
    activeConnections: number;
  }> {
    try {
      const platforms = {
        boltdiy: {
          connected: this.authenticated,
          lastSync: new Date().toISOString(),
          deploymentUrl: this.currentProject?.url || this.currentProject?.previewUrl
        },
        cursor: {
          connected: false, // Will be updated by actual connection status
          lastSync: undefined as string | undefined,
          status: 'unknown'
        },
        firebase: {
          connected: false, // Will be updated by actual connection status
          lastSync: undefined as string | undefined
        },
        traeai: {
          connected: false, // Will be updated by actual connection status
          lastSync: undefined as string | undefined,
          analysisStatus: 'pending'
        }
      };

      // Check actual connection status (simplified for now)
      const activeConnections = Object.values(platforms).filter(p => p.connected).length;
      
      let overallHealth: 'healthy' | 'warning' | 'error' = 'healthy';
      if (activeConnections === 0) {
        overallHealth = 'error';
      } else if (activeConnections < 2) {
        overallHealth = 'warning';
      }

      return {
        platforms,
        overallHealth,
        activeConnections
      };
    } catch (error) {
      console.error('Error getting unified integration status:', error);
      return {
        platforms: {
          boltdiy: { connected: false },
          cursor: { connected: false },
          firebase: { connected: false },
          traeai: { connected: false }
        },
        overallHealth: 'error',
        activeConnections: 0
      };
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
}

// Export singleton instance
export const boltDiyService = new BoltDiyService()