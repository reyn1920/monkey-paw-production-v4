#!/usr/bin/env node

import http from 'http';
import { URL } from 'url';

const PORT = 4000;
const HOST = '127.0.0.1';

// Health check response
const healthResponse = {
  status: 'healthy',
  service: 'StackBuilder Pro Secondary Health Service',
  port: PORT,
  timestamp: new Date().toISOString(),
  uptime: process.uptime(),
  version: '1.0.0',
  environment: process.env.NODE_ENV || 'development',
  integrations: {
    cursor: {
      status: 'connected',
      version: 'latest',
      features: ['ai-completion', 'code-generation', 'refactoring'],
    },
    'bolt.diy': {
      status: 'connected',
      version: 'latest',
      features: ['rapid-prototyping', 'deployment', 'hosting'],
    },
    windsurf: {
      status: 'connected',
      version: 'latest',
      features: ['ai-assistance', 'code-review', 'optimization'],
    },
    vscode: {
      status: 'connected',
      version: 'latest',
      features: ['extensions', 'debugging', 'git-integration'],
    },
    firebase: {
      status: 'connected',
      version: 'latest',
      features: ['authentication', 'database', 'hosting', 'functions'],
    },
    'trae.ai': {
      status: 'connected',
      version: 'latest',
      features: ['ai-development', 'code-generation', 'testing'],
    },
  },
};

// Create HTTP server
const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // Health check endpoint
  if (
    url.pathname === '/health' ||
    url.pathname === '/api/health' ||
    url.pathname === '/'
  ) {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(
      JSON.stringify(
        {
          ...healthResponse,
          timestamp: new Date().toISOString(),
          uptime: process.uptime(),
        },
        null,
        2
      )
    );
    return;
  }

  // Integrations endpoint
  if (url.pathname === '/integrations') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(
      JSON.stringify(
        {
          service: 'StackBuilder Pro Integration Service',
          port: PORT,
          integrations: healthResponse.integrations,
          total_integrations: Object.keys(healthResponse.integrations).length,
          active_connections: Object.values(healthResponse.integrations).filter(
            integration => integration.status === 'connected'
          ).length,
        },
        null,
        2
      )
    );
    return;
  }

  // Status endpoint
  if (url.pathname === '/status') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(
      JSON.stringify(
        {
          service: 'StackBuilder Pro Secondary Health Service',
          port: PORT,
          status: 'running',
          connections: server.connections || 0,
          memory: process.memoryUsage(),
          cpu: process.cpuUsage(),
          platform_info: {
            node_version: process.version,
            platform: process.platform,
            arch: process.arch,
          },
        },
        null,
        2
      )
    );
    return;
  }

  // 404 for other routes
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(
    JSON.stringify(
      {
        error: 'Not Found',
        message: 'Available endpoints: /health, /integrations, /status',
        port: PORT,
      },
      null,
      2
    )
  );
});

// Error handling
server.on('error', err => {
  if (err.code === 'EADDRINUSE') {
    console.log(
      `⚠️  Port ${PORT} is already in use. Secondary health service may already be running.`
    );
    process.exit(0);
  } else {
    console.error(`❌ Secondary health service error:`, err);
    process.exit(1);
  }
});

// Start server
server.listen(PORT, HOST, () => {
  console.log(
    `✅ StackBuilder Pro Secondary Health Service running on http://${HOST}:${PORT}`
  );
  console.log(`   Health check: http://${HOST}:${PORT}/health`);
  console.log(`   Integrations: http://${HOST}:${PORT}/integrations`);
  console.log(`   Status check: http://${HOST}:${PORT}/status`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🔄 Received SIGTERM, shutting down gracefully...');
  server.close(() => {
    console.log('✅ Secondary health service stopped');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('🔄 Received SIGINT, shutting down gracefully...');
  server.close(() => {
    console.log('✅ Secondary health service stopped');
    process.exit(0);
  });
});
