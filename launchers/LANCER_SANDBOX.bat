@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
title Sandbox — NetGuardPro Suite

echo.
echo  ============================================
echo    Sandbox v1.0.0
echo    Automated File Analysis
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
python -m pip install pywebview psutil requests websockets yara-python pefile winotify pystray Pillow >nul 2>&1
echo  [OK] Dependencies ready.

echo.
echo  [*] Starting Sandbox on port 8890...
echo.

cd /d "%~dp0..\sandbox"
start /B pythonw sandbox.py 2>nul
if %errorLevel% neq 0 (
    start /B python sandbox.py
)

echo  [OK] Sandbox started!
timeout /t 5 >nul
