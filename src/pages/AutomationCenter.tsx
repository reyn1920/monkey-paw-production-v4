import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Play, 
  Pause, 
  Square, 
  Settings, 
  Plus,
  Bot,
  Globe,
  Camera,
  MousePointer,
  Keyboard,
  Eye,
  Clock,
  CheckCircle,
  AlertCircle,
  Download,
  Upload,
  Code,
  Zap
} from 'lucide-react'

interface AutomationTask {
  id: string
  name: string
  description: string
  type: 'web_test' | 'screenshot' | 'form_fill' | 'navigation' | 'api_test'
  status: 'idle' | 'running' | 'completed' | 'failed'
  lastRun?: string
  duration?: number
  results?: any
  testId: string
}

interface AutomationScript {
  id: string
  name: string
  description: string
  category: 'testing' | 'monitoring' | 'data_collection' | 'ui_automation'
  actions: string[]
  testId: string
}

const mockTasks: AutomationTask[] = [
  {
    id: '1',
    name: 'StackBuilder Pro Health Check',
    description: 'Automated health check of all system components',
    type: 'web_test',
    status: 'completed',
    lastRun: '2024-01-20T10:30:00Z',
    duration: 45,
    results: { passed: 8, failed: 0, warnings: 1 },
    testId: 'task-health-check'
  },
  {
    id: '2',
    name: 'Platform Integration Test',
    description: 'Test connections to all integrated platforms',
    type: 'api_test',
    status: 'running',
    lastRun: '2024-01-20T11:00:00Z',
    testId: 'task-integration-test'
  },
  {
    id: '3',
    name: 'UI Screenshot Capture',
    description: 'Capture screenshots of all main pages',
    type: 'screenshot',
    status: 'idle',
    testId: 'task-screenshot'
  }
]

const automationScripts: AutomationScript[] = [
  {
    id: '1',
    name: 'Full Application Test',
    description: 'Complete end-to-end testing of StackBuilder Pro',
    category: 'testing',
    actions: ['Navigate to Dashboard', 'Check System Status', 'Test Navigation', 'Capture Screenshots'],
    testId: 'script-full-test'
  },
  {
    id: '2',
    name: 'Platform Health Monitor',
    description: 'Monitor health of all integrated platforms',
    category: 'monitoring',
    actions: ['Check API Endpoints', 'Verify Connections', 'Log Status', 'Send Alerts'],
    testId: 'script-health-monitor'
  },
  {
    id: '3',
    name: 'User Journey Test',
    description: 'Simulate typical user workflows',
    category: 'ui_automation',
    actions: ['Login Flow', 'Create Template', 'Deploy Stack', 'Check Results'],
    testId: 'script-user-journey'
  }
]

