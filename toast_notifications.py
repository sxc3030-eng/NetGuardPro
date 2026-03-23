#!/usr/bin/env python3
"""
toast_notifications.py — NetGuardPro Suite Windows Toast Notifications
=======================================================================
Sends native Windows 10/11 toast notifications for security alerts.
Graceful fallback — if winotify is not installed, all calls are silent no-ops.

Usage:
    from toast_notifications import toast_threat, toast_block, toast_scan, toast_event

    toast_threat("NetGuard Pro", "Port Scan", "high", "Source: 192.168.1.50")
    toast_block("SentinelOS", "192.0.2.42", "Suspicious activity")
    toast_scan("CleanGuard Pro", "3 threats found, 2 quarantined")
    toast_event("VPN Guard", "Connected to wg0 tunnel")
"""

import os
import logging

logger = logging.getLogger("NetGuardPro.Toast")

# ─── Graceful import ────────────────────────────────────────────────────
try:
    from winotify import Notification, audio
    HAS_TOAST = True
except ImportError:
    HAS_TOAST = False
    logger.info("winotify not installed — toast notifications disabled")

# ─── Icon paths ─────────────────────────────────────────────────────────
SUITE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(SUITE_DIR, "sentinel", "icons")
DEFAULT_ICON = os.path.join(SUITE_DIR, "netguard_icon.ico")

PROGRAM_ICONS = {
    "NetGuard Pro":    os.path.join(ICON_DIR, "netguard.ico"),
    "CleanGuard Pro":  os.path.join(ICON_DIR, "cleanguard.ico"),
    "MailShield Pro":  os.path.join(ICON_DIR, "mailshield.ico"),
    "VPN Guard Pro":   os.path.join(ICON_DIR, "vpnguard.ico"),
    "SentinelOS":      os.path.join(ICON_DIR, "sentinel.ico"),
    "Sentinel Mapper": os.path.join(ICON_DIR, "sentinel.ico"),
    "Cortex":          os.path.join(ICON_DIR, "sentinel.ico"),
    "FIM":             os.path.join(ICON_DIR, "fim.ico"),
    "Honeypot":        os.path.join(ICON_DIR, "honeypot.ico"),
    "StrikeBack":      os.path.join(ICON_DIR, "strikeback.ico"),
    "Recorder":        os.path.join(ICON_DIR, "recorder.ico"),
}

# ─── Severity colors (for title prefix) ────────────────────────────────
SEVERITY_PREFIX = {
    "critical": "🔴 CRITICAL",
    "high":     "🟠 HIGH",
    "medium":   "🟡 MEDIUM",
    "low":      "🟢 LOW",
    "info":     "ℹ️ INFO",
}


def _get_icon(program: str) -> str:
    """Get icon path for a program, fallback to default."""
    icon = PROGRAM_ICONS.get(program, DEFAULT_ICON)
    if os.path.exists(icon):
        return icon
    if os.path.exists(DEFAULT_ICON):
        return DEFAULT_ICON
    return ""


# ─── Core send function ─────────────────────────────────────────────────

def send_toast(title: str, message: str, icon_path: str = None,
               app_id: str = "NetGuardPro Suite", duration: str = "short"):
    """
    Send a Windows toast notification.
    Silent no-op if winotify is not available.

    Args:
        title:     Notification title
        message:   Notification body text
        icon_path: Path to .ico file (optional)
        app_id:    Application identifier
        duration:  "short" (5s) or "long" (25s)
    """
    if not HAS_TOAST:
        return
    try:
        toast = Notification(
            app_id=app_id,
            title=title,
            msg=message,
            duration=duration,
            icon=icon_path or ""
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
    except Exception as e:
        logger.warning(f"Toast notification failed: {e}")


# ─── Specialized toast functions ─────────────────────────────────────────

def toast_threat(program: str, threat_type: str, severity: str, details: str = ""):
    """
    Threat detection notification.
    Example: toast_threat("NetGuard Pro", "Port Scan", "high", "Source: 10.0.0.50")
    """
    prefix = SEVERITY_PREFIX.get(severity.lower(), "⚠️")
    title = f"{prefix} — {program}"
    msg = f"Threat detected: {threat_type}"
    if details:
        msg += f"\n{details}"
    send_toast(title, msg, _get_icon(program), duration="long" if severity in ("critical", "high") else "short")


def toast_block(program: str, ip: str, reason: str = ""):
    """
    Device/IP blocked notification.
    Example: toast_block("SentinelOS", "192.0.2.42", "Suspicious activity")
    """
    title = f"🛡️ Blocked — {program}"
    msg = f"Device blocked: {ip}"
    if reason:
        msg += f"\nReason: {reason}"
    send_toast(title, msg, _get_icon(program))


def toast_unblock(program: str, ip: str):
    """Device/IP unblocked notification."""
    title = f"✅ Unblocked — {program}"
    msg = f"Device unblocked: {ip}"
    send_toast(title, msg, _get_icon(program))


def toast_scan(program: str, summary: str):
    """
    Scan complete notification.
    Example: toast_scan("CleanGuard Pro", "3 threats found, 2 quarantined")
    """
    title = f"🔍 Scan Complete — {program}"
    send_toast(title, summary, _get_icon(program))


def toast_event(program: str, message: str):
    """
    Generic event notification.
    Example: toast_event("VPN Guard", "Connected to wg0 tunnel")
    """
    title = f"📢 {program}"
    send_toast(title, message, _get_icon(program))


def toast_connection(program: str, status: str, details: str = ""):
    """VPN/network connection status notification."""
    icon_map = {"connected": "🟢", "disconnected": "🔴", "error": "⚠️"}
    emoji = icon_map.get(status.lower(), "📡")
    title = f"{emoji} {status.title()} — {program}"
    send_toast(title, details or status, _get_icon(program))


def toast_quarantine(program: str, filename: str, threat: str = ""):
    """File quarantined notification."""
    title = f"🔒 Quarantined — {program}"
    msg = f"File quarantined: {filename}"
    if threat:
        msg += f"\nThreat: {threat}"
    send_toast(title, msg, _get_icon(program))


def toast_integrity(program: str, filepath: str, change_type: str = "modified"):
    """File integrity change notification."""
    title = f"📁 File {change_type.title()} — {program}"
    send_toast(title, filepath, _get_icon(program), duration="long")


def toast_honeypot(program: str, trap_type: str, source_ip: str):
    """Honeypot trap triggered notification."""
    title = f"🍯 Trap Triggered — {program}"
    msg = f"Type: {trap_type}\nSource: {source_ip}"
    send_toast(title, msg, _get_icon(program), duration="long")
