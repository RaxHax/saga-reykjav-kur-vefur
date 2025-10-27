import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import {
  startIndexing,
  getIndexingJobs,
  pauseIndexing,
  resumeIndexing,
  cancelIndexing,
  getIndexingLogs,
  handleAPIError,
} from '../services/api'
import './IndexingPanel.css'

/**
 * IndexingPanel Component
 *
 * Manages image indexing jobs with real-time progress tracking.
 * Features:
 * - Start new indexing jobs
 * - Monitor active jobs
 * - Pause/Resume/Cancel jobs
 * - View job logs
 * - Job history
 */
const IndexingPanel = ({ onComplete }) => {
  const [jobs, setJobs] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [imageFolder, setImageFolder] = useState('./scraped_images')
  const [showNewJobForm, setShowNewJobForm] = useState(false)

  // Load jobs on mount and poll for updates
  useEffect(() => {
    loadJobs()
    const interval = setInterval(loadJobs, 3000) // Poll every 3 seconds
    return () => clearInterval(interval)
  }, [])

  const loadJobs = async () => {
    try {
      const data = await getIndexingJobs({ limit: 10 })
      setJobs(data.jobs || [])
    } catch (error) {
      console.error('Failed to load jobs:', error)
    }
  }

  const handleStartIndexing = async (e) => {
    e.preventDefault()

    if (!imageFolder.trim()) {
      toast.error('Please enter an image folder path')
      return
    }

    setIsLoading(true)

    try {
      const result = await startIndexing(imageFolder)
      toast.success('Indexing job started successfully')
      setShowNewJobForm(false)
      setImageFolder('./scraped_images')
      await loadJobs()
      if (onComplete) onComplete()
    } catch (error) {
      toast.error(handleAPIError(error))
    } finally {
      setIsLoading(false)
    }
  }

  const handlePause = async (jobId) => {
    try {
      await pauseIndexing(jobId)
      toast.success('Job paused')
      await loadJobs()
    } catch (error) {
      toast.error(handleAPIError(error))
    }
  }

  const handleResume = async (jobId) => {
    try {
      await resumeIndexing(jobId)
      toast.success('Job resumed')
      await loadJobs()
    } catch (error) {
      toast.error(handleAPIError(error))
    }
  }

  const handleCancel = async (jobId) => {
    if (!confirm('Are you sure you want to cancel this job?')) return

    try {
      await cancelIndexing(jobId)
      toast.success('Job cancelled')
      await loadJobs()
    } catch (error) {
      toast.error(handleAPIError(error))
    }
  }

  return (
    <motion.div
      className="indexing-panel"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="panel-header">
        <div>
          <h2 className="panel-title">Image Indexing</h2>
          <p className="panel-description">
            Index new image collections and manage indexing jobs
          </p>
        </div>

        <button
          className="btn btn-primary"
          onClick={() => setShowNewJobForm(!showNewJobForm)}
        >
          {showNewJobForm ? 'Cancel' : '+ New Indexing Job'}
        </button>
      </div>

      {/* New Job Form */}
      {showNewJobForm && (
        <motion.div
          className="new-job-form glass"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
        >
          <h3 className="form-title">Start New Indexing Job</h3>

          <form onSubmit={handleStartIndexing}>
            <div className="form-group">
              <label htmlFor="imageFolder" className="form-label">
                Image Folder Path
              </label>
              <input
                id="imageFolder"
                type="text"
                className="form-input"
                placeholder="e.g., ./scraped_images or /path/to/images"
                value={imageFolder}
                onChange={(e) => setImageFolder(e.target.value)}
                disabled={isLoading}
              />
              <p className="form-hint">
                Path to the folder containing images to index (.jpg, .jpeg, .png)
              </p>
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-lg"
              disabled={isLoading || !imageFolder.trim()}
            >
              {isLoading ? (
                <>
                  <div className="spinner spinner-sm" />
                  <span>Starting...</span>
                </>
              ) : (
                <span>Start Indexing</span>
              )}
            </button>
          </form>
        </motion.div>
      )}

      {/* Jobs List */}
      <div className="jobs-section">
        <h3 className="section-title">Active & Recent Jobs</h3>

        {jobs.length === 0 ? (
          <div className="empty-state-small">
            <p>No indexing jobs yet. Start a new job to index your images.</p>
          </div>
        ) : (
          <div className="jobs-list">
            {jobs.map((job) => (
              <JobCard
                key={job.id}
                job={job}
                onPause={handlePause}
                onResume={handleResume}
                onCancel={handleCancel}
              />
            ))}
          </div>
        )}
      </div>
    </motion.div>
  )
}

