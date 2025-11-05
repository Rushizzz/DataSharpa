import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  Bug, 
  Upload, 
  Terminal, 
  Gauge, 
  FileText,
  Mountain
} from 'lucide-react';

const Layout = ({ children }) => {
  const location = useLocation();

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/debug', icon: Bug, label: 'Debug' },
    { path: '/logs', icon: Upload, label: 'Upload Logs' },
    { path: '/shell', icon: Terminal, label: 'Shell Generator' },
    { path: '/optimize', icon: Gauge, label: 'Optimize' },
    { path: '/docs', icon: FileText, label: 'Documentation' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <Mountain className="h-8 w-8 text-primary-600" />
              <h1 className="text-2xl font-bold text-gray-900">DataSherpa</h1>
            </div>
            <div className="text-sm text-gray-500">
              GenAI-powered Data Engineering Assistant
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-white shadow-sm min-h-[calc(100vh-73px)]">
          <nav className="p-4 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-primary-50 text-primary-700 font-medium'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8">
          <div className="max-w-6xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
