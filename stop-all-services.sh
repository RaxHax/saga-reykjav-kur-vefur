#!/bin/bash

# =============================================================================
# SAGA Reykjavík - Stop All Services
# =============================================================================
# This script stops all running services
#
# Usage: ./stop-all-services.sh
# =============================================================================

echo "=================================================="
echo " SAGA Reykjavík - Stopping All Services"
echo "=================================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

if [ ! -f .pids ]; then
    echo -e "${YELLOW}⚠️  No .pids file found. Services may not be running.${NC}"
    echo "Attempting to find and kill processes manually..."

    # Try to kill by port
    echo -e "${YELLOW}Looking for processes on ports 3000, 5000, 8001...${NC}"

    for port in 3000 5000 8001; do
        PID=$(lsof -ti:$port 2>/dev/null)
        if [ ! -z "$PID" ]; then
            echo -e "${RED}Killing process on port $port (PID: $PID)${NC}"
            kill -9 $PID 2>/dev/null || true
        fi
    done

    echo -e "${GREEN}✅ Manual cleanup complete${NC}"
    exit 0
fi

# Read PIDs from file
FLASK_PID=$(sed -n '1p' .pids)
INDEXING_PID=$(sed -n '2p' .pids)
FRONTEND_PID=$(sed -n '3p' .pids)

echo "Stopping services..."

# Stop Flask
if [ ! -z "$FLASK_PID" ]; then
    if kill -0 $FLASK_PID 2>/dev/null; then
        echo -e "${RED}Stopping Flask backend (PID: $FLASK_PID)...${NC}"
        kill $FLASK_PID 2>/dev/null || true
        sleep 1
        kill -9 $FLASK_PID 2>/dev/null || true
    else
        echo -e "${YELLOW}Flask backend already stopped${NC}"
    fi
fi

# Stop Indexing Service
if [ ! -z "$INDEXING_PID" ]; then
    if kill -0 $INDEXING_PID 2>/dev/null; then
        echo -e "${RED}Stopping Indexing service (PID: $INDEXING_PID)...${NC}"
        kill $INDEXING_PID 2>/dev/null || true
        sleep 1
        kill -9 $INDEXING_PID 2>/dev/null || true
    else
        echo -e "${YELLOW}Indexing service already stopped${NC}"
    fi
fi

# Stop Frontend
if [ ! -z "$FRONTEND_PID" ]; then
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${RED}Stopping React frontend (PID: $FRONTEND_PID)...${NC}"
        kill $FRONTEND_PID 2>/dev/null || true
        sleep 1
        kill -9 $FRONTEND_PID 2>/dev/null || true
    else
        echo -e "${YELLOW}React frontend already stopped${NC}"
    fi
fi

# Clean up child processes
pkill -f "uvicorn main:app" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true
pkill -f "app_enhanced.py" 2>/dev/null || true

# Remove PID file
rm -f .pids

echo ""
echo -e "${GREEN}✅ All services stopped${NC}"
echo "=================================================="
