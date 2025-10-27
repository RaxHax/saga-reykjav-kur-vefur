import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import DashboardPage from './pages/DashboardPage'
import IndexingPage from './pages/IndexingPage'
import JobsPage from './pages/JobsPage'

function App() {
  return (
    <Router>
      <div className="animated-bg">
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
        <div className="orb orb-3"></div>
      </div>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/indexing" element={<IndexingPage />} />
        <Route path="/jobs" element={<JobsPage />} />
      </Routes>
    </Router>
  )
}

export default App
