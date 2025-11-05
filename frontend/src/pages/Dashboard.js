import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Bug, Upload, Terminal, Gauge, FileText, Activity } from 'lucide-react';
import { apiService } from '../services/api';

const Dashboard = () => {
  const [healthStatus, setHealthStatus] = useState(null);

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const status = await apiService.healthCheck();
      setHealthStatus(status);
    } catch (error) {
      setHealthStatus({ status: 'unhealthy' });
    }
  };

  const features = [
    {
      icon: Bug,
      title: 'Natural Language Debugging',
      description: 'Ask questions about pipeline failures and get contextual answers',
      link: '/debug',
      color: 'bg-red-500',
    },
    {
      icon: Upload,
      title: 'Log Embedding & Retrieval',
      description: 'Upload and index pipeline logs for semantic search',
      link: '/logs',
      color: 'bg-blue-500',
    },
    {
      icon: Terminal,
      title: 'Shell Command Generator',
      description: 'Generate optimized bash commands for log processing',
      link: '/shell',
      color: 'bg-green-500',
    },
    {
      icon: Gauge,
      title: 'Resource Optimization',
      description: 'Get Spark configuration recommendations',
      link: '/optimize',
      color: 'bg-yellow-500',
    },
    {
      icon: FileText,
      title: 'Auto-Documentation',
      description: 'Generate markdown docs from pipeline code',
      link: '/docs',
      color: 'bg-purple-500',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Welcome to DataSherpa</h1>
        <p className="mt-2 text-gray-600">
          Your GenAI-powered assistant for debugging, optimizing, and documenting data pipelines
        </p>
      </div>

      {/* Health Status */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center space-x-3">
          <Activity className={`h-6 w-6 ${healthStatus?.status === 'healthy' ? 'text-green-500' : 'text-red-500'}`} />
          <div>
            <h2 className="text-lg font-semibold text-gray-900">System Status</h2>
            <p className="text-sm text-gray-600">
              API is {healthStatus?.status === 'healthy' ? 'healthy and running' : 'unavailable'}
            </p>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <Link
              key={index}
              to={feature.link}
              className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6 group"
            >
              <div className={`${feature.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                <Icon className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 text-sm">
                {feature.description}
              </p>
            </Link>
          );
        })}
      </div>

      {/* Quick Start */}
      <div className="bg-primary-50 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Start</h2>
        <ol className="space-y-3 text-gray-700">
          <li className="flex items-start">
            <span className="font-semibold mr-2">1.</span>
            <span>Upload your pipeline logs using the Log Upload feature</span>
          </li>
          <li className="flex items-start">
            <span className="font-semibold mr-2">2.</span>
            <span>Ask debugging questions in natural language</span>
          </li>
          <li className="flex items-start">
            <span className="font-semibold mr-2">3.</span>
            <span>Generate shell commands for log analysis</span>
          </li>
          <li className="flex items-start">
            <span className="font-semibold mr-2">4.</span>
            <span>Get resource optimization recommendations</span>
          </li>
        </ol>
      </div>
    </div>
  );
};

export default Dashboard;
