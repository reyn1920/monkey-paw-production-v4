import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Progress } from '@/components/ui/Progress';
import { 
  Brain, 
  DollarSign, 
  Video, 
  Users, 
  TrendingUp, 
  Settings,
  Play,
  Pause,
  BarChart3,
  Zap,
  Target,
  Cpu
} from 'lucide-react';

interface BusinessMetrics {
  revenue_streams: Record<string, number>;
  content_performance: Record<string, any>;
  audience_engagement: Record<string, number>;
  automation_efficiency: number;
  system_health: Record<string, boolean>;
  timestamp: string;
}

interface AIDecision {
  decision_id: string;
  category: string;
  action: string;
  reasoning: string;
  expected_outcome: string;
  confidence: number;
  timestamp: string;
}

interface AICEOStatus {
  ai_ceo: {
    name: string;
    version: string;
    uptime: string;
    status: string;
  };
  systems: Record<string, any>;
  metrics: BusinessMetrics;
  recent_decisions: AIDecision[];
  configuration: Record<string, any>;
}

export default function AICEODashboard() {
  const [status, setStatus] = useState<AICEOStatus | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching AI CEO status
    const fetchStatus = async () => {
      setLoading(true);
      // This would connect to the Python AI CEO backend
      const mockStatus: AICEOStatus = {
        ai_ceo: {
          name: "Monkey Paw AI CEO",
          version: "1.0.0",
          uptime: new Date().toISOString(),
          status: "operational"
        },
        systems: {
          content_engine: { status: "active" },
          revenue_optimizer: { status: "active" },
          social_manager: { status: "active" },
          production_pipeline: { status: "active" },
          marketing_automation: { status: "active" },
          api_orchestrator: { status: "active" }
        },
        metrics: {
          revenue_streams: {
            youtube_ads: 18000,
            affiliate_marketing: 15000,
            sponsored_content: 12000,
            product_sales: 5000
          },
          content_performance: {
            views: 1250000,
            engagement_rate: 0.078,
            subscriber_growth: 0.12
          },
          audience_engagement: {
            total_followers: 850000,
            engagement_rate: 0.065
          },
          automation_efficiency: 0.92,
          system_health: {
            content_engine: true,
            revenue_optimizer: true,
            social_manager: true,
            production_pipeline: true
          },
          timestamp: new Date().toISOString()
        },
        recent_decisions: [
          {
            decision_id: "decision_20241201_143022",
            category: "content",
            action: "enhance_content_strategy",
            reasoning: "Content performance below threshold, need better content",
            expected_outcome: "Improve content metrics by 15-25%",
            confidence: 0.85,
            timestamp: new Date().toISOString()
          }
        ],
        configuration: {
          business_objectives: {
            primary_revenue_target: 100000,
            content_output_target: 50,
            audience_growth_target: 0.15
          }
        }
      };
      
      setStatus(mockStatus);
      setIsRunning(true);
      setLoading(false);
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 30000); // Update every 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  const toggleAICEO = async () => {
    setIsRunning(!isRunning);
    // This would start/stop the AI CEO backend
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US').format(num);
  };

  if (loading || !status) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  const totalRevenue = Object.values(status.metrics.revenue_streams).reduce((a, b) => a + b, 0);

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Brain className="h-8 w-8 text-purple-600" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                {status.ai_ceo.name}
              </h1>
              <p className="text-gray-600">v{status.ai_ceo.version}</p>
            </div>
          </div>
          <Badge 
            variant={isRunning ? "default" : "secondary"}
            className={isRunning ? "bg-green-500" : "bg-gray-500"}
          >
            {isRunning ? "OPERATIONAL" : "OFFLINE"}
          </Badge>
        </div>
        
        <Button
          onClick={toggleAICEO}
          variant={isRunning ? "danger" : "primary"}
          className="flex items-center space-x-2"
        >
          {isRunning ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
          <span>{isRunning ? "Stop AI CEO" : "Start AI CEO"}</span>
        </Button>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="text-sm font-medium">Total Revenue</h3>
            <DollarSign className="h-4 w-4 text-gray-500" />
          </div>
          <div>
            <div className="text-2xl font-bold">{formatCurrency(totalRevenue)}</div>
            <p className="text-xs text-gray-500">
              +12% from last month
            </p>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="text-sm font-medium">Content Views</h3>
            <Video className="h-4 w-4 text-gray-500" />
          </div>
          <div>
            <div className="text-2xl font-bold">
              {formatNumber(status.metrics.content_performance.views)}
            </div>
            <p className="text-xs text-gray-500">
              +7.8% engagement rate
            </p>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="text-sm font-medium">Total Followers</h3>
            <Users className="h-4 w-4 text-gray-500" />
          </div>
          <div>
            <div className="text-2xl font-bold">
              {formatNumber(status.metrics.audience_engagement.total_followers)}
            </div>
            <p className="text-xs text-gray-500">
              +12% subscriber growth
            </p>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="text-sm font-medium">Automation</h3>
            <Zap className="h-4 w-4 text-gray-500" />
          </div>
          <div>
            <div className="text-2xl font-bold">
              {Math.round(status.metrics.automation_efficiency * 100)}%
            </div>
            <Progress 
              value={status.metrics.automation_efficiency * 100} 
              className="mt-2"
            />
          </div>
        </Card>
      </div>

      {/* Revenue Breakdown */}
      <Card className="p-6">
        <div className="mb-4">
          <h3 className="text-lg font-semibold flex items-center space-x-2">
            <TrendingUp className="h-5 w-5" />
            <span>Revenue Streams</span>
          </h3>
        </div>
        <div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {Object.entries(status.metrics.revenue_streams).map(([stream, amount]) => (
              <div key={stream} className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-lg font-semibold">{formatCurrency(amount)}</div>
                <div className="text-sm text-gray-600 capitalize">
                  {stream.replace('_', ' ')}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {Math.round((amount / totalRevenue) * 100)}% of total
                </div>
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* System Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <div className="mb-4">
            <h3 className="text-lg font-semibold flex items-center space-x-2">
              <Cpu className="h-5 w-5" />
              <span>System Health</span>
            </h3>
          </div>
          <div>
            <div className="space-y-3">
              {Object.entries(status.systems).map(([system, config]) => (
                <div key={system} className="flex items-center justify-between">
                  <span className="text-sm font-medium capitalize">
                    {system.replace('_', ' ')}
                  </span>
                  <Badge 
                    variant={config.status === 'active' ? 'default' : 'secondary'}
                    className={config.status === 'active' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'}
                  >
                    {config.status}
                  </Badge>
                </div>
              ))}
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="mb-4">
            <h3 className="text-lg font-semibold flex items-center space-x-2">
              <Target className="h-5 w-5" />
              <span>Recent AI Decisions</span>
            </h3>
          </div>
          <div>
            <div className="space-y-4">
              {status.recent_decisions.map((decision) => (
                <div key={decision.decision_id} className="border-l-4 border-purple-500 pl-4">
                  <div className="flex items-center justify-between">
                    <span className="font-medium capitalize">{decision.action.replace('_', ' ')}</span>
                    <Badge variant="outline">
                      {Math.round(decision.confidence * 100)}% confidence
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">{decision.reasoning}</p>
                  <p className="text-xs text-gray-500 mt-1">{decision.expected_outcome}</p>
                </div>
              ))}
            </div>
          </div>
        </Card>
      </div>

      {/* Business Objectives */}
      <Card className="p-6">
        <div className="mb-4">
          <h3 className="text-lg font-semibold flex items-center space-x-2">
            <BarChart3 className="h-5 w-5" />
            <span>Business Objectives Progress</span>
          </h3>
        </div>
        <div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium">Revenue Target</span>
                <span className="text-sm text-gray-600">
                  {formatCurrency(totalRevenue)} / {formatCurrency(status.configuration.business_objectives.primary_revenue_target)}
                </span>
              </div>
              <Progress value={(totalRevenue / status.configuration.business_objectives.primary_revenue_target) * 100} />
            </div>
            
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium">Content Output</span>
                <span className="text-sm text-gray-600">
                  35 / {status.configuration.business_objectives.content_output_target}
                </span>
              </div>
              <Progress value={(35 / status.configuration.business_objectives.content_output_target) * 100} />
            </div>
            
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium">Audience Growth</span>
                <span className="text-sm text-gray-600">
                  12% / {status.configuration.business_objectives.audience_growth_target * 100}%
                </span>
              </div>
              <Progress value={(0.12 / status.configuration.business_objectives.audience_growth_target) * 100} />
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}