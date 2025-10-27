import { motion } from 'framer-motion'
import Masonry from 'react-masonry-css'
import { searchAPI } from '../services/api'
import './ImageGrid.css'

function ImageGrid({ results, onImageClick }) {
  const breakpointColumns = {
    default: 4,
    1400: 3,
    1024: 2,
    768: 1,
  }

  return (
    <Masonry
      breakpointCols={breakpointColumns}
      className="masonry-grid"
      columnClassName="masonry-grid-column"
    >
      {results.map((result, index) => (
        <motion.div
          key={result.image_path || index}
          className="image-card glass"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: index * 0.05, duration: 0.4 }}
          whileHover={{ scale: 1.02 }}
          onClick={() => onImageClick(result)}
        >
          <div className="image-wrapper">
            <img
              src={searchAPI.getImageUrl(result.image_path)}
              alt={result.description || 'Search result'}
              loading="lazy"
              className="result-image"
              onError={(e) => {
                e.target.style.display = 'none'
                e.target.parentElement.classList.add('image-error')
              }}
            />
            <div className="image-overlay">
              <div className="image-info">
                <div className="score-badge glass">
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                  </svg>
                  {(result.score * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          </div>
          {result.description && (
            <div className="image-description">
              <p>{result.description}</p>
            </div>
          )}
        </motion.div>
      ))}
    </Masonry>
  )
}

export default ImageGrid
