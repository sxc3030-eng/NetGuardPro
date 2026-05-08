@echo off
echo === Creation des raccourcis bureau NetGuard Pro Suite ===
echo.

set APP=C:\Program Files\NetGuard Pro
set PY=%APP%\python\pythonw.exe
set ICO=%APP%\netguard_icon.ico
set DESK=%USERPROFILE%\Desktop

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\SentinelOS.lnk'); $s.TargetPath = '%PY%'; $s.Arguments = '\"%APP%\sentinel\cortex.py\"'; $s.WorkingDirectory = '%APP%\sentinel'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] SentinelOS

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\CleanGuard Pro.lnk'); $s.TargetPath = '%PY%'; $s.Arguments = '\"%APP%\cleanguard\cleanguard.py\"'; $s.WorkingDirectory = '%APP%\cleanguard'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] CleanGuard Pro

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\VPN Guard Pro.lnk'); $s.TargetPath = '%PY%'; $s.Arguments = '\"%APP%\vpnguard\vpnguard.py\"'; $s.WorkingDirectory = '%APP%\vpnguard'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] VPN Guard Pro

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\MailShield Pro.lnk'); $s.TargetPath = '%PY%'; $s.Arguments = '\"%APP%\mailshield\mailshield.py\"'; $s.WorkingDirectory = '%APP%\mailshield'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] MailShield Pro

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\HoneyPot Agent.lnk'); $s.TargetPath = '%PY%'; $s.Arguments = '\"%APP%\honeypot\honeypot.py\"'; $s.WorkingDirectory = '%APP%\honeypot'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] HoneyPot Agent

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\File Integrity Monitor.lnk'); $s.TargetPath = '%PY%'; $s.Arguments = '\"%APP%\fim\file_integrity_monitor.py\"'; $s.WorkingDirectory = '%APP%\fim'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] File Integrity Monitor

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\StrikeBack.lnk'); $s.TargetPath = '%PY%'; $s.Arguments = '\"%APP%\strikeback\strikeback.py\"'; $s.WorkingDirectory = '%APP%\strikeback'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] StrikeBack

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\Session Recorder.lnk'); $s.TargetPath = '%PY%'; $s.Arguments = '\"%APP%\recorder\recorder.py\"'; $s.WorkingDirectory = '%APP%\recorder'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] Session Recorder

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\SIEM Monitor.lnk'); $s.TargetPath = '%PY%'; $s.Arguments = '\"%APP%\siem\siem.py\"'; $s.WorkingDirectory = '%APP%\siem'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] SIEM Monitor

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\RedTeam Toolkit.lnk'); $s.TargetPath = '%PY%'; $s.Arguments = '\"%APP%\redteam\redteam.py\"'; $s.WorkingDirectory = '%APP%\redteam'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] RedTeam Toolkit

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\Sandbox Analyzer.lnk'); $s.TargetPath = '%PY%'; $s.Arguments = '\"%APP%\sandbox\sandbox.py\"'; $s.WorkingDirectory = '%APP%\sandbox'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] Sandbox Analyzer

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\NetGuard Tray.lnk'); $s.TargetPath = '%PY%'; $s.Arguments = '\"%APP%\netguard_tray.py\"'; $s.WorkingDirectory = '%APP%'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] NetGuard Tray

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESK%\NetGuard Dashboard.lnk'); $s.TargetPath = '%APP%\netguard_dashboard.html'; $s.IconLocation = '%ICO%'; $s.Save()"
echo [OK] NetGuard Dashboard

echo.
echo === 14 raccourcis crees! ===
pause
