@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
title SIEM/SOAR — NetGuardPro Suite

echo.
echo  ============================================
echo    SIEM/SOAR v1.0.0
echo    Security Information ^& Event Management
echo  ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  [!] Python is not installed or not in PATH.
    pause
    exit /b 1
)
echo  [OK] Python detected.

echo  [*] Installing dependencies...
python -m pip install pywebview psutil requests websockets winotify pystray Pillow >nul 2>&1
echo  [OK] Dependencies ready.

echo.
echo  [*] Starting SIEM/SOAR on port 8880...
echo.

cd /d "%~dp0..\siem"
start /B pythonw siem.py 2>nul
if %errorLevel% neq 0 (
    start /B python siem.py
)

echo  [OK] SIEM/SOAR started!
timeout /t 5 >nul
