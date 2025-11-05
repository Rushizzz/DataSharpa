import React, { useState } from 'react';
import { Gauge, Loader2 } from 'lucide-react';
import { apiService } from '../services/api';

const ResourceOptimizer = () => {
  const [jobHistory, setJobHistory] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!jobHistory.trim()) return;

    setLoading(true);
    try {
      const response = await apiService.optimizeResources(jobHistory);
      setResult(response);
    } catch (error) {
      setResult({ error: 'Failed to get recommendations' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Resource Optimization</h1>
        <p className="mt-2 text-gray-600">Get Spark configuration recommendations</p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job History / Logs
            </label>
            <textarea
              value={jobHistory}
              onChange={(e) => setJobHistory(e.target.value)}
              placeholder="Paste your Spark job history or logs here..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 resize-none"
              rows="8"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-600 text-white py-3 px-6 rounded-lg hover:bg-primary-700 flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Gauge className="h-5 w-5" />
                <span>Get Recommendations</span>
              </>
            )}
          </button>
        </form>
      </div>

      {result && !result.error && (
        <div className="bg-white rounded-lg shadow p-6 space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Analysis</h3>
            <div className="prose max-w-none bg-gray-50 p-4 rounded-lg">
              <pre className="whitespace-pre-wrap text-sm">{result.recommendations.llm_analysis}</pre>
            </div>
          </div>

          {result.recommendations.quick_wins && result.recommendations.quick_wins.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Quick Wins</h3>
              <div className="space-y-3">
                {result.recommendations.quick_wins.map((win, index) => (
                  <div key={index} className="bg-yellow-50 p-4 rounded-lg">
                    <p className="font-medium text-gray-900">{win.issue}</p>
                    <p className="text-sm text-gray-700 mt-1">{win.recommendation}</p>
                    <code className="block mt-2 bg-gray-900 text-green-400 p-2 rounded text-xs">
                      {win.config}
                    </code>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ResourceOptimizer;
