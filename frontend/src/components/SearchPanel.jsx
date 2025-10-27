import { motion } from 'framer-motion'
import './SearchPanel.css'

/**
 * SearchPanel Component
 *
 * Search interface with support for different search modes:
 * - Semantic: Standard CLIP semantic search
 * - Hybrid: Combined text + metadata search
 * - Icelandic: Icelandic language support with translation
 */
const SearchPanel = ({
  searchQuery,
  setSearchQuery,
  searchMode,
  setSearchMode,
  filters,
  setFilters,
  onSearch,
  isSearching,
}) => {
  return (
    <motion.div
      className="search-panel glass"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="search-header">
        <h2 className="search-title">Image Search</h2>
        <p className="search-subtitle">
          Search using natural language in English or Icelandic
        </p>
      </div>

      <form onSubmit={onSearch} className="search-form">
        {/* Search Input */}
        <div className="search-input-wrapper">
          <svg
            className="search-icon"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <circle cx="8" cy="8" r="5" stroke="currentColor" strokeWidth="1.5" />
            <path d="M12 12L16 16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
          </svg>

          <input
            type="text"
            className="search-input"
            placeholder="e.g., 'old buildings in downtown' or 'gamlar byggingar í miðbænum'"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            disabled={isSearching}
          />

          {searchQuery && (
            <button
              type="button"
              className="clear-button"
              onClick={() => setSearchQuery('')}
              disabled={isSearching}
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path
                  d="M12 4L4 12M4 4L12 12"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
            </button>
          )}
        </div>

        {/* Search Mode Tabs */}
        <div className="search-modes">
          <button
            type="button"
            className={`mode-tab ${searchMode === 'semantic' ? 'active' : ''}`}
            onClick={() => setSearchMode('semantic')}
            disabled={isSearching}
          >
            <span className="mode-icon">🔍</span>
            <span>Semantic</span>
          </button>

          <button
            type="button"
            className={`mode-tab ${searchMode === 'hybrid' ? 'active' : ''}`}
            onClick={() => setSearchMode('hybrid')}
            disabled={isSearching}
          >
            <span className="mode-icon">⚡</span>
            <span>Hybrid</span>
          </button>

          <button
            type="button"
            className={`mode-tab ${searchMode === 'icelandic' ? 'active' : ''}`}
            onClick={() => setSearchMode('icelandic')}
            disabled={isSearching}
          >
            <span className="mode-icon">🇮🇸</span>
            <span>Icelandic</span>
          </button>
        </div>

        {/* Filters */}
        <div className="search-filters">
          <div className="filter-group">
            <label htmlFor="limit" className="filter-label">
              Max Results
            </label>
            <select
              id="limit"
              className="filter-select"
              value={filters.limit}
              onChange={(e) => setFilters({ ...filters, limit: parseInt(e.target.value) })}
              disabled={isSearching}
            >
              <option value="20">20</option>
              <option value="50">50</option>
              <option value="100">100</option>
              <option value="200">200</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="minScore" className="filter-label">
              Min Score ({(filters.minScore * 100).toFixed(0)}%)
            </label>
            <input
              id="minScore"
              type="range"
              className="filter-slider"
              min="0"
              max="1"
              step="0.05"
              value={filters.minScore}
              onChange={(e) => setFilters({ ...filters, minScore: parseFloat(e.target.value) })}
              disabled={isSearching}
            />
          </div>
        </div>

        {/* Search Button */}
        <button
          type="submit"
          className="btn btn-primary btn-lg search-button"
          disabled={isSearching || !searchQuery.trim()}
        >
          {isSearching ? (
            <>
              <div className="spinner spinner-sm" />
              <span>Searching...</span>
            </>
          ) : (
            <>
              <span>Search Images</span>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path
                  d="M4 10h12m0 0l-4-4m4 4l-4 4"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </>
          )}
        </button>
      </form>

      {/* Mode Description */}
      <div className="mode-description">
        {searchMode === 'semantic' && (
          <p>
            <strong>Semantic Search:</strong> Uses CLIP AI model to find images that match the
            meaning of your query, even if the exact words aren't in the metadata.
          </p>
        )}
        {searchMode === 'hybrid' && (
          <p>
            <strong>Hybrid Search:</strong> Combines semantic search with metadata filtering
            for more precise results using configurable scoring weights.
          </p>
        )}
        {searchMode === 'icelandic' && (
          <p>
            <strong>Icelandic Search:</strong> Optimized for Icelandic language queries with
            automatic translation fallback for better cross-language search.
          </p>
        )}
      </div>
    </motion.div>
  )
}

export default SearchPanel
