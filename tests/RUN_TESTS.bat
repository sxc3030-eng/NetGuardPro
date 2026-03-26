@echo off
title NetGuardPro - Test Suite
color 0A

echo ================================================================
echo   NetGuardPro - Comprehensive Test Suite
echo ================================================================
echo.

cd /d "%~dp0\.."

echo [1/3] Running Python tests...
python tests\test_all.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [FAIL] Python tests failed!
    echo.
) else (
    echo.
    echo [PASS] Python tests passed!
    echo.
)

echo [2/3] Checking Python syntax of all programs...
set SYNTAX_OK=1
for %%f in (
    netguard\netguard.py
    cleanguard\cleanguard.py
    mailshield\mailshield.py
    vpnguard\vpnguard.py
    sentinel\cortex.py
    sentinel\sentinel.py
    fim\fim.py
    honeypot\honeypot.py
    strikeback\strikeback.py
    recorder\recorder.py
    redteam\redteam.py
    siem\siem.py
    sandbox\sandbox.py
    mobile_gateway\gateway.py
    help_agent\help_agent.py
) do (
    python -c "import py_compile; py_compile.compile(r'%%f', doraise=True)" 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo   [FAIL] %%f
        set SYNTAX_OK=0
    ) else (
        echo   [OK]   %%f
    )
)

echo.
echo [3/3] Checking HTML dashboards exist...
set HTML_OK=1
for %%f in (
    netguard_dashboard.html
    cleanguard\cleanguard_dashboard.html
    mailshield\mailshield_dashboard.html
    vpnguard\vpnguard_dashboard.html
    sentinel\sentinel_dashboard.html
    redteam\redteam_dashboard.html
    siem\siem_dashboard.html
    sandbox\sandbox_dashboard.html
    mobile_gateway\gateway_dashboard.html
) do (
    if exist "%%f" (
        echo   [OK]   %%f
    ) else (
        echo   [MISS] %%f
        set HTML_OK=0
    )
)

echo.
echo ================================================================
echo   Test Summary
echo ================================================================
echo.

pause
