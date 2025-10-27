import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import './HexagonCard.css'

/**
 * HexagonCard Component
 *
 * A hexagonal card with glow effects, minimalist icons, and smooth animations.
 * Icons are configurable placeholders that can be easily swapped.
 *
 * @param {Object} props
 * @param {string} props.title - Card title
 * @param {string} props.description - Card description
 * @param {ReactNode} props.icon - Icon component (configurable)
 * @param {string} props.accentColor - Accent color for glow effect
 * @param {string} props.href - Link destination
 * @param {number} props.delay - Animation delay
 */
const HexagonCard = ({
  title,
  description,
  icon,
  accentColor = '#5ac8fa',
  href = '#',
  delay = 0,
}) => {
  const navigate = useNavigate()

  const handleClick = () => {
    if (href.startsWith('http')) {
      window.open(href, '_blank')
    } else {
      navigate(href)
    }
  }

  return (
    <motion.div
      className="hexagon-card-wrapper"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{
        duration: 0.5,
        delay,
        ease: [0.4, 0, 0.2, 1],
      }}
      whileHover={{
        scale: 1.05,
        transition: { duration: 0.2 },
      }}
      onClick={handleClick}
    >
      <div
        className="hexagon-card"
        style={{
          '--accent-color': accentColor,
          '--glow-color': `${accentColor}80`,
        }}
      >
        {/* Hexagon Border */}
        <div className="hexagon-border">
          <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id={`gradient-${title}`} x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor={accentColor} stopOpacity="0.6" />
                <stop offset="100%" stopColor={accentColor} stopOpacity="0.2" />
              </linearGradient>
            </defs>
            <polygon
              points="50,5 90,27.5 90,72.5 50,95 10,72.5 10,27.5"
              fill="none"
              stroke={`url(#gradient-${title})`}
              strokeWidth="0.5"
              className="hexagon-path"
            />
          </svg>
        </div>

        {/* Card Content */}
        <div className="hexagon-content">
          {/* Icon Container */}
          <motion.div
            className="icon-container"
            whileHover={{ scale: 1.1, rotate: 5 }}
            transition={{ duration: 0.3 }}
          >
            {icon}
          </motion.div>

          {/* Title */}
          <h3 className="card-title">{title}</h3>

          {/* Description */}
          <p className="card-description">{description}</p>

          {/* Hover Arrow */}
          <motion.div
            className="hover-arrow"
            initial={{ x: -10, opacity: 0 }}
            whileHover={{ x: 0, opacity: 1 }}
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path
                d="M4 10h12m0 0l-4-4m4 4l-4 4"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </motion.div>
        </div>

        {/* Glow Effect */}
        <div className="hexagon-glow" />
      </div>
    </motion.div>
  )
}

export default HexagonCard
