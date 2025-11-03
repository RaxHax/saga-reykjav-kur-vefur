# SAGA Reykjavík - Image Search Platform

Modern semantic image search platform powered by CLIP (Contrastive Language-Image Pre-training) and vector similarity search. Search images using natural language, with support for Icelandic translation and hybrid metadata filtering.

## ✨ Features

- 🔍 **Semantic Search** - Search images using natural language descriptions
- 🇮🇸 **Icelandic Support** - Automatic translation from Icelandic to English
- 🎯 **Hybrid Search** - Combine text search with metadata filters
- ⚡ **Fast Indexing** - Asynchronous batch image processing
- 📊 **Real-time Progress** - Track indexing jobs with live updates
- 🎨 **Modern UI** - Beautiful React interface with honeycomb navigation
- 🔄 **Job Management** - Pause, resume, and cancel indexing operations
- 📈 **Statistics** - Database insights and search analytics

## 🏗️ Architecture

This project uses a clean, modular microservices architecture:

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  React Frontend │ ───▶ │   Flask API      │ ───▶ │  CLIP + Qdrant  │
│  (Port 3000)    │      │   (Port 5000)    │      │  Vector Search  │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                 │
                                 │
                         ┌───────▼──────────┐
                         │ Indexing Service │
                         │   (Port 8001)    │
                         └──────────────────┘
```

### Directory Structure

```
saga-reykjav-kur-vefur/
├── backend/                    # All backend services
│   ├── flask_api/              # REST API service
│   │   ├── app.py              # Main application
│   │   ├── routes/             # API endpoints by function
│   │   └── services/           # Business logic layer
│   ├── indexing_service/       # FastAPI indexing microservice
│   │   ├── main.py             # FastAPI application
│   │   ├── api/                # API routes
│   │   └── services/           # Job management & indexing
│   ├── shared/                 # Shared utilities (singletons)
│   │   ├── config.py           # Centralized configuration
│   │   ├── logger.py           # Logging setup
│   │   ├── clip_manager.py     # CLIP model singleton
│   │   └── qdrant_manager.py   # Qdrant client singleton
│   ├── tools/                  # Utility scripts
│   └── tests/                  # Backend tests
├── frontend/                   # React application
│   └── src/
│       ├── pages/              # Page components
│       ├── components/         # Reusable UI components
│       ├── services/           # API clients
│       └── styles/             # Styling
├── scripts/                    # Service management scripts
├── docs/                       # Documentation
├── templates/                  # Jinja2 templates (for Flask)
└── static/                     # Static assets
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- 4GB+ RAM (8GB recommended for GPU)
- Optional: CUDA-capable GPU for faster processing

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd saga-reykjav-kur-vefur
```

2. **Setup Python environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Setup Frontend**
```bash
cd frontend
npm install
cd ..
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

### Running the Application

**Option 1: Start all services at once (Recommended)**
```bash
./scripts/start-all-services.sh
```

**Option 2: Start services individually**

Terminal 1 - Flask API:
```bash
cd backend/flask_api
python app.py
```

Terminal 2 - Indexing Service:
```bash
cd backend/indexing_service
uvicorn main:app --host 0.0.0.0 --port 8001
```

Terminal 3 - Frontend:
```bash
cd frontend
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Flask API**: http://localhost:5000
- **Indexing API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

## 📖 Usage

### 1. Index Your Images

1. Place images in a folder (default: `./scraped_images/`)
2. Optionally add `.txt` files with same name as images for descriptions
3. Navigate to the Workspace page
4. Click "Start Indexing" in the Indexing Panel
5. Monitor progress in real-time

### 2. Search Images

1. Enter a search query in natural language
   - English: "sunset over mountains"
   - Icelandic: "sólsetur yfir fjöllum" (automatically translated)
2. View results ranked by semantic similarity
3. Click images to view in fullscreen

### 3. Advanced Search

Use hybrid search to combine semantic search with metadata filters:

```bash
curl -X POST http://localhost:5000/api/search/hybrid \
  -H "Content-Type: application/json" \
  -d '{
    "text_query": "landscape",
    "metadata_filter": {"folder": "/path/to/specific/folder"},
    "weights": {"text": 0.7, "metadata": 0.3}
  }'
