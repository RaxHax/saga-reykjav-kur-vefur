import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Link } from 'react-router-dom'
import toast from 'react-hot-toast'
import Masonry from 'react-masonry-css'
import {
  searchImages,
  hybridSearch,
  icelandicSearch,
  getStats,
  getImageUrl,
  handleAPIError,
} from '../services/api'
import ImageModal from '../components/ImageModal'
import SearchPanel from '../components/SearchPanel'
import IndexingPanel from '../components/IndexingPanel'
import './WorkspacePage.css'

/**
 * WorkspacePage Component
 *
 * Main search and indexing workspace with dark-tech visual language.
 * Features:
 * - Semantic image search with Icelandic support
 * - Hybrid search (text + metadata)
 * - Masonry grid results layout
 * - Real-time indexing panel
 * - Statistics dashboard
 */
const WorkspacePage = () => {
  const [activeTab, setActiveTab] = useState('search')
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [isSearching, setIsSearching] = useState(false)
  const [stats, setStats] = useState(null)
  const [selectedImage, setSelectedImage] = useState(null)
  const [searchMode, setSearchMode] = useState('semantic') // semantic, hybrid, icelandic
  const [filters, setFilters] = useState({
    limit: 50,
    minScore: 0.0,
  })

  // Load stats on mount
  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const data = await getStats()
      setStats(data)
    } catch (error) {
      console.error('Failed to load stats:', error)
    }
  }

  const handleSearch = async (e) => {
    e?.preventDefault()

    if (!searchQuery.trim()) {
      toast.error('Please enter a search query')
      return
    }

    setIsSearching(true)

    try {
      let results

      switch (searchMode) {
        case 'hybrid':
          results = await hybridSearch({
            textQuery: searchQuery,
            metadata: {},
            weights: { text: 0.7, metadata: 0.3 },
            limit: filters.limit,
          })
          break

        case 'icelandic':
          results = await icelandicSearch(searchQuery, {
            limit: filters.limit,
            min_score: filters.minScore,
          })
          break

        default: // semantic
          results = await searchImages(searchQuery, filters)
          break
      }

      setSearchResults(results.results || [])
      toast.success(`Found ${results.results?.length || 0} results`)
    } catch (error) {
      toast.error(handleAPIError(error))
    } finally {
      setIsSearching(false)
    }
  }

  const breakpointColumns = {
    default: 4,
    1400: 3,
    1024: 2,
    640: 1,
  }

  return (
    <div className="workspace-page">
      {/* Sidebar */}
      <aside className="workspace-sidebar glass">
        <div className="sidebar-header">
          <Link to="/" className="sidebar-logo">
            <h2 className="logo-text-workspace">SAGA</h2>
            <span className="logo-subtitle-workspace">Reykjavík</span>
          </Link>

          <div className="status-badge">
            <div className="status-dot" />
            <span>Active</span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="sidebar-nav">
          <button
            className={`nav-item ${activeTab === 'search' ? 'active' : ''}`}
            onClick={() => setActiveTab('search')}
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="8" cy="8" r="5" stroke="currentColor" strokeWidth="1.5" />
              <path d="M12 12L16 16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            </svg>
            <span>Search</span>
          </button>

          <button
            className={`nav-item ${activeTab === 'indexing' ? 'active' : ''}`}
            onClick={() => setActiveTab('indexing')}
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <rect x="3" y="3" width="14" height="3" rx="1" fill="currentColor" opacity="0.5" />
              <rect x="3" y="8.5" width="14" height="3" rx="1" fill="currentColor" opacity="0.7" />
              <rect x="3" y="14" width="14" height="3" rx="1" fill="currentColor" />
            </svg>
            <span>Indexing</span>
          </button>

          <button
            className={`nav-item ${activeTab === 'analytics' ? 'active' : ''}`}
            onClick={() => setActiveTab('analytics')}
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <rect x="3" y="11" width="3" height="6" rx="0.5" fill="currentColor" opacity="0.5" />
              <rect x="8.5" y="8" width="3" height="9" rx="0.5" fill="currentColor" opacity="0.7" />
              <rect x="14" y="5" width="3" height="12" rx="0.5" fill="currentColor" />
            </svg>
            <span>Analytics</span>
          </button>
        </nav>

        {/* Stats */}
        {stats && (
          <div className="sidebar-stats">
            <div className="stat-item">
              <div className="stat-label">Images Indexed</div>
              <div className="stat-value">{stats.total_images?.toLocaleString() || '0'}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Vector Size</div>
              <div className="stat-value">{stats.vector_size || '512'}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Device</div>
              <div className="stat-value">{stats.device || 'CPU'}</div>
            </div>
          </div>
        )}

        {/* Back to Home */}
        <div className="sidebar-footer">
          <Link to="/" className="btn btn-ghost btn-block">
            ← Back to Home
          </Link>
        </div>
      </aside>

      {/* Main Content */}
      <main className="workspace-main">
        <AnimatePresence mode="wait">
          {activeTab === 'search' && (
            <motion.div
              key="search"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="tab-content"
            >
              {/* Search Panel */}
              <SearchPanel
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                searchMode={searchMode}
                setSearchMode={setSearchMode}
                filters={filters}
                setFilters={setFilters}
                onSearch={handleSearch}
                isSearching={isSearching}
              />

              {/* Search Results */}
              {searchResults.length > 0 && (
                <div className="results-section">
                  <div className="results-header">
                    <h3 className="results-title">
                      {searchResults.length} Results
                    </h3>
                    <button
                      className="btn btn-ghost btn-sm"
                      onClick={() => setSearchResults([])}
                    >
                      Clear Results
                    </button>
                  </div>

                  <Masonry
                    breakpointCols={breakpointColumns}
                    className="masonry-grid"
                    columnClassName="masonry-column"
                  >
                    {searchResults.map((result, index) => (
                      <ImageCard
                        key={index}
                        result={result}
                        onClick={() => setSelectedImage(result)}
                      />
                    ))}
                  </Masonry>
                </div>
              )}

              {!isSearching && searchResults.length === 0 && searchQuery && (
                <div className="empty-state">
                  <div className="empty-icon">🔍</div>
                  <h3>No results found</h3>
                  <p>Try adjusting your search query or filters</p>
                </div>
              )}
            </motion.div>
          )}

          {activeTab === 'indexing' && (
            <motion.div
              key="indexing"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="tab-content"
            >
              <IndexingPanel onComplete={loadStats} />
            </motion.div>
          )}

          {activeTab === 'analytics' && (
            <motion.div
              key="analytics"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="tab-content"
            >
              <div className="analytics-panel">
                <h2 className="panel-title">Analytics Dashboard</h2>
                <p className="panel-description">Coming soon - search insights and usage statistics</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Image Modal */}
      <AnimatePresence>
        {selectedImage && (
          <ImageModal
            image={selectedImage}
            onClose={() => setSelectedImage(null)}
          />
        )}
      </AnimatePresence>
    </div>
  )
}

// Image Card Component
const ImageCard = ({ result, onClick }) => {
  const [imageLoaded, setImageLoaded] = useState(false)

  return (
    <motion.div
      className="image-card glass glass-hover"
      onClick={onClick}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
    >
      <div className="image-wrapper">
        {!imageLoaded && (
          <div className="image-skeleton">
            <div className="spinner spinner-sm" />
          </div>
        )}
        <img
          src={getImageUrl(result.path)}
          alt={result.description || 'Search result'}
          onLoad={() => setImageLoaded(true)}
          style={{ display: imageLoaded ? 'block' : 'none' }}
        />
        <div className="image-overlay">
          <div className="score-badge">
            {(result.score * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      {result.description && (
        <div className="card-content">
          <p className="card-description">{result.description}</p>
        </div>
      )}

      <div className="card-footer">
        <span className="card-filename">{result.filename}</span>
      </div>
    </motion.div>
  )
}

export default WorkspacePage
