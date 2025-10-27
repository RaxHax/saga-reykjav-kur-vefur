/**
 * API Service Layer
 * Handles all communication with Flask backend and Indexing service
 */

import axios from 'axios'

// Create axios instances for different services
const flaskAPI = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

const indexingAPI = axios.create({
  baseURL: import.meta.env.VITE_INDEXING_API_BASE_URL || 'http://localhost:8001',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptors for adding auth tokens (future)
const setupInterceptors = (instance) => {
  instance.interceptors.request.use(
    (config) => {
      // Add auth token if available
      const token = localStorage.getItem('auth_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => Promise.reject(error)
  )

  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      // Handle common errors
      if (error.response?.status === 401) {
        // Handle unauthorized
        localStorage.removeItem('auth_token')
      }
      return Promise.reject(error)
    }
  )
}

setupInterceptors(flaskAPI)
setupInterceptors(indexingAPI)

// =============================================================================
// Flask API Endpoints
// =============================================================================

/**
 * Search for images using semantic text query
 * @param {string} query - Search query text
 * @param {Object} options - Search options (limit, minScore, metadata)
 * @returns {Promise} - Search results
 */
export const searchImages = async (query, options = {}) => {
  const { limit = 50, minScore = 0.0, metadata = {} } = options

  const response = await flaskAPI.post('/api/search', {
    query,
    limit,
    min_score: minScore,
    metadata_filter: metadata,
  })

  return response.data
}

/**
 * Get database statistics
 * @returns {Promise} - Database stats
 */
export const getStats = async () => {
  const response = await flaskAPI.get('/api/stats')
  return response.data
}

/**
 * Health check for Flask service
 * @returns {Promise} - Health status
 */
export const checkHealth = async () => {
  const response = await flaskAPI.get('/api/health')
  return response.data
}

/**
 * Get image URL for serving
 * @param {string} imagePath - Path to image
 * @returns {string} - Full image URL
 */
export const getImageUrl = (imagePath) => {
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
  return `${baseURL}/api/image/${encodeURIComponent(imagePath)}`
}

// =============================================================================
// Indexing Service API Endpoints
// =============================================================================

/**
 * Start a new indexing job
 * @param {string} imageFolder - Path to folder containing images
 * @param {Object} options - Indexing options
 * @returns {Promise} - Job details
 */
export const startIndexing = async (imageFolder, options = {}) => {
  const response = await indexingAPI.post('/jobs/start', {
    image_folder: imageFolder,
    ...options,
  })
  return response.data
}

/**
 * Get status of an indexing job
 * @param {string} jobId - Job ID
 * @returns {Promise} - Job status
 */
export const getIndexingStatus = async (jobId) => {
  const response = await indexingAPI.get(`/jobs/${jobId}/status`)
  return response.data
}

/**
 * Get all indexing jobs
 * @param {Object} filters - Filter options (status, limit)
 * @returns {Promise} - List of jobs
 */
export const getIndexingJobs = async (filters = {}) => {
  const response = await indexingAPI.get('/jobs', { params: filters })
  return response.data
}

/**
 * Pause an indexing job
 * @param {string} jobId - Job ID
 * @returns {Promise} - Updated job status
 */
export const pauseIndexing = async (jobId) => {
  const response = await indexingAPI.post(`/jobs/${jobId}/pause`)
  return response.data
}

/**
 * Resume a paused indexing job
 * @param {string} jobId - Job ID
 * @returns {Promise} - Updated job status
 */
export const resumeIndexing = async (jobId) => {
  const response = await indexingAPI.post(`/jobs/${jobId}/resume`)
  return response.data
}

/**
 * Cancel an indexing job
 * @param {string} jobId - Job ID
 * @returns {Promise} - Cancellation confirmation
 */
export const cancelIndexing = async (jobId) => {
  const response = await indexingAPI.post(`/jobs/${jobId}/cancel`)
  return response.data
}

/**
 * Get logs for an indexing job
 * @param {string} jobId - Job ID
 * @param {Object} options - Log options (tail, follow)
 * @returns {Promise} - Job logs
 */
export const getIndexingLogs = async (jobId, options = {}) => {
  const response = await indexingAPI.get(`/jobs/${jobId}/logs`, { params: options })
  return response.data
}

/**
 * Get indexing job history/audit trail
 * @param {Object} filters - Filter options (user, dateRange, status)
 * @returns {Promise} - Job history
 */
export const getJobHistory = async (filters = {}) => {
  const response = await indexingAPI.get('/jobs/history', { params: filters })
  return response.data
}

/**
 * Get indexing service health
 * @returns {Promise} - Health status
 */
export const checkIndexingHealth = async () => {
  const response = await indexingAPI.get('/health')
  return response.data
}

// =============================================================================
// Advanced Search Features
// =============================================================================

/**
 * Hybrid search combining text and metadata
 * @param {Object} searchParams - Combined search parameters
 * @returns {Promise} - Search results
 */
export const hybridSearch = async (searchParams) => {
  const {
    textQuery,
    metadata = {},
    weights = { text: 0.7, metadata: 0.3 },
    limit = 50,
  } = searchParams

  const response = await flaskAPI.post('/api/search/hybrid', {
    text_query: textQuery,
    metadata_filter: metadata,
    weights,
    limit,
  })

  return response.data
}

/**
 * Search with Icelandic text (auto-translation if needed)
 * @param {string} query - Query in Icelandic or English
 * @param {Object} options - Search options
 * @returns {Promise} - Search results
 */
export const icelandicSearch = async (query, options = {}) => {
  const response = await flaskAPI.post('/api/search/icelandic', {
    query,
    ...options,
  })
  return response.data
}

// =============================================================================
// Utility Functions
// =============================================================================

/**
 * Handle API errors with user-friendly messages
 * @param {Error} error - Axios error object
 * @returns {string} - User-friendly error message
 */
export const handleAPIError = (error) => {
  if (error.response) {
    // Server responded with error
    const status = error.response.status
    const message = error.response.data?.message || error.response.data?.error

    if (status === 404) return 'Resource not found'
    if (status === 500) return 'Server error. Please try again later.'
    if (message) return message

    return `Error: ${status}`
  } else if (error.request) {
    // Request made but no response
    return 'Cannot connect to server. Please check your connection.'
  } else {
    // Something else happened
    return error.message || 'An unexpected error occurred'
  }
}

export default {
  // Flask API
  searchImages,
  getStats,
  checkHealth,
  getImageUrl,

  // Indexing Service API
  startIndexing,
  getIndexingStatus,
  getIndexingJobs,
  pauseIndexing,
  resumeIndexing,
  cancelIndexing,
  getIndexingLogs,
  getJobHistory,
  checkIndexingHealth,

  // Advanced Search
  hybridSearch,
  icelandicSearch,

  // Utils
  handleAPIError,
}
