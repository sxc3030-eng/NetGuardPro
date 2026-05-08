#!/usr/bin/env python3
"""
NetGuard Pro - HTTP Authentication Server (port 8080)
Handles /auth/login and /auth/verify for the login page.
"""
import hashlib
import json
import os
import secrets
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# -- pythonw stdout fix --
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

AUTH_PORT = 8080
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "netguard_users.json")
TOKENS = {}  # {token: {user, role, name, expires}}
TOKEN_TTL = 86400  # 24h

# Default admin credentials
DEFAULT_USERS = {
    "admin": {
        "password_hash": hashlib.sha256("netguard2024".encode()).hexdigest(),
        "role": "admin",
        "name": "Administrateur",
    }
}


def load_users():
    """Load users from JSON file, or use defaults."""
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        users = {}
        for username, data in raw.items():
            pw = data.get("password", "")
            # Old format had salt:hash - just use simple sha256 now
            users[username] = {
                "password_hash": pw if len(pw) == 64 else None,
                "role": data.get("role", "viewer"),
                "name": data.get("name", username),
            }
        return users
    except Exception:
        return {}


def save_users(users):
    """Save users to JSON file."""
    data = {}
    for username, info in users.items():
        data[username] = {
            "password": info["password_hash"],
            "role": info["role"],
            "name": info["name"],
        }
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[AUTH] Error saving users: {e}")


def check_password(username, password, users):
    """Check password against stored hash."""
    user = users.get(username)
    if not user:
        return False
    stored = user.get("password_hash")
    if not stored:
        return False
    return hashlib.sha256(password.encode()).hexdigest() == stored


def init_default_users():
    """Reset users file with default admin/netguard2024."""
    save_users(DEFAULT_USERS)
    return DEFAULT_USERS.copy()


class AuthHandler(BaseHTTPRequestHandler):
    users = {}

    def log_message(self, format, *args):
        print(f"[AUTH] {args[0]}" if args else "")

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """Serve static HTML/CSS/JS/SVG/ICO files from the NetGuard directory."""
        MIME = {
            ".html": "text/html", ".css": "text/css", ".js": "application/javascript",
            ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png",
            ".ico": "image/x-icon", ".jpg": "image/jpeg",
        }
        # Map /map to netguard_map.html
        req_path = self.path.split("?")[0]
        if req_path == "/map":
            req_path = "/netguard_map.html"
        # Only serve files from project root, no directory traversal
        if ".." in req_path:
            self.send_error(403)
            return
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, req_path.lstrip("/"))
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in MIME or not os.path.isfile(file_path):
            self.send_error(404)
            return
        try:
            mode = "rb"
            with open(file_path, mode) as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", MIME[ext])
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        except Exception:
            self.send_error(500)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
        except Exception:
            self._send_json({"ok": False, "error": "Invalid JSON"}, 400)
            return

        if self.path == "/auth/login":
            self._handle_login(body)
        elif self.path == "/auth/verify":
            self._handle_verify(body)
        else:
            self._send_json({"ok": False, "error": "Not found"}, 404)

    def _handle_login(self, body):
        username = body.get("username", "").strip()
        password = body.get("password", "")

        # Reload users each login attempt
        AuthHandler.users = load_users()
        # If no valid users or admin has old format, reset defaults
        if not AuthHandler.users or not AuthHandler.users.get("admin", {}).get("password_hash"):
            AuthHandler.users = init_default_users()

        if check_password(username, password, AuthHandler.users):
            token = secrets.token_hex(32)
            user_info = AuthHandler.users[username]
            TOKENS[token] = {
                "user": username,
                "role": user_info["role"],
                "name": user_info["name"],
                "expires": time.time() + TOKEN_TTL,
            }
            print(f"[AUTH] Login OK: {username} (role: {user_info['role']})")
            self._send_json({
                "ok": True,
                "token": token,
                "user": username,
                "role": user_info["role"],
                "name": user_info["name"],
            })
        else:
            print(f"[AUTH] Login FAILED: {username}")
            self._send_json({"ok": False, "error": "Invalid credentials"}, 401)

    def _handle_verify(self, body):
        token = body.get("token", "")
        session = TOKENS.get(token)
        if session and session["expires"] > time.time():
            self._send_json({
                "ok": True,
                "user": session["user"],
                "role": session["role"],
                "name": session["name"],
            })
        else:
            if token in TOKENS:
                del TOKENS[token]
            self._send_json({"ok": False, "error": "Invalid or expired token"}, 401)


def main():
    # Init users file with default password if needed
    users = load_users()
    if not users or not users.get("admin", {}).get("password_hash"):
        print("[AUTH] Resetting admin password to default: admin / netguard2024")
        init_default_users()

    server = HTTPServer(("localhost", AUTH_PORT), AuthHandler)
    print(f"[AUTH] Serveur d'authentification demarre sur http://localhost:{AUTH_PORT}")
    print(f"[AUTH] Compte par defaut: admin / netguard2024")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[AUTH] Arret du serveur d'authentification")
        server.server_close()


if __name__ == "__main__":
    main()
