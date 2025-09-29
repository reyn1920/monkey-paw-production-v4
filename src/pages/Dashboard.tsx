import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Activity, 
  Zap, 
  Users, 
  TrendingUp,
  Server,
  Database,
  Globe,
  AlertCircle,
  CheckCircle,
  Clock,
  Play,
  Settings,
  Code,
  Layers,
  Brain,
  RefreshCw,
  Link,
  Unlink
} from 'lucide-react'

interface SystemStatus {
  name: string
  status: 'online' | 'offline' | 'warning'
  port?: number
  lastCheck: string
}

interface QuickAction {
  name: string
  description: string
  icon: React.ElementType
  action: () => void
  testId: string
}

interface PlatformStatus {
  id: string
  name: string
  status: 'connected' | 'disconnected' | 'syncing' | 'error'
  lastSync: string
  projects?: number
  icon: React.ElementType
  color: string
}

function Dashboard() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus[]>([
    { name: 'FastAPI Backend', status: 'online', port: 8002, lastCheck: new Date().toISOString() },
    { name: 'Health Service 8000', status: 'online', port: 8000, lastCheck: new Date().toISOString() },
    { name: 'Health Service 4000', status: 'online', port: 4000, lastCheck: new Date().toISOString() },
    { name: 'Firebase Connection', status: 'online', lastCheck: new Date().toISOString() },
    { name: 'Trae.ai Integration', status: 'warning', lastCheck: new Date().toISOString() },
  ])

  const [platformStatus, setPlatformStatus] = useState<PlatformStatus[]>([
    {
      id: 'cursor',
      name: 'Cursor IDE',
      status: 'connected',
      lastSync: new Date().toISOString(),
      projects: 3,
      icon: Code,
      color: 'blue'
    },
    {
      id: 'vscode',
      name: 'VS Code',
      status: 'connected',
      lastSync: new Date().toISOString(),
      projects: 4,
      icon: Code,
      color: 'blue'
    },
    {
      id: 'windsurf',
      name: 'Windsurf AI',
      status: 'connected',
      lastSync: new Date().toISOString(),
      projects: 2,
      icon: Brain,
      color: 'cyan'
    },
    {
      id: 'boltdiy',
      name: 'Bolt.diy',
      status: 'connected',
      lastSync: new Date().toISOString(),
      projects: 2,
      icon: Zap,
      color: 'purple'
    },
    {
      id: 'firebase',
      name: 'Firebase',
      status: 'connected',
      lastSync: new Date().toISOString(),
      projects: 5,
      icon: Database,
      color: 'orange'
    },
    {
      id: 'traeai',
      name: 'Trae.ai',
      status: 'syncing',
      lastSync: new Date().toISOString(),
      projects: 1,
      icon: Brain,
      color: 'green'
    }
  ])

  const [stats] = useState({
    totalStacks: 12,
    activeIntegrations: 5,
    automationRuns: 47,
    uptime: '99.9%'
  })

  const quickActions: QuickAction[] = [
    {
      name: 'Create New Stack',
      description: 'Generate a new development stack template',
      icon: Zap,
      action: () => console.log('Creating new stack...'),
      testId: 'quick-action-create-stack'
    },
    {
      name: 'Run Health Check',
      description: 'Check all system components',
      icon: Activity,
      action: () => checkSystemHealth(),
      testId: 'quick-action-health-check'
    },
    {
      name: 'Start Automation',
      description: 'Launch web automation suite',
      icon: Play,
      action: () => console.log('Starting automation...'),
      testId: 'quick-action-automation'
    },
    {
      name: 'System Settings',
      description: 'Configure platform integrations',
      icon: Settings,
      action: () => console.log('Opening settings...'),
      testId: 'quick-action-settings'
    }
  ]

  const checkSystemHealth = async () => {
    console.log('Checking system health...')
    // Simulate health check
    setSystemStatus(prev => prev.map(service => ({
      ...service,
      lastCheck: new Date().toISOString(),
      status: Math.random() > 0.1 ? 'online' : 'warning'
    })))
  }

  const syncAllPlatforms = async () => {
    console.log('Syncing all platforms...')
    setPlatformStatus(prev => prev.map(platform => ({
      ...platform,
      status: 'syncing' as const
    })))

    // Simulate sync process
    setTimeout(() => {
      setPlatformStatus(prev => prev.map(platform => ({
        ...platform,
        status: 'connected' as const,
        lastSync: new Date().toISOString()
      })))
    }, 2000)
  }

  const togglePlatformConnection = (platformId: string) => {
    setPlatformStatus(prev => prev.map(platform => 
      platform.id === platformId 
        ? { 
            ...platform, 
            status: platform.status === 'connected' ? 'disconnected' : 'connected',
            lastSync: new Date().toISOString()
          }
        : platform
    ))
  }

  useEffect(() => {
    // Auto-refresh system status every 30 seconds
    const interval = setInterval(checkSystemHealth, 30000)
    return () => clearInterval(interval)
  }, [])

  const getStatusIcon = (status: SystemStatus['status']) => {
    switch (status) {
      case 'online':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'warning':
        return <AlertCircle className="h-5 w-5 text-yellow-500" />
      case 'offline':
        return <AlertCircle className="h-5 w-5 text-red-500" />
    }
  }

  const getStatusColor = (status: SystemStatus['status']) => {
    switch (status) {
      case 'online':
        return 'bg-green-100 text-green-800'
      case 'warning':
        return 'bg-yellow-100 text-yellow-800'
      case 'offline':
        return 'bg-red-100 text-red-800'
    }
  }

  const getPlatformStatusIcon = (status: PlatformStatus['status']) => {
    switch (status) {
      case 'connected':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'syncing':
        return <RefreshCw className="h-5 w-5 text-blue-500 animate-spin" />
      case 'disconnected':
        return <Unlink className="h-5 w-5 text-gray-400" />
      case 'error':
        return <AlertCircle className="h-5 w-5 text-red-500" />
    }
  }

  const getPlatformStatusColor = (status: PlatformStatus['status']) => {
    switch (status) {
      case 'connected':
        return 'bg-green-100 text-green-800'
      case 'syncing':
        return 'bg-blue-100 text-blue-800'
      case 'disconnected':
        return 'bg-gray-100 text-gray-800'
      case 'error':
        return 'bg-red-100 text-red-800'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-4">
        <h1 className="text-3xl font-bold text-gray-900">Unified Development Platform</h1>
        <p className="mt-2 text-gray-600">
          Connect and manage Cursor, Bolt.diy, Firebase, Trae.ai, VS Code, and Windsurf in one unified environment
        </p>
      </div>

      {/* Platform Integration Status */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-gray-900">Platform Integrations</h2>
          <button
            onClick={syncAllPlatforms}
            className="btn-primary flex items-center"
            data-testid="sync-all-platforms"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Sync All
          </button>
        </div>
        
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
          {platformStatus.map((platform, index) => (
            <motion.div
              key={platform.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 * index }}
              className="p-4 bg-gray-50 rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <platform.icon className={`h-6 w-6 text-${platform.color}-600`} />
                  <h3 className="font-medium text-gray-900">{platform.name}</h3>
                </div>
                {getPlatformStatusIcon(platform.status)}
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-500">Status:</span>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${getPlatformStatusColor(platform.status)}`}>
                    {platform.status.toUpperCase()}
                  </span>
                </div>
                
                {platform.projects && (
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-500">Projects:</span>
                    <span className="text-sm font-medium text-gray-900">{platform.projects}</span>
                  </div>
                )}
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-500">Last Sync:</span>
                  <span className="text-xs text-gray-500">
                    {new Date(platform.lastSync).toLocaleTimeString()}
                  </span>
                </div>
              </div>
              
              <div className="mt-3 pt-3 border-t border-gray-200">
                <button
                  onClick={() => togglePlatformConnection(platform.id)}
                  className={`w-full text-sm py-2 px-3 rounded-md transition-colors ${
                    platform.status === 'connected' 
                      ? 'bg-red-100 text-red-700 hover:bg-red-200' 
                      : 'bg-green-100 text-green-700 hover:bg-green-200'
                  }`}
                  data-testid={`toggle-${platform.id}`}
                >
                  {platform.status === 'connected' ? (
                    <>
                      <Unlink className="h-3 w-3 inline mr-1" />
                      Disconnect
                    </>
                  ) : (
                    <>
                      <Link className="h-3 w-3 inline mr-1" />
                      Connect
                    </>
                  )}
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Layers className="h-8 w-8 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Connected Platforms</p>
              <p className="text-2xl font-semibold text-gray-900">
                {platformStatus.filter(p => p.status === 'connected').length}
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Zap className="h-8 w-8 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Projects</p>
              <p className="text-2xl font-semibold text-gray-900">
                {platformStatus.reduce((sum, p) => sum + (p.projects || 0), 0)}
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <TrendingUp className="h-8 w-8 text-success-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Automation Runs</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.automationRuns}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="card"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Activity className="h-8 w-8 text-warning-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">System Uptime</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.uptime}</p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* System Status */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="card"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">System Status</h2>
          <button
            onClick={checkSystemHealth}
            className="btn-secondary"
            data-testid="refresh-status"
          >
            <Activity className="h-4 w-4 mr-2" />
            Refresh
          </button>
        </div>
        
        <div className="space-y-3">
          {systemStatus.map((service, index) => (
            <motion.div
              key={service.name}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * index }}
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center space-x-3">
                {getStatusIcon(service.status)}
                <div>
                  <p className="font-medium text-gray-900">{service.name}</p>
                  {service.port && (
                    <p className="text-sm text-gray-500">Port: {service.port}</p>
                  )}
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(service.status)}`}>
                  {service.status.toUpperCase()}
                </span>
                <div className="flex items-center text-xs text-gray-500">
                  <Clock className="h-3 w-3 mr-1" />
                  {new Date(service.lastCheck).toLocaleTimeString()}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="card"
      >
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {quickActions.map((action, index) => (
            <motion.button
              key={action.name}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 * index }}
              onClick={action.action}
              data-testid={action.testId}
              className="p-4 text-left bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <action.icon className="h-8 w-8 text-primary-600 mb-2" />
              <h3 className="font-medium text-gray-900">{action.name}</h3>
              <p className="text-sm text-gray-600 mt-1">{action.description}</p>
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="card"
      >
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
        <div className="space-y-3">
          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <Server className="h-5 w-5 text-blue-500" />
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">All platforms synchronized</p>
              <p className="text-xs text-gray-500">2 minutes ago</p>
            </div>
          </div>
          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <Database className="h-5 w-5 text-green-500" />
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">Firebase connection established</p>
              <p className="text-xs text-gray-500">5 minutes ago</p>
            </div>
          </div>
          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <Globe className="h-5 w-5 text-purple-500" />
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">Cursor IDE integration active</p>
              <p className="text-xs text-gray-500">10 minutes ago</p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default Dashboard