@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
title SentinelOS — NetGuardPro Suite

echo.
echo  ============================================
echo    SentinelOS v2.0
echo    Cybersecurity Command Center
echo  ============================================
echo.

:: Admin required for firewall + network scanning
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo  [!] Admin rights required for firewall and scanning.
    echo  [*] Relaunching as admin...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b 0
)
echo  [OK] Admin rights confirmed.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [!] Python is not installed or not in PATH.
    pause
    exit /b 1
)
echo  [OK] Python detected.

:: Check WireGuard
where wg >nul 2>&1
if %errorLevel% equ 0 (
    echo  [OK] WireGuard detected.
) else (
    if exist "C:\Program Files\WireGuard\wg.exe" (
        set "PATH=%PATH%;C:\Program Files\WireGuard"
        echo  [OK] WireGuard found.
    ) else (
        echo  [INFO] WireGuard not installed — VPN features will be limited.
    )
)

:: Install dependencies
echo.
echo  [*] Installing Python dependencies...
python -m pip install pywebview psutil requests scapy websockets aiohttp pystray Pillow cryptography winotify >nul 2>&1
echo  [OK] Dependencies ready.

:: Launch Cortex (starts all agents)
echo.
echo  ============================================
echo    Starting SentinelOS Cortex...
echo  ============================================
echo.
echo  [*] Cortex will start all agents:
echo      - NetGuard Pro           (port 8765)
echo      - CleanGuard Pro         (port 8810)
echo      - MailShield Pro         (port 8801)
echo      - VPN Guard Pro          (port 8820)
echo      - HoneyPot               (port 8830)
echo      - File Integrity Monitor (port 8840)
echo      - StrikeBack             (port 8850)
echo      - Recorder               (port 8860)
echo.
echo  [*] Cortex dashboard on port 8900
echo.

cd /d "%~dp0..\sentinel"
start /B pythonw cortex.py 2>nul
if %errorLevel% neq 0 (
    start /B python cortex.py
)

echo  [OK] SentinelOS started in background!
echo  [*] Check the system tray icon.
echo.
timeout /t 5 >nul
