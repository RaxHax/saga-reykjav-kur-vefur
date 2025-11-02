@echo off
REM ============================================================================
REM SAGA Reykjavík - Windows Start Script
REM ============================================================================
REM This script starts all three services in separate windows:
REM 1. Flask Backend (Port 5000)
REM 2. FastAPI Indexing Service (Port 8001)
REM 3. React Frontend (Port 5173)
REM ============================================================================

echo.
echo ========================================
echo   SAGA Reykjavik - Starting Services
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first to initialize the application.
    pause
    exit /b 1
)

REM Check if Node modules exist
if not exist frontend\node_modules (
    echo [ERROR] Node modules not found!
    echo Please run setup.bat first to initialize the application.
    pause
    exit /b 1
)

echo Starting services in separate windows...
echo.
echo Services:
echo   [1] Flask Backend          - http://localhost:5000
echo   [2] Indexing Service       - http://localhost:8001
echo   [3] React Frontend         - http://localhost:5173
echo.
echo Each service will open in a new window.
echo Close the windows or press Ctrl+C to stop each service.
echo.
pause

REM Start Flask Backend
echo Starting Flask Backend...
start "SAGA - Flask Backend (Port 5000)" cmd /k "cd /d %~dp0 && call venv\Scripts\activate.bat && python app_enhanced.py"

REM Wait a moment before starting next service
timeout /t 2 /nobreak >nul

REM Start Indexing Service
echo Starting Indexing Service...
start "SAGA - Indexing Service (Port 8001)" cmd /k "cd /d %~dp0indexing_service && call ..\venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8001"

REM Wait a moment before starting next service
timeout /t 2 /nobreak >nul

REM Start React Frontend
echo Starting React Frontend...
start "SAGA - React Frontend (Port 5173)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo   All Services Started!
echo ========================================
echo.
echo Services are running in separate windows:
echo   - Flask Backend:      http://localhost:5000
echo   - Indexing Service:   http://localhost:8001
echo   - React Frontend:     http://localhost:5173
echo.
echo Access the application at: http://localhost:5173
echo.
echo To stop services: Close the service windows or press Ctrl+C in each window
echo.
echo Waiting 5 seconds before opening browser...
timeout /t 5 /nobreak >nul

REM Open browser to the application
start http://localhost:5173

echo.
echo Browser opened to http://localhost:5173
echo.
echo This window can be closed safely.
echo The services will continue running in their separate windows.
echo.
pause
