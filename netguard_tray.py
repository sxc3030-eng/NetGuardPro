"""
NetGuard Pro - System Tray (Windows)
Icone dans la barre des taches en bas a droite
Clic droit : Menu avec options
Double-clic : Ouvrir le dashboard
"""
import sys
import os

# Fix pythonw (no console)
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

import threading
import subprocess

try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
except ImportError:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pystray", "pillow"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        import pystray
        from pystray import MenuItem as item
        from PIL import Image, ImageDraw
    except Exception as e:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tray_error.log"), "w") as f:
            f.write(f"Failed to install pystray/pillow: {e}\n")
        sys.exit(1)


def create_icon(color=(77, 159, 255)):
    """Cree une icone 64x64 avec le logo NG"""
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([2, 2, 62, 62], radius=12, fill=(15, 15, 19))
    r, g, b = color
    draw.line([12, 12, 52, 52], fill=(r, g, b, 255), width=5)
    draw.line([52, 12, 32, 32], fill=(r, g, b, 200), width=4)
    draw.line([32, 32, 12, 52], fill=(r, g, b, 200), width=4)
    draw.ellipse([28, 28, 36, 36], fill=(180, 125, 255, 255))
    return img


def create_icon_status(running=True):
    color = (61, 255, 180) if running else (255, 77, 106)
    return create_icon(color)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD  = os.path.join(SCRIPT_DIR, "netguard_dashboard.html")
SERVICE    = os.path.join(SCRIPT_DIR, "netguard_service.html")
MAP_FILE   = os.path.join(SCRIPT_DIR, "netguard_map.html")
BACKEND    = os.path.join(SCRIPT_DIR, "netguard.py")

_backend_process = None


def is_running():
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex(('localhost', 8765))
        s.close()
        return result == 0
    except Exception:
        return False


def open_dashboard(icon, item):
    import webbrowser
    webbrowser.open(f"file:///{DASHBOARD.replace(os.sep, '/')}")


def open_service_manager(icon, item):
    import webbrowser
    webbrowser.open(f"file:///{SERVICE.replace(os.sep, '/')}")


def open_map(icon, item):
    import webbrowser
    webbrowser.open(f"file:///{MAP_FILE.replace(os.sep, '/')}")


def start_backend(icon, item):
    global _backend_process
    if not is_running():
        flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        _backend_process = subprocess.Popen(
            [sys.executable, BACKEND],
            cwd=SCRIPT_DIR,
            creationflags=flags,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        update_icon(icon)


def stop_backend(icon, item):
    global _backend_process
    if _backend_process and _backend_process.poll() is None:
        _backend_process.terminate()
        try:
            _backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _backend_process.kill()
        _backend_process = None
    # Also kill any orphan netguard.py processes still holding the port
    _kill_orphan_backends()
    update_icon(icon)


def _kill_orphan_backends():
    """Kill any pythonw/python processes running netguard.py that we didn't start"""
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                name = (proc.info['name'] or '').lower()
                cmdline = ' '.join(proc.info['cmdline'] or []).lower()
                if name in ('pythonw.exe', 'python.exe') and 'netguard.py' in cmdline:
                    if _backend_process and proc.pid == _backend_process.pid:
                        continue
                    proc.terminate()
                    try:
                        proc.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except ImportError:
        # No psutil — try taskkill as fallback
        try:
            subprocess.run(
                ['taskkill', '/F', '/FI', 'WINDOWTITLE eq NetGuard*', '/IM', 'pythonw.exe'],
                capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
        except Exception:
            pass


def restart_backend(icon, item):
    stop_backend(icon, item)
    import time
    time.sleep(1)
    start_backend(icon, item)


def update_icon(icon):
    try:
        running = is_running()
        icon.icon = create_icon_status(running)
        icon.title = "NetGuard Pro - " + ("Actif" if running else "Arrete")
    except Exception:
        pass


def quit_tray(icon, item):
    stop_backend(icon, item)
    icon.stop()


def status_poller(icon):
    import time
    while True:
        try:
            update_icon(icon)
        except Exception:
            pass
        time.sleep(5)


def main():
    running = is_running()

    menu = pystray.Menu(
        item('Ouvrir Dashboard',     open_dashboard, default=True),
        item('Service Manager',      open_service_manager),
        item('Carte mondiale',       open_map),
        pystray.Menu.SEPARATOR,
        item('Demarrer NetGuard',    start_backend),
        item('Arreter NetGuard',     stop_backend),
        item('Redemarrer',           restart_backend),
        pystray.Menu.SEPARATOR,
        item('Quitter',              quit_tray),
    )

    icon = pystray.Icon(
        name="NetGuardPro",
        icon=create_icon_status(running),
        title="NetGuard Pro - " + ("Actif" if running else "Arrete"),
        menu=menu,
    )

    t = threading.Thread(target=status_poller, args=(icon,), daemon=True)
    t.start()

    icon.run()


if __name__ == "__main__":
    main()
