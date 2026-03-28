@echo off
REM ============================================================
REM  NetGuard Pro — Code Signing Script
REM  Signs the installer .exe with your code signing certificate
REM ============================================================
REM
REM  BEFORE USING:
REM  1. Buy a code signing certificate (Certum ~$65/yr, Sectigo ~$180/yr)
REM  2. Export it as .pfx file
REM  3. Place the .pfx in this directory
REM  4. Update CERT_FILE and CERT_PASS below
REM
REM  This removes the "Unknown Publisher" warning in Windows SmartScreen.
REM ============================================================

set CERT_FILE=netguardpro_cert.pfx
set CERT_PASS=YOUR_PASSWORD_HERE
set TIMESTAMP_URL=http://timestamp.sectigo.com
set EXE_FILE=..\dist\NetGuardPro_Setup_3.0.0.exe

REM Check if signtool exists
where signtool >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] signtool.exe not found.
    echo     Install Windows SDK: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
    echo     Or use: "C:\Program Files (x86)\Windows Kits\10\bin\10.0.xxxxx.0\x64\signtool.exe"
    pause
    exit /b 1
)

REM Check if certificate exists
if not exist "%CERT_FILE%" (
    echo [!] Certificate file not found: %CERT_FILE%
    echo     Place your .pfx certificate in this directory.
    pause
    exit /b 1
)

REM Check if EXE exists
if not exist "%EXE_FILE%" (
    echo [!] Installer not found: %EXE_FILE%
    echo     Build the installer first with Inno Setup.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Signing NetGuard Pro Installer
echo ============================================================
echo.
echo   Certificate : %CERT_FILE%
echo   Installer   : %EXE_FILE%
echo   Timestamp   : %TIMESTAMP_URL%
echo.

REM Sign with SHA-256
signtool sign /f "%CERT_FILE%" /p "%CERT_PASS%" /tr "%TIMESTAMP_URL%" /td sha256 /fd sha256 /d "NetGuard Pro - Cybersecurity Suite" /du "https://netguardpro.com" "%EXE_FILE%"

if %errorlevel% equ 0 (
    echo.
    echo [OK] Installer signed successfully!
    echo.
    REM Verify signature
    echo [*] Verifying signature...
    signtool verify /pa /v "%EXE_FILE%"
    echo.
    echo [OK] Ready to distribute: %EXE_FILE%
) else (
    echo.
    echo [!] Signing failed. Check your certificate and password.
)

echo.
pause
