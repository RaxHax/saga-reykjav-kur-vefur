# SAGA Indexing Service

FastAPI-based asynchronous image indexing microservice for the SAGA Reykjavík platform. Provides dedicated job management, progress tracking, audit logging, and scheduling capabilities separate from the main Flask web application.

## 🎯 Purpose

The indexing service is a **production-ready microservice** designed to handle computationally intensive image indexing operations without blocking the main web server. It provides:

- **Async Operations** - Non-blocking I/O for efficient resource usage
- **Job Queuing** - Automatic queuing when concurrent job limits are reached
- **Progress Tracking** - Real-time progress updates with ETA calculations
- **Job Management** - Pause, resume, cancel operations
- **Audit Trail** - Complete history of all indexing operations
- **Concurrent Control** - Configurable limits on simultaneous jobs

## 🏗️ Architecture

```
┌──────────────────────────────────────────┐
│       FastAPI Application (Port 8001)     │
├──────────────────────────────────────────┤
│                                           │
│  ┌─────────────┐      ┌──────────────┐  │
│  │   API       │──────│ Job Manager  │  │
│  │   Routes    │      │              │  │
│  └─────────────┘      │ - Create     │  │
│                       │ - Monitor    │  │
│                       │ - Control    │  │
│                       └──────┬───────┘  │
│                              │          │
│                       ┌──────▼───────┐  │
│                       │  Image       │  │
│                       │  Indexer     │  │
│                       │              │  │
│                       │ - CLIP       │  │
│                       │ - Qdrant     │  │
│                       └──────────────┘  │
└──────────────────────────────────────────┘
```

## 📋 API Endpoints

### Job Management

#### **POST /jobs/start**
Create and start a new indexing job.

**Request Body:**
```json
{
  "folder_path": "/path/to/images",
  "options": {
    "batch_size": 100,
    "recursive": true,
    "skip_existing": false,
    "image_formats": ["jpg", "jpeg", "png", "webp"]
  }
}
```

**Response:**
```json
{
  "job_id": "job_123abc",
  "status": "pending",
  "message": "Job created successfully"
}
```

#### **GET /jobs/{job_id}/status**
Get current status and progress of a job.

**Response:**
```json
{
  "job_id": "job_123abc",
  "status": "running",
  "folder_path": "/path/to/images",
  "progress": {
    "processed": 450,
    "total": 1000,
    "percentage": 45.0,
    "eta_seconds": 120
  },
  "created_at": "2025-10-30T10:00:00Z",
  "started_at": "2025-10-30T10:00:05Z",
  "error": null
}
```

**Status Values:**
- `pending` - Job created, waiting to start
- `running` - Currently processing images
- `paused` - Temporarily paused by user
- `completed` - Successfully finished
- `failed` - Encountered an error
- `cancelled` - Cancelled by user

#### **GET /jobs**
List all indexing jobs with optional filtering.

**Query Parameters:**
- `status` (optional) - Filter by job status
- `limit` (optional, default: 100) - Max jobs to return
- `offset` (optional, default: 0) - Pagination offset

**Response:**
```json
{
  "jobs": [
    {
      "job_id": "job_123abc",
      "status": "completed",
      "folder_path": "/path/to/images",
      "progress": {
        "processed": 1000,
        "total": 1000,
        "percentage": 100.0
      },
      "created_at": "2025-10-30T10:00:00Z"
    }
  ],
  "total": 25,
  "limit": 100,
  "offset": 0
}
```

#### **POST /jobs/{job_id}/pause**
Pause a running job.

**Response:**
```json
{
  "job_id": "job_123abc",
  "status": "paused",
  "message": "Job paused successfully"
}
```

#### **POST /jobs/{job_id}/resume**
Resume a paused job.

**Response:**
```json
{
  "job_id": "job_123abc",
  "status": "running",
  "message": "Job resumed successfully"
}
```

#### **POST /jobs/{job_id}/cancel**
Cancel a job (running or paused).

**Response:**
```json
{
  "job_id": "job_123abc",
  "status": "cancelled",
  "message": "Job cancelled successfully"
}
```

### Monitoring

#### **GET /jobs/{job_id}/logs**
Retrieve logs for a specific job.

**Query Parameters:**
- `limit` (optional, default: 100) - Max log entries
- `level` (optional) - Filter by log level (INFO, WARNING, ERROR)

**Response:**
```json
{
  "job_id": "job_123abc",
  "logs": [
    {
      "timestamp": "2025-10-30T10:00:05Z",
      "level": "INFO",
      "message": "Started indexing folder: /path/to/images"
    },
    {
      "timestamp": "2025-10-30T10:00:10Z",
      "level": "INFO",
      "message": "Processed batch 1/10 (100 images)"
    }
  ],
  "total": 25
}
```

