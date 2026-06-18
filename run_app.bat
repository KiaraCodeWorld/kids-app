@echo off
setlocal enabledelayedexpansion

REM Brain Quest - Desktop Launcher
REM This script starts the Django development server and opens it in your browser

cd /d "c:\Users\vrajp\CodeFolder\Fun-Projects\Math-Tricks"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if port 8000 is already in use and kill the process if it is
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8000"') do (
    taskkill /PID %%a /F 2>nul
)

REM Wait a moment for port to be released
timeout /t 1 /nobreak

REM Start Django server in background
start "" python manage.py runserver 0.0.0.0:8000

REM Wait for server to start
timeout /t 3 /nobreak

REM Open browser
start http://localhost:8000

REM Keep window open
echo.
echo Brain Quest is running at http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver 0.0.0.0:8000
