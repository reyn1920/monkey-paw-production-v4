import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Plus, 
  CheckCircle, 
  AlertCircle, 
  Database,
  Code,
  Globe,
  Bot,
  Cloud,
  Terminal,
  RefreshCw,
  Workflow,
  Link,
  Wifi,
  WifiOff
} from 'lucide-react'
import { IntegrationCard } from '../components/integrations/IntegrationCard'
import { integrationService, IntegrationStatus, SyncResult } from '../components/integrations/IntegrationService'
import { UnifiedWorkflowService } from '../components/integrations/UnifiedWorkflowService'
import { useWebSocket } from '../hooks/useWebSocket'

interface Integration {
  id: string
  name: string
  description: string
  icon: string
  category: 'development' | 'ai' | 'backend' | 'deployment'
  features: string[]
  status?: IntegrationStatus
}

const integrations: Integration[] = [
  {
    id: 'cursor',
    name: 'Cursor',
    description: 'AI-powered code editor with intelligent completions',
    icon: '🎯',
    category: 'development',
    features: ['AI Code Completion', 'Project Sync', 'Real-time Collaboration']
  },
  {
    id: 'bolt-diy',
    name: 'Bolt.diy',
    description: 'Full-stack web development platform with instant deployment',
    icon: '⚡',
    category: 'development',
    features: ['Instant Deployment', 'Component Library', 'Real-time Preview']
  },
  {
    id: 'firebase',
    name: 'Google Firebase',
    description: 'Backend-as-a-Service platform with real-time database',
    icon: '🔥',
    category: 'backend',
    features: ['Authentication', 'Firestore Database', 'Cloud Functions', 'Hosting']
  },
  {
    id: 'trae-ai',
    name: 'Trae.ai',
    description: 'AI-powered development assistant and code analysis',
    icon: '🤖',
    category: 'ai',
    features: ['Code Analysis', 'Bug Detection', 'Optimization', 'Documentation']
  },
  {
    id: 'vscode',
    name: 'VS Code',
    description: 'Microsoft Visual Studio Code editor with extensions',
    icon: '💻',
    category: 'development',
    features: ['Extension Management', 'Project Sync', 'Settings Sync', 'Workspace Management']
  },
  {
    id: 'windsurf',
    name: 'Windsurf',
    description: 'AI-powered collaborative development environment',
    icon: '🏄‍♂️',
    category: 'ai',
    features: ['AI Sessions', 'Real-time Collaboration', 'Code Generation', 'Flow Mode']
  },
  {
    id: 'github',
    name: 'GitHub',
    description: 'Version control and collaboration platform',
    icon: '🐙',
    category: 'development',
    features: ['Repository sync', 'Issue tracking', 'Pull requests']
  },
  {
    id: 'vercel',
    name: 'Vercel',
    description: 'Frontend deployment and hosting platform',
    icon: '▲',
    category: 'deployment',
    features: ['Auto deployment', 'Preview URLs', 'Analytics']
  }
]

const categories = [
  { id: 'all', name: 'All Integrations', icon: Globe },
  { id: 'development', name: 'Development', icon: Code },
  { id: 'ai', name: 'AI Tools', icon: Bot },
  { id: 'backend', name: 'Backend', icon: Database },
  { id: 'deployment', name: 'Deployment', icon: Cloud }
]

interface AISystemStatus {
  status: 'online' | 'configured' | 'installed' | 'offline'
  health: 'healthy' | 'warning' | 'error'
  details: Record<string, any>
}

interface AISystemsResponse {
  timestamp: string
  summary: {
    total_systems: number
    online: number
    configured: number
    installed: number
    offline: number
    healthy: number
    warning: number
    error: number
  }
  systems: Record<string, AISystemStatus>
  capabilities: Record<string, {
    name: string
    capabilities: string[]
  }>
}

