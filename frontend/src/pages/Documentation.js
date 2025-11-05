import React, { useState } from 'react';
import { FileText, Loader2, Download } from 'lucide-react';
import { apiService } from '../services/api';

const Documentation = () => {
  const [pipelineCode, setPipelineCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!pipelineCode.trim()) return;

    setLoading(true);
    try {
      const response = await apiService.generateDocumentation(pipelineCode);
      setResult(response);
    } catch (error) {
      setResult({ error: 'Failed to generate documentation' });
    } finally {
      setLoading(false);
    }
  };

  const downloadDocs = () => {
    const blob = new Blob([result.documentation], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'pipeline-documentation.md';
    a.click();
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Auto-Documentation</h1>
        <p className="mt-2 text-gray-600">Generate markdown documentation from pipeline code</p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Pipeline Code
            </label>
            <textarea
              value={pipelineCode}
              onChange={(e) => setPipelineCode(e.target.value)}
              placeholder="Paste your pipeline or DAG code here..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 font-mono text-sm resize-none"
              rows="12"
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
                <span>Generating...</span>
              </>
            ) : (
              <>
                <FileText className="h-5 w-5" />
                <span>Generate Documentation</span>
              </>
            )}
          </button>
        </form>
      </div>

      {result && !result.error && (
        <div className="bg-white rounded-lg shadow p-6 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold text-gray-900">Generated Documentation</h3>
            <button
              onClick={downloadDocs}
              className="text-primary-600 hover:text-primary-700 flex items-center space-x-1"
            >
              <Download className="h-4 w-4" />
              <span className="text-sm">Download</span>
            </button>
          </div>
          <div className="prose max-w-none bg-gray-50 p-6 rounded-lg overflow-auto max-h-96">
            <pre className="whitespace-pre-wrap text-sm">{result.documentation}</pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default Documentation;
