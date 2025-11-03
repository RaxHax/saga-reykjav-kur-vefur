#!/bin/bash

# =============================================================================
# SAGA Reykjavík - Start All Services
# =============================================================================
# This script starts all three services needed for the application:
# 1. Flask backend (port 5000)
# 2. FastAPI indexing service (port 8001)
# 3. React frontend dev server (port 3000)
#
# Usage: ./start-all-services.sh
# =============================================================================

set -e

echo "=================================================="
echo " SAGA Reykjavík - Starting All Services"
echo "=================================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Change to project root directory
cd "$(dirname "$0")/.."

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file. Please configure it before running again.${NC}"
    exit 1
fi

# Check if Python venv exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Python virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created.${NC}"
fi

# Activate venv
echo -e "${BLUE}🔧 Activating Python virtual environment...${NC}"
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Python dependencies not installed. Installing...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Python dependencies installed.${NC}"
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}⚠️  Frontend dependencies not installed. Installing...${NC}"
    cd frontend && npm install && cd ..
    echo -e "${GREEN}✅ Frontend dependencies installed.${NC}"
fi

# Create logs directory
mkdir -p logs

echo ""
echo -e "${GREEN}Starting services...${NC}"
echo ""

# Start Flask backend in background
echo -e "${BLUE}1. Starting Flask backend (port 5000)...${NC}"
cd backend/flask_api
python app.py > ../../logs/flask.log 2>&1 &
FLASK_PID=$!
cd ../..
echo -e "${GREEN}   ✅ Flask started (PID: $FLASK_PID)${NC}"

# Wait a bit for Flask to start
sleep 2

# Start Indexing service in background
echo -e "${BLUE}2. Starting Indexing service (port 8001)...${NC}"
cd backend/indexing_service
uvicorn main:app --host 0.0.0.0 --port 8001 > ../../logs/indexing.log 2>&1 &
INDEXING_PID=$!
cd ../..
echo -e "${GREEN}   ✅ Indexing service started (PID: $INDEXING_PID)${NC}"

# Wait a bit for indexing service to start
sleep 2

# Start React frontend in background
echo -e "${BLUE}3. Starting React frontend (port 3000)...${NC}"
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo -e "${GREEN}   ✅ React frontend started (PID: $FRONTEND_PID)${NC}"

# Save PIDs to file for easy cleanup
echo "$FLASK_PID" > .pids
echo "$INDEXING_PID" >> .pids
echo "$FRONTEND_PID" >> .pids

echo ""
echo "=================================================="
echo -e "${GREEN}✨ All services started successfully!${NC}"
echo "=================================================="
echo ""
echo "📋 Service URLs:"
echo "   Frontend:         http://localhost:3000"
echo "   Flask API:        http://localhost:5000"
echo "   Indexing API:     http://localhost:8001"
echo ""
echo "📝 Logs:"
echo "   Flask:            logs/flask.log"
echo "   Indexing Service: logs/indexing.log"
echo "   Frontend:         logs/frontend.log"
echo ""
echo "🛑 To stop all services, run:"
echo "   ./stop-all-services.sh"
echo ""
echo "=================================================="
