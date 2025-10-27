# SAGA Reykjavík - Admin Application

Powerful indexing management system with elegant glassmorphic UI.

## Features

- 📤 **Start Indexing Jobs** - Add new images to the database
- 📊 **Job Monitoring** - Real-time job status and progress
- ⏸️ **Job Control** - Pause, resume, or cancel jobs
- 📈 **Analytics** - View indexing statistics
- 🎨 **Beautiful UI** - iOS-inspired glassmorphic design

## Quick Start

### 1. Install Dependencies

**Frontend:**
```bash
cd frontend
npm install
```

**Backend (Indexing Service):**
```bash
cd ../indexing_service
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env`:
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
# Terminal 1 - Indexing Service
cd ../indexing_service
python main.py

# Terminal 2 - Admin Frontend
cd frontend
npm run dev
```

### 4. Open Application

- Admin UI: http://localhost:3001
- Indexing API: http://localhost:8001

## Project Structure

```
admin-app/
├── frontend/              # React + Vite frontend
│   ├── src/
│   │   ├── pages/        # Dashboard, Indexing, Jobs
│   │   ├── components/   # JobCard, etc.
│   │   ├── services/     # Job API service
│   │   └── styles/       # Glassmorphism styles
│   ├── package.json
│   └── vite.config.js
│
├── .env.example          # Environment configuration
├── start.sh              # Startup script
└── README.md
```

## Using the Admin Panel

### Starting an Indexing Job

1. Navigate to **Start Indexing**
2. Enter the full path to your image folder
3. Configure options:
   - **Recursive:** Include subfolders
   - **Skip Existing:** Skip already indexed images
   - **Extract Metadata:** Read .txt description files
4. Set batch size (10-500 images per batch)
5. Click **Start Indexing**

### Monitoring Jobs

1. Navigate to **View Jobs**
2. Filter by status: All, Running, Completed, Failed
3. View real-time progress with progress bars
4. See ETA for running jobs

### Job Controls

- **Pause:** Temporarily stop a running job
- **Resume:** Continue a paused job
- **Cancel:** Stop and cancel a job

## API Endpoints

### Jobs
- `POST /jobs/start` - Create new indexing job
- `GET /jobs` - List all jobs
- `GET /jobs/{id}/status` - Get job status
- `POST /jobs/{id}/pause` - Pause job
- `POST /jobs/{id}/resume` - Resume job
- `POST /jobs/{id}/cancel` - Cancel job
- `GET /jobs/{id}/logs` - Get job logs

### System
- `GET /health` - Health check

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| VITE_API_URL | http://localhost:8001 | Indexing service URL |

## Technologies

- **Frontend:** React, Vite, Framer Motion, React Router
- **Backend:** FastAPI, CLIP, Qdrant, asyncio
- **Styling:** Custom glassmorphism CSS

## License

SAGA Reykjavík © 2025
