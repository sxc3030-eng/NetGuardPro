@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
title CleanGuard Pro — NetGuardPro Suite

echo.
echo  +============================================+
echo  !    CleanGuard Pro                          !
echo  !    System Cleaner / Antivirus              !
echo  +============================================+
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python is not installed or not in PATH.
    echo     Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [*] Checking dependencies...
python -m pip install pywebview psutil watchdog winotify pystray Pillow >nul 2>&1
echo [OK] Dependencies ready.

echo [*] Starting CleanGuard Pro...
cd /d "%~dp0.."
python cleanguard\cleanguard.py

pause
