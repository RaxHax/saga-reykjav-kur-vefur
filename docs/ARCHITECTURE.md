# SAGA Reykjavík - Architecture Guide

## Overview

SAGA Reykjavík is a modern image search platform built with a microservices architecture, featuring semantic search powered by CLIP (Contrastive Language-Image Pre-training) and vector similarity search via Qdrant.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                  │
│                          Port 3000                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  React Router                                       │    │
│  │  ├── HomePage (Honeycomb navigation)                │    │
│  │  ├── WorkspacePage (Search + Indexing)             │    │
│  │  └── ProjectsPage                                   │    │
│  │                                                      │    │
│  │  Components:                                        │    │
│  │  ├── SearchPanel                                    │    │
│  │  ├── IndexingPanel                                  │    │
│  │  ├── HoneycombGrid                                  │    │
│  │  └── ImageModal                                     │    │
│  └─────────────────────────────────────────────────────┘    │
│  Services:                                                  │
│  └── api.js (Axios → Flask + FastAPI)                      │
└────────┬──────────────────────────────────┬─────────────────┘
         │                                  │
         ▼                                  ▼
    ┌─────────────────┐          ┌──────────────────────┐
    │ FLASK API       │          │  INDEXING SERVICE    │
    │   Port 5000     │          │  FastAPI Port 8001   │
    │                 │          │                      │
    │ Routes:         │          │ Routes:              │
    │ ├── search.py   │          │ ├── jobs.py          │
    │ ├── health.py   │          │ └── health.py        │
    │ ├── ui.py       │          │                      │
    │ └── images.py   │          │ Services:            │
    │                 │          │ ├── job_manager.py   │
    │ Services:       │          │ └── indexer.py       │
    │ ├── search      │          │                      │
    │ └── translation │          │ Uses shared:         │
    │                 │          │ ├── CLIPManager      │
    │ Uses shared:    │          │ └── QdrantManager    │
    │ ├── CLIPManager │          └──────────────────────┘
    │ └── QdrantManager│
    └─────────────────┘
             │
             ├──────────────┬─────────────────┐
             │              │                 │
             ▼              ▼                 ▼
    ┌──────────────┐  ┌──────────┐  ┌──────────────┐
    │  CLIP Model  │  │  Qdrant  │  │  Translator  │
    │  (ViT-B-32)  │  │  Vector  │  │  (is → en)   │
    │              │  │   DB     │  │              │
    │ - Text emb.  │  │          │  │ Google       │
    │ - Image emb. │  │ 512-dim  │  │ Translate    │
    │              │  │ cosine   │  │              │
    └──────────────┘  └──────────┘  └──────────────┘
```

## Technology Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Framer Motion** - Animations
- **CSS Modules** - Styling

### Backend Services

#### Flask API
- **Flask** - Web framework
- **Flask-CORS** - CORS handling
- **Gunicorn** - Production WSGI server

#### Indexing Service
- **FastAPI** - Modern async API framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### AI/ML
- **OpenCLIP** - CLIP model implementation
- **PyTorch** - Deep learning framework
- **Pillow** - Image processing

### Database
- **Qdrant** - Vector similarity search engine
  - Local storage mode
  - Cosine similarity
  - 512-dimensional vectors

### Translation
- **deep-translator** - Google Translate API wrapper

## Directory Structure

```
saga-reykjav-kur-vefur/
├── backend/
│   ├── flask_api/          # REST API service
│   │   ├── app.py          # Main app
│   │   ├── routes/         # API endpoints
│   │   └── services/       # Business logic
│   ├── indexing_service/   # Indexing microservice
│   │   ├── main.py         # FastAPI app
│   │   ├── api/            # API routes
│   │   ├── services/       # Job management
│   │   ├── models/         # Pydantic models
│   │   └── utils/          # Utilities
│   ├── shared/             # Shared utilities
│   │   ├── config.py       # Configuration
│   │   ├── logger.py       # Logging
│   │   ├── clip_manager.py # CLIP singleton
│   │   └── qdrant_manager.py # Qdrant singleton
│   ├── tools/              # Utility scripts
│   └── tests/              # Backend tests
├── frontend/
│   ├── src/
│   │   ├── pages/          # Page components
│   │   ├── components/     # Reusable components
│   │   ├── services/       # API clients
│   │   ├── styles/         # Global styles
│   │   ├── hooks/          # Custom React hooks
│   │   ├── utils/          # Helper functions
│   │   └── store/          # State management
│   └── public/             # Static assets
├── scripts/                # Service management
├── docs/                   # Documentation
├── qdrant_storage/         # Vector database storage
├── static/                 # Static assets for templates
├── templates/              # Jinja2 templates
└── .env                    # Configuration
```

## Key Design Patterns

### 1. Singleton Pattern
**CLIP Manager and Qdrant Manager**

Both services use the same CLIP model and Qdrant client through singleton managers. This:
- Reduces memory usage (CLIP model loaded once)
- Ensures consistency
- Simplifies configuration

```python
# Anywhere in backend code
from shared.clip_manager import get_clip_manager
clip = get_clip_manager()  # Always returns same instance
embedding = clip.embed_text("query")
```

### 2. Service Layer Pattern
**Business logic separated from routes**

```python
# Routes handle HTTP
@search_bp.route("/search", methods=["POST"])
def search():
    data = request.json
    service = get_search_service()
    results = service.search(data["query"])
    return jsonify(results)

# Services handle business logic
class SearchService:
    def search(self, query):
        embedding = self.clip_manager.embed_text(query)
        return self.qdrant_manager.search(embedding)
