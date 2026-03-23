#!/usr/bin/env python3
"""
netguardpro_installer.py — NetGuardPro Suite Selective Installer
=================================================================
Standalone pywebview installer that lets users choose which programs
to install, checks dependencies, copies files, and creates shortcuts.

Launch: python netguardpro_installer.py
"""

import json
import os
import sys
import shutil
import subprocess
import ctypes
import webview

INSTALLER_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.dirname(INSTALLER_DIR)  # Parent = full suite
HTML_FILE = os.path.join(INSTALLER_DIR, "installer_ui.html")

# ═══════════════════════════════════════════════════════════════════════
#  Program definitions
# ═══════════════════════════════════════════════════════════════════════

PROGRAMS = [
    {
        "id": "netguard",
        "name": "NetGuard Pro",
        "icon": "🛡️",
        "description": "Network IDS, packet capture, deep packet inspection, firewall",
        "description_fr": "IDS réseau, capture de paquets, inspection approfondie, pare-feu",
        "files": [
            "netguard.py", "netguard_dashboard.html", "netguard_help.html",
            "netguard_login.html", "netguard_map.html", "netguard_network.html",
            "netguard_analyze.html", "netguard_history.html", "netguard_panels.html",
            "netguard_service.html", "netguard_vitrine.html", "netguard_settings.json",
            "netguard_icon.ico", "netguard_icon.png", "netguard_logo.svg"
        ],
        "shared": ["startup_utils.py", "netguard_tray.py", "permissions.py",
                    "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "scapy", "requests", "psutil", "winotify", "pystray", "Pillow"],
        "optional_deps": ["Npcap (for packet capture)"],
        "launcher": "LANCER_NETGUARD.bat",
        "size_mb": 1.2,
        "admin": False
    },
    {
        "id": "cleanguard",
        "name": "CleanGuard Pro",
        "icon": "🧹",
        "description": "System cleaner, malware scanner, YARA rules, quarantine",
        "description_fr": "Nettoyeur système, scanner malware, règles YARA, quarantaine",
        "files": ["cleanguard/"],
        "shared": ["startup_utils.py", "permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "psutil", "watchdog", "winotify", "pystray", "Pillow"],
        "launcher": "LANCER_CLEANGUARD.bat",
        "size_mb": 0.8,
        "admin": False
    },
    {
        "id": "mailshield",
        "name": "MailShield Pro",
        "icon": "📧",
        "description": "Secure email client with phishing detection and SPF/DKIM validation",
        "description_fr": "Client email sécurisé avec détection phishing et validation SPF/DKIM",
        "files": ["mailshield/"],
        "shared": ["startup_utils.py", "permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "requests", "cryptography", "dnspython", "bleach", "winotify", "pystray", "Pillow"],
        "launcher": "LANCER_MAILSHIELD.bat",
        "size_mb": 0.9,
        "admin": False
    },
    {
        "id": "vpnguard",
        "name": "VPN Guard Pro",
        "icon": "🔐",
        "description": "WireGuard VPN client with kill switch and DNS leak protection",
        "description_fr": "Client VPN WireGuard avec kill switch et protection fuite DNS",
        "files": ["vpnguard/", "wireguard/"],
        "shared": ["startup_utils.py", "permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "psutil", "requests", "cryptography", "winotify", "pystray", "Pillow"],
        "optional_deps": ["WireGuard (system install)"],
        "launcher": "LANCER_VPNGUARD.bat",
        "size_mb": 0.6,
        "admin": True
    },
    {
        "id": "sentinel_mapper",
        "name": "SentinelOS Mapper",
        "icon": "🗺️",
        "description": "Interactive network map with device firewall and multi-interface scanning",
        "description_fr": "Carte réseau interactive avec pare-feu appareils et scan multi-interface",
        "files": ["sentinel/sentinel_mapper.py", "sentinel/sentinel_map.html",
                  "sentinel/sentinel_settings.json", "sentinel/SentinelOS.ico", "sentinel/icons/"],
        "shared": ["startup_utils.py", "permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "psutil", "requests", "winotify"],
        "launcher": "LANCER_SENTINEL_MAPPER.bat",
        "size_mb": 0.5,
        "admin": True
    },
    {
        "id": "cortex",
        "name": "SentinelOS Cortex",
        "icon": "🧠",
        "description": "Central orchestrator — starts and manages all agents",
        "description_fr": "Orchestrateur central — démarre et gère tous les agents",
        "files": ["sentinel/cortex.py", "sentinel/agent_bus.py", "sentinel/playbook_engine.py",
                  "sentinel/threat_intel.py", "sentinel/alert_manager.py",
                  "sentinel/sentinel_dashboard.html", "sentinel/sentinel_settings.json",
                  "sentinel/SentinelOS.ico", "sentinel/icons/", "sentinel/threat_data/"],
        "shared": ["startup_utils.py", "permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "psutil", "requests", "aiohttp", "websockets", "scapy",
                 "cryptography", "winotify", "pystray", "Pillow"],
        "launcher": "LANCER_SENTINEL.bat",
        "size_mb": 1.5,
        "admin": True
    },
    {
        "id": "fim",
        "name": "File Integrity Monitor",
        "icon": "📁",
        "description": "Monitors files for unauthorized changes using SHA-256 hashing",
        "description_fr": "Surveille les fichiers pour les changements non autorisés via SHA-256",
        "files": ["fim/"],
        "shared": ["permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "psutil", "winotify"],
        "launcher": None,
        "size_mb": 0.2,
        "admin": False
    },
    {
        "id": "honeypot",
        "name": "Honeypot",
        "icon": "🍯",
        "description": "Deception traps simulating vulnerable services to detect intruders",
        "description_fr": "Pièges simulant des services vulnérables pour détecter les intrus",
        "files": ["honeypot/"],
        "shared": ["permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "psutil", "winotify"],
        "launcher": None,
        "size_mb": 0.2,
        "admin": True
    },
    {
        "id": "strikeback",
        "name": "StrikeBack",
        "icon": "⚔️",
        "description": "Active defense with automated counter-measures against threats",
        "description_fr": "Défense active avec contre-mesures automatisées contre les menaces",
        "files": ["strikeback/"],
        "shared": ["permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "psutil", "winotify"],
        "launcher": None,
        "size_mb": 0.3,
        "admin": True
    },
    {
        "id": "recorder",
        "name": "Recorder",
        "icon": "🎙️",
        "description": "Forensic recording of network events and security incidents",
        "description_fr": "Enregistrement forensique des événements réseau et incidents de sécurité",
        "files": ["recorder/"],
        "shared": ["permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "psutil", "winotify"],
        "launcher": None,
        "size_mb": 0.3,
        "admin": False
    },
    {
        "id": "redteam",
        "name": "RedTeam Agent",
        "icon": "🎯",
        "description": "Penetration testing toolkit with automated vulnerability scanning",
        "description_fr": "Boite a outils de test de penetration avec scan de vulnerabilites automatise",
        "files": ["redteam/"],
        "shared": ["permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "psutil", "requests", "scapy", "winotify"],
        "launcher": None,
        "size_mb": 0.4,
        "admin": True
    },
    {
        "id": "siem",
        "name": "SIEM Agent",
        "icon": "🧠",
        "description": "Security information and event management — log collection and correlation",
        "description_fr": "Gestion des informations et evenements de securite — collecte et correlation de logs",
        "files": ["siem/"],
        "shared": ["permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "psutil", "requests", "winotify"],
        "launcher": None,
        "size_mb": 0.4,
        "admin": False
    },
    {
        "id": "sandbox",
        "name": "Sandbox Agent",
        "icon": "📦",
        "description": "Dynamic file analysis in isolated environment for malware detection",
        "description_fr": "Analyse dynamique de fichiers en environnement isole pour detection de malware",
        "files": ["sandbox/"],
        "shared": ["permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "psutil", "requests", "winotify"],
        "launcher": None,
        "size_mb": 0.5,
        "admin": True
    },
    {
        "id": "mobile_gateway",
        "name": "Mobile Gateway",
        "icon": "📱",
        "description": "Mobile device gateway for remote monitoring and push notifications",
        "description_fr": "Passerelle mobile pour surveillance a distance et notifications push",
        "files": ["mobile_gateway/"],
        "shared": ["permissions.py", "toast_notifications.py", "permissions_state.json"],
        "deps": ["pywebview", "psutil", "requests", "aiohttp", "winotify"],
        "launcher": None,
        "size_mb": 0.3,
        "admin": False
    },
    {
        "id": "help_agent",
        "name": "Help Agent",
        "icon": "🤖",
        "description": "Interactive guide for all NetGuardPro programs",
        "description_fr": "Guide interactif pour tous les programmes NetGuardPro",
        "files": ["help_agent/"],
        "shared": [],
        "deps": ["pywebview", "winotify"],
        "launcher": "LANCER_HELPAGENT.bat",
        "size_mb": 0.1,
        "admin": False
    }
]


class InstallerAPI:
    """pywebview API for the installer."""

    def get_programs(self) -> str:
        """Return list of installable programs."""
        return json.dumps(PROGRAMS)

    def check_dependencies(self) -> str:
        """Check system dependencies."""
        results = {"python": False, "python_version": "", "npcap": False,
                   "wireguard": False, "pip": False, "admin": False}

        # Python
        try:
            import platform
            results["python"] = True
            results["python_version"] = platform.python_version()
        except Exception:
            pass

        # pip
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"],
                          capture_output=True, timeout=10)
            results["pip"] = True
        except Exception:
            pass

        # Npcap
        results["npcap"] = os.path.exists(r"C:\Program Files\Npcap") or \
                           os.path.exists(r"C:\Windows\System32\Npcap")

        # WireGuard
        try:
            r = subprocess.run(["where", "wg"], capture_output=True, timeout=5)
            results["wireguard"] = r.returncode == 0
        except Exception:
            results["wireguard"] = os.path.exists(r"C:\Program Files\WireGuard\wg.exe")

        # Admin
        try:
            results["admin"] = bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            pass

        return json.dumps(results)

    def install(self, selected_ids: list, install_path: str) -> str:
        """Install selected programs to the specified path."""
        if not selected_ids:
            return json.dumps({"error": "No programs selected / Aucun programme sélectionné"})

        install_path = install_path.strip() or r"C:\NetGuardPro"
        os.makedirs(install_path, exist_ok=True)

        installed = []
        errors = []
        all_deps = set()

        for prog in PROGRAMS:
            if prog["id"] not in selected_ids:
                continue

            try:
                # Copy files
                for f in prog["files"]:
                    src = os.path.join(SOURCE_DIR, f)
                    dst = os.path.join(install_path, f)
                    if f.endswith("/"):
                        # Directory copy
                        src = src.rstrip("/\\")
                        dst = dst.rstrip("/\\")
                        if os.path.isdir(src):
                            if os.path.exists(dst):
                                shutil.rmtree(dst)
                            shutil.copytree(src, dst)
                    else:
                        os.makedirs(os.path.dirname(dst) if os.path.dirname(dst) else install_path, exist_ok=True)
                        if os.path.isfile(src):
                            shutil.copy2(src, dst)

                # Copy shared modules
                for sf in prog.get("shared", []):
                    src = os.path.join(SOURCE_DIR, sf)
                    dst = os.path.join(install_path, sf)
                    if os.path.isfile(src) and not os.path.exists(dst):
                        shutil.copy2(src, dst)

                # Copy launcher
                if prog.get("launcher"):
                    src = os.path.join(SOURCE_DIR, "launchers", prog["launcher"])
                    dst_dir = os.path.join(install_path, "launchers")
                    os.makedirs(dst_dir, exist_ok=True)
                    if os.path.isfile(src):
                        shutil.copy2(src, os.path.join(dst_dir, prog["launcher"]))

                # Collect deps
                all_deps.update(prog.get("deps", []))
                installed.append(prog["id"])

            except Exception as e:
                errors.append(f"{prog['name']}: {str(e)}")

        # Install pip dependencies
        pip_errors = []
        if all_deps:
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install"] + list(all_deps),
                    capture_output=True, timeout=120
                )
            except Exception as e:
                pip_errors.append(str(e))

        # Copy requirements.txt
        req_src = os.path.join(SOURCE_DIR, "requirements.txt")
        if os.path.isfile(req_src):
            shutil.copy2(req_src, os.path.join(install_path, "requirements.txt"))

        return json.dumps({
            "ok": True,
            "installed": installed,
            "install_path": install_path,
            "errors": errors,
            "pip_errors": pip_errors,
            "deps_installed": list(all_deps)
        })

    def create_shortcuts(self, install_path: str, selected_ids: list) -> str:
        """Create desktop shortcuts for installed programs."""
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        created = []

        for prog in PROGRAMS:
            if prog["id"] not in selected_ids or not prog.get("launcher"):
                continue

            launcher_path = os.path.join(install_path, "launchers", prog["launcher"])
            if not os.path.exists(launcher_path):
                continue

            # Create .lnk shortcut via PowerShell
            shortcut_path = os.path.join(desktop, f"{prog['name']} — NetGuardPro.lnk")
            ps_cmd = f'''
$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut("{shortcut_path}")
$sc.TargetPath = "{launcher_path}"
$sc.WorkingDirectory = "{os.path.join(install_path, 'launchers')}"
$sc.Description = "{prog['description']}"
$sc.Save()
'''
            try:
                subprocess.run(["powershell.exe", "-Command", ps_cmd],
                              capture_output=True, timeout=10)
                created.append(prog["name"])
            except Exception:
                pass

        return json.dumps({"ok": True, "shortcuts": created})

    def browse_folder(self) -> str:
        """Open folder browser dialog."""
        try:
            result = webview.windows[0].create_file_dialog(
                webview.FOLDER_DIALOG,
                directory=r"C:\\"
            )
            if result and len(result) > 0:
                return json.dumps({"path": result[0]})
        except Exception:
            pass
        return json.dumps({"path": ""})


def main():
    api = InstallerAPI()

    if not os.path.exists(HTML_FILE):
        print(f"[!] Installer UI not found: {HTML_FILE}")
        sys.exit(1)

    window = webview.create_window(
        "NetGuardPro Suite — Installer",
        HTML_FILE,
        js_api=api,
        width=900,
        height=700,
        min_size=(800, 600),
        background_color="#0f0f13",
        text_select=True
    )
    webview.start(debug=False)


if __name__ == "__main__":
    main()