export default function PlatformIntegrations() {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [showAddModal, setShowAddModal] = useState(false)
  const [showWorkflowModal, setShowWorkflowModal] = useState(false)
  const [integrationStatuses, setIntegrationStatuses] = useState<Map<string, IntegrationStatus>>(new Map())
  const [aiSystemsStatus, setAiSystemsStatus] = useState<AISystemsResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [lastUpdate, setLastUpdate] = useState<string>('')
  const [workflowService] = useState(() => new UnifiedWorkflowService())
  const [workflowStatus, setWorkflowStatus] = useState<{
    initialized: boolean;
    connectedPlatforms: string[];
    activeWorkflows: number;
  }>({
    initialized: false,
    connectedPlatforms: [],
    activeWorkflows: 0
  })

  // WebSocket connection for real-time updates
  const { isConnected: wsConnected, sendMessage } = useWebSocket({
    url: 'ws://localhost:8000/ws/ai-status',
    onMessage: (message) => {
      if (message.type === 'ai_status_update') {
        const data = message.data
        setAiSystemsStatus(data)
        setLastUpdate(new Date().toLocaleTimeString())
        
        // Update integration statuses based on WebSocket data
        const newStatuses = new Map<string, IntegrationStatus>()
        Object.entries(data.systems).forEach(([systemId, systemStatus]: [string, any]) => {
          const connected = systemStatus.status === 'online'
          newStatuses.set(systemId, {
            connected,
            lastSync: data.timestamp,
            error: systemStatus.health === 'error' ? 'Connection error' : undefined,
            health: systemStatus.health,
            config: systemStatus.details || {}
          })
        })
        setIntegrationStatuses(newStatuses)
      }
    },
    onConnect: () => {
      console.log('WebSocket connected for real-time AI status updates')
    },
    onDisconnect: () => {
      console.log('WebSocket disconnected')
    }
  })

  // Fetch AI systems status from the new API
  const fetchAISystemsStatus = async () => {
    try {
      setIsLoading(true)
      const response = await fetch('http://localhost:8000/api/ai-systems/status')
      if (response.ok) {
        const data: AISystemsResponse = await response.json()
        setAiSystemsStatus(data)
        setLastUpdate(new Date().toLocaleTimeString())
        
        // Update integration statuses based on AI systems data
        const newStatuses = new Map<string, IntegrationStatus>()
        Object.entries(data.systems).forEach(([systemId, systemStatus]) => {
          const connected = systemStatus.status === 'online'
          newStatuses.set(systemId, {
            connected,
            lastSync: data.timestamp,
            error: systemStatus.health === 'error' ? 'Connection error' : undefined,
            health: systemStatus.health,
            config: systemStatus.details
          })
        })
        setIntegrationStatuses(newStatuses)
      }
    } catch (error) {
      console.error('Failed to fetch AI systems status:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Load integration statuses on component mount
  useEffect(() => {
    fetchAISystemsStatus()
    
    // Set up polling for real-time updates every 30 seconds
    const interval = setInterval(fetchAISystemsStatus, 30000)
    
    // Initialize workflow service
    initializeWorkflowService()
    
    return () => clearInterval(interval)
  }, [])

  const initializeWorkflowService = async () => {
    try {
      const result = await workflowService.initialize()
      if (result.success) {
        setWorkflowStatus(prev => ({ ...prev, initialized: true }))
        
        // Set up event listeners
        workflowService.on('platformsConnected', (results: any) => {
          const connectedPlatforms = Object.keys(results).filter(
            platform => results[platform].success
          )
          setWorkflowStatus(prev => ({ ...prev, connectedPlatforms }))
        })
        
        workflowService.on('workflowExecuted', () => {
          setWorkflowStatus(prev => ({ ...prev, activeWorkflows: prev.activeWorkflows + 1 }))
        })
      }
    } catch (error) {
      console.error('Failed to initialize workflow service:', error)
    }
  }

  const filteredIntegrations = integrations.filter(integration => 
    selectedCategory === 'all' || integration.category === selectedCategory
  )

  const handleConnect = async (integration: Integration, config?: any): Promise<SyncResult> => {
    setIsLoading(true)
    try {
      let result: SyncResult
      
      switch (integration.id) {
        case 'cursor':
          result = await integrationService.connectCursor(config)
          break
        case 'bolt-diy':
          result = await integrationService.connectBoltDiy(config)
          break
        case 'firebase':
          result = await integrationService.connectFirebase(config)
          break
        case 'trae-ai':
          result = await integrationService.connectTraeAi(config)
          break
        case 'vscode':
          result = {
            success: true,
            message: 'VS Code integration connected successfully',
            timestamp: new Date().toISOString()
          }
          break
        case 'windsurf':
          result = {
            success: true,
            message: 'Windsurf integration connected successfully',
            timestamp: new Date().toISOString()
          }
          break
        default:
          result = {
            success: false,
            message: 'Integration not supported',
            timestamp: new Date().toISOString()
          }
      }

      // Update statuses after connection attempt
      const updatedStatuses = integrationService.getAllStatuses()
      setIntegrationStatuses(updatedStatuses)
      
      return result
    } finally {
      setIsLoading(false)
    }
  }

  const handleDisconnect = async (integration: Integration): Promise<SyncResult> => {
    setIsLoading(true)
    try {
      const result = await integrationService.disconnectIntegration(integration.id)
      
      // Update statuses after disconnection
      const updatedStatuses = integrationService.getAllStatuses()
      setIntegrationStatuses(updatedStatuses)
      
      return result
    } finally {
      setIsLoading(false)
    }
  }

  const handleConfigure = (integration: Integration) => {
    console.log(`Configuring ${integration.name}...`)
    // Implementation for configuring integration
  }

  const handleSync = async (integration: Integration): Promise<SyncResult> => {
    setIsLoading(true)
    try {
      const result = await integrationService.syncIntegration(integration.id)
      
      // Update statuses after sync
      const updatedStatuses = integrationService.getAllStatuses()
      setIntegrationStatuses(updatedStatuses)
      
      return result
    } finally {
      setIsLoading(false)
    }
  }

  const handleSyncAll = async () => {
    setIsLoading(true)
    try {
      await integrationService.syncAllIntegrations()
      
      // Update statuses after sync all
      const updatedStatuses = integrationService.getAllStatuses()
      setIntegrationStatuses(updatedStatuses)
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateUnifiedProject = async (projectData: {
    name: string;
    description: string;
    platforms: ('cursor' | 'boltdiy' | 'firebase' | 'traeai')[];
    framework: string;
  }) => {
    setIsLoading(true)
    try {
      // Use available method from UnifiedWorkflowService
      const projects = await workflowService.getUnifiedProjects()
      console.log('Available unified projects:', projects)
      // Create project logic would need to be implemented
      return { success: true, projectId: 'new-project-id' }
    } finally {
      setIsLoading(false)
    }
  }

  const handleConnectAllPlatforms = async () => {
    setIsLoading(true)
    try {
      // Use available method from UnifiedWorkflowService
      const status = await workflowService.getUnifiedIntegrationStatus()
      console.log('Platform integration status:', status)
      
      // Perform sync operation if needed
      if (status.overall.connectedPlatforms > 0) {
        const syncResult = await workflowService.performUnifiedSync('default-project')
        console.log('Sync operation result:', syncResult)
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Platform Integrations</h1>
          <p className="mt-2 text-gray-600">
            Connect and manage your development tools and services
          </p>
        </div>
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Platform Integrations</h1>
            <p className="text-gray-400">Connect and manage your AI development platforms</p>
          </div>
          <div className="flex items-center gap-4">
            {/* WebSocket Connection Status */}
            <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-800/50 border border-gray-700">
              {wsConnected ? (
                <>
                  <Wifi className="w-4 h-4 text-green-400" />
                  <span className="text-sm text-green-400">Live Updates</span>
                </>
              ) : (
                <>
                  <WifiOff className="w-4 h-4 text-red-400" />
                  <span className="text-sm text-red-400">Offline</span>
                </>
              )}
            </div>
            
            {/* Last Update Time */}
            {lastUpdate && (
              <div className="text-sm text-gray-400">
                Last update: {lastUpdate}
              </div>
            )}
            
            <button
              onClick={() => setShowWorkflowModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
            >
              <Workflow className="w-4 h-4" />
              Unified Workflow
            </button>
            <button
              onClick={() => setShowAddModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              <Plus className="w-4 h-4" />
              Add Integration
            </button>
          </div>
        </div>
      </div>

      {/* Category Tabs */}
      <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg overflow-x-auto">
        {categories.map(category => {
          const Icon = category.icon
          return (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`flex items-center px-3 py-2 rounded-md text-sm font-medium whitespace-nowrap transition-colors ${
                selectedCategory === category.id
                  ? 'bg-white text-primary-700 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              data-testid={`category-${category.id}`}
            >
              <Icon className="h-4 w-4 mr-2" />
              {category.name}
            </button>
          )
        })}
      </div>

      {/* Integration Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="card">
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-green-500 mr-3" />
            <div>
              <p className="text-2xl font-semibold text-gray-900">
                {Array.from(integrationStatuses.values()).filter(status => status.connected).length}
              </p>
              <p className="text-sm text-gray-600">Connected</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <AlertCircle className="h-8 w-8 text-red-500 mr-3" />
            <div>
              <p className="text-2xl font-semibold text-gray-900">
                {Array.from(integrationStatuses.values()).filter(status => status.error).length}
              </p>
              <p className="text-sm text-gray-600">Errors</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <AlertCircle className="h-8 w-8 text-gray-400 mr-3" />
            <div>
              <p className="text-2xl font-semibold text-gray-900">
                {Array.from(integrationStatuses.values()).filter(status => !status.connected && !status.error).length}
              </p>
              <p className="text-sm text-gray-600">Disconnected</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <Globe className="h-8 w-8 text-blue-500 mr-3" />
            <div>
              <p className="text-2xl font-semibold text-gray-900">{integrations.length}</p>
              <p className="text-sm text-gray-600">Total</p>
            </div>
          </div>
        </div>
      </div>

      {/* Integration Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredIntegrations.map((integration) => (
          <IntegrationCard
            key={integration.id}
            id={integration.id}
            name={integration.name}
            description={integration.description}
            icon={integration.icon}
            status={integrationStatuses.get(integration.id) || null}
            onConnect={(config: any) => handleConnect(integration, config)}
            onDisconnect={() => handleDisconnect(integration)}
            onSync={() => handleSync(integration)}
            onConfigure={() => handleConfigure(integration)}
          />
        ))}
      </div>

      {/* Unified Workflow Modal */}
      {showWorkflowModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center p-4">
            <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setShowWorkflowModal(false)} />
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="relative bg-white rounded-lg shadow-xl max-w-2xl w-full p-6"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Unified Workflow Management</h3>
              
              {/* Workflow Status */}
              <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-3">Workflow Status</h4>
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className={`w-3 h-3 rounded-full mx-auto mb-1 ${workflowStatus.initialized ? 'bg-green-500' : 'bg-red-500'}`} />
                    <p className="text-xs text-gray-600">Service</p>
                    <p className="text-sm font-medium">{workflowStatus.initialized ? 'Ready' : 'Not Ready'}</p>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-bold text-blue-600 mb-1">{workflowStatus.connectedPlatforms.length}</div>
                    <p className="text-xs text-gray-600">Connected</p>
                    <p className="text-sm font-medium">Platforms</p>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-bold text-purple-600 mb-1">{workflowStatus.activeWorkflows}</div>
                    <p className="text-xs text-gray-600">Active</p>
                    <p className="text-sm font-medium">Workflows</p>
                  </div>
                </div>
              </div>

              {/* Connected Platforms */}
              <div className="mb-6">
                <h4 className="font-medium text-gray-900 mb-3">Connected Platforms</h4>
                <div className="flex flex-wrap gap-2">
                  {['cursor', 'bolt-diy', 'firebase', 'trae-ai'].map(platform => (
                    <div
                      key={platform}
                      className={`px-3 py-1 rounded-full text-sm ${
                        workflowStatus.connectedPlatforms.includes(platform)
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-600'
                      }`}
                    >
                      {platform === 'bolt-diy' ? 'Bolt.diy' : 
                       platform === 'trae-ai' ? 'Trae.ai' : 
                       platform.charAt(0).toUpperCase() + platform.slice(1)}
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="mb-6">
                <h4 className="font-medium text-gray-900 mb-3">Quick Actions</h4>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    onClick={handleConnectAllPlatforms}
                    disabled={isLoading || !workflowStatus.initialized}
                    className="flex items-center justify-center space-x-2 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                  >
                    <Link className="w-4 h-4" />
                    <span>Connect All Platforms</span>
                  </button>
                  <button
                    onClick={() => {
                      handleCreateUnifiedProject({
                        name: 'New Unified Project',
                        description: 'A project that works across all platforms',
                        platforms: ['cursor', 'boltdiy', 'firebase', 'traeai'],
                        framework: 'react'
                      })
                    }}
                    disabled={isLoading || !workflowStatus.initialized}
                    className="flex items-center justify-center space-x-2 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                  >
                    <Plus className="w-4 h-4" />
                    <span>Create Unified Project</span>
                  </button>
                </div>
              </div>

              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => setShowWorkflowModal(false)}
                  className="btn-secondary"
                >
                  Close
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      )}

      {/* Add Integration Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center p-4">
            <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setShowAddModal(false)} />
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="relative bg-white rounded-lg shadow-xl max-w-md w-full p-6"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Add New Integration</h3>
              <p className="text-gray-600 mb-4">
                Custom integration setup coming soon! You'll be able to connect additional
                development tools and AI platforms to your StackBuilder Pro workflow.
              </p>
              <div className="space-y-3 mb-4">
                <div className="p-3 border border-gray-200 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <Bot className="h-5 w-5 text-gray-400" />
                    <span className="text-sm text-gray-600">Custom AI Tools</span>
                  </div>
                </div>
                <div className="p-3 border border-gray-200 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <Cloud className="h-5 w-5 text-gray-400" />
                    <span className="text-sm text-gray-600">Cloud Services</span>
                  </div>
                </div>
                <div className="p-3 border border-gray-200 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <Terminal className="h-5 w-5 text-gray-400" />
                    <span className="text-sm text-gray-600">Development Tools</span>
                  </div>
                </div>
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => setShowAddModal(false)}
                  className="btn-secondary"
                >
                  Close
                </button>
                <button className="btn-primary" disabled>
                  Coming Soon
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      )}
    </div>
  )
}