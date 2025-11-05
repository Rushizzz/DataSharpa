import React, { useState } from 'react';
import { Upload, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import { apiService } from '../services/api';

const LogUpload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setResult(null);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    try {
      const response = await apiService.uploadLogs(file);
      setResult({ success: true, data: response });
      setFile(null);
    } catch (error) {
      console.error('Upload error:', error);
      setResult({
        success: false,
        error: 'Failed to upload logs. Please check if the API is running.',
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Log Upload & Indexing</h1>
        <p className="mt-2 text-gray-600">
          Upload pipeline logs for semantic search and troubleshooting
        </p>
      </div>

      {/* Upload Area */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          
          <div className="space-y-2">
            <label className="cursor-pointer">
              <span className="text-primary-600 hover:text-primary-700 font-medium">
                Choose a file
              </span>
              <input
                type="file"
                onChange={handleFileChange}
                className="hidden"
                accept=".log,.txt"
              />
            </label>
            <p className="text-sm text-gray-500">or drag and drop</p>
            <p className="text-xs text-gray-400">LOG, TXT files up to 10MB</p>
          </div>

          {file && (
            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
              <p className="text-sm font-medium text-gray-700">{file.name}</p>
              <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(2)} KB</p>
            </div>
          )}
        </div>

        {file && (
          <button
            onClick={handleUpload}
            disabled={uploading}
            className="mt-4 w-full bg-primary-600 text-white py-3 px-6 rounded-lg hover:bg-primary-700 transition-colors flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {uploading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                <span>Uploading and Indexing...</span>
              </>
            ) : (
              <>
                <Upload className="h-5 w-5" />
                <span>Upload and Index</span>
              </>
            )}
          </button>
        )}
      </div>

      {/* Result */}
      {result && (
        <div className={`rounded-lg shadow p-6 ${result.success ? 'bg-green-50' : 'bg-red-50'}`}>
          <div className="flex items-start space-x-3">
            {result.success ? (
              <CheckCircle className="h-6 w-6 text-green-600 flex-shrink-0" />
            ) : (
              <XCircle className="h-6 w-6 text-red-600 flex-shrink-0" />
            )}
            <div className="flex-1">
              <h3 className={`font-semibold ${result.success ? 'text-green-900' : 'text-red-900'}`}>
                {result.success ? 'Upload Successful' : 'Upload Failed'}
              </h3>
              {result.success ? (
                <div className="mt-2 text-sm text-green-800">
                  <p>{result.data.message}</p>
                  <p className="mt-1">
                    <span className="font-medium">File:</span> {result.data.filename}
                  </p>
                  <p>
                    <span className="font-medium">Chunks indexed:</span> {result.data.chunks_indexed}
                  </p>
                </div>
              ) : (
                <p className="mt-2 text-sm text-red-800">{result.error}</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Info */}
      <div className="bg-blue-50 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">How it works</h3>
        <ol className="space-y-2 text-gray-700">
          <li className="flex items-start">
            <span className="font-semibold mr-2">1.</span>
            <span>Upload your log files (Spark, Airflow, shell outputs)</span>
          </li>
          <li className="flex items-start">
            <span className="font-semibold mr-2">2.</span>
            <span>Logs are automatically chunked and embedded using NIM</span>
          </li>
          <li className="flex items-start">
            <span className="font-semibold mr-2">3.</span>
            <span>Indexed logs become searchable via semantic search</span>
          </li>
          <li className="flex items-start">
            <span className="font-semibold mr-2">4.</span>
            <span>Use the Debug feature to ask questions about your logs</span>
          </li>
        </ol>
      </div>
    </div>
  );
};

export default LogUpload;