```

### 3. Microservices Architecture
**Separation of concerns**

- **Flask API**: Handles search and UI serving
- **Indexing Service**: Manages long-running indexing jobs
- Both services are independent and can scale separately

### 4. Configuration Management
**Centralized configuration**

All configuration is in one place (`backend/shared/config.py`) and loaded from environment variables.

## Data Flow

### Search Flow

1. User enters query in frontend
2. Frontend sends POST to `/api/search`
3. Flask API receives request
4. `SearchService` calls `CLIPManager.embed_text()`
5. Text embedding generated (512-dim vector)
6. `QdrantManager.search()` finds similar images
7. Results formatted and returned to frontend
8. Frontend displays images in grid

### Indexing Flow

1. User clicks "Start Indexing"
2. Frontend sends POST to `/jobs/start`
3. Indexing Service creates async job
4. `JobManager` spawns background task
5. `ImageIndexer` processes images:
   - Read image file
   - Generate embedding via `CLIPManager`
   - Read paired .txt description
   - Create point with metadata
   - Batch upsert to Qdrant
6. Job progress tracked in real-time
7. Frontend polls `/jobs/{id}/status`
8. Progress updates displayed

### Translation Flow (Icelandic)

1. User enters Icelandic query
2. POST to `/api/search/icelandic`
3. `TranslationService.translate_if_icelandic()` detects Icelandic characters
4. Google Translate called to translate to English
5. English query used for search
6. Results returned with translation info

## Scalability Considerations

### Current Setup (Single Machine)
- Flask: Single process with threading
- Indexing: Single worker with async I/O
- Qdrant: Local storage
- CLIP: CPU or single GPU

### Production Scaling Options

#### 1. Horizontal Scaling
```
Load Balancer
    │
    ├── Flask API (x3)
    ├── Indexing Service (x2)
    └── Shared:
        ├── Redis (job queue)
        ├── Qdrant Cluster
        └── Shared storage for CLIP
```

#### 2. Database Scaling
- Move Qdrant to server mode
- Use Qdrant Cloud for managed service
- Enable sharding for large collections

#### 3. CLIP Model Optimization
- Use ONNX runtime for faster inference
- Quantization (FP16 or INT8)
- Model distillation for smaller models
- GPU acceleration in production

#### 4. Caching Layer
- Redis for search result caching
- CDN for image serving
- Browser caching for static assets

## Security Considerations

### Current Implementation
- CORS configured for specific origins
- No authentication (suitable for internal use)
- File path validation for image serving
- Environment variable for secrets

### Production Hardening
1. **Authentication**: Add JWT or OAuth2
2. **Rate Limiting**: Prevent API abuse
3. **Input Validation**: Sanitize all inputs
4. **HTTPS**: TLS certificates
5. **API Keys**: For external access
6. **File Access**: Restrict to specific directories

## Performance Metrics

### Search Performance
- Embedding generation: ~50ms (CPU) / ~5ms (GPU)
- Vector search: ~10ms (1M vectors)
- Total latency: < 100ms

### Indexing Performance
- Single image: ~100ms
- Batch (100 images): ~8s
- Large dataset (10K images): ~15 minutes

### Resource Usage
- CLIP model: ~2GB RAM
- Qdrant: ~500MB RAM + storage
- Per image: ~2KB vector + metadata

## Monitoring & Logging

### Logging Structure
```python
# Centralized logging
[2024-11-03 12:34:56] INFO - flask_api - Search query: 'sunset'
[2024-11-03 12:34:56] INFO - shared.clip_manager - Encoding text...
[2024-11-03 12:34:56] INFO - shared.qdrant_manager - Searching 512-dim vector
[2024-11-03 12:34:56] INFO - flask_api - Found 42 results
```

### Health Checks
- `GET /api/health` - Flask health
- `GET /health` - Indexing service health
- Checks: Model loaded, DB connected, disk space

### Metrics to Monitor
- Request rate and latency
- Search result quality
- Indexing throughput
- Model inference time
- Database size and query performance
- Error rates

## Development Workflow

### Local Development
```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your settings

# 3. Start services
./scripts/start-all-services.sh

# 4. Access
# Frontend: http://localhost:3000
# Flask API: http://localhost:5000
# Indexing API: http://localhost:8001
```

### Testing
```bash
# Backend tests
pytest backend/tests/

# Frontend tests
cd frontend && npm test

# Integration tests
python backend/tools/demo_all_features.py
```

### Code Style
- Python: PEP 8, Black formatter
- JavaScript: ESLint, Prettier
- Type hints: Python (Pydantic), TypeScript (optional)

## Deployment

### Docker Deployment
```yaml
version: '3.8'
services:
  flask-api:
    build: ./backend/flask_api
    ports:
      - "5000:5000"
    volumes:
      - ./qdrant_storage:/app/qdrant_storage
      - ./scraped_images:/app/scraped_images
    env_file: .env

  indexing-service:
    build: ./backend/indexing_service
    ports:
      - "8001:8001"
    volumes:
      - ./qdrant_storage:/app/qdrant_storage
      - ./scraped_images:/app/scraped_images
    env_file: .env

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_BASE_URL=http://flask-api:5000
      - VITE_INDEXING_API_BASE_URL=http://indexing-service:8001
```

## Future Enhancements

1. **Multi-modal Search**: Image-to-image search
2. **Advanced Filters**: Date, size, color filters
3. **User Accounts**: Personal collections
4. **Tagging System**: Manual and auto-tagging
5. **Export Features**: Download collections
6. **Analytics Dashboard**: Usage statistics
7. **Mobile App**: React Native client
8. **API Gateway**: Unified API entry point
9. **Message Queue**: RabbitMQ/Kafka for jobs
10. **GraphQL API**: Alternative to REST

## References

- [CLIP Paper](https://arxiv.org/abs/2103.00020)
- [OpenCLIP Documentation](https://github.com/mlfoundations/open_clip)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
