import { motion } from 'framer-motion'
import './JobCard.css'

function JobCard({ job, index, onPause, onResume, onCancel }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'RUNNING':
        return '#4facfe'
      case 'COMPLETED':
        return '#2ecc71'
      case 'FAILED':
        return '#e74c3c'
      case 'PAUSED':
        return '#f39c12'
      case 'CANCELLED':
        return '#95a5a6'
      default:
        return '#95a5a6'
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    const date = new Date(dateString)
    return date.toLocaleString()
  }

  const formatDuration = (startDate, endDate) => {
    if (!startDate) return 'N/A'
    const start = new Date(startDate)
    const end = endDate ? new Date(endDate) : new Date()
    const diff = Math.floor((end - start) / 1000)

    if (diff < 60) return `${diff}s`
    if (diff < 3600) return `${Math.floor(diff / 60)}m ${diff % 60}s`
    return `${Math.floor(diff / 3600)}h ${Math.floor((diff % 3600) / 60)}m`
  }

  const percentage = job.progress?.percentage || 0

  return (
    <motion.div
      className="job-card glass"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ delay: index * 0.05, duration: 0.4 }}
    >
      {/* Status Badge */}
      <div
        className="status-badge"
        style={{ backgroundColor: getStatusColor(job.status) }}
      >
        {job.status}
      </div>

      {/* Job Info */}
      <div className="job-info">
        <div className="job-header">
          <h3 className="job-id">Job {job.id.substring(0, 8)}...</h3>
          <span className="job-date">{formatDate(job.created_at)}</span>
        </div>

        <div className="job-folder">
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
          </svg>
          <span>{job.image_folder}</span>
        </div>

        {/* Progress Bar */}
        {job.status === 'RUNNING' && (
          <div className="progress-section">
            <div className="progress-info">
              <span>
                {job.progress?.processed || 0} / {job.progress?.total || 0}
              </span>
              <span>{percentage.toFixed(1)}%</span>
            </div>
            <div className="progress-bar">
              <motion.div
                className="progress-fill"
                initial={{ width: 0 }}
                animate={{ width: `${percentage}%` }}
                transition={{ duration: 0.5 }}
                style={{ backgroundColor: getStatusColor(job.status) }}
              />
            </div>
            {job.progress?.eta_seconds && (
              <div className="eta">
                ETA: {Math.floor(job.progress.eta_seconds / 60)}m{' '}
                {job.progress.eta_seconds % 60}s
              </div>
            )}
          </div>
        )}

        {/* Completed Info */}
        {job.status === 'COMPLETED' && (
          <div className="completion-info">
            <div className="stat-item">
              <span className="stat-label">Processed:</span>
              <span className="stat-value">{job.progress?.total || 0} images</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Duration:</span>
              <span className="stat-value">
                {formatDuration(job.started_at, job.completed_at)}
              </span>
            </div>
          </div>
        )}

        {/* Error Message */}
        {job.error_message && (
          <div className="error-message">
            ⚠️ {job.error_message}
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="job-actions">
        {job.status === 'RUNNING' && (
          <>
            <motion.button
              className="action-button pause-button"
              onClick={() => onPause(job.id)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <rect x="6" y="4" width="4" height="16" />
                <rect x="14" y="4" width="4" height="16" />
              </svg>
              Pause
            </motion.button>
            <motion.button
              className="action-button cancel-button"
              onClick={() => onCancel(job.id)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
              Cancel
            </motion.button>
          </>
        )}

        {job.status === 'PAUSED' && (
          <motion.button
            className="action-button resume-button"
            onClick={() => onResume(job.id)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <polygon points="5 3 19 12 5 21 5 3" />
            </svg>
            Resume
          </motion.button>
        )}
      </div>
    </motion.div>
  )
}

export default JobCard
