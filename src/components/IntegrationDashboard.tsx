import React, { useState, useEffect } from 'react';
import { Card } from './ui/Card';
import { Badge } from './ui/Badge';
import { Button } from './ui/Button';
import { Progress } from './ui/Progress';

interface PlatformStatus {
  name: string;
  status: 'connected' | 'disconnected' | 'connecting';
  lastSync: string;
  features: string[];
}

interface IntegrationStats {
  totalPlatforms: number;
  connectedPlatforms: number;
  syncEvents: number;
  lastSync: string;
}

const IntegrationDashboard: React.FC = () => {
  const [platforms, setPlatforms] = useState<PlatformStatus[]>([
    {
      name: 'Cursor IDE',
      status: 'connected',
      lastSync: '2 minutes ago',
      features: ['Code Sync', 'Project Management', 'AI Assistance']
    },
    {
      name: 'Bolt.diy',
      status: 'connected',
      lastSync: '5 minutes ago',
      features: ['Rapid Prototyping', 'Deployment', 'Testing']
    },
    {
      name: 'Google Firebase',
      status: 'connected',
      lastSync: '1 minute ago',
      features: ['Database', 'Hosting', 'Authentication', 'Analytics']
    },
    {
      name: 'Trae.ai',
      status: 'connected',
      lastSync: '3 minutes ago',
      features: ['AI Code Analysis', 'Suggestions', 'Quality Metrics']
    }
  ]);

  const [stats, setStats] = useState<IntegrationStats>({
    totalPlatforms: 4,
    connectedPlatforms: 4,
    syncEvents: 127,
    lastSync: '1 minute ago'
  });

  const [isLoading, setIsLoading] = useState(false);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected':
        return 'default';
      case 'connecting':
        return 'outline';
      case 'disconnected':
        return 'destructive';
      default:
        return 'secondary';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected':
        return '✅';
      case 'connecting':
        return '🔄';
      case 'disconnected':
        return '❌';
      default:
        return '⚪';
    }
  };

  const handleSyncAll = async () => {
    setIsLoading(true);
    // Simulate sync process
    setTimeout(() => {
      setStats(prev => ({
        ...prev,
        syncEvents: prev.syncEvents + 1,
        lastSync: 'Just now'
      }));
      setIsLoading(false);
    }, 2000);
  };

  const connectionRate = (stats.connectedPlatforms / stats.totalPlatforms) * 100;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Integration Hub
          </h1>
          <p className="text-gray-600 mt-2">
            Unified development workflow across 4 platforms
          </p>
        </div>
        <Button
          onClick={handleSyncAll}
          variant="primary"
          disabled={isLoading}
        >
          {isLoading ? '🔄 Syncing...' : '🔄 Sync All'}
        </Button>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="p-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">
              {stats.connectedPlatforms}/{stats.totalPlatforms}
            </div>
            <div className="text-sm text-gray-600 mt-1">
              Connected Platforms
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">
              {Math.round(connectionRate)}%
            </div>
            <div className="text-sm text-gray-600 mt-1">
              Connection Rate
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">
              {stats.syncEvents}
            </div>
            <div className="text-sm text-gray-600 mt-1">
              Sync Events
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-orange-600">
              {stats.lastSync}
            </div>
            <div className="text-sm text-gray-600 mt-1">
              Last Sync
            </div>
          </div>
        </Card>
      </div>

      {/* Connection Progress */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">
          Overall Connection Health
        </h3>
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>Connection Stability</span>
            <span>{Math.round(connectionRate)}%</span>
          </div>
          <Progress value={connectionRate} max={100} />
        </div>
      </Card>

      {/* Platform Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {platforms.map((platform, index) => (
          <Card key={index} className="p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">
                  {getStatusIcon(platform.status)}
                </span>
                <div>
                  <h3 className="font-semibold text-lg">
                    {platform.name}
                  </h3>
                  <p className="text-sm text-gray-600">
                    Last sync: {platform.lastSync}
                  </p>
                </div>
              </div>
              <Badge variant={getStatusColor(platform.status)}>
                {platform.status}
              </Badge>
            </div>

            <div className="space-y-2">
              <h4 className="font-medium text-sm text-gray-700">
                Active Features:
              </h4>
              <div className="flex flex-wrap gap-2">
                {platform.features.map((feature, featureIndex) => (
                  <Badge
                    key={featureIndex}
                    variant="secondary"
                    className="text-xs"
                  >
                    {feature}
                  </Badge>
                ))}
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex space-x-2">
                <Button
                  variant="secondary"
                  className="flex-1 text-sm"
                >
                  Configure
                </Button>
                <Button
                  variant="primary"
                  className="flex-1 text-sm"
                >
                  Sync Now
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Recent Activity */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
        <div className="space-y-3">
          <div className="flex items-center space-x-3 text-sm">
            <span className="text-green-500">✅</span>
            <span className="text-gray-600">2 minutes ago</span>
            <span>Firebase database synchronized successfully</span>
          </div>
          <div className="flex items-center space-x-3 text-sm">
            <span className="text-blue-500">🔄</span>
            <span className="text-gray-600">3 minutes ago</span>
            <span>Trae.ai code analysis completed</span>
          </div>
          <div className="flex items-center space-x-3 text-sm">
            <span className="text-purple-500">🚀</span>
            <span className="text-gray-600">5 minutes ago</span>
            <span>Bolt.diy prototype deployment successful</span>
          </div>
          <div className="flex items-center space-x-3 text-sm">
            <span className="text-orange-500">📝</span>
            <span className="text-gray-600">7 minutes ago</span>
            <span>Cursor IDE project files synchronized</span>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default IntegrationDashboard;