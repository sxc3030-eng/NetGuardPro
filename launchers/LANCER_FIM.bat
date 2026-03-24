@echo off
title NetGuardPro - File Integrity Monitor
echo.
echo   ========================================
echo    NetGuardPro Suite
echo    File Integrity Monitor v1.0.0
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
echo   [*] Starting FIM on port 8840...
echo.

cd /d "%~dp0\..\fim"
start "" python fim.py
echo   [OK] FIM started!
timeout /t 2 >nul
