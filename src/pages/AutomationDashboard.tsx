import { motion } from 'framer-motion';
import {
  Activity,
  AlertCircle,
  AlertTriangle,
  CheckCircle,
  Clock,
  Eye,
  EyeOff,
  FileText,
  Play,
  PlayCircle,
  RefreshCw,
  Server,
  StopCircle,
  TrendingUp,
  Upload,
  Video,
  Zap,
} from 'lucide-react';
import { useEffect, useState } from 'react';

interface HealthStatus {
  service: string;
  status: 'healthy' | 'unhealthy' | 'warning';
  port: number;
  responseTime: number;
  lastCheck: string;
  uptime: number;
}

interface AutomationMetrics {
  totalContentGenerated: number;
  totalPostsPublished: number;
  successRate: number;
  averageProcessingTime: number;
  lastRun: string;
  errors: Array<{
    task: string;
    error: string;
    timestamp: string;
  }>;
}

interface ContentItem {
  id: string;
  topic: string;
  format: string;
  status: 'generated' | 'published' | 'failed';
  createdAt: string;
  wordCount: number;
  filename: string;
}

interface VideoPipelineStatus {
  isRunning: boolean;
  currentStep: string | null;
  progress: number;
  scripts: number;
  videos: number;
  voices: number;
  thumbnails: number;
  errors: string[];
}

interface BusinessSystemStatus {
  incomeStreams: {
    youtube: {
      active: boolean;
      revenue: number;
      subscribers: number;
      views: number;
    };
    newsletter: {
      active: boolean;
      revenue: number;
      subscribers: number;
      opens: number;
    };
    affiliate: {
      active: boolean;
      revenue: number;
      clicks: number;
      conversions: number;
    };
    courses: {
      active: boolean;
      revenue: number;
      students: number;
      sales: number;
    };
    consulting: {
      active: boolean;
      revenue: number;
      clients: number;
      hours: number;
    };
    products: {
      active: boolean;
      revenue: number;
      sales: number;
      inventory: number;
    };
    services: {
      active: boolean;
      revenue: number;
      bookings: number;
      completion: number;
    };
    licensing: {
      active: boolean;
      revenue: number;
      licenses: number;
      downloads: number;
    };
    sponsorships: {
      active: boolean;
      revenue: number;
      deals: number;
      reach: number;
    };
  };
  automationSystems: {
    contentGeneration: {
      status: string;
      lastRun: string | null;
      success: number;
      errors: number;
    };
    videoPipeline: {
      status: string;
      lastRun: string | null;
      success: number;
      errors: number;
    };
    marketingAutomation: {
      status: string;
      lastRun: string | null;
      success: number;
      errors: number;
    };
    analyticsProcessing: {
      status: string;
      lastRun: string | null;
      success: number;
      errors: number;
    };
    avatarGeneration: {
      status: string;
      lastRun: string | null;
      success: number;
      errors: number;
    };
    socialMediaAutomation: {
      status: string;
      lastRun: string | null;
      success: number;
      errors: number;
    };
    emailAutomation: {
      status: string;
      lastRun: string | null;
      success: number;
      errors: number;
    };
    revenueOptimization: {
      status: string;
      lastRun: string | null;
      success: number;
      errors: number;
    };
  };
  metrics: {
    totalRevenue: number;
    monthlyGoal: number;
    dailyTarget: number;
    contentGenerated: number;
    videosPublished: number;
    socialPosts: number;
    emailsSent: number;
    leadsGenerated: number;
    conversions: number;
  };
}

