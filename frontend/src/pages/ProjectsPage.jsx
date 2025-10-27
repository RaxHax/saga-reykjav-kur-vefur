import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import './ProjectsPage.css'

/**
 * ProjectsPage Component
 *
 * Placeholder page for project management features.
 * This can be expanded in the future to include:
 * - Image collection management
 * - Project-specific search scopes
 * - Collaboration features
 * - Export capabilities
 */
const ProjectsPage = () => {
  return (
    <div className="projects-page">
      {/* Navigation */}
      <nav className="projects-nav">
        <Link to="/" className="nav-logo-link">
          <h2 className="logo-text">SAGA</h2>
          <span className="logo-subtitle">Reykjavík</span>
        </Link>

        <Link to="/workspace" className="btn btn-ghost">
          Go to Workspace
        </Link>
      </nav>

      {/* Content */}
      <section className="projects-content">
        <motion.div
          className="placeholder-container"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
        >
          <div className="placeholder-icon">
            <svg width="120" height="120" viewBox="0 0 120 120" fill="none">
              <rect
                x="20"
                y="20"
                width="80"
                height="20"
                rx="4"
                stroke="currentColor"
                strokeWidth="3"
                fill="currentColor"
                opacity="0.3"
              />
              <rect
                x="20"
                y="50"
                width="80"
                height="20"
                rx="4"
                stroke="currentColor"
                strokeWidth="3"
                fill="currentColor"
                opacity="0.5"
              />
              <rect
                x="20"
                y="80"
                width="80"
                height="20"
                rx="4"
                stroke="currentColor"
                strokeWidth="3"
                fill="currentColor"
                opacity="0.7"
              />
            </svg>
          </div>

          <h1 className="placeholder-title">
            Projects Management
          </h1>

          <p className="placeholder-description">
            This section will allow you to organize your image collections into projects,
            manage collaborative workspaces, and configure project-specific search settings.
          </p>

          <div className="placeholder-features">
            <div className="feature-badge">
              <span className="badge-icon">📁</span>
              <span>Collection Management</span>
            </div>
            <div className="feature-badge">
              <span className="badge-icon">👥</span>
              <span>Team Collaboration</span>
            </div>
            <div className="feature-badge">
              <span className="badge-icon">🔍</span>
              <span>Project-Scoped Search</span>
            </div>
            <div className="feature-badge">
              <span className="badge-icon">📤</span>
              <span>Export & Sharing</span>
            </div>
          </div>

          <div className="placeholder-actions">
            <Link to="/workspace" className="btn btn-primary btn-lg">
              Start Searching Images
            </Link>
            <Link to="/" className="btn btn-secondary btn-lg">
              Back to Home
            </Link>
          </div>

          <div className="placeholder-note">
            <p>
              <strong>Note:</strong> This feature is currently under development.
              For now, you can use the main workspace to search and index your images.
            </p>
          </div>
        </motion.div>
      </section>
    </div>
  )
}

export default ProjectsPage
