import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import './DashboardPage.css'

function DashboardPage() {
  const navigate = useNavigate()

  const cards = [
    {
      title: 'Start Indexing',
      description: 'Add new images to the database',
      icon: '📤',
      path: '/indexing',
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    },
    {
      title: 'View Jobs',
      description: 'Monitor indexing jobs and history',
      icon: '📊',
      path: '/jobs',
      gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    },
  ]

  return (
    <div className="dashboard-container">
      <motion.div
        className="dashboard-content"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        {/* Header */}
        <motion.div
          className="dashboard-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.6 }}
        >
          <div className="logo-badge glass">
            <svg
              width="40"
              height="40"
              viewBox="0 0 100 100"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <circle cx="50" cy="50" r="35" stroke="white" strokeWidth="2" opacity="0.5" />
              <path
                d="M35 50 L45 40 L55 50 L65 40"
                stroke="white"
                strokeWidth="3"
                strokeLinecap="round"
                opacity="0.9"
              />
              <circle cx="45" cy="58" r="6" fill="white" opacity="0.9" />
              <circle cx="58" cy="62" r="5" fill="white" opacity="0.7" />
            </svg>
          </div>
          <h1 className="dashboard-title">SAGA Admin</h1>
          <p className="dashboard-subtitle">Indexing Management System</p>
        </motion.div>

        {/* Cards Grid */}
        <div className="cards-grid">
          {cards.map((card, index) => (
            <motion.div
              key={card.path}
              className="dashboard-card glass"
              style={{ background: card.gradient }}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 + index * 0.1, duration: 0.6 }}
              whileHover={{ scale: 1.05, y: -10 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate(card.path)}
            >
              <div className="card-icon">{card.icon}</div>
              <h3 className="card-title">{card.title}</h3>
              <p className="card-description">{card.description}</p>
              <div className="card-arrow">
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
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Info Box */}
        <motion.div
          className="info-box glass"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.6 }}
        >
          <div className="info-icon">ℹ️</div>
          <div className="info-content">
            <h4>Admin Panel</h4>
            <p>
              Manage image indexing jobs for the SAGA Reykjavík search system.
              Start new indexing jobs or monitor existing ones.
            </p>
          </div>
        </motion.div>
      </motion.div>
    </div>
  )
}

export default DashboardPage
