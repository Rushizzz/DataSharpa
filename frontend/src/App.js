import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Debug from './pages/Debug';
import LogUpload from './pages/LogUpload';
import ShellGenerator from './pages/ShellGenerator';
import ResourceOptimizer from './pages/ResourceOptimizer';
import Documentation from './pages/Documentation';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/debug" element={<Debug />} />
          <Route path="/logs" element={<LogUpload />} />
          <Route path="/shell" element={<ShellGenerator />} />
          <Route path="/optimize" element={<ResourceOptimizer />} />
          <Route path="/docs" element={<Documentation />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
