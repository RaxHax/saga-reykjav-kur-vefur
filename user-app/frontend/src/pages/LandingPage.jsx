import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import './LandingPage.css'

function LandingPage() {
  const navigate = useNavigate()

  return (
    <div className="landing-container">
      <motion.div
        className="hero-section"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: [0.4, 0, 0.2, 1] }}
      >
        {/* Logo */}
        <motion.div
          className="logo-container glass"
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.6 }}
        >
          <svg
            width="80"
            height="80"
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle cx="50" cy="50" r="45" stroke="white" strokeWidth="2" opacity="0.3" />
            <path
              d="M30 50 L45 35 L60 50 L75 35"
              stroke="white"
              strokeWidth="3"
              strokeLinecap="round"
              strokeLinejoin="round"
              opacity="0.9"
            />
            <circle cx="45" cy="60" r="8" fill="white" opacity="0.9" />
            <circle cx="65" cy="65" r="6" fill="white" opacity="0.7" />
          </svg>
        </motion.div>

        {/* Title */}
        <motion.h1
          className="hero-title"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
        >
          SAGA Reykjavík
        </motion.h1>

        <motion.p
          className="hero-subtitle"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          Leitaðu í myndasafni sögunnar
        </motion.p>

        {/* Description */}
        <motion.p
          className="hero-description"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.6 }}
        >
          Öflug myndleit með gervigreind - finndu nákvæmlega það sem þú ert að leita að
        </motion.p>

        {/* CTA Button */}
        <motion.button
          className="glass-button glass-button-primary cta-button"
          onClick={() => navigate('/search')}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.7, duration: 0.6 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{ marginRight: '10px' }}
          >
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          Hefja leit
        </motion.button>

        {/* Stats */}
        <motion.div
          className="stats-container"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.6 }}
        >
          <div className="stat-item glass">
            <div className="stat-icon">⚡</div>
            <div className="stat-text">
              <div className="stat-value">Öflug</div>
              <div className="stat-label">AI Leit</div>
            </div>
          </div>
          <div className="stat-item glass">
            <div className="stat-icon">🇮🇸</div>
            <div className="stat-text">
              <div className="stat-value">Íslenska</div>
              <div className="stat-label">Stuðningur</div>
            </div>
          </div>
          <div className="stat-item glass">
            <div className="stat-icon">🎯</div>
            <div className="stat-text">
              <div className="stat-value">Nákvæm</div>
              <div className="stat-label">Niðurstöður</div>
            </div>
          </div>
        </motion.div>
      </motion.div>

      {/* Footer */}
      <motion.footer
        className="landing-footer"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 0.6 }}
      >
        <p>Byggt með CLIP &amp; Qdrant</p>
      </motion.footer>
    </div>
  )
}

export default LandingPage
