import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Save, 
  RefreshCw, 
  Bell, 
  Shield, 
  Palette, 
  Globe,
  Database,
  Code,
  Monitor,
  Download,
  Upload,
  Trash2
} from 'lucide-react'


interface SettingsSection {
  id: string
  name: string
  icon: React.ElementType
  testId: string
}

const settingsSections: SettingsSection[] = [
  { id: 'general', name: 'General', icon: Monitor, testId: 'settings-general' },
  { id: 'integrations', name: 'Integrations', icon: Globe, testId: 'settings-integrations' },
  { id: 'automation', name: 'Automation', icon: Code, testId: 'settings-automation' },
  { id: 'notifications', name: 'Notifications', icon: Bell, testId: 'settings-notifications' },
  { id: 'security', name: 'Security', icon: Shield, testId: 'settings-security' },
  { id: 'appearance', name: 'Appearance', icon: Palette, testId: 'settings-appearance' },
  { id: 'data', name: 'Data & Storage', icon: Database, testId: 'settings-data' }
]

export default function Settings() {
  const [activeSection, setActiveSection] = useState('general')
  const [settings, setSettings] = useState({
    general: {
      appName: 'StackBuilder Pro',
      autoSave: true,
      checkUpdates: true,
      telemetry: false,
      defaultPort: 3001
    },
    integrations: {
      cursorEnabled: true,
      boltEnabled: true,
      firebaseEnabled: true,
      traeEnabled: false,
      windsurfEnabled: false,
      vscodeEnabled: true,
      autoSync: true,
      syncInterval: 30
    },
    automation: {
      enableWebAutomation: true,
      screenshotQuality: 'high',
      maxConcurrentTasks: 5,
      taskTimeout: 300,
      retryAttempts: 3,
      headlessMode: true
    },
    notifications: {
      taskComplete: true,
      taskFailed: true,
      systemAlerts: true,
      integrationUpdates: false,
      emailNotifications: false,
      pushNotifications: true
    },
    security: {
      requireAuth: false,
      sessionTimeout: 3600,
      encryptData: true,
      auditLogs: true,
      apiKeyRotation: 90
    },
    appearance: {
      theme: 'light',
      primaryColor: 'blue',
      fontSize: 'medium',
      compactMode: false,
      showAnimations: true
    },
    data: {
      autoBackup: true,
      backupInterval: 24,
      retentionDays: 30,
      exportFormat: 'json',
      compressionEnabled: true
    }
  })

  const handleSettingChange = (section: string, key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section as keyof typeof prev],
        [key]: value
      }
    }))
  }

  const handleSaveSettings = () => {
    console.log('Saving settings...', settings)
    // Implementation for saving settings
  }

  const handleResetSettings = () => {
    console.log('Resetting settings...')
    // Implementation for resetting settings
  }

  const handleExportSettings = () => {
    const dataStr = JSON.stringify(settings, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'stackbuilder-settings.json'
    link.click()
  }

  const renderGeneralSettings = () => (
    <div className="space-y-6">
      <div>
        <label className="label">Application Name</label>
        <input
          type="text"
          value={settings.general.appName}
          onChange={(e) => handleSettingChange('general', 'appName', e.target.value)}
          className="input"
          data-testid="app-name-input"
        />
      </div>
      
      <div>
        <label className="label">Default Port</label>
        <input
          type="number"
          value={settings.general.defaultPort}
          onChange={(e) => handleSettingChange('general', 'defaultPort', parseInt(e.target.value))}
          className="input"
          min="1000"
          max="65535"
          data-testid="default-port-input"
        />
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium text-gray-900">Auto-save</p>
            <p className="text-sm text-gray-600">Automatically save changes</p>
          </div>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={settings.general.autoSave}
              onChange={(e) => handleSettingChange('general', 'autoSave', e.target.checked)}
              className="sr-only peer"
              data-testid="auto-save-toggle"
            />
            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
          </label>
        </div>

        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium text-gray-900">Check for Updates</p>
            <p className="text-sm text-gray-600">Automatically check for application updates</p>
          </div>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={settings.general.checkUpdates}
              onChange={(e) => handleSettingChange('general', 'checkUpdates', e.target.checked)}
              className="sr-only peer"
              data-testid="check-updates-toggle"
            />
            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
          </label>
        </div>

        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium text-gray-900">Telemetry</p>
            <p className="text-sm text-gray-600">Share anonymous usage data</p>
          </div>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={settings.general.telemetry}
              onChange={(e) => handleSettingChange('general', 'telemetry', e.target.checked)}
              className="sr-only peer"
              data-testid="telemetry-toggle"
            />
            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
          </label>
        </div>
      </div>
    </div>
  )

  const renderIntegrationsSettings = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {Object.entries({
          cursorEnabled: 'Cursor',
          boltEnabled: 'Bolt.diy',
          firebaseEnabled: 'Firebase',
          traeEnabled: 'Trae.ai',
          windsurfEnabled: 'Windsurf',
          vscodeEnabled: 'VS Code'
        }).map(([key, label]) => (
          <div key={key} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
            <span className="font-medium text-gray-900">{label}</span>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.integrations[key as keyof typeof settings.integrations] as boolean}
                onChange={(e) => handleSettingChange('integrations', key, e.target.checked)}
                className="sr-only peer"
                data-testid={`${key}-toggle`}
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>
        ))}
      </div>

      <div>
        <label className="label">Sync Interval (seconds)</label>
        <input
          type="number"
          value={settings.integrations.syncInterval}
          onChange={(e) => handleSettingChange('integrations', 'syncInterval', parseInt(e.target.value))}
          className="input"
          min="10"
          max="3600"
          data-testid="sync-interval-input"
        />
      </div>

      <div className="flex items-center justify-between">
        <div>
          <p className="font-medium text-gray-900">Auto Sync</p>
          <p className="text-sm text-gray-600">Automatically sync with integrated platforms</p>
        </div>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={settings.integrations.autoSync}
            onChange={(e) => handleSettingChange('integrations', 'autoSync', e.target.checked)}
            className="sr-only peer"
            data-testid="auto-sync-toggle"
          />
          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
        </label>
      </div>
    </div>
  )

  const renderAutomationSettings = () => (
    <div className="space-y-6">
      <div>
        <label className="label">Screenshot Quality</label>
        <select
          value={settings.automation.screenshotQuality}
          onChange={(e) => handleSettingChange('automation', 'screenshotQuality', e.target.value)}
          className="input"
          data-testid="screenshot-quality-select"
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="ultra">Ultra</option>
        </select>
      </div>

      <div>
        <label className="label">Max Concurrent Tasks</label>
        <input
          type="number"
          value={settings.automation.maxConcurrentTasks}
          onChange={(e) => handleSettingChange('automation', 'maxConcurrentTasks', parseInt(e.target.value))}
          className="input"
          min="1"
          max="20"
          data-testid="max-concurrent-tasks-input"
        />
      </div>

      <div>
        <label className="label">Task Timeout (seconds)</label>
        <input
          type="number"
          value={settings.automation.taskTimeout}
          onChange={(e) => handleSettingChange('automation', 'taskTimeout', parseInt(e.target.value))}
          className="input"
          min="30"
          max="3600"
          data-testid="task-timeout-input"
        />
      </div>

      <div className="flex items-center justify-between">
        <div>
          <p className="font-medium text-gray-900">Headless Mode</p>
          <p className="text-sm text-gray-600">Run browser automation in headless mode</p>
        </div>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={settings.automation.headlessMode}
            onChange={(e) => handleSettingChange('automation', 'headlessMode', e.target.checked)}
            className="sr-only peer"
            data-testid="headless-mode-toggle"
          />
          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
        </label>
      </div>
    </div>
  )

  const renderCurrentSection = () => {
    switch (activeSection) {
      case 'general':
        return renderGeneralSettings()
      case 'integrations':
        return renderIntegrationsSettings()
      case 'automation':
        return renderAutomationSettings()
      default:
        return (
          <div className="text-center py-8">
            <p className="text-gray-600">Settings for {activeSection} coming soon!</p>
          </div>
        )
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-4">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="mt-2 text-gray-600">
          Configure your StackBuilder Pro application and integrations
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Settings Navigation */}
        <div className="lg:col-span-1">
          <nav className="space-y-1">
            {settingsSections.map((section) => {
              const Icon = section.icon
              return (
                <button
                  key={section.id}
                  onClick={() => setActiveSection(section.id)}
                  className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                    activeSection === section.id
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
                  }`}
                  data-testid={section.testId}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {section.name}
                </button>
              )
            })}
          </nav>
        </div>

        {/* Settings Content */}
        <div className="lg:col-span-3">
          <motion.div
            key={activeSection}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="card"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">
                {settingsSections.find(s => s.id === activeSection)?.name} Settings
              </h2>
              <div className="flex space-x-2">
                <button
                  onClick={handleResetSettings}
                  className="btn-secondary text-sm"
                  data-testid="reset-settings-btn"
                >
                  <RefreshCw className="h-4 w-4 mr-1" />
                  Reset
                </button>
                <button
                  onClick={handleSaveSettings}
                  className="btn-primary text-sm"
                  data-testid="save-settings-btn"
                >
                  <Save className="h-4 w-4 mr-1" />
                  Save
                </button>
              </div>
            </div>

            {renderCurrentSection()}
          </motion.div>

          {/* Data Management */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="card mt-6"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Management</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <button
                onClick={handleExportSettings}
                className="btn-secondary"
                data-testid="export-settings-btn"
              >
                <Download className="h-4 w-4 mr-2" />
                Export Settings
              </button>
              <button className="btn-secondary" data-testid="import-settings-btn">
                <Upload className="h-4 w-4 mr-2" />
                Import Settings
              </button>
              <button className="btn-secondary text-red-600 hover:bg-red-50" data-testid="clear-data-btn">
                <Trash2 className="h-4 w-4 mr-2" />
                Clear Data
              </button>
            </div>
          </motion.div>

          {/* System Information */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="card mt-6"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4">System Information</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-600">Version</p>
                <p className="font-medium">1.0.0</p>
              </div>
              <div>
                <p className="text-gray-600">Platform</p>
                <p className="font-medium">macOS (M1)</p>
              </div>
              <div>
                <p className="text-gray-600">Node.js</p>
                <p className="font-medium">v18.19.0</p>
              </div>
              <div>
                <p className="text-gray-600">Memory Usage</p>
                <p className="font-medium">2.1 GB / 16 GB</p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}