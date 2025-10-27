import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const jobAPI = {
  // Health check
  health: async () => {
    const response = await api.get('/health')
    return response.data
  },

  // Create new indexing job
  startJob: async (imageFolder, options = {}) => {
    const response = await api.post('/jobs/start', {
      image_folder: imageFolder,
      options: {
        batch_size: options.batchSize || 100,
        image_formats: options.imageFormats || ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'],
        recursive: options.recursive !== undefined ? options.recursive : true,
        skip_existing: options.skipExisting !== undefined ? options.skipExisting : true,
        extract_metadata: options.extractMetadata !== undefined ? options.extractMetadata : true,
      },
    })
    return response.data
  },

  // Get all jobs
  listJobs: async (status = null, limit = 50, offset = 0) => {
    const params = { limit, offset }
    if (status) params.status = status
    const response = await api.get('/jobs', { params })
    return response.data
  },

  // Get specific job status
  getJobStatus: async (jobId) => {
    const response = await api.get(`/jobs/${jobId}/status`)
    return response.data
  },

  // Pause job
  pauseJob: async (jobId) => {
    const response = await api.post(`/jobs/${jobId}/pause`)
    return response.data
  },

  // Resume job
  resumeJob: async (jobId) => {
    const response = await api.post(`/jobs/${jobId}/resume`)
    return response.data
  },

  // Cancel job
  cancelJob: async (jobId) => {
    const response = await api.post(`/jobs/${jobId}/cancel`)
    return response.data
  },

  // Get job logs
  getJobLogs: async (jobId, tail = null) => {
    const params = tail ? { tail } : {}
    const response = await api.get(`/jobs/${jobId}/logs`, { params })
    return response.data
  },

  // Get job history
  getJobHistory: async (jobId) => {
    const response = await api.get(`/jobs/${jobId}/history`)
    return response.data
  },

  // Get all job history
  getAllHistory: async () => {
    const response = await api.get('/jobs/history')
    return response.data
  },
}

export default api
