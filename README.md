# 🖼️ SAGA Reykjavík - Image Search System

Modern, elegant image search platform with AI-powered semantic search and beautiful iOS-inspired glassmorphic design.

## 📋 Overview

This project has been refactored into **two separate applications**:

### 1. 👤 User Search App (`user-app/`)
Clean, elegant search interface for end users.
- Beautiful landing page
- Powerful AI-based image search
- Icelandic language support
- Responsive masonry grid layout
- Image preview modal

**Port:** Frontend (3000), API (5000)

### 2. ⚙️ Admin Management App (`admin-app/`)
Powerful backend management for indexing operations.
- Start new indexing jobs
- Monitor job progress in real-time
- Pause/resume/cancel jobs
- View job history and logs
- Analytics dashboard

**Port:** Frontend (3001), API (8001)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- pip and npm

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd saga-reykjav-kur-vefur
```

2. **Set up User Search App:**
```bash
cd user-app

# Backend
cd backend
pip install -r requirements.txt
cp ../.env.example .env
cd ..

# Frontend
cd frontend
npm install
cd ..
```

3. **Set up Admin App:**
```bash
cd ../admin-app

# Frontend
cd frontend
npm install
cp ../.env.example .env
cd ..

# Backend (Indexing Service)
cd ../indexing_service
pip install -r requirements.txt
cd ..
```

### Running the Applications

#### User Search App
```bash
cd user-app
./start.sh
```
Then open: http://localhost:3000

#### Admin Management App
```bash
cd admin-app
./start.sh
```
Then open: http://localhost:3001

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    SAGA Reykjavík System                      │
└──────────────────────────────────────────────────────────────┘

┌─────────────────────────┐    ┌─────────────────────────┐
│   User Search App       │    │   Admin Management App  │
│   (Port 3000)           │    │   (Port 3001)           │
│                         │    │                         │
│  ┌──────────────────┐  │    │  ┌──────────────────┐  │
│  │  Landing Page    │  │    │  │  Dashboard       │  │
│  │  Search Page     │  │    │  │  Start Indexing  │  │
│  │  Results Grid    │  │    │  │  View Jobs       │  │
│  │  Image Modal     │  │    │  │  Job Controls    │  │
│  └──────────────────┘  │    │  └──────────────────┘  │
└────────────┬────────────┘    └────────────┬───────────┘
             │                              │
             ↓                              ↓
    ┌────────────────┐           ┌────────────────────┐
    │ Flask Search   │           │ FastAPI Indexing   │
    │ API (5000)     │           │ Service (8001)     │
    │                │           │                    │
    │ - Search       │           │ - Job Management   │
    │ - Stats        │           │ - Progress Track   │
    │ - Images       │           │ - Pause/Resume     │
    └────────┬───────┘           └─────────┬──────────┘
             │                             │
             │                             │
             └─────────────┬───────────────┘
                           ↓
                  ┌─────────────────┐
                  │  Qdrant Vector  │
                  │    Database     │
                  │ (Image Vectors) │
                  └─────────────────┘
```

---

## 🎨 Features

### User Search App
- ✨ **Glassmorphic UI** - Beautiful iOS-inspired design
- 🔍 **AI Search** - CLIP-powered semantic search
- 🇮🇸 **Icelandic Support** - Automatic translation
- 🎯 **Smart Filters** - Adjust result count and minimum score
- 📱 **Responsive** - Works on all devices
- ⚡ **Fast** - Optimized with lazy loading

### Admin Management App
- 📤 **Easy Indexing** - Simple folder selection
- 📊 **Real-time Monitoring** - Live progress tracking
- 🎛️ **Job Control** - Pause, resume, cancel operations
- 📈 **Analytics** - View indexing statistics
- 🔄 **Auto-refresh** - Real-time updates
- 🎨 **Beautiful Dashboard** - Clean, modern interface

---

## 📂 Project Structure

