#!/bin/bash

echo "============================================"
echo "🚀 Starting SAGA Reykjavík Search App"
echo "============================================"

# Start Backend
echo "📦 Starting Flask Search API..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to initialize
sleep 5

# Start Frontend
echo "🎨 Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "============================================"
echo "✅ Application Started!"
echo "============================================"
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"
echo "============================================"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
