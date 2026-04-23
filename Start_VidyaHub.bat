@echo off
title VidyaHub Hackathon Launcher
echo ==========================================
echo    🚀 STARTING VIDYAHUB PLATFORM  🚀
echo ==========================================
echo.

:: Check for environment variables
if not exist .env (
    echo [ERROR] .env file not found! Please ensure it is present.
    pause
    exit /b
)

:: Start the Eventlet Server (supports Socket.io and real-time features)
echo [1/2] Launching AI & Real-time Server...
start "VidyaHub Server" cmd /k "python run_app.py"

:: Give the server a moment to warm up
timeout /t 5 /nobreak > nul

:: Open the browser to the dashboard
echo [2/2] Opening VidyaHub Dashboard...
start http://172.16.102.168:8000/dashboard/student/

echo.
echo ==========================================
echo    🌟 VIDYAHUB IS NOW LIVE! ✨
echo ==========================================
echo.
echo Closing launcher in 10 seconds...
timeout /t 10
exit
