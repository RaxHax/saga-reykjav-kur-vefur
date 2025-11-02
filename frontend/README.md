# SAGA Frontend - React Application

Modern, dark-tech React application built with Vite for the SAGA Reykjavík image search platform. Features a honeycomb landing page with 5 hexagonal feature cards, glassmorphism effects, neon accents, and a cohesive workspace UI.

![React](https://img.shields.io/badge/React-18.2-blue)
![Vite](https://img.shields.io/badge/Vite-5.0-purple)
![Framer Motion](https://img.shields.io/badge/Framer_Motion-11.0-pink)

## 🎨 Design System

### Visual Language

The frontend implements a **dark-tech aesthetic** with:

- **Dark Gradient Backgrounds** - Deep blues and purples (#05050b to #0f0f1a)
- **Neon Accent Colors** - Cyan (#5ac8fa), Purple (#af52de), Orange (#ff9500), Green (#7bffa7), Pink (#ff2d55)
- **Glassmorphism Effects** - Blurred, semi-transparent surfaces
- **Geometric Patterns** - Grid overlays and halftone effects
- **Hexagonal Honeycomb Layout** - 5 feature cards on landing page
- **Clean Typography** - Inter font family with varied weights
- **Smooth Animations** - Framer Motion for fluid transitions

### Theme Structure

All design tokens are centralized in `src/styles/theme.css`:

```css
:root {
  /* Colors */
  --color-bg-primary: #05050b;
  --color-accent-cyan: #5ac8fa;
  --color-accent-purple: #af52de;

  /* Typography */
  --font-size-base: 1rem;
  --font-weight-bold: 700;

  /* Spacing (8px grid) */
  --space-4: 1rem;
  --space-8: 2rem;

  /* Gradients */
  --gradient-cyan-purple: linear-gradient(135deg, #5ac8fa 0%, #af52de 100%);

  /* Effects */
  --glow-cyan: 0 0 20px rgba(90, 200, 250, 0.5);
}
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── App.jsx                      # Main router
│   ├── main.jsx                     # Entry point
│   │
│   ├── pages/
│   │   ├── HomePage.jsx             # Landing page with honeycomb
│   │   ├── HomePage.css             # Landing page styles
│   │   ├── WorkspacePage.jsx        # Search & indexing workspace
│   │   ├── WorkspacePage.css        # Workspace styles
│   │   └── ProjectsPage.jsx         # Projects hub (placeholder)
│   │
│   ├── components/
│   │   ├── HoneycombGrid.jsx        # 5-card honeycomb layout
│   │   ├── HoneycombGrid.css        # Honeycomb positioning
│   │   ├── HexagonCard.jsx          # Individual hex card
│   │   ├── HexagonCard.css          # Card styles with glows
│   │   ├── SearchPanel.jsx          # Search UI
│   │   ├── IndexingPanel.jsx        # Indexing job UI
│   │   ├── ImageModal.jsx           # Image detail viewer
│   │   └── icons/
│   │       └── IconPlaceholders.jsx # Configurable icon components
│   │
│   ├── services/
│   │   └── api.js                   # Axios API client
│   │
│   └── styles/
│       ├── theme.css                # Design system tokens
│       └── global.css               # Global styles & utilities
│
├── public/                          # Static assets
├── index.html                       # HTML template
├── vite.config.js                   # Vite configuration
├── package.json                     # Dependencies
└── README.md                        # This file
```

## 🚀 Getting Started

### Prerequisites

- **Node.js 18+** and npm
- Backend services running:
  - Flask backend on http://localhost:5000
  - Indexing service on http://localhost:8001

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment configuration
echo "VITE_API_BASE_URL=http://localhost:5000" > .env.local
echo "VITE_INDEXING_API_BASE_URL=http://localhost:8001" >> .env.local
```

### Development Server

```bash
npm run dev
```

Application will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

Build artifacts will be in `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## 🎯 Key Features

### 1. Landing Page (HomePage.jsx)

Modern landing page with **5 hexagonal feature cards** in honeycomb layout.

**Features:**
- Hero section with gradient background
- Animated honeycomb grid
- Configurable feature cards with neon glows
- Statistics section (CLIP, Qdrant, image count)
- Features overview grid
- Floating bottom-right logo with tooltip
- Footer with branding

**Customization Points:**
```jsx
const featureCards = [
  {
    title: 'AI Search',
    description: 'Semantic image search powered by CLIP',
    icon: <SearchIcon />,
    accentColor: '#5ac8fa',  // Cyan glow
    href: '/workspace',
  },
  // ... 4 more cards
]
```

### 2. Workspace (WorkspacePage.jsx)

Comprehensive search and indexing interface.

**Features:**
- Sidebar navigation with status badge
- Search panel with mode selection (semantic/hybrid/Icelandic)
- Masonry grid results layout
- Image modal with metadata viewer
- Indexing panel with real-time progress
- Job management (pause/resume/cancel)
- Statistics dashboard

**Search Modes:**
- **Semantic** - Natural language queries in English
- **Icelandic** - Automatic translation for Icelandic queries
- **Hybrid** - Text + metadata filters with configurable weights

### 3. Honeycomb Grid System

Responsive hexagonal card layout system.

**Layout Patterns:**
```
Desktop (5 cards):     Tablet (5 cards):      Mobile (5 cards):
   1     2                1   2                    1
  3   4                  3  4                      2
    5                      5                       3
                                                   4
                                                   5
```

**Implementation:**
```jsx
<HoneycombGrid cards={[
  { title, description, icon, accentColor, href },
  // ... 5 cards total
]} />
```

### 4. Hexagonal Cards

Individual cards with glow effects and animations.

**Features:**
- SVG hexagon border with gradient
- Configurable accent color
- Icon container with hover animations
- Glow effect on hover
- Click navigation
- Responsive sizing

**Accent Colors:**
- Cyan: `#5ac8fa`
- Purple: `#af52de`
- Orange: `#ff9500`
- Pink: `#ff2d55`
- Green: `#7bffa7`

## 🎨 Theming & Customization

### Changing Colors

Edit `src/styles/theme.css`:

```css
:root {
  /* Primary accent - affects most UI elements */
  --color-accent-cyan: #5ac8fa;

  /* Secondary accent - for variety */
  --color-accent-purple: #af52de;

  /* Background layers */
  --color-bg-primary: #05050b;
  --color-bg-secondary: #0a0a12;

  /* Gradients - used extensively */
  --gradient-cyan-purple: linear-gradient(135deg, #5ac8fa 0%, #af52de 100%);
}
```

### Customizing Icons

Icons are **SVG components** in `src/components/icons/IconPlaceholders.jsx`. Each icon is a React component returning inline SVG.

**To add a new icon:**

```jsx
// In IconPlaceholders.jsx
export const MyCustomIcon = () => (
  <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    {/* Your SVG paths here */}
    <path d="..." stroke="currentColor" strokeWidth="2.5" />
  </svg>
)
```

**To replace an existing icon:**

Simply update the SVG paths in the corresponding function. The `currentColor` value will automatically use the card's accent color.

**Available Icons:**
- `SearchIcon` - Magnifying glass with AI sparkle
- `ProjectsIcon` - Three stacked layers
- `ArchiveIcon` - Folder with document lines
- `IndexIcon` - Database with layers
- `AnalyticsIcon` - Bar chart with trend arrow
- `SettingsIcon` - Gear with spokes
- `VectorIcon` - Neural network nodes
- `UploadIcon` - Cloud with arrow

### Modifying Hexagon Layout

Edit `src/components/HoneycombGrid.css`:

```css
.honeycomb-grid {
  grid-template-columns: repeat(3, var(--hexagon-size));
  grid-template-rows: repeat(3, calc(var(--hexagon-size) * 0.6));
  gap: var(--hexagon-gap);
}

/* Position each card */
.honeycomb-cell.cell-1 {
  grid-column: 1 / 2;
  grid-row: 1 / 2;
}
```

### Logo Customization

The logo appears in **3 locations**:

1. **Floating Logo** (bottom-right)
   - File: `src/pages/HomePage.jsx` (lines 218-241)
   - Animated, with tooltip on hover

2. **Footer Logo**
   - File: `src/pages/HomePage.jsx` (lines 244-276)
   - Larger, with text

3. **Workspace Sidebar**
   - File: `src/pages/WorkspacePage.jsx`
   - Compact, clickable to home

**To update all logos:**
```jsx
// Replace the SVG in each location
<svg width="48" height="48" viewBox="0 0 48 48" fill="none">
  {/* Your logo paths */}
  <circle cx="24" cy="24" r="20" stroke="url(#logo-gradient)" strokeWidth="2" />
</svg>
```

### Typography

Edit `src/styles/theme.css` to change fonts:

```css
:root {
  /* Font family */
  --font-family-primary: 'Your Font', -apple-system, sans-serif;

  /* Font sizes (responsive) */
  --font-size-6xl: 3.75rem;  /* Hero titles */
  --font-size-base: 1rem;    /* Body text */

  /* Font weights */
  --font-weight-extrabold: 800;  /* Headlines */
  --font-weight-medium: 500;     /* UI text */
}
```

**Importing custom fonts:**
```css
/* In src/styles/global.css */
@import url('https://fonts.googleapis.com/css2?family=YourFont:wght@300;400;500;600;700;800&display=swap');
```

### Spacing System

Based on **8px grid**:

```css
:root {
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-4: 1rem;     /* 16px */
  --space-8: 2rem;     /* 32px */
  --space-16: 4rem;    /* 64px */
}
```

Use consistently:
```jsx
<div style={{ padding: 'var(--space-4)', marginTop: 'var(--space-8)' }}>
```

## 🔌 API Integration

### API Client (services/api.js)

Two axios instances for different backends:

```javascript
// Flask backend (search)
const flaskAPI = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  headers: { 'Content-Type': 'application/json' }
})

// Indexing service (jobs)
const indexingAPI = axios.create({
  baseURL: import.meta.env.VITE_INDEXING_API_BASE_URL || 'http://localhost:8001',
  headers: { 'Content-Type': 'application/json' }
})
```

### Available API Methods

**Search:**
```javascript
import { searchImages, hybridSearch, icelandicSearch } from './services/api'

// Semantic search
const results = await searchImages('old buildings', { limit: 50, minScore: 0.0 })

// Icelandic search
const results = await icelandicSearch('gamlar byggingar', { limit: 50 })

// Hybrid search
const results = await hybridSearch({
  textQuery: 'harbor',
  metadata: { folder: '/collection' },
  weights: { text: 0.7, metadata: 0.3 }
})
```

**Indexing:**
```javascript
import { startIndexing, getIndexingStatus, pauseIndexing } from './services/api'

// Start job
const job = await startIndexing('/path/to/images', {
  batchSize: 100,
  recursive: true
})

// Monitor progress
const status = await getIndexingStatus(job.job_id)
console.log(`Progress: ${status.progress.percentage}%`)

// Control job
await pauseIndexing(job.job_id)
await resumeIndexing(job.job_id)
await cancelIndexing(job.job_id)
```

**Statistics:**
```javascript
import { getStats } from './services/api'

const stats = await getStats()
console.log(`Indexed images: ${stats.count}`)
```

### Authentication (Future)

The API client includes auth token interceptors (currently unused):

```javascript
// Request interceptor (adds auth token)
flaskAPI.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor (handles 401)
flaskAPI.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      // Redirect to login
    }
    return Promise.reject(error)
  }
)
```

## 🎬 Animations

### Framer Motion

All animations use **Framer Motion** for fluid, spring-based transitions.

**Page Transitions:**
```jsx
<motion.div
  initial={{ opacity: 0, y: 30 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.7, delay: 0.2 }}
>
  {content}
</motion.div>
```

**Hover Effects:**
```jsx
<motion.div
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
  {card}
</motion.div>
```

**Staggered Children:**
```jsx
<motion.div
  initial="hidden"
  animate="visible"
  variants={{
    visible: { transition: { staggerChildren: 0.1 } }
  }}
>
  {cards.map(card => (
    <motion.div variants={itemVariants} />
  ))}
</motion.div>
```

### CSS Animations

Custom keyframe animations in `src/styles/global.css`:

```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse-glow {
  0%, 100% { opacity: 0.4; transform: scale(0.9); }
  50% { opacity: 0.6; transform: scale(1.1); }
}
```

## 📱 Responsive Design

### Breakpoints

Defined in `src/styles/theme.css`:

```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}
```

### Mobile-First Approach

All components are designed **mobile-first**, with enhancements for larger screens:

```css
/* Mobile default */
.hero-title {
  font-size: var(--font-size-3xl);
}

/* Tablet and up */
@media (min-width: 768px) {
  .hero-title {
    font-size: var(--font-size-5xl);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .hero-title {
    font-size: var(--font-size-6xl);
  }
}
```

### Honeycomb Responsive Behavior

- **Desktop (>1024px)**: 3-column grid with offset rows
- **Tablet (768-1024px)**: 2-column grid with offset
- **Mobile (<768px)**: Single column, vertical stack

## 🧪 Testing

### Manual Testing

```bash
# Start dev server
npm run dev

# Test features:
# 1. Navigate to http://localhost:5173
# 2. Verify landing page renders with 5 hexagon cards
# 3. Click "Start Searching" → should navigate to /workspace
# 4. Test search functionality
# 5. Test indexing panel
# 6. Check responsive behavior (resize window)
```

### Build Testing

```bash
# Build for production
npm run build

# Preview build
npm run preview

# Access at http://localhost:4173
```

## 🚀 Deployment

### Static Hosting (Netlify, Vercel)

```bash
# Build
npm run build

# Deploy dist/ folder
# Configure environment variables in hosting platform:
# VITE_API_BASE_URL=https://api.yourdomain.com
# VITE_INDEXING_API_BASE_URL=https://indexing.yourdomain.com
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/saga/dist;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy (optional)
    location /api/ {
        proxy_pass http://localhost:5000/api/;
    }

    location /indexing/ {
        proxy_pass http://localhost:8001/;
    }
}
```

### Docker

```dockerfile
# Build stage
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 🐛 Troubleshooting

### Issue: API requests fail with CORS error
**Solution:** Ensure Flask backend has CORS configured:
```python
# In Flask app
from flask_cors import CORS
CORS(app, origins=['http://localhost:5173'])
```

### Issue: Environment variables not loading
**Solution:**
- Ensure `.env.local` exists in `frontend/` directory
- Variable names must start with `VITE_`
- Restart dev server after changing .env

### Issue: Hexagon cards not displaying
**Solution:**
- Check that `featureCards` array has 5 items
- Verify icon imports in HomePage.jsx
- Check browser console for errors

### Issue: Animations jerky or not smooth
**Solution:**
- Ensure `framer-motion` is installed: `npm install framer-motion`
- Check browser dev tools for performance issues
- Reduce animation complexity if needed

## 📚 Component Library

### HoneycombGrid

**Props:**
```typescript
interface Card {
  title: string
  description: string
  icon: ReactNode
  accentColor: string
  href: string
}

interface HoneycombGridProps {
  cards: Card[]  // Must be exactly 5 cards
}
```

### HexagonCard

**Props:**
```typescript
interface HexagonCardProps {
  title: string
  description: string
  icon: ReactNode
  accentColor?: string  // Default: '#5ac8fa'
  href?: string         // Default: '#'
  delay?: number        // Animation delay
}
```

### SearchPanel

**Props:**
```typescript
interface SearchPanelProps {
  onSearch: (query: string, options: SearchOptions) => void
  isSearching: boolean
  searchMode: 'semantic' | 'hybrid' | 'icelandic'
  onModeChange: (mode: string) => void
}
```

### IndexingPanel

**Props:**
```typescript
interface IndexingPanelProps {
  onStartIndexing: (folder: string, options: IndexOptions) => void
  jobStatus: JobStatus | null
  isIndexing: boolean
}
```

## 🎓 Best Practices

### Component Organization
- One component per file
- Co-locate styles with components (.jsx + .css)
- Use barrel exports for cleaner imports

### Styling
- Prefer CSS variables for theming
- Use semantic class names (`.card-title`, not `.text-18-bold`)
- Keep specificity low (avoid deep nesting)

### Performance
- Use `React.memo()` for expensive components
- Optimize images (compress, use WebP)
- Lazy load routes with `React.lazy()`

### Accessibility
- Include ARIA labels on interactive elements
- Ensure keyboard navigation works
- Maintain sufficient color contrast

## 📄 License

MIT License - See main project LICENSE

---

**Questions?** Refer to the [main README](../README.md) or open an issue in the repository.
