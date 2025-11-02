@echo off
REM ============================================================================
REM SAGA Reykjavík - Windows Stop Script
REM ============================================================================
REM This script stops all running services by killing the processes
REM ============================================================================

echo.
echo ========================================
echo   SAGA Reykjavik - Stopping Services
echo ========================================
echo.

echo Stopping Flask Backend (Python)...
taskkill /F /FI "WindowTitle eq SAGA - Flask Backend*" 2>nul
if %errorlevel% equ 0 (
    echo   - Flask Backend stopped
) else (
    echo   - Flask Backend not running
)

echo.
echo Stopping Indexing Service (Python/Uvicorn)...
taskkill /F /FI "WindowTitle eq SAGA - Indexing Service*" 2>nul
if %errorlevel% equ 0 (
    echo   - Indexing Service stopped
) else (
    echo   - Indexing Service not running
)

echo.
echo Stopping React Frontend (Node)...
taskkill /F /FI "WindowTitle eq SAGA - React Frontend*" 2>nul
if %errorlevel% equ 0 (
    echo   - React Frontend stopped
) else (
    echo   - React Frontend not running
)

echo.
echo Alternative: Killing processes by port (if windows didn't close)...

REM Kill process on port 5000 (Flask)
for /f "tokens=5" %%a in ('netstat -ano ^| find ":5000" ^| find "LISTENING"') do (
    echo Killing process on port 5000 (PID: %%a^)
    taskkill /F /PID %%a 2>nul
)

REM Kill process on port 8001 (Indexing)
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8001" ^| find "LISTENING"') do (
    echo Killing process on port 8001 (PID: %%a^)
    taskkill /F /PID %%a 2>nul
)

REM Kill process on port 5173 (Vite)
for /f "tokens=5" %%a in ('netstat -ano ^| find ":5173" ^| find "LISTENING"') do (
    echo Killing process on port 5173 (PID: %%a^)
    taskkill /F /PID %%a 2>nul
)

echo.
echo ========================================
echo   All Services Stopped!
echo ========================================
echo.
pause
