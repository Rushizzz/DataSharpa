import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Debug endpoint
  debug: async (question, context = null) => {
    const response = await api.post('/debug', { question, context });
    return response.data;
  },

  // Upload logs
  uploadLogs: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/upload-logs', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Generate shell command
  generateShellCommand: async (query, logFormat = null, errorPattern = null) => {
    const response = await api.post('/generate-shell-command', {
      query,
      log_format: logFormat,
      error_pattern: errorPattern,
    });
    return response.data;
  },

  // Optimize resources
  optimizeResources: async (jobHistory, clusterMetrics = null) => {
    const response = await api.post('/optimize-resources', {
      job_history: jobHistory,
      cluster_metrics: clusterMetrics,
    });
    return response.data;
  },

  // Generate documentation
  generateDocumentation: async (pipelineCode, dagCode = null) => {
    const response = await api.post('/generate-documentation', {
      pipeline_code: pipelineCode,
      dag_code: dagCode,
    });
    return response.data;
  },

  // Search logs
  searchLogs: async (query, limit = 5) => {
    const response = await api.get('/search-logs', {
      params: { query, limit },
    });
    return response.data;
  },
};

export default api;