```
saga-reykjav-kur-vefur/
├── user-app/                    # User-facing search application
│   ├── frontend/                # React frontend
│   │   ├── src/
│   │   │   ├── pages/          # Landing, Search
│   │   │   ├── components/     # ImageGrid, ImageModal
│   │   │   ├── services/       # API client
│   │   │   └── styles/         # Glassmorphism CSS
│   │   └── package.json
│   ├── backend/                 # Flask search API
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── start.sh
│   └── README.md
│
├── admin-app/                   # Admin management application
│   ├── frontend/                # React admin UI
│   │   ├── src/
│   │   │   ├── pages/          # Dashboard, Indexing, Jobs
│   │   │   ├── components/     # JobCard
│   │   │   ├── services/       # Job API client
│   │   │   └── styles/         # Glassmorphism CSS
│   │   └── package.json
│   ├── start.sh
│   └── README.md
│
├── indexing_service/            # FastAPI indexing service
│   ├── main.py
│   ├── api/routes.py
│   ├── services/
│   │   ├── indexer.py          # Image processing
│   │   └── job_manager.py      # Job orchestration
│   └── models/job.py
│
├── qdrant_storage/              # Vector database storage
│
└── README.md                    # This file
```

---

## 🔧 Configuration

### User App Environment (user-app/.env)
```env
FLASK_PORT=5000
CORS_ORIGINS=http://localhost:3000
CLIP_MODEL=ViT-B-32
QDRANT_STORAGE_PATH=../qdrant_storage
ENABLE_ICELANDIC_TRANSLATION=true
```

### Admin App Environment (admin-app/.env)
```env
VITE_API_URL=http://localhost:8001
```

### Indexing Service (indexing_service/.env)
```env
SERVICE_PORT=8001
CLIP_MODEL=ViT-B-32
QDRANT_STORAGE_PATH=../qdrant_storage
MAX_CONCURRENT_JOBS=3
```

---

## 🛠️ Technologies

### Frontend
- **Framework:** React 18
- **Build Tool:** Vite
- **Routing:** React Router v6
- **Animations:** Framer Motion
- **HTTP Client:** Axios
- **Grid Layout:** React Masonry CSS

### Backend
- **Search API:** Flask
- **Indexing Service:** FastAPI
- **AI Model:** OpenAI CLIP (ViT-B-32)
- **Vector DB:** Qdrant
- **Deep Learning:** PyTorch
- **Translation:** Deep Translator

### Design
- **Style:** Custom iOS Glassmorphism
- **Fonts:** SF Pro Display (system fonts)
- **Colors:** Dynamic gradients with floating orbs
- **Effects:** Backdrop blur, glass borders

---

## 📖 Usage

### For End Users (Search App)

1. Open http://localhost:3000
2. Click "Hefja leit" (Start Search)
3. Enter your search query in Icelandic or English
4. Adjust filters if needed
5. Click "Leita" (Search)
6. Browse beautiful masonry grid results
7. Click any image to view details

### For Administrators (Admin App)

1. Open http://localhost:3001
2. Click "Start Indexing"
3. Enter full path to image folder
4. Configure indexing options
5. Click "Start Indexing"
6. Monitor progress in "View Jobs"
7. Pause/resume/cancel as needed

---

## 🔍 API Documentation

### User Search API (Port 5000)

#### Search Images
```http
POST /api/search
Content-Type: application/json

{
  "query": "gamlar byggingar",
  "limit": 50,
  "min_score": 0.2
}
```

#### Search with Icelandic
```http
POST /api/search/icelandic
Content-Type: application/json

{
  "query": "gamlar byggingar",
  "limit": 50,
  "min_score": 0.2
}
```

### Admin Indexing API (Port 8001)

#### Start Job
```http
POST /jobs/start
Content-Type: application/json

{
  "image_folder": "C:\\Users\\user\\images",
  "options": {
    "recursive": true,
    "skip_existing": true,
    "batch_size": 100
  }
}
```

#### Get Job Status
```http
GET /jobs/{job_id}/status
```

#### Pause Job
```http
POST /jobs/{job_id}/pause
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both applications
5. Submit a pull request

---

## 📝 License

SAGA Reykjavík © 2025

---

## 🎉 Credits

Built with ❤️ using:
- [CLIP](https://github.com/openai/CLIP) by OpenAI
- [Qdrant](https://qdrant.tech/) Vector Database
- [React](https://react.dev/) & [Vite](https://vitejs.dev/)
- [Flask](https://flask.palletsprojects.com/) & [FastAPI](https://fastapi.tiangolo.com/)

---

## 📧 Support

For issues or questions, please open an issue on GitHub.

**Enjoy your beautiful, elegant image search system!** ✨
