# SAGA Reykjavík - Windows Setup Guide

Quick start guide for Windows users.

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Python 3.9 or higher**
   - Download from: https://www.python.org/downloads/
   - ✅ During installation, check "Add Python to PATH"

2. **Node.js 18 or higher**
   - Download from: https://nodejs.org/
   - ✅ The installer will automatically add Node to PATH

3. **Git** (optional, if cloning from repository)
   - Download from: https://git-scm.com/download/win

## 🚀 Quick Start (3 Steps)

### Step 1: Run Setup (First Time Only)

Double-click `setup.bat` or run in Command Prompt:

```cmd
setup.bat
```

This will:
- ✅ Create Python virtual environment
- ✅ Install all Python dependencies
- ✅ Install all Node.js dependencies
- ✅ Create configuration files (.env and frontend/.env.local)
- ✅ Create demo_images folder

**Time:** ~5-10 minutes (depending on internet speed)

### Step 2: Start the Application

Double-click `start.bat` or run in Command Prompt:

```cmd
start.bat
```

This will:
- ✅ Open 3 separate windows for each service
- ✅ Automatically open your browser to http://localhost:5173

**Services started:**
- Flask Backend → Port 5000
- Indexing Service → Port 8001
- React Frontend → Port 5173

### Step 3: Use the Application

The application will automatically open in your default browser at:
**http://localhost:5173**

You can now:
- Search for images using natural language
- Index new image collections
- Manage indexing jobs

## 🛑 Stopping the Application

### Option 1: Close Windows
Simply close the 3 service windows that were opened by `start.bat`

### Option 2: Run Stop Script
Double-click `stop.bat` or run:

```cmd
stop.bat
```

This will automatically kill all service processes.

## 🧪 Testing

### Quick API Test

Run `quick_test.bat` to test all API endpoints:

```cmd
quick_test.bat
```

Expected output:
```
=== Flask Backend Tests ===
Testing Flask Health...      PASS
Testing Database Stats...    PASS
Testing Semantic Search...   PASS
...

Total Tests: 7
Passed: 7
Failed: 0
```

### Comprehensive Demo

Run the Python demo script:

```cmd
venv\Scripts\activate
python demo_all_features.py --demo-data-path demo_images
```

This interactive demo will walk you through all features.

## 📁 Windows Batch Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `setup.bat` | Initial setup and installation | **First time only** |
| `start.bat` | Start all services | **Every time you want to run the app** |
| `stop.bat` | Stop all services | When you want to stop the app |
| `quick_test.bat` | Test API endpoints | To verify services are working |

## ⚙️ Configuration

### Environment Variables

Edit `.env` file to configure:

```env
# Flask
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# CLIP Model
CLIP_DEVICE=auto        # auto, cuda, or cpu
CLIP_MODEL=ViT-B-32

# Qdrant
QDRANT_STORAGE_PATH=./qdrant_storage

# Icelandic Support
ENABLE_ICELANDIC_TRANSLATION=true
```

### Frontend Configuration

Edit `frontend\.env.local` to change API URLs:

```env
VITE_API_BASE_URL=http://localhost:5000
VITE_INDEXING_API_BASE_URL=http://localhost:8001
```

## 🐛 Troubleshooting

### "Python is not installed or not in PATH"

**Solution:**
1. Install Python from https://www.python.org/
2. During installation, check ✅ "Add Python to PATH"
3. Restart Command Prompt
4. Run `setup.bat` again

### "Node.js is not installed or not in PATH"

**Solution:**
1. Install Node.js from https://nodejs.org/
2. Restart Command Prompt
3. Run `setup.bat` again

### Port Already in Use

**Error:** `Address already in use: 5000` or similar

**Solution:**
```cmd
# Run stop.bat to kill any running services
stop.bat

# Then start again
start.bat
```

### CUDA Out of Memory

**Solution:** Edit `.env` and set:
```env
CLIP_DEVICE=cpu
```

### Services Start But Frontend Shows Connection Error

**Check if all services are running:**
1. Open browser to http://localhost:5000/api/health (Flask)
2. Open browser to http://localhost:8001/health (Indexing)
3. Check if all 3 service windows are still open

**Solution:**
```cmd
# Stop everything
stop.bat

# Check configuration
notepad frontend\.env.local

# Start again
start.bat
```

### Virtual Environment Not Found

**Error:** `Virtual environment not found!`

**Solution:**
```cmd
# Run setup first
setup.bat

# Then start
start.bat
```

## 📂 Directory Structure After Setup

```
saga-reykjav-kur-vefur/
├── venv/                    # Python virtual environment
├── frontend/
│   ├── node_modules/        # Node.js dependencies
│   └── .env.local           # Frontend configuration
├── .env                     # Backend configuration
├── demo_images/             # Demo image folder
├── qdrant_storage/          # Vector database (created on first run)
│
├── setup.bat                # Setup script
├── start.bat                # Start script
├── stop.bat                 # Stop script
└── quick_test.bat           # Test script
```

## 🎯 Common Tasks

### Adding Images to Index

1. Copy your images to any folder (e.g., `C:\MyImages\`)
2. Start the application (`start.bat`)
3. Go to http://localhost:5173
4. Click "Indexing" tab in workspace
5. Enter folder path: `C:\MyImages`
6. Click "Start Indexing Job"
7. Watch progress in real-time

### Searching for Images

1. Go to the workspace (http://localhost:5173/workspace)
2. Select search mode:
   - **Semantic** - Natural language (English)
   - **Icelandic** - Queries in Icelandic
   - **Hybrid** - Text + metadata filters
3. Enter your query (e.g., "old buildings")
4. Press Enter or click Search
5. Browse results in the masonry grid

### Viewing Database Statistics

Open in browser: http://localhost:5000/api/stats

You'll see:
```json
{
  "collection_name": "image_search",
  "count": 1234,
  "vector_size": 512,
  "distance": "Cosine"
}
```

## 🚀 Performance Tips

### For Faster Indexing

Edit `.env`:
```env
# Use GPU if available (requires NVIDIA GPU with CUDA)
CLIP_DEVICE=cuda

# Increase batch size (requires more memory)
INDEX_BATCH_SIZE=200
```

### For Lower Memory Usage

Edit `.env`:
```env
# Use CPU
CLIP_DEVICE=cpu

# Decrease batch size
INDEX_BATCH_SIZE=50
```

## 📚 Additional Resources

- **Main Documentation:** [README.md](README.md)
- **Frontend Guide:** [frontend/README.md](frontend/README.md)
- **API Documentation:** [indexing_service/README.md](indexing_service/README.md)
- **Project Summary:** [DELIVERABLES.md](DELIVERABLES.md)

## 💡 Tips

1. **First Run:** Always run `setup.bat` first
2. **Keep Windows Open:** Don't close the 3 service windows while using the app
3. **Stop Properly:** Use `stop.bat` or close the windows before shutting down
4. **Check Logs:** If something fails, check the service windows for error messages
5. **Demo Images:** Place sample images in `demo_images\` folder for testing

## ✅ Checklist

- [ ] Installed Python 3.9+ (with PATH enabled)
- [ ] Installed Node.js 18+ (with PATH enabled)
- [ ] Ran `setup.bat` successfully
- [ ] Ran `start.bat` and saw 3 windows open
- [ ] Accessed http://localhost:5173 in browser
- [ ] Tested search functionality
- [ ] Added images and tested indexing

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review error messages in the service windows
3. Run `quick_test.bat` to diagnose which service is failing
4. Check the logs in the service windows
5. Verify all prerequisites are installed correctly

---

**Happy searching! 🔍**

For detailed documentation, see the main [README.md](README.md)
