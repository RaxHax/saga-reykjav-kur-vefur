import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import HoneycombGrid from '../components/HoneycombGrid'
import {
  SearchIcon,
  ProjectsIcon,
  ArchiveIcon,
  IndexIcon,
  AnalyticsIcon,
} from '../components/icons/IconPlaceholders'
import './HomePage.css'

/**
 * HomePage Component
 *
 * Modern dark-tech landing page with hero section and honeycomb feature cards.
 * Features:
 * - Animated hero section with gradient background
 * - 5 hexagonal feature cards in honeycomb layout
 * - Configurable icon placeholders
 * - Bottom-right logo placement
 * - Responsive design
 */
const HomePage = () => {
  // Feature cards configuration
  const featureCards = [
    {
      title: 'AI Search',
      description: 'Semantic image search powered by CLIP',
      icon: <SearchIcon />,
      accentColor: '#5ac8fa',
      href: '/workspace',
    },
    {
      title: 'Projects',
      description: 'Manage your image collections',
      icon: <ProjectsIcon />,
      accentColor: '#ff9500',
      href: '/projects',
    },
    {
      title: 'Archives',
      description: 'Browse Reykjavík historical photos',
      icon: <ArchiveIcon />,
      accentColor: '#af52de',
      href: '/workspace?tab=archives',
    },
    {
      title: 'Index',
      description: 'Index new image collections',
      icon: <IndexIcon />,
      accentColor: '#7bffa7',
      href: '/workspace?tab=indexing',
    },
    {
      title: 'Analytics',
      description: 'View search insights and stats',
      icon: <AnalyticsIcon />,
      accentColor: '#ff2d55',
      href: '/workspace?tab=analytics',
    },
  ]

  return (
    <div className="home-page">
      {/* Navigation */}
      <motion.nav
        className="main-nav"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="nav-container">
          <div className="nav-logo">
            <h2 className="logo-text">SAGA</h2>
            <span className="logo-subtitle">Reykjavík</span>
          </div>

          <div className="nav-actions">
            <Link to="/workspace" className="btn btn-ghost">
              Launch Workspace
            </Link>
          </div>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <section className="hero-section halftone-bg">
        <div className="hero-container">
          <motion.div
            className="hero-content"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.2 }}
          >
            <h1 className="hero-title">
              Visual Search for
              <br />
              <span className="text-gradient">Icelandic Archives</span>
            </h1>

            <p className="hero-description">
              Modern AI-powered platform for semantic image search.
              <br />
              Explore historical collections with natural language queries.
            </p>

            <motion.div
              className="hero-cta"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.8 }}
            >
              <Link to="/workspace" className="btn btn-primary">
                Start Searching
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  style={{ marginLeft: '8px' }}
                >
                  <path
                    d="M4 10h12m0 0l-4-4m4 4l-4 4"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </Link>

              <button className="btn btn-secondary">
                View Documentation
              </button>
            </motion.div>
          </motion.div>

          {/* Honeycomb Feature Cards */}
          <HoneycombGrid cards={featureCards} />

          {/* Stats Section */}
          <motion.div
            className="stats-section"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 1.2 }}
          >
            <div className="stat-card">
              <div className="stat-value">10K+</div>
              <div className="stat-label">Images Indexed</div>
            </div>
            <div className="stat-divider" />
            <div className="stat-card">
              <div className="stat-value">CLIP</div>
              <div className="stat-label">AI Model</div>
            </div>
            <div className="stat-divider" />
            <div className="stat-card">
              <div className="stat-value">Qdrant</div>
              <div className="stat-label">Vector DB</div>
            </div>
          </motion.div>
        </div>

        {/* Geometric background patterns */}
        <div className="hero-bg-pattern grid-pattern" />
      </section>

      {/* Features Overview Section */}
      <section className="features-overview section">
        <div className="container">
          <motion.div
            className="section-header"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="section-title">
              Modern Visual Search Platform
            </h2>
            <p className="section-description">
              Built for researchers, archivists, and historians working with Icelandic visual collections
            </p>
          </motion.div>

          <div className="features-grid">
            <FeatureItem
              icon="🔍"
              title="Semantic Search"
              description="Search images using natural language. Supports both Icelandic and English queries with automatic translation."
              delay={0.1}
            />
            <FeatureItem
              icon="⚡"
              title="Real-time Indexing"
              description="Monitor indexing jobs in real-time with progress tracking, logs, and scheduling capabilities."
              delay={0.2}
            />
            <FeatureItem
              icon="🎯"
              title="Hybrid Queries"
              description="Combine text search with metadata filters for precise results using configurable scoring weights."
              delay={0.3}
            />
            <FeatureItem
              icon="📊"
              title="Audit Trail"
              description="Complete history of indexing jobs, searches, and system operations for compliance and analysis."
              delay={0.4}
            />
          </div>
        </div>
      </section>

      {/* Footer with Logo */}
      <footer className="main-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-logo">
              {/* Logo placeholder - easily swappable */}
              <div className="logo-mark">
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                  <circle cx="24" cy="24" r="20" stroke="url(#logo-gradient)" strokeWidth="2" />
                  <path
                    d="M24 12L30 24L24 36L18 24L24 12Z"
                    fill="url(#logo-gradient)"
                    opacity="0.6"
                  />
                  <defs>
                    <linearGradient id="logo-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#5ac8fa" />
                      <stop offset="100%" stopColor="#af52de" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
              <div className="logo-text-footer">
                <strong>SAGA</strong> Reykjavík
              </div>
            </div>

            <div className="footer-info">
              <p>Modern AI-powered visual search for Icelandic archives</p>
              <p className="copyright">© 2025 SAGA Reykjavík. Built with CLIP & Qdrant.</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

// Helper component for feature items
const FeatureItem = ({ icon, title, description, delay }) => (
  <motion.div
    className="feature-item glass glass-hover"
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ duration: 0.5, delay }}
  >
    <div className="feature-icon">{icon}</div>
    <h3 className="feature-title">{title}</h3>
    <p className="feature-description">{description}</p>
  </motion.div>
)

export default HomePage
