#!/usr/bin/env python3
"""
NetGuardPro Desktop — Graphical Launcher
Windows Desktop Environment for the NetGuardPro Cybersecurity Suite
"""

import json
import os
import socket
import subprocess
import sys
import threading
import time
import platform

try:
    import webview
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywebview", "--quiet"])
    import webview

# ── Paths ────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
LAUNCHERS_DIR = os.path.join(ROOT_DIR, "launchers")
THEMES_DIR = os.path.join(BASE_DIR, "themes")
SETTINGS_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "NetGuardPro")
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "desktop_settings.json")

# ── Program Registry ─────────────────────────────────────────
PROGRAMS = [
    {"id": "netguard",    "name": "NetGuard Pro",     "port": 8765, "icon": "shield-halved",   "color": "#00e5ff",
     "desc": "IDS / Firewall",           "launcher": "LANCER_NETGUARD.bat",         "category": "defense"},
    {"id": "sentinel",    "name": "SentinelOS Cortex","port": 8900, "icon": "brain",           "color": "#ff00ff",
     "desc": "Command Center",           "launcher": "LANCER_SENTINEL.bat",         "category": "core"},
    {"id": "cleanguard",  "name": "CleanGuard Pro",   "port": 8810, "icon": "broom",           "color": "#00ff88",
     "desc": "System Cleanup",           "launcher": "LANCER_CLEANGUARD.bat",       "category": "utility"},
    {"id": "mailshield",  "name": "MailShield Pro",   "port": 8801, "icon": "envelope-open-text","color": "#ff6600",
     "desc": "Email Security",           "launcher": "LANCER_MAILSHIELD.bat",       "category": "defense"},
    {"id": "vpnguard",    "name": "VPN Guard Pro",    "port": 8820, "icon": "lock",            "color": "#8855ff",
     "desc": "WireGuard VPN",            "launcher": "LANCER_VPNGUARD.bat",         "category": "network"},
    {"id": "honeypot",    "name": "HoneyPot",         "port": 8830, "icon": "jar",             "color": "#ffcc00",
     "desc": "Honeypot Trap System",     "launcher": "LANCER_HONEYPOT.bat",         "category": "defense"},
    {"id": "fim",         "name": "File Integrity",   "port": 8840, "icon": "file-shield",     "color": "#22ddaa",
     "desc": "File Integrity Monitor",   "launcher": "LANCER_FIM.bat",              "category": "defense"},
    {"id": "strikeback",  "name": "StrikeBack",       "port": 8850, "icon": "crosshairs",      "color": "#ff2255",
     "desc": "Active Defense",           "launcher": "LANCER_STRIKEBACK.bat",       "category": "defense"},
    {"id": "recorder",    "name": "Recorder",         "port": 8860, "icon": "video",           "color": "#33aaff",
     "desc": "Forensic Recorder",        "launcher": "LANCER_RECORDER.bat",         "category": "forensics"},
    {"id": "redteam",     "name": "RedTeam Simulator","port": 8870, "icon": "crosshairs",      "color": "#ff2222",
     "desc": "Penetration Testing",      "launcher": "LANCER_REDTEAM.bat",          "category": "offense"},
    {"id": "siem",        "name": "SIEM / SOAR",      "port": 8880, "icon": "chart-line",      "color": "#00ccff",
     "desc": "Security Brain",           "launcher": "LANCER_SIEM.bat",             "category": "core"},
    {"id": "sandbox",     "name": "Sandbox",          "port": 8890, "icon": "flask-vial",      "color": "#aa44ff",
     "desc": "Malware Analysis",         "launcher": "LANCER_SANDBOX.bat",          "category": "forensics"},
    {"id": "mobile",      "name": "Mobile Gateway",   "port": 8895, "icon": "mobile-screen",   "color": "#11cc88",
     "desc": "Mobile Protection",        "launcher": "LANCER_MOBILE_GATEWAY.bat",   "category": "network"},
    {"id": "helpagent",   "name": "Help Agent",       "port": 8899, "icon": "robot",           "color": "#ffaa00",
     "desc": "AI Assistant",             "launcher": "LANCER_HELPAGENT.bat",         "category": "utility"},
]


