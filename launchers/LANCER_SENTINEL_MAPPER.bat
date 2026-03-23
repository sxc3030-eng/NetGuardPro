@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
title SentinelOS Mapper — NetGuardPro Suite

echo.
echo  ============================================
echo    SentinelOS Network Mapper + Firewall
echo  ============================================
echo.

:: Admin required for firewall
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo  [!] Admin rights required for firewall.
    echo  [*] Relaunching as admin...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b 0
)
echo  [OK] Admin rights confirmed.

python --version >nul 2>&1
if errorlevel 1 (
    echo  [!] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo [*] Checking dependencies...
python -m pip install pywebview psutil requests winotify >nul 2>&1
echo [OK] Dependencies ready.

echo [*] Starting SentinelOS Mapper...
cd /d "%~dp0.."
python sentinel\sentinel_mapper.py

pause
