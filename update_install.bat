@echo off
echo === Mise a jour COMPLETE NetGuard Pro ===
taskkill /F /IM pythonw.exe >nul 2>&1
timeout /t 2 >nul

set SRC=D:\NetGuardPro
set DST=C:\Program Files\NetGuard Pro

icacls "%DST%" /grant *S-1-5-32-545:(OI)(CI)M /T /Q >nul 2>&1

for %%F in (netguard.py netguard_tray.py netguard_auth.py startup_utils.py license_manager.py permissions.py toast_notifications.py netguard_users.json) do (
    copy /Y "%SRC%\%%F" "%DST%\%%F" >nul && echo [OK] %%F
)

for %%M in (sentinel cleanguard vpnguard mailshield honeypot strikeback fim recorder siem sandbox redteam updater help_agent mobile_gateway netguardpro_desktop) do (
    if exist "%SRC%\%%M" (
        xcopy /Y /S /Q /I "%SRC%\%%M\*.*" "%DST%\%%M\" >nul 2>nul && echo [OK] %%M
    )
)

for %%M in (sentinel cleanguard vpnguard mailshield honeypot strikeback fim recorder siem sandbox redteam) do (
    if not exist "%DST%\%%M\logs" mkdir "%DST%\%%M\logs" 2>nul
)

echo.
echo === Termine! Test de chaque programme... ===
echo.

"%DST%\python\python.exe" -c "import py_compile,os,sys;sys.path.insert(0,r'%DST%');errs=[];[py_compile.compile(os.path.join(r,f),doraise=True) if f.endswith('.py') else None for r,d,fs in os.walk(r'%DST%') if not any(x in r for x in ['python','__pycache__']) for f in fs];print('Compilation OK')" 2>nul
if errorlevel 1 echo [FAIL] Erreur de compilation

echo.
pause