def port_is_open(port: int) -> bool:
    """Check if a local port is listening."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False


# ── Desktop API (pywebview bridge) ───────────────────────────
class DesktopAPI:
    """Exposed to JavaScript via window.pywebview.api"""

    def __init__(self):
        self._procs: dict[str, subprocess.Popen] = {}

    # ── Launch / Stop ────────────────────────────────────────
    def launch_program(self, prog_id: str) -> dict:
        prog = next((p for p in PROGRAMS if p["id"] == prog_id), None)
        if not prog:
            return {"ok": False, "error": f"Unknown program: {prog_id}"}
        bat = os.path.join(LAUNCHERS_DIR, prog["launcher"])
        if not os.path.isfile(bat):
            return {"ok": False, "error": f"Launcher not found: {prog['launcher']}"}
        try:
            proc = subprocess.Popen(
                ["cmd", "/c", bat],
                cwd=LAUNCHERS_DIR,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            self._procs[prog_id] = proc
            return {"ok": True, "pid": proc.pid}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop_program(self, prog_id: str) -> dict:
        prog = next((p for p in PROGRAMS if p["id"] == prog_id), None)
        if not prog:
            return {"ok": False, "error": f"Unknown program: {prog_id}"}
        try:
            if prog_id in self._procs:
                self._procs[prog_id].terminate()
                del self._procs[prog_id]
            # Also kill by port
            os.system(f'for /f "tokens=5" %a in (\'netstat -aon ^| findstr :{prog["port"]}\') do taskkill /F /PID %a 2>nul')
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def shutdown_all(self) -> dict:
        stopped = []
        for prog in PROGRAMS:
            if port_is_open(prog["port"]):
                self.stop_program(prog["id"])
                stopped.append(prog["name"])
        return {"ok": True, "stopped": stopped}

    # ── Status ───────────────────────────────────────────────
    def get_status(self) -> list:
        result = []
        for p in PROGRAMS:
            result.append({
                "id": p["id"],
                "name": p["name"],
                "port": p["port"],
                "icon": p["icon"],
                "color": p["color"],
                "desc": p["desc"],
                "category": p["category"],
                "running": port_is_open(p["port"]),
            })
        return result

    def get_system_info(self) -> dict:
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=0.3)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("C:\\")
            net = psutil.net_io_counters()
            return {
                "hostname": platform.node(),
                "os": f"Windows {platform.release()}",
                "cpu_percent": cpu,
                "ram_total_gb": round(mem.total / 1e9, 1),
                "ram_used_gb": round(mem.used / 1e9, 1),
                "ram_percent": mem.percent,
                "disk_total_gb": round(disk.total / 1e9, 1),
                "disk_used_gb": round(disk.used / 1e9, 1),
                "disk_percent": disk.percent,
                "net_sent_mb": round(net.bytes_sent / 1e6, 1),
                "net_recv_mb": round(net.bytes_recv / 1e6, 1),
            }
        except ImportError:
            return {"hostname": platform.node(), "os": f"Windows {platform.release()}",
                    "cpu_percent": 0, "ram_percent": 0, "disk_percent": 0,
                    "ram_total_gb": 0, "ram_used_gb": 0,
                    "disk_total_gb": 0, "disk_used_gb": 0,
                    "net_sent_mb": 0, "net_recv_mb": 0}

    # ── Settings / Themes ────────────────────────────────────
    def save_settings(self, settings_json: str) -> dict:
        try:
            os.makedirs(SETTINGS_DIR, exist_ok=True)
            with open(SETTINGS_FILE, "w") as f:
                f.write(settings_json)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def load_settings(self) -> str:
        try:
            if os.path.isfile(SETTINGS_FILE):
                with open(SETTINGS_FILE, "r") as f:
                    return f.read()
        except Exception:
            pass
        return json.dumps({"wallpaper": "#0a0a12", "accent": "#00e5ff", "iconSize": "medium", "layout": "grid"})

    def load_theme(self, name: str) -> str:
        theme_file = os.path.join(THEMES_DIR, f"{name}.json")
        try:
            if os.path.isfile(theme_file):
                with open(theme_file, "r") as f:
                    return f.read()
        except Exception:
            pass
        return "{}"

    def get_security_score(self) -> dict:
        running = sum(1 for p in PROGRAMS if port_is_open(p["port"]))
        total = len(PROGRAMS)
        pct = int((running / max(total, 1)) * 100)
        if pct >= 80:
            grade, color = "A", "#00ff88"
        elif pct >= 60:
            grade, color = "B", "#88ff00"
        elif pct >= 40:
            grade, color = "C", "#ffcc00"
        elif pct >= 20:
            grade, color = "D", "#ff8800"
        else:
            grade, color = "F", "#ff2222"
        return {"grade": grade, "color": color, "running": running, "total": total, "percent": pct}

    def get_notifications(self) -> list:
        notes = []
        for p in PROGRAMS:
            if port_is_open(p["port"]):
                notes.append({"type": "info", "msg": f"{p['name']} is running on port {p['port']}"})
        return notes[-8:]


# ── Status Poller (pushes updates to JS) ─────────────────────
class StatusPoller(threading.Thread):
    def __init__(self, api: DesktopAPI):
        super().__init__(daemon=True)
        self.api = api
        self.window = None

    def run(self):
        time.sleep(3)
        while True:
            try:
                if self.window:
                    status = self.api.get_status()
                    score = self.api.get_security_score()
                    sys_info = self.api.get_system_info()
                    js = f"if(window.updateStatus) window.updateStatus({json.dumps(status)},{json.dumps(score)},{json.dumps(sys_info)})"
                    self.window.evaluate_js(js)
            except Exception:
                pass
            time.sleep(3)


# ── Main ─────────────────────────────────────────────────────
def main():
    api = DesktopAPI()
    poller = StatusPoller(api)

    html_path = os.path.join(BASE_DIR, "desktop.html")

    def on_loaded():
        poller.window = window

    window = webview.create_window(
        "NetGuardPro Desktop — Cybersecurity Suite",
        html_path,
        js_api=api,
        width=1440,
        height=900,
        min_size=(1024, 600),
        background_color="#0a0a12",
    )
    window.events.loaded += on_loaded
    poller.start()
    webview.start(debug=False)


if __name__ == "__main__":
    main()
