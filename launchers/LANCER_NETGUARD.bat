@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
title NetGuard Pro v4.0 — NetGuardPro Suite

:: Auto-elevation: request admin rights for WireGuard VPN
net session >nul 2>&1
if errorlevel 1 (
    echo [*] Demande des droits administrateur pour WireGuard VPN...
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d \"%~dp0..\" && python netguard.py && pause' -Verb RunAs" 2>nul
    exit /b
)

echo.
echo  +============================================+
echo  !    NetGuard Pro v4.0  [ADMIN]              !
echo  !    Network IDS / Packet Capture / Firewall !
echo  !    WireGuard VPN Active                    !
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

:: Launch
echo [*] Starting NetGuard Pro (admin mode)...
cd /d "%~dp0.."
python netguard.py

pause
