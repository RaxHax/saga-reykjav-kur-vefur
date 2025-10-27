import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { jobAPI } from '../services/api'
import JobCard from '../components/JobCard'
import './JobsPage.css'

function JobsPage() {
  const navigate = useNavigate()
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')
  const [autoRefresh, setAutoRefresh] = useState(true)

  useEffect(() => {
    loadJobs()

    if (autoRefresh) {
      const interval = setInterval(loadJobs, 3000)
      return () => clearInterval(interval)
    }
  }, [filter, autoRefresh])

  const loadJobs = async () => {
    try {
      const statusFilter = filter === 'all' ? null : filter.toUpperCase()
      const data = await jobAPI.listJobs(statusFilter, 100, 0)
      setJobs(data.jobs || [])
    } catch (error) {
      console.error('Failed to load jobs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePauseJob = async (jobId) => {
    try {
      await jobAPI.pauseJob(jobId)
      loadJobs()
    } catch (error) {
      console.error('Failed to pause job:', error)
    }
  }

  const handleResumeJob = async (jobId) => {
    try {
      await jobAPI.resumeJob(jobId)
      loadJobs()
    } catch (error) {
      console.error('Failed to resume job:', error)
    }
  }

  const handleCancelJob = async (jobId) => {
    if (!confirm('Are you sure you want to cancel this job?')) return

    try {
      await jobAPI.cancelJob(jobId)
      loadJobs()
    } catch (error) {
      console.error('Failed to cancel job:', error)
    }
  }

  const filteredJobs = jobs

  const statusCounts = {
    all: jobs.length,
    running: jobs.filter(j => j.status === 'RUNNING').length,
    completed: jobs.filter(j => j.status === 'COMPLETED').length,
    failed: jobs.filter(j => j.status === 'FAILED').length,
  }

  return (
    <div className="jobs-page">
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

          <h1 className="page-title">Indexing Jobs</h1>

          <div className="header-actions">
            <label className="auto-refresh-toggle glass">
              <input
                type="checkbox"
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
              />
              <span>Auto-refresh</span>
            </label>
          </div>
        </div>
      </motion.header>

      {/* Filter Tabs */}
      <motion.div
        className="filter-tabs glass"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.6 }}
      >
        {['all', 'running', 'completed', 'failed'].map((status) => (
          <button
            key={status}
            className={`filter-tab ${filter === status ? 'active' : ''}`}
            onClick={() => setFilter(status)}
          >
            <span className="tab-label">
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </span>
            <span className="tab-count">{statusCounts[status]}</span>
          </button>
        ))}
      </motion.div>

      {/* Jobs List */}
      <motion.div
        className="jobs-container"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4, duration: 0.6 }}
      >
        {loading ? (
          <div className="loading-state glass">
            <div className="loading-spinner" />
            <p>Loading jobs...</p>
          </div>
        ) : filteredJobs.length > 0 ? (
          <div className="jobs-grid">
            <AnimatePresence>
              {filteredJobs.map((job, index) => (
                <JobCard
                  key={job.id}
                  job={job}
                  index={index}
                  onPause={handlePauseJob}
                  onResume={handleResumeJob}
                  onCancel={handleCancelJob}
                />
              ))}
            </AnimatePresence>
          </div>
        ) : (
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
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
              <line x1="9" y1="9" x2="15" y2="9" />
              <line x1="9" y1="15" x2="15" y2="15" />
            </svg>
            <h3>No jobs found</h3>
            <p>Start a new indexing job to see it here</p>
            <button
              className="glass-button glass-button-primary"
              onClick={() => navigate('/indexing')}
            >
              Start Indexing
            </button>
          </div>
        )}
      </motion.div>
    </div>
  )
}

export default JobsPage
