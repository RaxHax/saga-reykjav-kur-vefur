# Backend Services

This directory contains all backend services for the SAGA Reykjavík Image Search application.

## Structure

```
backend/
├── flask_api/          # Flask REST API service
├── indexing_service/   # FastAPI indexing microservice
├── shared/             # Shared utilities and managers
├── tools/              # Utility scripts
└── tests/              # Backend tests
```

## Services

### Flask API (`flask_api/`)

Main REST API service that handles:
- Semantic image search
- Icelandic language support with translation
- Hybrid search (text + metadata)
- Health checks and statistics
- Image serving
- UI template rendering

**Port:** 5000

**Start:**
```bash
cd backend/flask_api
python app.py
```

### Indexing Service (`indexing_service/`)

Dedicated FastAPI microservice for image indexing:
- Asynchronous job management
- Real-time progress tracking
- Pause/resume/cancel operations
- Job history and audit logs
- Batch image processing

**Port:** 8001

**Start:**
```bash
cd backend/indexing_service
uvicorn main:app --host 0.0.0.0 --port 8001
```

### Shared Utilities (`shared/`)

Common utilities used by both services:
- **config.py** - Centralized configuration management
- **logger.py** - Logging setup
- **clip_manager.py** - CLIP model singleton
- **qdrant_manager.py** - Qdrant database singleton

These are designed as singletons to ensure both services use the same CLIP model and Qdrant connection.

### Tools (`tools/`)

Utility scripts:
- **webscraper.py** - Web scraping tool with GUI
- **demo_all_features.py** - Feature demonstration script

## Installation

Install all dependencies:
```bash
# From project root
pip install -r requirements.txt
```

Or install service-specific dependencies:
```bash
# Flask API only
pip install -r backend/flask_api/requirements.txt

# Indexing Service only
pip install -r backend/indexing_service/requirements.txt

# Shared utilities
pip install -r backend/shared/requirements.txt
```

## Configuration

All services use the same `.env` file in the project root. See `.env.example` for available options.

Key configuration sections:
- CLIP Model settings
- Qdrant database settings
- Flask configuration
- Indexing service settings
- CORS settings
- Logging settings

## Development

### Running Services Individually

**Flask API:**
```bash
cd backend/flask_api
python app.py
```

**Indexing Service:**
```bash
cd backend/indexing_service
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Running All Services

Use the startup script from project root:
```bash
./scripts/start-all-services.sh
```

### Testing

Run backend tests:
```bash
cd backend/tests
pytest
```

## Architecture

Both services share common resources:
1. **CLIP Model** - Singleton managed by `CLIPManager`
2. **Qdrant Database** - Singleton managed by `QdrantManager`
3. **Configuration** - Centralized in `Config` class
4. **Logging** - Standardized logging setup

This ensures consistency and reduces memory usage by not loading CLIP twice.

## API Documentation

### Flask API Endpoints

- `GET /` - Landing page
- `GET /workspace` - Workspace UI
- `POST /api/search` - Standard search
- `POST /api/search/icelandic` - Icelandic search
- `POST /api/search/hybrid` - Hybrid search
- `GET /api/stats` - Database statistics
- `GET /api/health` - Health check
- `GET /api/image/<path>` - Serve image

### Indexing API Endpoints

- `GET /` - Service info
- `POST /jobs/start` - Start indexing job
- `GET /jobs/{id}/status` - Get job status
- `POST /jobs/{id}/pause` - Pause job
- `POST /jobs/{id}/resume` - Resume job
- `POST /jobs/{id}/cancel` - Cancel job
- `GET /jobs/{id}/logs` - Get job logs
- `GET /jobs/history` - Get all jobs
- `GET /health` - Health check

## Contributing

When adding new features:
1. Add shared utilities to `backend/shared/`
2. Add Flask routes to `backend/flask_api/routes/`
3. Add FastAPI routes to `backend/indexing_service/api/routes.py`
4. Update tests in `backend/tests/`
5. Update this README
