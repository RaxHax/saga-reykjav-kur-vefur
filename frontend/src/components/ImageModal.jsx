import { motion } from 'framer-motion'
import { getImageUrl } from '../services/api'
import './ImageModal.css'

/**
 * ImageModal Component
 *
 * Full-screen modal for viewing image details
 */
const ImageModal = ({ image, onClose }) => {
  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  const handleCopyPath = () => {
    navigator.clipboard.writeText(image.path)
    // You could add a toast notification here
  }

  return (
    <motion.div
      className="modal-backdrop"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={handleBackdropClick}
    >
      <motion.div
        className="modal-content"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        transition={{ duration: 0.2 }}
      >
        {/* Close Button */}
        <button className="modal-close" onClick={onClose}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path
              d="M18 6L6 18M6 6L18 18"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
            />
          </svg>
        </button>

        {/* Image */}
        <div className="modal-image-container">
          <img
            src={getImageUrl(image.path)}
            alt={image.description || 'Image'}
            className="modal-image"
          />
        </div>

        {/* Details */}
        <div className="modal-details glass">
          <div className="detail-row">
            <span className="detail-label">Filename</span>
            <span className="detail-value">{image.filename}</span>
          </div>

          {image.description && (
            <div className="detail-row">
              <span className="detail-label">Description</span>
              <span className="detail-value">{image.description}</span>
            </div>
          )}

          {image.score !== undefined && (
            <div className="detail-row">
              <span className="detail-label">Similarity Score</span>
              <span className="detail-value score-highlight">
                {(image.score * 100).toFixed(2)}%
              </span>
            </div>
          )}

          <div className="detail-row">
            <span className="detail-label">Path</span>
            <div className="path-row">
              <span className="detail-value path-value">{image.path}</span>
              <button className="btn-icon btn-sm" onClick={handleCopyPath} title="Copy path">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <rect
                    x="5"
                    y="5"
                    width="9"
                    height="9"
                    rx="1"
                    stroke="currentColor"
                    strokeWidth="1.5"
                  />
                  <path
                    d="M11 3H3C2.44772 3 2 3.44772 2 4V12"
                    stroke="currentColor"
                    strokeWidth="1.5"
                  />
                </svg>
              </button>
            </div>
          </div>

          {image.folder && (
            <div className="detail-row">
              <span className="detail-label">Folder</span>
              <span className="detail-value">{image.folder}</span>
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  )
}

export default ImageModal
