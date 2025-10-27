# SAGA Reykjavík - Modern Visual Search Platform

A production-ready, AI-powered semantic image search platform designed for Icelandic visual archives. Features include dark-tech UI with hexagonal honeycomb design, Icelandic language support, hybrid search capabilities, and dedicated job management services.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Node](https://img.shields.io/badge/node-18+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🌟 Features

### Core Capabilities
- **Semantic Image Search** - CLIP-powered visual search using natural language queries
- **Icelandic Language Support** - Automatic translation for Icelandic queries with fallback
- **Hybrid Search** - Combine text semantics with metadata filters for precision
- **Real-time Indexing** - Background job processing with progress tracking
- **Modern React UI** - Dark-tech design with honeycomb feature cards and neon accents

### Technical Highlights
- **Dual Backend Architecture**
  - Flask web server for search and UI
  - FastAPI indexing service for job management
- **Vector Database** - Qdrant for efficient similarity search
- **Production Features**
  - Audit logging and job history
  - Configurable metadata fields
  - Environment-driven settings
  - CORS-enabled APIs
  - Health check endpoints

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Deployment](#-deployment)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + Vite)                   │
│  - Honeycomb landing page with 5 hexagonal feature cards     │
│  - Search workspace with masonry grid results                │
│  - Real-time indexing job management UI                      │
└────────────────┬────────────────────────────┬────────────────┘
                 │                            │
        ┌────────▼────────┐          ┌────────▼─────────┐
        │  Flask Backend  │          │ FastAPI Indexing │
        │    (Port 5000)  │          │   Service (8001) │
        │                 │          │                  │
        │ - Semantic      │          │ - Job Manager    │
        │   Search        │          │ - Progress Track │
        │ - Icelandic     │          │ - Audit Logs     │
        │ - Hybrid Search │          │ - Scheduling     │
        └────────┬────────┘          └────────┬─────────┘
                 │                            │
                 └────────────┬───────────────┘
                              │
                   ┌──────────▼──────────┐
                   │  CLIP ViT-B-32      │
                   │  (OpenCLIP)         │
                   │  512-dim embeddings │
                   └──────────┬──────────┘
                              │
                   ┌──────────▼──────────┐
                   │  Qdrant Vector DB   │
                   │  Cosine similarity  │
                   │  Local storage      │
                   └─────────────────────┘
```

## 🚀 Installation

### Prerequisites

- **Python 3.9+** with pip
- **Node.js 18+** with npm
- **Git**
- **CUDA** (optional, for GPU acceleration)

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd saga-reykjav-kur-vefur
```

2. **Create Python virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install Node dependencies**
```bash
npm install
```

3. **Configure frontend environment**
```bash
# Create frontend/.env.local
echo "VITE_API_BASE_URL=http://localhost:5000" > .env.local
echo "VITE_INDEXING_API_BASE_URL=http://localhost:8001" >> .env.local
```

## ⚡ Quick Start

### Run All Services

**Terminal 1 - Flask Backend:**
```bash
source venv/bin/activate
python app_enhanced.py
```

**Terminal 2 - Indexing Service:**
```bash
source venv/bin/activate
cd indexing_service
uvicorn main:app --host 0.0.0.0 --port 8001
```

**Terminal 3 - React Frontend:**
```bash
cd frontend
npm run dev
```

Access the application at `http://localhost:3000`

## ⚙️ Configuration

See `.env.example` for all available configuration options. Key settings:

```env
# Flask
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# CLIP Model
CLIP_MODEL=ViT-B-32
CLIP_DEVICE=auto  # auto, cuda, cpu

# Qdrant
QDRANT_STORAGE_PATH=./qdrant_storage
QDRANT_COLLECTION_NAME=image_search

# Icelandic Support
ENABLE_ICELANDIC_TRANSLATION=true

# Search
DEFAULT_SEARCH_LIMIT=50
TEXT_SEARCH_WEIGHT=0.7
METADATA_SEARCH_WEIGHT=0.3
```

## 📖 Usage

### Indexing Images

#### Via UI
1. Navigate to `/workspace`
2. Click "Indexing" tab
3. Enter folder path
4. Click "Start Indexing Job"

#### Via API
```bash
curl -X POST http://localhost:5000/api/index \
  -H "Content-Type: application/json" \
  -d '{"folder": "./scraped_images"}'
```

### Searching Images

#### Semantic Search
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "old buildings", "limit": 20}'
```

#### Icelandic Search
```bash
curl -X POST http://localhost:5000/api/search/icelandic \
  -H "Content-Type: application/json" \
  -d '{"query": "gamlar byggingar", "limit": 20}'
```

#### Hybrid Search
```bash
curl -X POST http://localhost:5000/api/search/hybrid \
  -H "Content-Type: application/json" \
  -d '{
    "text_query": "harbor scene",
    "metadata_filter": {"folder": "/path/to/collection"},
    "weights": {"text": 0.7, "metadata": 0.3}
  }'
```

## 📚 API Documentation

### Flask Backend (Port 5000)

- **POST /api/search** - Semantic search
- **POST /api/search/icelandic** - Icelandic language support
- **POST /api/search/hybrid** - Hybrid text + metadata search
- **POST /api/index** - Start indexing
- **GET /api/index/status** - Get indexing progress
- **GET /api/stats** - Database statistics
- **GET /api/health** - Health check

### Indexing Service (Port 8001)

- **POST /jobs/start** - Create indexing job
- **GET /jobs/{id}/status** - Get job status
- **POST /jobs/{id}/pause** - Pause job
- **POST /jobs/{id}/resume** - Resume job
- **POST /jobs/{id}/cancel** - Cancel job
- **GET /jobs/{id}/logs** - Get job logs
- **GET /jobs/history** - Get audit history

## 🛠️ Development

### Frontend Development
```bash
cd frontend
npm run dev     # Start dev server
npm run build   # Build for production
npm run preview # Preview build
```

### Backend Development
```bash
export FLASK_DEBUG=true
python app_enhanced.py

# Indexing Service with auto-reload
cd indexing_service
uvicorn main:app --reload --port 8001
```

## 📝 Customization

### Theme Variables
Edit `frontend/src/styles/theme.css`:
```css
:root {
  --color-accent-cyan: #5ac8fa;
  --color-accent-purple: #af52de;
  --hexagon-size: 180px;
}
```

### Icons
Replace icons in `frontend/src/components/icons/IconPlaceholders.jsx`

### Logo
Update logo in `HomePage.jsx` footer section

## 🐛 Troubleshooting

**CUDA Out of Memory**
- Set `CLIP_DEVICE=cpu` in `.env`

**Translation Errors**
- Set `TRANSLATION_FALLBACK=true`
- Or disable: `ENABLE_ICELANDIC_TRANSLATION=false`

**Port Conflicts**
- Change `FLASK_PORT` and `INDEXING_SERVICE_PORT` in `.env`

## 📄 License

MIT License

## 🙏 Acknowledgments

- OpenCLIP - CLIP model implementation
- Qdrant - Vector database
- React & Vite - Frontend framework
- Flask & FastAPI - Backend frameworks

---

Built with ❤️ for preserving Icelandic visual history