// Job Card Component
const JobCard = ({ job, onPause, onResume, onCancel }) => {
  const [showLogs, setShowLogs] = useState(false)
  const [logs, setLogs] = useState([])

  const loadLogs = async () => {
    try {
      const data = await getIndexingLogs(job.id, { tail: 50 })
      setLogs(data.logs || [])
    } catch (error) {
      console.error('Failed to load logs:', error)
    }
  }

  useEffect(() => {
    if (showLogs) {
      loadLogs()
    }
  }, [showLogs])

  const getStatusColor = (status) => {
    switch (status) {
      case 'running':
        return 'var(--color-info)'
      case 'paused':
        return 'var(--color-warning)'
      case 'completed':
        return 'var(--color-success)'
      case 'failed':
      case 'cancelled':
        return 'var(--color-error)'
      default:
        return 'var(--color-text-tertiary)'
    }
  }

  const progress = job.progress || 0
  const status = job.status || 'pending'

  return (
    <motion.div
      className="job-card glass"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="job-header">
        <div className="job-info">
          <div className="job-title">
            <span className="job-id">Job #{job.id?.slice(0, 8)}</span>
            <span
              className="job-status"
              style={{ color: getStatusColor(status) }}
            >
              {status.toUpperCase()}
            </span>
          </div>
          <p className="job-folder">{job.folder || job.image_folder}</p>
        </div>

        <div className="job-actions">
          {status === 'running' && (
            <button
              className="btn-icon"
              onClick={() => onPause(job.id)}
              title="Pause"
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <rect x="5" y="4" width="3" height="12" rx="1" fill="currentColor" />
                <rect x="12" y="4" width="3" height="12" rx="1" fill="currentColor" />
              </svg>
            </button>
          )}

          {status === 'paused' && (
            <button
              className="btn-icon"
              onClick={() => onResume(job.id)}
              title="Resume"
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M6 4L15 10L6 16V4Z" fill="currentColor" />
              </svg>
            </button>
          )}

          {(status === 'running' || status === 'paused') && (
            <button
              className="btn-icon btn-danger"
              onClick={() => onCancel(job.id)}
              title="Cancel"
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path
                  d="M15 5L5 15M5 5L15 15"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
            </button>
          )}

          <button
            className="btn-icon"
            onClick={() => setShowLogs(!showLogs)}
            title="Toggle Logs"
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path
                d="M5 6H15M5 10H15M5 14H10"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      {status === 'running' && (
        <div className="progress-section">
          <div className="progress-bar-bg">
            <motion.div
              className="progress-bar-fill"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
          <div className="progress-text">{progress.toFixed(1)}%</div>
        </div>
      )}

      {/* Job Stats */}
      <div className="job-stats">
        <div className="stat-item-small">
          <span className="stat-label-small">Processed</span>
          <span className="stat-value-small">{job.processed || 0}</span>
        </div>
        <div className="stat-item-small">
          <span className="stat-label-small">Total</span>
          <span className="stat-value-small">{job.total || 0}</span>
        </div>
        {job.eta && (
          <div className="stat-item-small">
            <span className="stat-label-small">ETA</span>
            <span className="stat-value-small">{job.eta}</span>
          </div>
        )}
      </div>

      {/* Logs */}
      {showLogs && (
        <div className="logs-section">
          <div className="logs-container">
            {logs.length === 0 ? (
              <p className="logs-empty">No logs available</p>
            ) : (
              logs.map((log, index) => (
                <div key={index} className="log-line">
                  {log}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </motion.div>
  )
}

export default IndexingPanel
