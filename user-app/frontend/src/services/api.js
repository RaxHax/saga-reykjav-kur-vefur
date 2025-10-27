import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const searchAPI = {
  // Search for images
  search: async (query, limit = 50, minScore = 0.2) => {
    const response = await api.post('/api/search', {
      query,
      limit,
      min_score: minScore,
    })
    return response.data
  },

  // Search with Icelandic support
  searchIcelandic: async (query, limit = 50, minScore = 0.2) => {
    const response = await api.post('/api/search/icelandic', {
      query,
      limit,
      min_score: minScore,
    })
    return response.data
  },

  // Get database stats
  getStats: async () => {
    const response = await api.get('/api/stats')
    return response.data
  },

  // Get image URL
  getImageUrl: (imagePath) => {
    return `${API_BASE_URL}/api/image/${encodeURIComponent(imagePath)}`
  },
}

export default api
