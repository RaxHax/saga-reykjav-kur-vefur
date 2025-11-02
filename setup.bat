@echo off
REM ============================================================================
REM SAGA Reykjavík - Windows Setup Script
REM ============================================================================
REM This script performs initial setup of the application:
REM - Creates Python virtual environment
REM - Installs Python dependencies
REM - Installs Node.js dependencies
REM - Creates environment configuration files
REM ============================================================================

echo.
echo ========================================
echo   SAGA Reykjavik - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/6] Checking Python installation...
python --version
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

echo [2/6] Checking Node.js installation...
node --version
npm --version
echo.

REM Create Python virtual environment
echo [3/6] Creating Python virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)
echo.

REM Activate virtual environment and install dependencies
echo [4/6] Installing Python dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo Python dependencies installed successfully
echo.

REM Install Node.js dependencies
echo [5/6] Installing Node.js dependencies...
cd frontend
if exist node_modules (
    echo Node modules already exist, skipping...
) else (
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Node.js dependencies
        cd ..
        pause
        exit /b 1
    )
    echo Node.js dependencies installed successfully
)
cd ..
echo.

REM Create environment configuration files
echo [6/6] Creating environment configuration files...

REM Create .env if it doesn't exist
if exist .env (
    echo .env already exists, skipping...
) else (
    if exist .env.example (
        copy .env.example .env
        echo Created .env from .env.example
        echo Please review and configure .env file before running the application
    ) else (
        echo [WARNING] .env.example not found, skipping .env creation
    )
)

REM Create frontend .env.local
if exist frontend\.env.local (
    echo frontend\.env.local already exists, skipping...
) else (
    (
        echo VITE_API_BASE_URL=http://localhost:5000
        echo VITE_INDEXING_API_BASE_URL=http://localhost:8001
    ) > frontend\.env.local
    echo Created frontend\.env.local
)
echo.

REM Create demo_images directory
if not exist demo_images (
    mkdir demo_images
    echo Created demo_images directory
    echo You can place sample images here for testing
)
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Review and configure .env file if needed
echo   2. Run 'start.bat' to start all services
echo   3. Access the application at http://localhost:5173
echo.
echo Optional:
echo   - Place sample images in demo_images\ folder
echo   - Run 'demo_all_features.py' to test all features
echo   - Run 'quick_test.bat' for quick API health check
echo.
pause
