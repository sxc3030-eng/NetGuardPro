@echo off
title NetGuardPro - Recorder
echo.
echo   ========================================
echo    NetGuardPro Suite
echo    Recorder v1.0.0 - Forensic Recorder
echo   ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo   [!] Python is not installed.
    pause
    exit /b 1
)
echo   [OK] Python detected.

echo   [*] Installing dependencies...
python -m pip install pywebview psutil requests websockets --quiet 2>nul
echo   [OK] Dependencies ready.

echo.
echo   [*] Starting Recorder on port 8860...
echo.

cd /d "%~dp0\..\recorder"
start "" python recorder.py
echo   [OK] Recorder started!
timeout /t 2 >nul