```

## 🔧 Configuration

Key environment variables (`.env` file):

### CLIP Model
```env
CLIP_MODEL=ViT-B-32
CLIP_PRETRAINED=laion2b_s34b_b79k
CLIP_DEVICE=auto  # auto, cpu, or cuda
```

### Services
```env
FLASK_PORT=5000
INDEXING_SERVICE_PORT=8001
```

### Qdrant Database
```env
QDRANT_STORAGE_PATH=./qdrant_storage
QDRANT_COLLECTION_NAME=image_search
QDRANT_VECTOR_SIZE=512
```

### Search Settings
```env
DEFAULT_SEARCH_LIMIT=50
MIN_SIMILARITY_SCORE=0.0
```

### Icelandic Support
```env
ENABLE_ICELANDIC_TRANSLATION=true
```

See `.env.example` for all available options.

## 🧪 Testing

Run backend tests:
```bash
cd backend/tests
pytest
```

Run feature demo:
```bash
cd backend/tools
python demo_all_features.py
```

## 📚 Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)** - Detailed system design
- **[Backend README](backend/README.md)** - Backend services overview
- **[Flask API README](backend/flask_api/README.md)** - REST API documentation
- **[Indexing Service README](backend/indexing_service/README.md)** - Indexing API docs
- **[Frontend README](frontend/README.md)** - Frontend development guide

## 🛠️ Development

### Project Organization

The codebase is organized for easy development:

- **Work on search features**: Edit `backend/flask_api/`
- **Work on indexing**: Edit `backend/indexing_service/`
- **Work on UI**: Edit `frontend/src/`
- **Add shared utilities**: Edit `backend/shared/`
- **Update configuration**: Edit `backend/shared/config.py`

### Adding New Features

1. **New API endpoint**: Add route in `backend/flask_api/routes/`
2. **New business logic**: Add service in `backend/flask_api/services/`
3. **New UI component**: Add to `frontend/src/components/`
4. **New page**: Add to `frontend/src/pages/`

### Code Style

- **Python**: PEP 8, use Black formatter
- **JavaScript**: ESLint + Prettier
- **Commits**: Conventional commits format

## 🚢 Deployment

### Docker Deployment

```bash
docker-compose up -d
```

### Production Checklist

- [ ] Set `FLASK_DEBUG=false`
- [ ] Generate secure `FLASK_SECRET_KEY`
- [ ] Configure `CORS_ORIGINS` for your domain
- [ ] Set up HTTPS/TLS certificates
- [ ] Configure reverse proxy (nginx)
- [ ] Set up monitoring and logging
- [ ] Enable database backups
- [ ] Configure firewall rules

## 📊 Performance

- **Search latency**: < 100ms
- **Indexing speed**: ~100 images/minute (CPU), ~500 images/minute (GPU)
- **Memory usage**: ~2GB for CLIP model + ~500MB for Qdrant
- **Storage**: ~2KB per indexed image

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Update documentation
6. Submit a pull request

## 📝 License

[Your License Here]

## 🙏 Acknowledgments

- [OpenCLIP](https://github.com/mlfoundations/open_clip) - CLIP implementation
- [Qdrant](https://qdrant.tech/) - Vector similarity search
- [FastAPI](https://fastapi.tiangolo.com/) - Modern API framework
- [React](https://react.dev/) - UI framework

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check the [documentation](docs/)
- Review [common issues](docs/TROUBLESHOOTING.md)

## 🗺️ Roadmap

- [ ] Image-to-image search
- [ ] User authentication
- [ ] Collection management
- [ ] Advanced filters (date, size, color)
- [ ] Export functionality
- [ ] Mobile application
- [ ] Multi-language support
- [ ] Analytics dashboard

---

Made with ❤️ for SAGA Reykjavík
