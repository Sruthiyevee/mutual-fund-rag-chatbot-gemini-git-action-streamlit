@echo off
cd /d "%~dp0.."
echo Installing dependencies for MF Facts Chatbot...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies. Please ensure Python is installed and in your PATH.
    pause
    exit /b %errorlevel%
)
echo Dependencies installed successfully!
pause
