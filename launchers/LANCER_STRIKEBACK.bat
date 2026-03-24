@echo off
title NetGuardPro - StrikeBack
echo.
echo   ========================================
echo    NetGuardPro Suite
echo    StrikeBack v1.0.0 - Active Defense
echo   ========================================
echo.

net session >nul 2>&1
if errorlevel 1 (
    echo   [!] Administrator privileges recommended for active defense.
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
echo   [*] Starting StrikeBack on port 8850...
echo.

cd /d "%~dp0\..\strikeback"
start "" python strikeback.py
echo   [OK] StrikeBack started!
timeout /t 2 >nul
