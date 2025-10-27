import { useState } from 'react'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { jobAPI } from '../services/api'
import './IndexingPage.css'

function IndexingPage() {
  const navigate = useNavigate()
  const [folderPath, setFolderPath] = useState('')
  const [options, setOptions] = useState({
    recursive: true,
    skipExisting: true,
    extractMetadata: true,
    batchSize: 100,
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  const handleStartJob = async (e) => {
    e.preventDefault()
    if (!folderPath.trim()) {
      setError('Please enter a folder path')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      const result = await jobAPI.startJob(folderPath, options)
      setSuccess(`Job created successfully! Job ID: ${result.id}`)
      setFolderPath('')

      // Redirect to jobs page after 2 seconds
      setTimeout(() => {
        navigate('/jobs')
      }, 2000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start indexing job')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="indexing-page">
      {/* Header */}
      <motion.header
        className="page-header glass"
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
          <h1 className="page-title">Start Indexing</h1>
          <div style={{ width: '40px' }} />
        </div>
      </motion.header>

      {/* Form Container */}
      <motion.div
        className="form-container"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.6 }}
      >
        <form onSubmit={handleStartJob} className="indexing-form glass-strong">
          <div className="form-header">
            <div className="form-icon">📤</div>
            <div>
              <h2>Create Indexing Job</h2>
              <p>Add new images to the search database</p>
            </div>
          </div>

          {/* Folder Path */}
          <div className="form-group">
            <label className="form-label">Folder Path *</label>
            <input
              type="text"
              className="glass-input"
              placeholder="C:\Users\user\Desktop\images"
              value={folderPath}
              onChange={(e) => setFolderPath(e.target.value)}
              disabled={loading}
            />
            <span className="form-hint">
              Enter the full path to the folder containing images
            </span>
          </div>

          {/* Options */}
          <div className="options-grid">
            <label className="option-card glass">
              <input
                type="checkbox"
                checked={options.recursive}
                onChange={(e) =>
                  setOptions({ ...options, recursive: e.target.checked })
                }
                disabled={loading}
              />
              <div>
                <div className="option-title">Recursive</div>
                <div className="option-description">
                  Include subfolders
                </div>
              </div>
            </label>

            <label className="option-card glass">
              <input
                type="checkbox"
                checked={options.skipExisting}
                onChange={(e) =>
                  setOptions({ ...options, skipExisting: e.target.checked })
                }
                disabled={loading}
              />
              <div>
                <div className="option-title">Skip Existing</div>
                <div className="option-description">
                  Skip already indexed images
                </div>
              </div>
            </label>

            <label className="option-card glass">
              <input
                type="checkbox"
                checked={options.extractMetadata}
                onChange={(e) =>
                  setOptions({ ...options, extractMetadata: e.target.checked })
                }
                disabled={loading}
              />
              <div>
                <div className="option-title">Extract Metadata</div>
                <div className="option-description">
                  Read .txt description files
                </div>
              </div>
            </label>
          </div>

          {/* Batch Size */}
          <div className="form-group">
            <label className="form-label">
              Batch Size: {options.batchSize}
            </label>
            <input
              type="range"
              min="10"
              max="500"
              step="10"
              value={options.batchSize}
              onChange={(e) =>
                setOptions({ ...options, batchSize: parseInt(e.target.value) })
              }
              className="filter-slider"
              disabled={loading}
            />
            <span className="form-hint">
              Number of images to process per batch
            </span>
          </div>

          {/* Error/Success Messages */}
          {error && (
            <motion.div
              className="alert alert-error glass"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              ❌ {error}
            </motion.div>
          )}

          {success && (
            <motion.div
              className="alert alert-success glass"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              ✅ {success}
            </motion.div>
          )}

          {/* Submit Button */}
          <motion.button
            type="submit"
            className="glass-button glass-button-primary submit-button"
            disabled={loading || !folderPath.trim()}
            whileHover={{ scale: loading ? 1 : 1.02 }}
            whileTap={{ scale: loading ? 1 : 0.98 }}
          >
            {loading ? (
              <>
                <div className="spinner" />
                Starting Job...
              </>
            ) : (
              <>
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
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
                Start Indexing
              </>
            )}
          </motion.button>
        </form>

        {/* Info Cards */}
        <div className="info-cards">
          <div className="info-card glass">
            <div className="info-card-icon">💡</div>
            <div className="info-card-content">
              <h4>Tip</h4>
              <p>
                Make sure the folder path is accessible and contains valid image
                files (jpg, png, gif, etc.)
              </p>
            </div>
          </div>
          <div className="info-card glass">
            <div className="info-card-icon">⚙️</div>
            <div className="info-card-content">
              <h4>Processing</h4>
              <p>
                Jobs run in the background. Monitor progress on the Jobs page.
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default IndexingPage
