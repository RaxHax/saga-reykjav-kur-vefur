# SAGA Reykjavík - User Search Application

Beautiful, elegant image search interface with iOS glassmorphism design.

## Features

- 🔍 **Powerful AI Search** - CLIP-based semantic image search
- 🇮🇸 **Icelandic Support** - Automatic translation for Icelandic queries
- 🎨 **Beautiful UI** - iOS-inspired glassmorphic design
- 📱 **Responsive** - Works perfectly on all devices
- ⚡ **Fast** - Optimized performance with lazy loading

## Quick Start

### 1. Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env` and adjust settings:
```bash
cp .env.example .env
```

### 3. Start Application

**Easy way (recommended):**
```bash
./start.sh
```

**Manual way:**
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 4. Open Application

- Frontend: http://localhost:3000
- API: http://localhost:5000

## Project Structure

```
user-app/
├── frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── pages/         # Landing & Search pages
│   │   ├── components/    # Reusable components
│   │   ├── services/      # API service
│   │   └── styles/        # Glassmorphism styles
│   ├── package.json
│   └── vite.config.js
│
├── backend/               # Flask search API
│   ├── app.py            # Main Flask application
│   └── requirements.txt
│
├── .env.example          # Environment configuration
├── start.sh              # Startup script
└── README.md
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| FLASK_PORT | 5000 | Flask server port |
| CORS_ORIGINS | http://localhost:3000 | Allowed CORS origins |
| CLIP_DEVICE | auto | Device for CLIP (cuda/cpu/auto) |
| QDRANT_STORAGE_PATH | ../qdrant_storage | Path to Qdrant database |
| ENABLE_ICELANDIC_TRANSLATION | true | Enable Icelandic support |

## API Endpoints

### Search
- `POST /api/search` - Basic search
- `POST /api/search/icelandic` - Search with Icelandic translation
- `GET /api/image/<path>` - Serve image file

### System
- `GET /api/health` - Health check
- `GET /api/stats` - Database statistics

## Technologies

- **Frontend:** React, Vite, Framer Motion, React Router
- **Backend:** Flask, CLIP, Qdrant, PyTorch
- **Styling:** Custom glassmorphism CSS

## License

SAGA Reykjavík © 2025
