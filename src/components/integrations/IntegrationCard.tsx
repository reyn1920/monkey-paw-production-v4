import React, { useState } from 'react'
import { IntegrationStatus, SyncResult } from './IntegrationService'

interface IntegrationCardProps {
  id: string
  name: string
  description: string
  icon: string
  status: IntegrationStatus | null
  onConnect: (config: any) => Promise<SyncResult>
  onDisconnect: () => Promise<SyncResult>
  onSync: () => Promise<SyncResult>
  onConfigure: () => void
}

export const IntegrationCard: React.FC<IntegrationCardProps> = ({
  id,
  name,
  description,
  icon,
  status,
  onConnect,
  onDisconnect,
  onSync,
  onConfigure
}) => {
  const [isLoading, setIsLoading] = useState(false)
  const [showConfig, setShowConfig] = useState(false)
  const [config, setConfig] = useState({
    apiKey: '',
    authToken: '',
    projectId: '',
    settings: {}
  })

  const handleConnect = async () => {
    setIsLoading(true)
    try {
      await onConnect(config)
      setShowConfig(false)
    } catch (error) {
      console.error('Connection failed:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDisconnect = async () => {
    setIsLoading(true)
    try {
      await onDisconnect()
    } catch (error) {
      console.error('Disconnection failed:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSync = async () => {
    setIsLoading(true)
    try {
      await onSync()
    } catch (error) {
      console.error('Sync failed:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const getStatusColor = () => {
    if (!status?.connected) return 'text-gray-500'
    switch (status.health) {
      case 'healthy': return 'text-green-500'
      case 'warning': return 'text-yellow-500'
      case 'error': return 'text-red-500'
      default: return 'text-gray-500'
    }
  }

  const getStatusIcon = () => {
    if (!status?.connected) return '○'
    switch (status.health) {
      case 'healthy': return '●'
      case 'warning': return '⚠'
      case 'error': return '●'
      default: return '○'
    }
  }

  const formatLastSync = (timestamp?: string) => {
    if (!timestamp) return 'Never'
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`
    return date.toLocaleDateString()
  }

  return (
    <div className="card p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="text-2xl">{icon}</div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{name}</h3>
            <p className="text-sm text-gray-600">{description}</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className={`text-sm ${getStatusColor()}`}>
            {getStatusIcon()}
          </span>
          <span className="text-xs text-gray-500">
            {status?.connected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      {status?.error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-700">{status.error}</p>
        </div>
      )}

      <div className="space-y-3">
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Last Sync:</span>
          <span className="text-gray-900">{formatLastSync(status?.lastSync)}</span>
        </div>
        
        {status?.version && (
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Version:</span>
            <span className="text-gray-900">{status.version}</span>
          </div>
        )}

        <div className="flex space-x-2 pt-3">
          {status?.connected ? (
            <>
              <button
                onClick={handleSync}
                disabled={isLoading}
                className="flex-1 px-3 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Syncing...' : 'Sync'}
              </button>
              <button
                onClick={onConfigure}
                className="px-3 py-2 bg-gray-100 text-gray-700 text-sm rounded-lg hover:bg-gray-200"
              >
                Configure
              </button>
              <button
                onClick={handleDisconnect}
                disabled={isLoading}
                className="px-3 py-2 bg-red-100 text-red-700 text-sm rounded-lg hover:bg-red-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Disconnect
              </button>
            </>
          ) : (
            <button
              onClick={() => setShowConfig(true)}
              disabled={isLoading}
              className="flex-1 px-3 py-2 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Connect
            </button>
          )}
        </div>
      </div>

      {/* Configuration Modal */}
      {showConfig && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h3 className="text-lg font-semibold mb-4">Connect to {name}</h3>
            
            <div className="space-y-4">
              {id === 'cursor' && (
                <div>
                  <label className="label">Auth Token</label>
                  <input
                    type="password"
                    className="input"
                    placeholder="Enter your Cursor auth token"
                    value={config.authToken}
                    onChange={(e) => setConfig({...config, authToken: e.target.value})}
                  />
                </div>
              )}

              {id === 'bolt-diy' && (
                <>
                  <div>
                    <label className="label">API Key</label>
                    <input
                      type="password"
                      className="input"
                      placeholder="Enter your Bolt.diy API key"
                      value={config.apiKey}
                      onChange={(e) => setConfig({...config, apiKey: e.target.value})}
                    />
                  </div>
                  <div>
                    <label className="label">Project ID</label>
                    <input
                      type="text"
                      className="input"
                      placeholder="Enter your project ID"
                      value={config.projectId}
                      onChange={(e) => setConfig({...config, projectId: e.target.value})}
                    />
                  </div>
                </>
              )}

              {id === 'firebase' && (
                <>
                  <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                    <div className="flex items-center mb-2">
                      <span className="text-blue-600 font-medium">🆓 Free Tier Setup</span>
                    </div>
                    <p className="text-sm text-blue-700 mb-2">
                      Firebase offers generous free tier limits. No paid Google APIs required!
                    </p>
                    <a 
                      href="/FIREBASE_SETUP_GUIDE.md" 
                      target="_blank" 
                      className="text-blue-600 hover:text-blue-800 text-sm underline"
                    >
                      📖 View Complete Setup Guide
                    </a>
                  </div>
                  
                  <div>
                    <label className="label">API Key</label>
                    <input
                      type="password"
                      className="input"
                      placeholder="Enter your Firebase API key"
                      value={config.apiKey}
                      onChange={(e) => setConfig({...config, apiKey: e.target.value})}
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Get this from Firebase Console → Project Settings → Web App Config
                    </p>
                  </div>
                  <div>
                    <label className="label">Project ID</label>
                    <input
                      type="text"
                      className="input"
                      placeholder="Enter your Firebase project ID"
                      value={config.projectId}
                      onChange={(e) => setConfig({...config, projectId: e.target.value})}
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Found in Firebase Console → Project Settings → General
                    </p>
                  </div>
                  
                  <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                    <h4 className="text-green-800 font-medium text-sm mb-2">✅ Free Tier Includes:</h4>
                    <ul className="text-xs text-green-700 space-y-1">
                      <li>• 50,000 monthly active users (Auth)</li>
                      <li>• 1 GiB storage + 50K reads/day (Firestore)</li>
                      <li>• 5 GB storage + 1 GB/day downloads (Storage)</li>
                      <li>• 10 GB storage + 360 MB/day transfer (Hosting)</li>
                    </ul>
                  </div>
                </>
              )}

              {id === 'trae-ai' && (
                <div>
                  <label className="label">Auth Token</label>
                  <input
                    type="password"
                    className="input"
                    placeholder="Enter your Trae.ai auth token"
                    value={config.authToken}
                    onChange={(e) => setConfig({...config, authToken: e.target.value})}
                  />
                </div>
              )}
            </div>

            <div className="flex space-x-3 mt-6">
              <button
                onClick={() => setShowConfig(false)}
                className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
              >
                Cancel
              </button>
              <button
                onClick={handleConnect}
                disabled={isLoading}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Connecting...' : 'Connect'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}