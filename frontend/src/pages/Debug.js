import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { apiService } from '../services/api';

const Debug = () => {
  const [question, setQuestion] = useState('');
  const [context, setContext] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    try {
      const response = await apiService.debug(question, context || null);
      setResult(response);
    } catch (error) {
      console.error('Debug error:', error);
      setResult({
        error: 'Failed to get debug answer. Please check if the API is running.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Natural Language Debugging</h1>
        <p className="mt-2 text-gray-600">
          Ask questions about your pipeline failures and get contextual answers
        </p>
      </div>

      {/* Query Form */}
      <div className="bg-white rounded-lg shadow p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Question
            </label>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., Why is my Spark job failing on stage 3?"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              rows="3"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Additional Context (Optional)
            </label>
            <textarea
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="e.g., Running on EMR cluster with 10 executors..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              rows="2"
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
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Send className="h-5 w-5" />
                <span>Get Answer</span>
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
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Question</h3>
                <p className="text-gray-700 bg-gray-50 p-4 rounded-lg">{result.question}</p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Answer</h3>
                <div className="prose max-w-none bg-primary-50 p-4 rounded-lg">
                  <pre className="whitespace-pre-wrap text-gray-800">{result.answer}</pre>
                </div>
              </div>

              {result.relevant_logs && result.relevant_logs.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Relevant Log Traces</h3>
                  <div className="space-y-3">
                    {result.relevant_logs.map((log, index) => (
                      <div key={index} className="bg-gray-50 p-4 rounded-lg">
                        <div className="flex justify-between items-start mb-2">
                          <span className="text-sm font-medium text-gray-700">{log.filename}</span>
                          <span className="text-xs text-gray-500">Score: {log.score.toFixed(2)}</span>
                        </div>
                        <pre className="text-xs text-gray-600 whitespace-pre-wrap overflow-x-auto">
                          {log.text}
                        </pre>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}

      {/* Examples */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Example Questions</h3>
        <ul className="space-y-2 text-gray-700">
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>Why is my Spark job failing on stage 3?</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>What does this Airflow DAG error mean?</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>How can I fix the out of memory error in my pipeline?</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>Why is my data quality check failing?</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Debug;
