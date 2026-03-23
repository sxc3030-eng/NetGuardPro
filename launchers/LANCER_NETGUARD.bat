@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
title NetGuard Pro v4.0 — NetGuardPro Suite

echo.
echo  +============================================+
echo  !    NetGuard Pro v4.0                       !
echo  !    Network IDS / Packet Capture / Firewall !
echo  +============================================+
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python is not installed or not in PATH.
    echo     Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Install dependencies
echo [*] Checking dependencies...
python -m pip install pywebview scapy requests psutil winotify >nul 2>&1
echo [OK] Dependencies ready.

:: Launch
echo [*] Starting NetGuard Pro...
cd /d "%~dp0.."
python netguard.py

pause