#### **GET /jobs/history**
Get audit trail of all job operations.

**Query Parameters:**
- `job_id` (optional) - Filter by specific job
- `action` (optional) - Filter by action type (created, started, paused, resumed, cancelled, completed, failed)
- `limit` (optional, default: 100)
- `offset` (optional, default: 0)

**Response:**
```json
{
  "history": [
    {
      "job_id": "job_123abc",
      "action": "created",
      "timestamp": "2025-10-30T10:00:00Z",
      "details": {
        "folder_path": "/path/to/images",
        "options": {}
      }
    },
    {
      "job_id": "job_123abc",
      "action": "completed",
      "timestamp": "2025-10-30T10:05:00Z",
      "details": {
        "images_processed": 1000,
        "duration_seconds": 300
      }
    }
  ],
  "total": 50
}
```

### System

#### **GET /health**
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "saga-indexing-service",
  "version": "2.0.0",
  "clip_model": "ViT-B-32",
  "device": "cuda",
  "active_jobs": 2,
  "total_jobs": 47
}
```

#### **GET /**
Service information.

**Response:**
```json
{
  "service": "SAGA Indexing Service",
  "version": "2.0.0",
  "status": "running"
}
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Qdrant running (or configured storage path)
- CLIP model downloaded (automatic on first run)

### Installation

```bash
# From project root
cd indexing_service

# Install dependencies (should already be installed if you ran pip install -r requirements.txt from root)
pip install -r ../requirements.txt
```

### Running the Service

**Development Mode (with auto-reload):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

**Production Mode:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --workers 1
```

**With Custom Settings:**
```bash
export INDEXING_SERVICE_PORT=9000
export MAX_CONCURRENT_INDEXING_JOBS=5
uvicorn main:app --host 0.0.0.0 --port 9000
```

## ⚙️ Configuration

Configuration is loaded from environment variables (see `.env` in project root):

```env
# Service Configuration
INDEXING_SERVICE_HOST=0.0.0.0
INDEXING_SERVICE_PORT=8001
INDEXING_SERVICE_WORKERS=1

# Job Management
MAX_CONCURRENT_INDEXING_JOBS=3
INDEX_BATCH_SIZE=100

# CLIP Configuration
CLIP_MODEL=ViT-B-32
CLIP_PRETRAINED=laion2b_s34b_b79k
CLIP_DEVICE=auto

# Qdrant Configuration
QDRANT_STORAGE_PATH=./qdrant_storage
QDRANT_COLLECTION_NAME=image_search
QDRANT_VECTOR_SIZE=512

# Logging
LOG_LEVEL=INFO
ENABLE_AUDIT_LOG=true
```

## 📦 Components

### Services

#### **ImageIndexer** (`services/indexer.py`)
Handles CLIP model inference and Qdrant integration.

**Key Methods:**
- `initialize()` - Load CLIP model and connect to Qdrant
- `index_image(image_path, description)` - Index a single image
- `batch_index_images(folder, options, progress_callback)` - Batch indexing with progress tracking

**Features:**
- Async I/O for non-blocking operations
- Automatic .txt description file discovery
- Batch processing for efficiency
- Progress callbacks for real-time updates

#### **JobManager** (`services/job_manager.py`)
Manages job lifecycle and concurrency control.

**Key Methods:**
- `create_job(folder_path, options)` - Create new job
- `get_job(job_id)` - Retrieve job details
- `list_jobs(filters)` - List jobs with filtering
- `pause_job(job_id)` - Pause execution
- `resume_job(job_id)` - Resume execution
- `cancel_job(job_id)` - Cancel job

**Features:**
- Concurrent job limiting (default: 3 max)
- Automatic queuing when limit reached
- Job state machine (pending → running → completed/failed)
- Async task management

### Models

#### **Job** (`models/job.py`)
Complete job entity with all metadata.

**Fields:**
- `job_id` - Unique identifier
- `status` - Current status (JobStatus enum)
- `folder_path` - Path being indexed
- `options` - IndexingOptions configuration
- `progress` - JobProgress tracking
- `created_at` - Timestamp
- `started_at` - Timestamp (nullable)
- `completed_at` - Timestamp (nullable)
- `error` - Error message (nullable)
- `history` - List of JobHistoryEntry

#### **IndexingOptions** (`models/job.py`)
Configuration for indexing behavior.

**Fields:**
- `batch_size` - Images per batch (default: 100)
- `image_formats` - Supported formats (default: ["jpg", "jpeg", "png", "webp"])
- `recursive` - Traverse subdirectories (default: true)
- `skip_existing` - Skip already indexed images (default: false)

#### **JobProgress** (`models/job.py`)
Real-time progress tracking.

**Fields:**
- `processed` - Images processed so far
- `total` - Total images to process
- `percentage` - Completion percentage (0-100)
- `eta_seconds` - Estimated time remaining

## 🧪 Testing

### Manual Testing

```bash
# Start the service
uvicorn main:app --port 8001

