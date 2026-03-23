@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
title VPN Guard Pro — NetGuardPro Suite

echo.
echo  +============================================+
echo  !    VPN Guard Pro                           !
echo  !    WireGuard VPN Client                    !
echo  +============================================+
echo.

:: Admin required for WireGuard
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo  [!] Admin rights required for WireGuard.
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

:: Check WireGuard
where wg >nul 2>&1
if %errorLevel% equ 0 (
    echo  [OK] WireGuard detected.
    goto :wg_ready
)
if exist "C:\Program Files\WireGuard\wg.exe" (
    set "PATH=%PATH%;C:\Program Files\WireGuard"
    echo  [OK] WireGuard found.
    goto :wg_ready
)

echo  [!] WireGuard not installed.
echo  [*] Attempting install via winget...
winget install WireGuard.WireGuard --accept-package-agreements --accept-source-agreements --silent 2>nul
if %errorLevel% equ 0 (
    echo  [OK] WireGuard installed!
    timeout /t 3 >nul
    set "PATH=%PATH%;C:\Program Files\WireGuard"
    goto :wg_ready
)

echo  [INFO] WireGuard auto-install failed.
echo  [INFO] Install manually: https://www.wireguard.com/install/
echo.

:wg_ready
echo [*] Checking Python dependencies...
python -m pip install pywebview psutil requests cryptography winotify pystray Pillow >nul 2>&1
echo [OK] Dependencies ready.

echo [*] Starting VPN Guard Pro...
cd /d "%~dp0.."
python vpnguard\vpnguard.py

pause
