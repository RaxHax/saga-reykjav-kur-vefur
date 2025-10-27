import { motion } from 'framer-motion'
import { searchAPI } from '../services/api'
import './ImageModal.css'

function ImageModal({ image, onClose }) {
  return (
    <motion.div
      className="modal-backdrop"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className="modal-content glass-strong"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        transition={{ type: 'spring', damping: 25, stiffness: 300 }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <motion.button
          className="modal-close"
          onClick={onClose}
          whileHover={{ scale: 1.1, rotate: 90 }}
          whileTap={{ scale: 0.9 }}
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
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </motion.button>

        {/* Image */}
        <div className="modal-image-wrapper">
          <img
            src={searchAPI.getImageUrl(image.image_path)}
            alt={image.description || 'Image'}
            className="modal-image"
          />
        </div>

        {/* Info */}
        <div className="modal-info">
          {/* Score Badge */}
          <div className="modal-score glass">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="currentColor"
              stroke="none"
            >
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
            <span>{(image.score * 100).toFixed(1)}% samsvörun</span>
          </div>

          {/* Description */}
          {image.description && (
            <div className="modal-description">
              <h3>Lýsing</h3>
              <p>{image.description}</p>
            </div>
          )}

          {/* Metadata */}
          <div className="modal-metadata">
            <div className="metadata-item">
              <span className="metadata-label">Skrá:</span>
              <span className="metadata-value">
                {image.image_path.split(/[/\\]/).pop()}
              </span>
            </div>
            {image.metadata && Object.keys(image.metadata).length > 0 && (
              <>
                {Object.entries(image.metadata).map(([key, value]) => (
                  <div key={key} className="metadata-item">
                    <span className="metadata-label">{key}:</span>
                    <span className="metadata-value">{value}</span>
                  </div>
                ))}
              </>
            )}
          </div>
        </div>
      </motion.div>
    </motion.div>
  )
}

export default ImageModal
