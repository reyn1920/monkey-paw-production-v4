import {
  Activity,
  BarChart3,
  Brain,
  FileText,
  Play,
  Settings,
  Zap,
} from 'lucide-react';
import React from 'react';
import { Link, useLocation } from 'react-router-dom';

interface NavItem {
  name: string;
  href: string;
  icon: React.ElementType;
  description: string;
  badge?: string;
}

const navigation: NavItem[] = [
  {
    name: 'Automation Dashboard',
    href: '/',
    icon: Zap,
    description: 'Content generation and automation controls',
    badge: 'NEW',
  },
  {
    name: 'Platform Dashboard',
    href: '/dashboard',
    icon: BarChart3,
    description: 'Multi-platform integration status',
  },
  {
    name: 'AI Hub',
    href: '/ai-hub',
    icon: Brain,
    description: 'AI collaboration and assistance',
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: Settings,
    description: 'System configuration and preferences',
  },
];

const quickActions = [
  {
    name: 'Generate Content',
    href: '/automation',
    icon: FileText,
    description: 'Create new content',
  },
  {
    name: 'System Health',
    href: '/automation',
    icon: Activity,
    description: 'Check system status',
  },
  {
    name: 'Start Automation',
    href: '/automation',
    icon: Play,
    description: 'Launch automation',
  },
];

function Navigation() {
  const location = useLocation();

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and main navigation */}
          <div className="flex items-center space-x-8">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <Zap className="h-8 w-8 text-primary-600" />
                <span className="ml-2 text-xl font-bold text-gray-900">
                  Monkey Paw v4
                </span>
              </div>
            </div>

            <div className="hidden md:flex space-x-8">
              {navigation.map(item => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`relative flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                      isActive
                        ? 'text-primary-600 bg-primary-50'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                    }`}
                  >
                    <item.icon className="h-4 w-4 mr-2" />
                    {item.name}
                    {item.badge && (
                      <span className="ml-2 px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                        {item.badge}
                      </span>
                    )}
                  </Link>
                );
              })}
            </div>
          </div>

          {/* Quick actions */}
          <div className="flex items-center space-x-4">
            <div className="hidden lg:flex items-center space-x-2">
              {quickActions.map(action => (
                <Link
                  key={action.name}
                  to={action.href}
                  className="flex items-center px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md transition-colors"
                  title={action.description}
                >
                  <action.icon className="h-4 w-4 mr-1" />
                  <span className="hidden xl:inline">{action.name}</span>
                </Link>
              ))}
            </div>

            {/* System status indicator */}
            <div className="flex items-center space-x-2">
              <div className="flex items-center px-3 py-2 text-sm bg-green-100 text-green-800 rounded-full">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                <span className="hidden sm:inline">System Online</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile navigation */}
      <div className="md:hidden">
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          {navigation.map(item => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center px-3 py-2 text-base font-medium rounded-md transition-colors ${
                  isActive
                    ? 'text-primary-600 bg-primary-50'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                <item.icon className="h-5 w-5 mr-3" />
                {item.name}
                {item.badge && (
                  <span className="ml-auto px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                    {item.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}

export default Navigation;
