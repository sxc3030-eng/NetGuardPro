@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
title MailShield Pro — NetGuardPro Suite

echo.
echo  +============================================+
echo  !    MailShield Pro                          !
echo  !    Secure Email Client                     !
echo  +============================================+
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo [*] Checking dependencies...
python -m pip install pywebview requests cryptography dnspython bleach msal winotify pystray Pillow >nul 2>&1
echo [OK] Dependencies ready.

:: Kill any existing MailShield on ports 8800/8801
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8800 " ^| findstr "LISTENING" 2^>nul') do (
    taskkill /PID %%a /F >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8801 " ^| findstr "LISTENING" 2^>nul') do (
    taskkill /PID %%a /F >nul 2>&1
)
timeout /t 1 >nul 2>&1

echo [*] Starting MailShield Pro...
cd /d "%~dp0.."
python mailshield\mailshield.py

pause
