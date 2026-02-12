@echo off
cd /d "%~dp0.."
echo Starting MF Facts Chatbot...

:: Check if .env exists
if not exist .env (
    echo [WARNING] .env file not found! Please create one with your GROQ_API_KEY.
    echo Example: GROQ_API_KEY=your_key_here > .env.example
    echo Created .env.example template.
    pause
    exit /b 1
)

:: Start Backend in a new window
echo Starting Backend Server (Port 8000)...
start "MF Facts Backend" cmd /k "python -m uvicorn phase5_chat_interface.backend.main:app --host 127.0.0.1 --port 8000"

:: Start Frontend in a new window
echo Starting Frontend Server (Port 3000)...
start "MF Facts Frontend" cmd /k "python -m http.server 3000 --directory phase5_chat_interface/frontend"

:: Open Browser
echo Opening browser...
timeout /t 3 >nul
start http://localhost:3000

echo Application started! Close the terminal windows to stop the servers.
pause
