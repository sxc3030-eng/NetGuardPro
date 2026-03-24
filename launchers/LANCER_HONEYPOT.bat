@echo off
title NetGuardPro - HoneyPot
echo.
echo   ========================================
echo    NetGuardPro Suite
echo    HoneyPot v1.0.0 - Trap System
echo   ========================================
echo.

net session >nul 2>&1
if errorlevel 1 (
    echo   [!] Administrator privileges recommended for low ports.
    echo   [*] Continuing anyway...
)

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
echo   [*] Starting HoneyPot on port 8830...
echo.

cd /d "%~dp0\..\honeypot"
start "" python honeypot.py
echo   [OK] HoneyPot started!
timeout /t 2 >nul