export default function AutomationCenter() {
  const [tasks, setTasks] = useState<AutomationTask[]>(mockTasks)
  const [selectedTask, setSelectedTask] = useState<string | null>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)

  const handleRunTask = async (taskId: string) => {
    setTasks(prev => prev.map(task => 
      task.id === taskId 
        ? { ...task, status: 'running', lastRun: new Date().toISOString() }
        : task
    ))

    // Simulate task execution
    setTimeout(() => {
      setTasks(prev => prev.map(task => 
        task.id === taskId 
          ? { 
              ...task, 
              status: Math.random() > 0.2 ? 'completed' : 'failed',
              duration: Math.floor(Math.random() * 120) + 30,
              results: { passed: Math.floor(Math.random() * 10), failed: Math.floor(Math.random() * 2), warnings: Math.floor(Math.random() * 3) }
            }
          : task
      ))
    }, 3000)
  }

  const handleStopTask = (taskId: string) => {
    setTasks(prev => prev.map(task => 
      task.id === taskId ? { ...task, status: 'idle' } : task
    ))
  }

  const getStatusIcon = (status: AutomationTask['status']) => {
    switch (status) {
      case 'running':
        return <Play className="h-4 w-4 text-blue-500 animate-pulse" />
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-red-500" />
      case 'idle':
        return <Pause className="h-4 w-4 text-gray-400" />
    }
  }

  const getStatusColor = (status: AutomationTask['status']) => {
    switch (status) {
      case 'running':
        return 'bg-blue-100 text-blue-800'
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      case 'idle':
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getTypeIcon = (type: AutomationTask['type']) => {
    switch (type) {
      case 'web_test':
        return <Globe className="h-5 w-5 text-blue-500" />
      case 'screenshot':
        return <Camera className="h-5 w-5 text-purple-500" />
      case 'form_fill':
        return <Keyboard className="h-5 w-5 text-green-500" />
      case 'navigation':
        return <MousePointer className="h-5 w-5 text-orange-500" />
      case 'api_test':
        return <Code className="h-5 w-5 text-indigo-500" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Automation Center</h1>
          <p className="mt-2 text-gray-600">
            Manage web automation, testing, and monitoring tasks
          </p>
        </div>
        <div className="flex space-x-3 mt-4 sm:mt-0">
          <motion.button
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            onClick={() => setShowCreateModal(true)}
            className="btn-secondary"
            data-testid="create-automation-btn"
          >
            <Plus className="h-4 w-4 mr-2" />
            Create Task
          </motion.button>
          <motion.button
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="btn-primary"
            data-testid="run-all-btn"
          >
            <Play className="h-4 w-4 mr-2" />
            Run All
          </motion.button>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="card">
          <div className="flex items-center">
            <Bot className="h-8 w-8 text-primary-500 mr-3" />
            <div>
              <p className="text-2xl font-semibold text-gray-900">{tasks.length}</p>
              <p className="text-sm text-gray-600">Total Tasks</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <Play className="h-8 w-8 text-blue-500 mr-3" />
            <div>
              <p className="text-2xl font-semibold text-gray-900">
                {tasks.filter(t => t.status === 'running').length}
              </p>
              <p className="text-sm text-gray-600">Running</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-green-500 mr-3" />
            <div>
              <p className="text-2xl font-semibold text-gray-900">
                {tasks.filter(t => t.status === 'completed').length}
              </p>
              <p className="text-sm text-gray-600">Completed</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <AlertCircle className="h-8 w-8 text-red-500 mr-3" />
            <div>
              <p className="text-2xl font-semibold text-gray-900">
                {tasks.filter(t => t.status === 'failed').length}
              </p>
              <p className="text-sm text-gray-600">Failed</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Active Tasks */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Active Tasks</h2>
            <button className="btn-secondary text-sm">
              <Eye className="h-4 w-4 mr-1" />
              View All
            </button>
          </div>
          
          <div className="space-y-3">
            {tasks.map((task, index) => (
              <motion.div
                key={task.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                  selectedTask === task.id ? 'border-primary-300 bg-primary-50' : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => setSelectedTask(task.id)}
                data-testid={task.testId}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3">
                    {getTypeIcon(task.type)}
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">{task.name}</h3>
                      <p className="text-sm text-gray-600 mt-1">{task.description}</p>
                      {task.lastRun && (
                        <div className="flex items-center mt-2 text-xs text-gray-500">
                          <Clock className="h-3 w-3 mr-1" />
                          Last run: {new Date(task.lastRun).toLocaleString()}
                          {task.duration && ` (${task.duration}s)`}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(task.status)}`}>
                      {task.status.toUpperCase()}
                    </span>
                    {getStatusIcon(task.status)}
                  </div>
                </div>
                
                {task.results && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <div className="flex space-x-4 text-sm">
                      <span className="text-green-600">✓ {task.results.passed} passed</span>
                      <span className="text-red-600">✗ {task.results.failed} failed</span>
                      <span className="text-yellow-600">⚠ {task.results.warnings} warnings</span>
                    </div>
                  </div>
                )}
                
                <div className="flex justify-end space-x-2 mt-3">
                  {task.status === 'running' ? (
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleStopTask(task.id)
                      }}
                      className="btn-secondary text-sm"
                      data-testid={`stop-${task.id}`}
                    >
                      <Square className="h-3 w-3 mr-1" />
                      Stop
                    </button>
                  ) : (
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleRunTask(task.id)
                      }}
                      className="btn-primary text-sm"
                      data-testid={`run-${task.id}`}
                    >
                      <Play className="h-3 w-3 mr-1" />
                      Run
                    </button>
                  )}
                  <button
                    onClick={(e) => e.stopPropagation()}
                    className="btn-secondary text-sm"
                  >
                    <Settings className="h-3 w-3" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Automation Scripts */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Automation Scripts</h2>
            <button className="btn-secondary text-sm">
              <Upload className="h-4 w-4 mr-1" />
              Import
            </button>
          </div>
          
          <div className="space-y-3">
            {automationScripts.map((script, index) => (
              <motion.div
                key={script.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className="p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors"
                data-testid={script.testId}
              >
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h3 className="font-medium text-gray-900">{script.name}</h3>
                    <p className="text-sm text-gray-600 mt-1">{script.description}</p>
                  </div>
                  <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded-full">
                    {script.category}
                  </span>
                </div>
                
                <div className="mb-3">
                  <p className="text-xs text-gray-500 mb-1">Actions:</p>
                  <div className="flex flex-wrap gap-1">
                    {script.actions.slice(0, 2).map(action => (
                      <span
                        key={action}
                        className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-md"
                      >
                        {action}
                      </span>
                    ))}
                    {script.actions.length > 2 && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-md">
                        +{script.actions.length - 2} more
                      </span>
                    )}
                  </div>
                </div>
                
                <div className="flex justify-end space-x-2">
                  <button className="btn-secondary text-sm">
                    <Download className="h-3 w-3 mr-1" />
                    Export
                  </button>
                  <button className="btn-primary text-sm">
                    <Zap className="h-3 w-3 mr-1" />
                    Execute
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Create Task Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center p-4">
            <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setShowCreateModal(false)} />
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="relative bg-white rounded-lg shadow-xl max-w-md w-full p-6"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Create Automation Task</h3>
              <p className="text-gray-600 mb-4">
                Custom automation task creation coming soon! You'll be able to create
                sophisticated web automation workflows with visual scripting.
              </p>
              <div className="space-y-3 mb-4">
                <div className="p-3 border border-gray-200 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <Camera className="h-5 w-5 text-gray-400" />
                    <span className="text-sm text-gray-600">Screenshot Automation</span>
                  </div>
                </div>
                <div className="p-3 border border-gray-200 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <MousePointer className="h-5 w-5 text-gray-400" />
                    <span className="text-sm text-gray-600">UI Interaction Testing</span>
                  </div>
                </div>
                <div className="p-3 border border-gray-200 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <Code className="h-5 w-5 text-gray-400" />
                    <span className="text-sm text-gray-600">API Testing Suite</span>
                  </div>
                </div>
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => setShowCreateModal(false)}
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