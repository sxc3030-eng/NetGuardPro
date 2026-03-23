@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
title Help Agent — NetGuardPro Suite

echo.
echo  +============================================+
echo  !    NetGuardPro Help Agent                  !
echo  !    Interactive Guide for All Programs      !
echo  +============================================+
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo [*] Checking dependencies...
python -m pip install pywebview winotify >nul 2>&1
echo [OK] Dependencies ready.

echo [*] Starting Help Agent...
cd /d "%~dp0.."
python help_agent\help_agent.py

pause
