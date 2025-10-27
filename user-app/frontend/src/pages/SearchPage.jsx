import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { searchAPI } from '../services/api'
import ImageGrid from '../components/ImageGrid'
import ImageModal from '../components/ImageModal'
import './SearchPage.css'

function SearchPage() {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState(null)
  const [selectedImage, setSelectedImage] = useState(null)
  const [filters, setFilters] = useState({
    limit: 50,
    minScore: 0.2,
    useIcelandic: true,
  })
  const [showFilters, setShowFilters] = useState(false)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const data = await searchAPI.getStats()
      setStats(data)
    } catch (error) {
      console.error('Failed to load stats:', error)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    try {
      const searchFn = filters.useIcelandic
        ? searchAPI.searchIcelandic
        : searchAPI.search

      const data = await searchFn(query, filters.limit, filters.minScore)
      setResults(data.results || [])
    } catch (error) {
      console.error('Search failed:', error)
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="search-page">
      {/* Header */}
      <motion.header
        className="search-header glass"
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6 }}
      >
        <div className="header-content">
          <motion.button
            className="back-button"
            onClick={() => navigate('/')}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M19 12H5M12 19l-7-7 7-7" />
            </svg>
          </motion.button>

          <h1 className="page-title">SAGA Myndleit</h1>

          {stats && (
            <div className="stats-badge glass">
              <span>{stats.total_images?.toLocaleString() || 0}</span> myndir
            </div>
          )}
        </div>
      </motion.header>

      {/* Search Bar */}
      <motion.div
        className="search-container"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.6 }}
      >
        <form onSubmit={handleSearch} className="search-form glass-strong">
          <svg
            className="search-icon"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>

          <input
            type="text"
            className="search-input"
            placeholder="Leitaðu að myndum..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
          />

          <motion.button
            type="button"
            className="filter-toggle"
            onClick={() => setShowFilters(!showFilters)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="4" y1="21" x2="4" y2="14" />
              <line x1="4" y1="10" x2="4" y2="3" />
              <line x1="12" y1="21" x2="12" y2="12" />
              <line x1="12" y1="8" x2="12" y2="3" />
              <line x1="20" y1="21" x2="20" y2="16" />
              <line x1="20" y1="12" x2="20" y2="3" />
              <line x1="1" y1="14" x2="7" y2="14" />
              <line x1="9" y1="8" x2="15" y2="8" />
              <line x1="17" y1="16" x2="23" y2="16" />
            </svg>
          </motion.button>

          <motion.button
            type="submit"
            className="search-submit glass-button-primary"
            disabled={loading || !query.trim()}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {loading ? (
              <div className="spinner" />
            ) : (
              'Leita'
            )}
          </motion.button>
        </form>

        {/* Filter Panel */}
        <AnimatePresence>
          {showFilters && (
            <motion.div
              className="filter-panel glass"
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="filter-content">
                <div className="filter-group">
                  <label className="filter-label">
                    <input
                      type="checkbox"
                      checked={filters.useIcelandic}
                      onChange={(e) =>
                        setFilters({ ...filters, useIcelandic: e.target.checked })
                      }
                      className="filter-checkbox"
                    />
                    <span>Íslenskur texti</span>
                  </label>
                </div>

                <div className="filter-group">
                  <label className="filter-label">
                    <span>Fjöldi niðurstaðna: {filters.limit}</span>
                  </label>
                  <input
                    type="range"
                    min="10"
                    max="100"
                    step="10"
                    value={filters.limit}
                    onChange={(e) =>
                      setFilters({ ...filters, limit: parseInt(e.target.value) })
                    }
                    className="filter-slider"
                  />
                </div>

                <div className="filter-group">
                  <label className="filter-label">
                    <span>Lágmarks einkunn: {filters.minScore.toFixed(2)}</span>
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.05"
                    value={filters.minScore}
                    onChange={(e) =>
                      setFilters({ ...filters, minScore: parseFloat(e.target.value) })
                    }
                    className="filter-slider"
                  />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Results */}
      <motion.div
        className="results-container"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4, duration: 0.6 }}
      >
        {loading ? (
          <div className="loading-state glass">
            <div className="loading-spinner" />
            <p>Leita að myndum...</p>
          </div>
        ) : results.length > 0 ? (
          <>
            <div className="results-header">
              <p className="results-count">
                Fann <strong>{results.length}</strong> myndir
              </p>
            </div>
            <ImageGrid results={results} onImageClick={setSelectedImage} />
          </>
        ) : query ? (
          <div className="empty-state glass">
            <svg
              width="80"
              height="80"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1"
              strokeLinecap="round"
              strokeLinejoin="round"
              opacity="0.5"
            >
              <circle cx="11" cy="11" r="8" />
              <path d="m21 21-4.35-4.35" />
            </svg>
            <h3>Engar niðurstöður</h3>
            <p>Reyndu aðra leitarskilyrði</p>
          </div>
        ) : (
          <div className="welcome-state glass">
            <h2>Velkomin í myndleit</h2>
            <p>Byrjaðu að leita að myndum hér að ofan</p>
          </div>
        )}
      </motion.div>

      {/* Image Modal */}
      <AnimatePresence>
        {selectedImage && (
          <ImageModal image={selectedImage} onClose={() => setSelectedImage(null)} />
        )}
      </AnimatePresence>
    </div>
  )
}

export default SearchPage
