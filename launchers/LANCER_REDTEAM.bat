@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
title RedTeam Simulator — NetGuardPro Suite

echo.
echo  ============================================
echo    RedTeam Simulator v1.0.0
echo    Penetration Testing ^& Defense Validation
echo  ============================================
echo.

:: Admin required for raw sockets (scapy)
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo  [!] Admin rights required for raw socket attacks.
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
python -m pip install pywebview psutil requests scapy websockets winotify pystray Pillow >nul 2>&1
echo  [OK] Dependencies ready.

echo.
echo  [*] Starting RedTeam Simulator on port 8870...
echo  [!] WARNING: This tool attacks your local defenses for testing.
echo.

cd /d "%~dp0..\redteam"
start /B pythonw redteam.py 2>nul
if %errorLevel% neq 0 (
    start /B python redteam.py
)

echo  [OK] RedTeam Simulator started!
timeout /t 5 >nul
