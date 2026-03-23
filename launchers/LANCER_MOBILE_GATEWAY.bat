@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
title Mobile Gateway — NetGuardPro Suite

echo.
echo  ============================================
echo    Mobile Gateway v1.0.0
echo    VPN ^& DNS Filter for Mobile Devices
echo  ============================================
echo.

:: Admin required for WireGuard + DNS
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo  [!] Admin rights required for VPN and DNS services.
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
echo  [OK] Python detected.

echo  [*] Installing dependencies...
python -m pip install pywebview psutil requests websockets cryptography qrcode Pillow winotify pystray >nul 2>&1
echo  [OK] Dependencies ready.

echo.
echo  [*] Starting Mobile Gateway on port 8895...
echo.

cd /d "%~dp0..\mobile_gateway"
start /B pythonw gateway.py 2>nul
if %errorLevel% neq 0 (
    start /B python gateway.py
)

echo  [OK] Mobile Gateway started!
timeout /t 5 >nul