# Test health check
curl http://localhost:8001/health

# Start an indexing job
curl -X POST http://localhost:8001/jobs/start \
  -H "Content-Type: application/json" \
  -d '{
    "folder_path": "/path/to/images",
    "options": {
      "batch_size": 50,
      "recursive": true
    }
  }'

# Get job status (replace JOB_ID)
curl http://localhost:8001/jobs/JOB_ID/status

# Pause job
curl -X POST http://localhost:8001/jobs/JOB_ID/pause

# Resume job
curl -X POST http://localhost:8001/jobs/JOB_ID/resume

# List all jobs
curl http://localhost:8001/jobs
```

### Using the Demo Script

```bash
# From project root
python demo_all_features.py --demo-data-path ./demo_images
```

## 🔧 Advanced Usage

### Custom Job Options

```python
import requests

payload = {
    "folder_path": "/large/dataset",
    "options": {
        "batch_size": 200,           # Larger batches for speed
        "recursive": True,            # Include subdirectories
        "skip_existing": True,        # Don't re-index
        "image_formats": ["jpg", "png"]  # Only these formats
    }
}

response = requests.post("http://localhost:8001/jobs/start", json=payload)
job_id = response.json()["job_id"]

# Poll for status
while True:
    status = requests.get(f"http://localhost:8001/jobs/{job_id}/status").json()
    if status["status"] in ["completed", "failed", "cancelled"]:
        break
    time.sleep(2)
```

### Monitoring Multiple Jobs

```python
# Get all running jobs
response = requests.get("http://localhost:8001/jobs?status=running")
running_jobs = response.json()["jobs"]

for job in running_jobs:
    print(f"Job {job['job_id']}: {job['progress']['percentage']:.1f}% complete")
```

## 🐛 Troubleshooting

### Issue: Jobs stuck in "pending" status
**Cause:** Maximum concurrent jobs reached (default: 3)
**Solution:** Wait for other jobs to complete, or increase `MAX_CONCURRENT_INDEXING_JOBS`

### Issue: CUDA out of memory
**Cause:** Batch size too large for GPU memory
**Solution:** Reduce `INDEX_BATCH_SIZE` or set `CLIP_DEVICE=cpu`

### Issue: Jobs failing silently
**Cause:** Permissions or path issues
**Solution:** Check job logs with `GET /jobs/{id}/logs`

### Issue: Slow indexing performance
**Solutions:**
- Increase `INDEX_BATCH_SIZE` (if memory allows)
- Enable GPU: `CLIP_DEVICE=cuda`
- Use faster storage (SSD)
- Reduce `MAX_CONCURRENT_INDEXING_JOBS` to 1 to avoid CPU contention

## 📊 Performance Tuning

### Batch Size
- **Small batches (50-100)**: Lower memory, more frequent updates
- **Large batches (200-500)**: Higher memory, better throughput

### Concurrency
- **Single job (1)**: Maximum per-job performance
- **Multiple jobs (3-5)**: Better resource utilization for many small datasets

### Device Selection
- **CPU**: Slower but works everywhere
- **CUDA**: ~5-10x faster on modern GPUs
- **Auto**: Automatically uses CUDA if available

## 📝 Development Notes

### Adding New Job Types

1. Extend `JobStatus` enum in `models/job.py`
2. Add handler in `JobManager._start_job_task()`
3. Update API routes in `api/routes.py`

### Custom Progress Callbacks

```python
# In services/indexer.py
async def batch_index_images(self, folder, options, progress_callback=None):
    # ...
    if progress_callback:
        await progress_callback(processed, total, message)
```

### Logging

Logs are structured for easy parsing:
```python
logger.info("Job started", extra={
    "job_id": job_id,
    "folder_path": folder_path,
    "options": options.dict()
})
```

## 🚢 Deployment

### Docker

```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY indexing_service/ ./indexing_service/
WORKDIR /app/indexing_service

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Systemd Service

```ini
[Unit]
Description=SAGA Indexing Service
After=network.target

[Service]
Type=simple
User=saga
WorkingDirectory=/opt/saga/indexing_service
Environment="PATH=/opt/saga/venv/bin"
ExecStart=/opt/saga/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📄 License

MIT License - See main project README

## 🙏 Acknowledgments

- FastAPI for the async web framework
- Uvicorn for ASGI server
- OpenCLIP for CLIP implementation
- Qdrant for vector database

---

**Need help?** Open an issue in the main repository or check the [main README](../README.md) for general platform documentation.
