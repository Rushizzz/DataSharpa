import React, { useState } from 'react';
import { Terminal, Copy, Loader2 } from 'lucide-react';
import { apiService } from '../services/api';

const ShellGenerator = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await apiService.generateShellCommand(query);
      setResult(response);
    } catch (error) {
      console.error('Shell generation error:', error);
      setResult({
        error: 'Failed to generate shell command. Please check if the API is running.',
      });
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Shell Command Generator</h1>
        <p className="mt-2 text-gray-600">
          Generate optimized bash commands for log processing and analysis
        </p>
      </div>

      {/* Query Form */}
      <div className="bg-white rounded-lg shadow p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              What do you want to do?
            </label>
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., Count unique error types in my log file"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              rows="3"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-600 text-white py-3 px-6 rounded-lg hover:bg-primary-700 transition-colors flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                <span>Generating...</span>
              </>
            ) : (
              <>
                <Terminal className="h-5 w-5" />
                <span>Generate Command</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Results */}
      {result && (
        <div className="bg-white rounded-lg shadow p-6 space-y-6">
          {result.error ? (
            <div className="text-red-600">
              <p className="font-semibold">Error</p>
              <p>{result.error}</p>
            </div>
          ) : (
            <>
              <div>
                <div className="flex justify-between items-center mb-2">
                  <h3 className="text-lg font-semibold text-gray-900">Generated Command</h3>
                  <button
                    onClick={() => copyToClipboard(result.command)}
                    className="text-primary-600 hover:text-primary-700 flex items-center space-x-1"
                  >
                    <Copy className="h-4 w-4" />
                    <span className="text-sm">Copy</span>
                  </button>
                </div>
                <div className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                  {result.command}
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Explanation</h3>
                <div className="prose max-w-none bg-gray-50 p-4 rounded-lg">
                  <pre className="whitespace-pre-wrap text-gray-800 text-sm">{result.explanation}</pre>
                </div>
              </div>

              {result.examples && result.examples.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Examples</h3>
                  <div className="space-y-3">
                    {result.examples.map((example, index) => (
                      <div key={index} className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm font-medium text-gray-700 mb-2">
                          {example.description}
                        </p>
                        <div className="bg-gray-900 text-green-400 p-3 rounded font-mono text-xs overflow-x-auto">
                          {example.command}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}

      {/* Common Tasks */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Common Tasks</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            'Count all errors in log file',
            'Extract unique error types',
            'Filter logs by time range',
            'Find top 10 most frequent errors',
            'Extract specific field from CSV',
            'Search for pattern in logs',
          ].map((task, index) => (
            <button
              key={index}
              onClick={() => setQuery(task)}
              className="text-left p-3 bg-white rounded-lg hover:bg-primary-50 hover:border-primary-300 border border-gray-200 transition-colors"
            >
              <p className="text-sm text-gray-700">{task}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ShellGenerator;