function AutomationDashboard() {
  const [healthStatus, setHealthStatus] = useState<HealthStatus[]>([]);
  const [automationMetrics, setAutomationMetrics] = useState<AutomationMetrics>(
    {
      totalContentGenerated: 0,
      totalPostsPublished: 0,
      successRate: 0,
      averageProcessingTime: 0,
      lastRun: '',
      errors: [],
    }
  );
  const [recentContent, setRecentContent] = useState<ContentItem[]>([]);
  const [isAutomationRunning, setIsAutomationRunning] = useState(false);
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [systemStatus, setSystemStatus] = useState<
    'online' | 'offline' | 'warning'
  >('offline');
  const [videoPipelineStatus, setVideoPipelineStatus] =
    useState<VideoPipelineStatus>({
      isRunning: false,
      currentStep: null,
      progress: 0,
      scripts: 0,
      videos: 0,
      voices: 0,
      thumbnails: 0,
      errors: [],
    });
  const [businessSystemStatus, setBusinessSystemStatus] =
    useState<BusinessSystemStatus>({
      incomeStreams: {
        youtube: { active: true, revenue: 0, subscribers: 0, views: 0 },
        newsletter: { active: true, revenue: 0, subscribers: 0, opens: 0 },
        affiliate: { active: true, revenue: 0, clicks: 0, conversions: 0 },
        courses: { active: true, revenue: 0, students: 0, sales: 0 },
        consulting: { active: true, revenue: 0, clients: 0, hours: 0 },
        products: { active: true, revenue: 0, sales: 0, inventory: 0 },
        services: { active: true, revenue: 0, bookings: 0, completion: 0 },
        licensing: { active: true, revenue: 0, licenses: 0, downloads: 0 },
        sponsorships: { active: true, revenue: 0, deals: 0, reach: 0 },
      },
      automationSystems: {
        contentGeneration: {
          status: 'active',
          lastRun: null,
          success: 0,
          errors: 0,
        },
        videoPipeline: {
          status: 'active',
          lastRun: null,
          success: 0,
          errors: 0,
        },
        marketingAutomation: {
          status: 'active',
          lastRun: null,
          success: 0,
          errors: 0,
        },
        analyticsProcessing: {
          status: 'active',
          lastRun: null,
          success: 0,
          errors: 0,
        },
        avatarGeneration: {
          status: 'active',
          lastRun: null,
          success: 0,
          errors: 0,
        },
        socialMediaAutomation: {
          status: 'active',
          lastRun: null,
          success: 0,
          errors: 0,
        },
        emailAutomation: {
          status: 'active',
          lastRun: null,
          success: 0,
          errors: 0,
        },
        revenueOptimization: {
          status: 'active',
          lastRun: null,
          success: 0,
          errors: 0,
        },
      },
      metrics: {
        totalRevenue: 0,
        monthlyGoal: 5000,
        dailyTarget: 167,
        contentGenerated: 0,
        videosPublished: 0,
        socialPosts: 0,
        emailsSent: 0,
        leadsGenerated: 0,
        conversions: 0,
      },
    });

  // Check health services
  const checkHealthServices = async () => {
    try {
      const services = [
        {
          name: 'Health Service 8000',
          url: 'http://127.0.0.1:8000/api/health',
          port: 8000,
        },
        {
          name: 'Health Service 4000',
          url: 'http://localhost:4000/api/health',
          port: 4000,
        },
      ];

      const healthChecks = await Promise.allSettled(
        services.map(async service => {
          const startTime = Date.now();
          const response = await fetch(service.url);
          const responseTime = Date.now() - startTime;

          if (response.ok) {
            const data = await response.json();
            return {
              service: service.name,
              status: 'healthy' as const,
              port: service.port,
              responseTime,
              lastCheck: new Date().toISOString(),
              uptime: data.uptime || 0,
            };
          } else {
            throw new Error(`HTTP ${response.status}`);
          }
        })
      );

      const results = healthChecks.map((result, index) => {
        if (result.status === 'fulfilled') {
          return result.value;
        } else {
          return {
            service: services[index].name,
            status: 'unhealthy' as const,
            port: services[index].port,
            responseTime: 0,
            lastCheck: new Date().toISOString(),
            uptime: 0,
          };
        }
      });

      setHealthStatus(results);

      // Update overall system status
      const healthyServices = results.filter(
        r => r.status === 'healthy'
      ).length;
      if (healthyServices === results.length) {
        setSystemStatus('online');
      } else if (healthyServices > 0) {
        setSystemStatus('warning');
      } else {
        setSystemStatus('offline');
      }
    } catch (error) {
      console.error('Health check failed:', error);
      setSystemStatus('offline');
    }
  };

  // Get automation metrics
  const getAutomationMetrics = async () => {
    try {
      // In a real implementation, this would fetch from the automation system
      // For now, we'll simulate the data
      setAutomationMetrics({
        totalContentGenerated: 47,
        totalPostsPublished: 23,
        successRate: 0.95,
        averageProcessingTime: 2500,
        lastRun: new Date().toISOString(),
        errors: [
          {
            task: 'contentGeneration',
            error: 'Template not found',
            timestamp: new Date(Date.now() - 3600000).toISOString(),
          },
        ],
      });
    } catch (error) {
      console.error('Failed to get automation metrics:', error);
    }
  };

  // Get recent content
  const getRecentContent = async () => {
    try {
      // Simulate recent content data
      setRecentContent([
        {
          id: '1',
          topic: 'AI Trends 2024',
          format: 'article',
          status: 'published',
          createdAt: new Date(Date.now() - 1800000).toISOString(),
          wordCount: 1250,
          filename: 'article_AI_Trends_2024_2024-01-27T10:30:00.txt',
        },
        {
          id: '2',
          topic: 'Tech Tutorial',
          format: 'youtube_script',
          status: 'generated',
          createdAt: new Date(Date.now() - 3600000).toISOString(),
          wordCount: 850,
          filename: 'youtube_script_Tech_Tutorial_2024-01-27T09:30:00.txt',
        },
        {
          id: '3',
          topic: 'Quick Tip',
          format: 'short_script',
          status: 'published',
          createdAt: new Date(Date.now() - 7200000).toISOString(),
          wordCount: 120,
          filename: 'short_script_Quick_Tip_2024-01-27T08:30:00.txt',
        },
      ]);
    } catch (error) {
      console.error('Failed to get recent content:', error);
    }
  };

  // Get video pipeline status
  const getVideoPipelineStatus = async () => {
    try {
      // In a real implementation, this would fetch from the video pipeline API
      setVideoPipelineStatus({
        isRunning: false,
        currentStep: null,
        progress: 0,
        scripts: 68,
        videos: 68,
        voices: 68,
        thumbnails: 1,
        errors: [],
      });
    } catch (error) {
      console.error('Failed to get video pipeline status:', error);
    }
  };

  // Get business system status
  const getBusinessSystemStatus = async () => {
    try {
      // In a real implementation, this would fetch from the business automation API
      setBusinessSystemStatus({
        incomeStreams: {
          youtube: {
            active: true,
            revenue: 1250,
            subscribers: 5000,
            views: 50000,
          },
          newsletter: {
            active: true,
            revenue: 800,
            subscribers: 2500,
            opens: 15000,
          },
          affiliate: {
            active: true,
            revenue: 600,
            clicks: 2000,
            conversions: 50,
          },
          courses: { active: true, revenue: 2000, students: 100, sales: 25 },
          consulting: { active: true, revenue: 1500, clients: 10, hours: 40 },
          products: { active: true, revenue: 900, sales: 45, inventory: 200 },
          services: {
            active: true,
            revenue: 1200,
            bookings: 15,
            completion: 12,
          },
          licensing: {
            active: true,
            revenue: 400,
            licenses: 20,
            downloads: 500,
          },
          sponsorships: { active: true, revenue: 800, deals: 5, reach: 100000 },
        },
        automationSystems: {
          contentGeneration: {
            status: 'active',
            lastRun: new Date().toISOString(),
            success: 68,
            errors: 2,
          },
          videoPipeline: {
            status: 'active',
            lastRun: new Date().toISOString(),
            success: 68,
            errors: 1,
          },
          marketingAutomation: {
            status: 'active',
            lastRun: new Date().toISOString(),
            success: 45,
            errors: 0,
          },
          analyticsProcessing: {
            status: 'active',
            lastRun: new Date().toISOString(),
            success: 30,
            errors: 1,
          },
          avatarGeneration: {
            status: 'active',
            lastRun: new Date().toISOString(),
            success: 25,
            errors: 0,
          },
          socialMediaAutomation: {
            status: 'active',
            lastRun: new Date().toISOString(),
            success: 120,
            errors: 3,
          },
          emailAutomation: {
            status: 'active',
            lastRun: new Date().toISOString(),
            success: 80,
            errors: 1,
          },
          revenueOptimization: {
            status: 'active',
            lastRun: new Date().toISOString(),
            success: 15,
            errors: 0,
          },
        },
        metrics: {
          totalRevenue: 9450,
          monthlyGoal: 5000,
          dailyTarget: 167,
          contentGenerated: 68,
          videosPublished: 68,
          socialPosts: 120,
          emailsSent: 80,
          leadsGenerated: 500,
          conversions: 50,
        },
      });
    } catch (error) {
      console.error('Failed to get business system status:', error);
    }
  };

  // Start automation
  const startAutomation = async () => {
    try {
      setIsAutomationRunning(true);
      // In a real implementation, this would call the automation API
      console.log('Starting automation system...');
    } catch (error) {
      console.error('Failed to start automation:', error);
      setIsAutomationRunning(false);
    }
  };

  // Stop automation
  const stopAutomation = async () => {
    try {
      setIsAutomationRunning(false);
      // In a real implementation, this would call the automation API
      console.log('Stopping automation system...');
    } catch (error) {
      console.error('Failed to stop automation:', error);
    }
  };

  // Start monitoring
  const startMonitoring = async () => {
    try {
      setIsMonitoring(true);
      // In a real implementation, this would start the monitoring system
      console.log('Starting monitoring system...');
    } catch (error) {
      console.error('Failed to start monitoring:', error);
      setIsMonitoring(false);
    }
  };

  // Stop monitoring
  const stopMonitoring = async () => {
    try {
      setIsMonitoring(false);
      // In a real implementation, this would stop the monitoring system
      console.log('Stopping monitoring system...');
    } catch (error) {
      console.error('Failed to stop monitoring:', error);
    }
  };

  // Generate content
  const generateContent = async (topic: string, format: string) => {
    try {
      // In a real implementation, this would call the content generation API
      console.log(`Generating ${format} content for: ${topic}`);

      // Simulate content generation
      const newContent: ContentItem = {
        id: Date.now().toString(),
        topic,
        format,
        status: 'generated',
        createdAt: new Date().toISOString(),
        wordCount: Math.floor(Math.random() * 1000) + 500,
        filename: `${format}_${topic.replace(/\s+/g, '_')}_${Date.now()}.txt`,
      };

      setRecentContent(prev => [newContent, ...prev.slice(0, 9)]);
    } catch (error) {
      console.error('Failed to generate content:', error);
    }
  };

  // Start video pipeline
  const startVideoPipeline = async () => {
    try {
      setVideoPipelineStatus(prev => ({
        ...prev,
        isRunning: true,
        currentStep: 'Initializing',
      }));
      // In a real implementation, this would call the video pipeline API
      console.log('Starting video pipeline...');

      // Simulate video pipeline progress
      const steps = [
        'Scanning Assets',
        'Generating Voice',
        'Creating Video',
        'Generating Thumbnail',
        'Creating Captions',
        'Packaging',
      ];
      let progress = 0;

      for (const step of steps) {
        setVideoPipelineStatus(prev => ({
          ...prev,
          currentStep: step,
          progress,
        }));
        await new Promise(resolve => setTimeout(resolve, 1000));
        progress += 16.67;
      }

      setVideoPipelineStatus(prev => ({
        ...prev,
        isRunning: false,
        currentStep: 'Complete',
        progress: 100,
      }));
    } catch (error) {
      console.error('Failed to start video pipeline:', error);
      setVideoPipelineStatus(prev => ({
        ...prev,
        isRunning: false,
        errors: [...prev.errors, error.message],
      }));
    }
  };

  // Stop video pipeline
  const stopVideoPipeline = async () => {
    try {
      setVideoPipelineStatus(prev => ({
        ...prev,
        isRunning: false,
        currentStep: null,
        progress: 0,
      }));
      console.log('Stopping video pipeline...');
    } catch (error) {
      console.error('Failed to stop video pipeline:', error);
    }
  };

  // Run verification
  const runVerification = async () => {
    try {
      // In a real implementation, this would call the verification system
      console.log('Running system verification...');
      await checkHealthServices();
    } catch (error) {
      console.error('Verification failed:', error);
    }
  };

  useEffect(() => {
    // Initial load
    checkHealthServices();
    getAutomationMetrics();
    getRecentContent();
    getVideoPipelineStatus();
    getBusinessSystemStatus();

    // Set up auto-refresh
    const interval = setInterval(() => {
      checkHealthServices();
      getAutomationMetrics();
      getVideoPipelineStatus();
      getBusinessSystemStatus();
    }, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
      case 'online':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'warning':
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
      case 'unhealthy':
      case 'offline':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
      case 'online':
        return 'bg-green-100 text-green-800';
      case 'warning':
        return 'bg-yellow-100 text-yellow-800';
      case 'unhealthy':
      case 'offline':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Automation Dashboard
            </h1>
            <p className="mt-2 text-gray-600">
              Monitor and control your content generation and automation systems
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <div
              className={`flex items-center px-3 py-2 rounded-full ${getStatusColor(
                systemStatus
              )}`}
            >
              {getStatusIcon(systemStatus)}
              <span className="ml-2 font-medium">
                {systemStatus.toUpperCase()}
              </span>
            </div>
            <button
              onClick={runVerification}
              className="btn-secondary flex items-center"
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Verify System
            </button>
          </div>
        </div>
      </div>

      {/* System Status */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">System Health</h2>
          <button
            onClick={checkHealthServices}
            className="btn-secondary flex items-center"
          >
            <Activity className="h-4 w-4 mr-2" />
            Refresh
          </button>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {healthStatus.map((service, index) => (
            <motion.div
              key={service.service}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * index }}
              className="p-4 bg-gray-50 rounded-lg border border-gray-200"
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <Server className="h-5 w-5 text-blue-500" />
                  <div>
                    <h3 className="font-medium text-gray-900">
                      {service.service}
                    </h3>
                    <p className="text-sm text-gray-500">
                      Port: {service.port}
                    </p>
                  </div>
                </div>
                {getStatusIcon(service.status)}
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Response Time:</span>
                  <p className="font-medium">{service.responseTime}ms</p>
                </div>
                <div>
                  <span className="text-gray-500">Uptime:</span>
                  <p className="font-medium">
                    {Math.floor(service.uptime / 60)}m
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Automation Controls */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="card"
      >
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Automation Controls
        </h2>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <button
            onClick={isAutomationRunning ? stopAutomation : startAutomation}
            className={`p-4 rounded-lg border-2 transition-colors ${
              isAutomationRunning
                ? 'border-red-200 bg-red-50 hover:bg-red-100'
                : 'border-green-200 bg-green-50 hover:bg-green-100'
            }`}
          >
            <div className="flex items-center justify-center mb-2">
              {isAutomationRunning ? (
                <StopCircle className="h-8 w-8 text-red-600" />
              ) : (
                <PlayCircle className="h-8 w-8 text-green-600" />
              )}
            </div>
            <h3 className="font-medium text-gray-900">
              {isAutomationRunning ? 'Stop Automation' : 'Start Automation'}
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              {isAutomationRunning
                ? 'Stop content generation'
                : 'Start content generation'}
            </p>
          </button>

          <button
            onClick={isMonitoring ? stopMonitoring : startMonitoring}
            className={`p-4 rounded-lg border-2 transition-colors ${
              isMonitoring
                ? 'border-blue-200 bg-blue-50 hover:bg-blue-100'
                : 'border-gray-200 bg-gray-50 hover:bg-gray-100'
            }`}
          >
            <div className="flex items-center justify-center mb-2">
              {isMonitoring ? (
                <Eye className="h-8 w-8 text-blue-600" />
              ) : (
                <EyeOff className="h-8 w-8 text-gray-600" />
              )}
            </div>
            <h3 className="font-medium text-gray-900">
              {isMonitoring ? 'Stop Monitoring' : 'Start Monitoring'}
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              {isMonitoring
                ? 'Stop system monitoring'
                : 'Start system monitoring'}
            </p>
          </button>

          <button
            onClick={() => generateContent('AI Trends', 'article')}
            className="p-4 rounded-lg border-2 border-purple-200 bg-purple-50 hover:bg-purple-100 transition-colors"
          >
            <div className="flex items-center justify-center mb-2">
              <FileText className="h-8 w-8 text-purple-600" />
            </div>
            <h3 className="font-medium text-gray-900">Generate Article</h3>
            <p className="text-sm text-gray-600 mt-1">
              Create new article content
            </p>
          </button>

          <button
            onClick={() => generateContent('Tech Tutorial', 'youtube_script')}
            className="p-4 rounded-lg border-2 border-orange-200 bg-orange-50 hover:bg-orange-100 transition-colors"
          >
            <div className="flex items-center justify-center mb-2">
              <Zap className="h-8 w-8 text-orange-600" />
            </div>
            <h3 className="font-medium text-gray-900">Generate Script</h3>
            <p className="text-sm text-gray-600 mt-1">Create YouTube script</p>
          </button>
        </div>
      </motion.div>

      {/* Video Pipeline Controls */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="card"
      >
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Video Pipeline Controls
        </h2>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <button
            onClick={
              videoPipelineStatus.isRunning
                ? stopVideoPipeline
                : startVideoPipeline
            }
            className={`p-4 rounded-lg border-2 transition-colors ${
              videoPipelineStatus.isRunning
                ? 'border-red-200 bg-red-50 hover:bg-red-100'
                : 'border-blue-200 bg-blue-50 hover:bg-blue-100'
            }`}
          >
            <div className="flex items-center justify-center mb-2">
              {videoPipelineStatus.isRunning ? (
                <StopCircle className="h-8 w-8 text-red-600" />
              ) : (
                <Video className="h-8 w-8 text-blue-600" />
              )}
            </div>
            <h3 className="font-medium text-gray-900">
              {videoPipelineStatus.isRunning
                ? 'Stop Pipeline'
                : 'Start Pipeline'}
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              {videoPipelineStatus.isRunning
                ? 'Stop video processing'
                : 'Start video processing'}
            </p>
          </button>

          <div className="p-4 rounded-lg border-2 border-gray-200 bg-gray-50">
            <div className="flex items-center justify-center mb-2">
              <FileText className="h-8 w-8 text-gray-600" />
            </div>
            <h3 className="font-medium text-gray-900">Scripts</h3>
            <p className="text-2xl font-bold text-gray-900">
              {videoPipelineStatus.scripts}
            </p>
            <p className="text-sm text-gray-600 mt-1">Ready for processing</p>
          </div>

          <div className="p-4 rounded-lg border-2 border-gray-200 bg-gray-50">
            <div className="flex items-center justify-center mb-2">
              <Video className="h-8 w-8 text-gray-600" />
            </div>
            <h3 className="font-medium text-gray-900">Videos</h3>
            <p className="text-2xl font-bold text-gray-900">
              {videoPipelineStatus.videos}
            </p>
            <p className="text-sm text-gray-600 mt-1">Generated videos</p>
          </div>

          <div className="p-4 rounded-lg border-2 border-gray-200 bg-gray-50">
            <div className="flex items-center justify-center mb-2">
              <Play className="h-8 w-8 text-gray-600" />
            </div>
            <h3 className="font-medium text-gray-900">Voices</h3>
            <p className="text-2xl font-bold text-gray-900">
              {videoPipelineStatus.voices}
            </p>
            <p className="text-sm text-gray-600 mt-1">Voice files</p>
          </div>
        </div>

        {/* Video Pipeline Progress */}
        {videoPipelineStatus.isRunning && (
          <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-medium text-blue-900">
                Video Pipeline Progress
              </h3>
              <span className="text-sm text-blue-700">
                {Math.round(videoPipelineStatus.progress)}%
              </span>
            </div>
            <div className="w-full bg-blue-200 rounded-full h-2 mb-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${videoPipelineStatus.progress}%` }}
              ></div>
            </div>
            {videoPipelineStatus.currentStep && (
              <p className="text-sm text-blue-700">
                Current Step: {videoPipelineStatus.currentStep}
              </p>
            )}
          </div>
        )}
      </motion.div>

      {/* Business System Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="card"
      >
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          🏢 Complete Business System
        </h2>

        {/* Revenue Overview */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4 mb-6">
          <div className="p-4 bg-green-50 rounded-lg border border-green-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-green-600">
                  Total Revenue
                </p>
                <p className="text-2xl font-bold text-green-900">
                  ${businessSystemStatus.metrics.totalRevenue.toLocaleString()}
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-green-600" />
            </div>
            <p className="text-xs text-green-700 mt-1">
              Goal: ${businessSystemStatus.metrics.monthlyGoal.toLocaleString()}
              /month
            </p>
          </div>

          <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-blue-600">
                  Income Streams
                </p>
                <p className="text-2xl font-bold text-blue-900">
                  {Object.keys(businessSystemStatus.incomeStreams).length}
                </p>
              </div>
              <Zap className="h-8 w-8 text-blue-600" />
            </div>
            <p className="text-xs text-blue-700 mt-1">All systems active</p>
          </div>

          <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-purple-600">
                  Automation Systems
                </p>
                <p className="text-2xl font-bold text-purple-900">
                  {Object.keys(businessSystemStatus.automationSystems).length}
                </p>
              </div>
              <Activity className="h-8 w-8 text-purple-600" />
            </div>
            <p className="text-xs text-purple-700 mt-1">All systems running</p>
          </div>

          <div className="p-4 bg-orange-50 rounded-lg border border-orange-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-orange-600">
                  Content Generated
                </p>
                <p className="text-2xl font-bold text-orange-900">
                  {businessSystemStatus.metrics.contentGenerated}
                </p>
              </div>
              <FileText className="h-8 w-8 text-orange-600" />
            </div>
            <p className="text-xs text-orange-700 mt-1">
              Videos: {businessSystemStatus.metrics.videosPublished}
            </p>
          </div>
        </div>

        {/* Income Streams */}
        <div className="mb-6">
          <h3 className="text-md font-semibold text-gray-900 mb-3">
            💰 Income Streams
          </h3>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {Object.entries(businessSystemStatus.incomeStreams).map(
              ([stream, data]) => (
                <div
                  key={stream}
                  className="p-3 bg-gray-50 rounded-lg border border-gray-200"
                >
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-gray-900 capitalize">
                      {stream}
                    </h4>
                    <div
                      className={`w-2 h-2 rounded-full ${
                        data.active ? 'bg-green-500' : 'bg-red-500'
                      }`}
                    ></div>
                  </div>
                  <p className="text-lg font-bold text-gray-900">
                    ${data.revenue.toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-600">
                    {stream === 'youtube' &&
                      `${data.subscribers.toLocaleString()} subs`}
                    {stream === 'newsletter' &&
                      `${data.subscribers.toLocaleString()} subs`}
                    {stream === 'affiliate' &&
                      `${data.conversions} conversions`}
                    {stream === 'courses' && `${data.students} students`}
                    {stream === 'consulting' && `${data.clients} clients`}
                    {stream === 'products' && `${data.sales} sales`}
                    {stream === 'services' && `${data.bookings} bookings`}
                    {stream === 'licensing' && `${data.licenses} licenses`}
                    {stream === 'sponsorships' && `${data.deals} deals`}
                  </p>
                </div>
              )
            )}
          </div>
        </div>

        {/* Automation Systems */}
        <div>
          <h3 className="text-md font-semibold text-gray-900 mb-3">
            🤖 Automation Systems
          </h3>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {Object.entries(businessSystemStatus.automationSystems).map(
              ([system, data]) => (
                <div
                  key={system}
                  className="p-3 bg-gray-50 rounded-lg border border-gray-200"
                >
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-gray-900 capitalize">
                      {system.replace(/([A-Z])/g, ' $1').trim()}
                    </h4>
                    <div
                      className={`w-2 h-2 rounded-full ${
                        data.status === 'active' ? 'bg-green-500' : 'bg-red-500'
                      }`}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-600">
                    Success: {data.success}
                  </p>
                  <p className="text-xs text-gray-500">
                    {data.errors > 0 ? `${data.errors} errors` : 'No errors'}
                  </p>
                </div>
              )
            )}
          </div>
        </div>
      </motion.div>

      {/* Metrics */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <FileText className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">
                Content Generated
              </p>
              <p className="text-2xl font-semibold text-gray-900">
                {automationMetrics.totalContentGenerated}
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
              <Upload className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">
                Posts Published
              </p>
              <p className="text-2xl font-semibold text-gray-900">
                {automationMetrics.totalPostsPublished}
              </p>
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
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Success Rate</p>
              <p className="text-2xl font-semibold text-gray-900">
                {(automationMetrics.successRate * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="card"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Clock className="h-8 w-8 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">
                Avg. Processing
              </p>
              <p className="text-2xl font-semibold text-gray-900">
                {(automationMetrics.averageProcessingTime / 1000).toFixed(1)}s
              </p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Recent Content */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="card"
      >
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Recent Content
        </h2>
        <div className="space-y-3">
          {recentContent.map((content, index) => (
            <motion.div
              key={content.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * index }}
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center space-x-3">
                <div className="flex-shrink-0">
                  {content.format === 'article' && (
                    <FileText className="h-5 w-5 text-blue-500" />
                  )}
                  {content.format === 'youtube_script' && (
                    <Zap className="h-5 w-5 text-orange-500" />
                  )}
                  {content.format === 'short_script' && (
                    <Play className="h-5 w-5 text-purple-500" />
                  )}
                </div>
                <div>
                  <p className="font-medium text-gray-900">{content.topic}</p>
                  <p className="text-sm text-gray-500">
                    {content.format} • {content.wordCount} words
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <span
                  className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(
                    content.status
                  )}`}
                >
                  {content.status.toUpperCase()}
                </span>
                <div className="text-xs text-gray-500">
                  {new Date(content.createdAt).toLocaleTimeString()}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Errors */}
      {automationMetrics.errors.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="card"
        >
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Recent Errors
          </h2>
          <div className="space-y-3">
            {automationMetrics.errors.map((error, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className="flex items-center space-x-3 p-3 bg-red-50 rounded-lg border border-red-200"
              >
                <AlertCircle className="h-5 w-5 text-red-500" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-red-900">
                    {error.task}
                  </p>
                  <p className="text-xs text-red-700">{error.error}</p>
                </div>
                <div className="text-xs text-red-500">
                  {new Date(error.timestamp).toLocaleTimeString()}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}

export default AutomationDashboard;
