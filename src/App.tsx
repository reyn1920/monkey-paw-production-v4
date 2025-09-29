import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import AICEODashboard from './components/AICEODashboard';
import IntegrationDashboard from './components/IntegrationDashboard';

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/ai-ceo" element={<AICEODashboard />} />
        <Route path="/integrations" element={<IntegrationDashboard />} />
      </Routes>
    </Layout>
  );
}

export default App;