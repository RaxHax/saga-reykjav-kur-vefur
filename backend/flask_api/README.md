# Flask API Service

REST API service for SAGA Reykjavík Image Search.

## Structure

```
flask_api/
├── app.py              # Main application entry point
├── routes/             # API routes organized by function
│   ├── search.py       # Search endpoints
│   ├── health.py       # Health and stats endpoints
│   ├── ui.py           # UI/template routes
│   └── images.py       # Image serving
├── services/           # Business logic layer
│   ├── search_service.py      # Search operations
│   └── translation_service.py # Icelandic translation
└── requirements.txt    # Service dependencies
```

## Features

- **Semantic Search** - Text-to-image search using CLIP embeddings
- **Icelandic Support** - Automatic translation from Icelandic to English
- **Hybrid Search** - Combine semantic search with metadata filters
- **Statistics** - Database stats and health checks
- **Image Serving** - Direct image file serving
- **UI Templates** - Jinja2 template rendering

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Uses shared configuration from `backend/shared/config.py`.

Key settings:
- `FLASK_HOST` - Server host (default: 0.0.0.0)
- `FLASK_PORT` - Server port (default: 5000)
- `FLASK_DEBUG` - Debug mode (default: false)
- `ENABLE_ICELANDIC_TRANSLATION` - Enable translation (default: true)

## Running

```bash
# Development
python app.py

# Production (use gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

## API Endpoints

### Search

**POST /api/search**
```json
{
  "query": "mountain landscape",
  "limit": 50,
  "min_score": 0.0
}
```

**POST /api/search/icelandic**
```json
{
  "query": "fjallasýn",
  "limit": 50,
  "min_score": 0.0
}
```

**POST /api/search/hybrid**
```json
{
  "text_query": "sunset",
  "metadata_filter": {
    "folder": "/path/to/folder"
  },
  "weights": {
    "text": 0.7,
    "metadata": 0.3
  },
  "limit": 50
}
```

### Health & Stats

**GET /api/health**

Returns service health status.

**GET /api/stats**

Returns database statistics.

### Images

**GET /api/image/<path:filepath>**

Serves image files directly.

### UI Routes

- `GET /` - Landing page
- `GET /workspace` - Workspace UI
- `GET /projects` - Projects hub
- `GET /search/engines` - Search engines hub

## Architecture

### Routes Layer
Routes handle HTTP requests and responses. They are organized by functionality into separate blueprint modules.

### Services Layer
Business logic is separated into service classes:
- `SearchService` - Handles all search operations
- `TranslationService` - Manages Icelandic translation

### Shared Layer
Uses shared utilities from `backend/shared/`:
- `CLIPManager` - CLIP model management
- `QdrantManager` - Vector database operations
- `Config` - Centralized configuration
- `Logger` - Logging setup

## Development

### Adding New Routes

1. Create a new file in `routes/` directory
2. Define a Flask Blueprint
3. Implement route handlers
4. Register blueprint in `app.py`

Example:
```python
# routes/my_routes.py
from flask import Blueprint, jsonify

my_bp = Blueprint('my_routes', __name__, url_prefix='/api')

@my_bp.route("/my-endpoint", methods=["GET"])
def my_endpoint():
    return jsonify({"message": "Hello!"})
```

```python
# app.py
from flask_api.routes import my_bp
app.register_blueprint(my_bp)
```

### Adding New Services

1. Create a new file in `services/` directory
2. Implement service class
3. Use shared managers for CLIP/Qdrant
4. Import and use in routes

## Testing

```bash
pytest backend/tests/test_flask_api.py
```

## Deployment

### Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY backend/flask_api ./flask_api
COPY backend/shared ./shared
RUN pip install -r flask_api/requirements.txt
CMD ["python", "flask_api/app.py"]
```

### Environment Variables

Ensure all required environment variables are set in production:
- `FLASK_SECRET_KEY` - Secure random key
- `FLASK_DEBUG` - Set to false
- `CORS_ORIGINS` - Allowed origins
- CLIP and Qdrant configurations

## Troubleshooting

**Port already in use:**
```bash
# Change port in .env
FLASK_PORT=5001
```

**CLIP model not loading:**
- Check CUDA availability
- Verify model name and pretrained weights
- Check disk space for model downloads

**Translation not working:**
- Verify internet connection (required for Google Translate)
- Check `ENABLE_ICELANDIC_TRANSLATION` setting
- Review translation service logs
