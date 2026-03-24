@echo off
title NetGuardPro Desktop
echo.
echo   ========================================
echo    NetGuardPro Desktop - Cybersecurity Suite
echo    Graphical Launcher v1.0.0
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
python -m pip install pywebview psutil --quiet 2>nul
echo   [OK] Dependencies ready.

echo.
echo   [*] Launching NetGuardPro Desktop...
echo.

cd /d "%~dp0\..\netguardpro_desktop"
start "" python desktop.py
echo   [OK] Desktop launched!
timeout /t 2 >nul
