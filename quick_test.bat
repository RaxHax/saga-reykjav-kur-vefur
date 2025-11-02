@echo off
REM ============================================================================
REM SAGA Reykjavík - Quick API Test (Windows)
REM ============================================================================
REM Tests all API endpoints quickly without interactive prompts
REM ============================================================================

setlocal enabledelayedexpansion

set FLASK_URL=http://localhost:5000
set INDEXING_URL=http://localhost:8001

echo.
echo ==========================================
echo   SAGA Reykjavik - Quick API Test
echo ==========================================
echo.

REM Check if curl is available
curl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] curl is not installed or not in PATH
    echo Please install curl or use Windows 10+ which includes curl by default
    pause
    exit /b 1
)

set total=0
set passed=0

REM Test Flask Health
echo === Flask Backend Tests ===
call :test_endpoint "Flask Health" "%FLASK_URL%/api/health"

REM Test Flask Stats
call :test_endpoint "Database Stats" "%FLASK_URL%/api/stats"

REM Test Semantic Search
call :test_endpoint_post "Semantic Search" "%FLASK_URL%/api/search" "{\"query\":\"test\",\"limit\":5}"

REM Test Icelandic Search
call :test_endpoint_post "Icelandic Search" "%FLASK_URL%/api/search/icelandic" "{\"query\":\"mynd\",\"limit\":5}"

REM Test Hybrid Search
call :test_endpoint_post "Hybrid Search" "%FLASK_URL%/api/search/hybrid" "{\"text_query\":\"test\",\"metadata\":{},\"weights\":{\"text\":0.7,\"metadata\":0.3},\"limit\":5}"

echo.
echo === Indexing Service Tests ===

REM Test Indexing Service Health
call :test_endpoint "Indexing Health" "%INDEXING_URL%/health"

REM Test List Jobs
call :test_endpoint "List Jobs" "%INDEXING_URL%/jobs"

echo.
echo ==========================================
echo   TEST RESULTS
echo ==========================================
echo.
echo Total Tests: !total!
echo Passed: !passed!
set /a failed=!total!-!passed!
echo Failed: !failed!
echo.

if !passed! equ !total! (
    echo [32mAll tests passed![0m
    exit /b 0
) else (
    echo [33mSome tests failed. Check service status.[0m
    exit /b 1
)

REM ============================================================================
REM Helper Functions
REM ============================================================================

:test_endpoint
set /a total+=1
set "name=%~1"
set "url=%~2"
echo Testing %name%...
curl -s -o nul -w "%%{http_code}" "%url%" > temp_status.txt
set /p status=<temp_status.txt
del temp_status.txt
if "!status!"=="200" (
    echo [32m  PASS - HTTP !status![0m
    set /a passed+=1
) else (
    echo [31m  FAIL - HTTP !status![0m
)
goto :eof

:test_endpoint_post
set /a total+=1
set "name=%~1"
set "url=%~2"
set "data=%~3"
echo Testing %name%...
curl -s -o nul -w "%%{http_code}" -X POST -H "Content-Type: application/json" -d "%data%" "%url%" > temp_status.txt
set /p status=<temp_status.txt
del temp_status.txt
if "!status!"=="200" (
    echo [32m  PASS - HTTP !status![0m
    set /a passed+=1
) else (
    echo [31m  FAIL - HTTP !status![0m
)
goto :eof
