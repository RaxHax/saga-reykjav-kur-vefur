#!/bin/bash

echo "============================================"
echo "⚙️  Starting SAGA Reykjavík Admin App"
echo "============================================"

# Start Indexing Service
echo "🔧 Starting Indexing Service..."
cd ../indexing_service
python main.py &
INDEXING_PID=$!
cd ../admin-app

# Wait for indexing service to initialize
sleep 5

# Start Frontend
echo "🎨 Starting Admin Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "============================================"
echo "✅ Admin Application Started!"
echo "============================================"
echo "🌐 Admin UI: http://localhost:3001"
echo "🔌 Indexing API: http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop all services"
echo "============================================"

# Wait for user interrupt
trap "kill $INDEXING_PID $FRONTEND_PID; exit" INT
wait
