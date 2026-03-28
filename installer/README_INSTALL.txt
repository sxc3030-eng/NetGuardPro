================================================================================
  NetGuard Pro v3.0.0 — What Was Installed
================================================================================

INSTALLATION LOCATION:
  C:\Program Files\NetGuard Pro\

WHAT THIS SOFTWARE DOES:
  NetGuard Pro is a cybersecurity defense suite that monitors your network
  for threats, blocks malicious traffic, and protects your system.

COMPONENTS INSTALLED:
  - NetGuard Pro       : Network firewall and intrusion detection (port 8765)
  - SentinelOS Cortex  : Central security orchestrator (port 8900)
  - VPN Guard Pro      : WireGuard VPN manager (port 8820)
  - CleanGuard Pro     : Antivirus and system cleaner (port 8810)
  - MailShield Pro     : Email security and phishing filter (port 8801)
  - HoneyPot Agent     : Decoy services for attacker detection (port 8830)
  - FIM                : File integrity monitoring (port 8840)
  - Session Recorder   : Forensic session recording (port 8860)
  - StrikeBack         : Active defense and response (port 8850)

PYTHON RUNTIME:
  A portable Python 3.12 is bundled in the install directory.
  It does NOT modify your system Python or PATH.
  Location: C:\Program Files\NetGuard Pro\python\

NETWORK ACTIVITY:
  - All communication is LOCAL ONLY (localhost / 127.0.0.1)
  - No data is sent to external servers unless you configure:
    * VPN connections (WireGuard — user-configured)
    * Email alerts (SMTP — user-configured)
    * Threat intelligence feeds (public feeds — read-only)
  - Firewall rules added (if selected):
    * "NetGuard Pro" — allows Python inbound
    * "NetGuard Pro WS" — allows TCP port 8765

REGISTRY CHANGES:
  - HKCU\Software\Microsoft\Windows\CurrentVersion\Run\NetGuardPro
    (only if "auto-start" was selected during install)

FILES CREATED OUTSIDE INSTALL DIR:
  - Desktop shortcut (if selected)
  - Start Menu group: "NetGuard Pro"
  - Install log: %TEMP%\Setup Log *.txt

DATA STORAGE:
  - All data stays in the install directory
  - Logs: C:\Program Files\NetGuard Pro\logs\
  - Captures: C:\Program Files\NetGuard Pro\captures\
  - Reports: C:\Program Files\NetGuard Pro\reports\
  - No hidden files, no AppData pollution

HOW TO UNINSTALL:
  1. Settings > Apps > NetGuard Pro > Uninstall
  2. Or: Start Menu > NetGuard Pro > Uninstall
  The uninstaller removes ALL files, registry entries, and firewall rules.
  Nothing is left behind.

LOGS:
  - Install log: %TEMP%\Setup Log *.txt (created by installer)
  - Runtime log: C:\Program Files\NetGuard Pro\netguard.log
  - All actions are logged with timestamps

SUPPORT:
  - GitHub: https://github.com/sxc3030-eng/NetGuardPro
  - Issues: https://github.com/sxc3030-eng/NetGuardPro/issues

================================================================================
  No hidden behavior. No telemetry. No data collection.
  Everything NetGuard Pro does is visible and logged.
================================================================================
