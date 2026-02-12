@echo off
cd /d "%~dp0.."
setlocal

echo ==================================================
echo      Mutual Fund FAQ Assistant - Launcher
echo ==================================================

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo Installing/Verifying dependencies...
python -m pip install -r phase_6_streamlit_app/requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Warning: 'python -m pip' command failed.
)

echo.
echo Launching Streamlit App...
echo.
python -m streamlit run phase_6_streamlit_app/app.py
if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to launch the application.
    pause
    exit /b 1
)

pause
