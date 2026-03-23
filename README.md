# 🛡️ NetGuardPro Suite v3.0

**A modular cybersecurity platform for Windows** — 10 programs covering network defense, malware scanning, VPN, email security, and more.

> **Plateforme de cybersécurité modulaire pour Windows** — 10 programmes couvrant la défense réseau, le scan de malware, VPN, sécurité email, et plus.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?logo=windows)
![License](https://img.shields.io/badge/License-GPL%20v3-green)
![Programs](https://img.shields.io/badge/Programs-10-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   SentinelOS Cortex (:8900)                 │
│                Central Orchestrator / Agent Bus              │
├───────┬───────┬───────┬───────┬───────┬───────┬─────┬───────┤
│       │       │       │       │       │       │     │       │
▼       ▼       ▼       ▼       ▼       ▼       ▼     ▼       │
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌────────┐ │
│ Net ││Clean││Mail ││ VPN ││Honey││ FIM ││Strk ││Recorder│ │
│Guard││Guard││Shld ││Guard││ pot ││     ││Back ││        │ │
│:8765││:8810││:8801││:8820││:8830││:8840││:8850││:8860   │ │
└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└────────┘ │
                                                              │
         ┌──────────────────────────────┐                     │
         │   SentinelOS Mapper          │◄────────────────────┘
         │   Network Map + Firewall     │
         └──────────────────────────────┘

  Shared Modules:
  ├── permissions.py         (role-based access control)
  ├── toast_notifications.py (Windows toast alerts)
  ├── startup_utils.py       (system tray + auto-start)
  └── netguard_tray.py       (tray icon management)
```

Each program runs **independently** via its own launcher, or **all together** through **SentinelOS Cortex**.

---

## 🧩 Programs

| # | Program | Port | Description |
|---|---------|------|-------------|
| 1 | **NetGuard Pro** 🛡️ | 8765 | Network IDS, packet capture, DPI, firewall, geo-blocking |
| 2 | **CleanGuard Pro** 🧹 | 8810 | System cleaner, malware scanner, YARA rules, quarantine |
| 3 | **MailShield Pro** 📧 | 8801 | Secure email, phishing detection, SPF/DKIM, attachment scan |
| 4 | **VPN Guard Pro** 🔐 | 8820 | WireGuard VPN, kill switch, DNS leak protection |
| 5 | **SentinelOS Mapper** 🗺️ | — | Interactive network map, device firewall, multi-interface scan |
| 6 | **SentinelOS Cortex** 🧠 | 8900 | Central orchestrator, playbooks, threat intelligence, alerts |
| 7 | **File Integrity Monitor** 📁 | 8840 | SHA-256 file integrity monitoring |
| 8 | **Honeypot** 🍯 | 8830 | Deception traps (SSH, FTP, HTTP) |
| 9 | **StrikeBack** ⚔️ | 8850 | Active defense, auto-blocking, counter-measures |
| 10 | **Recorder** 🎙️ | 8860 | Forensic recording of security events |
| + | **Help Agent** 🤖 | — | Interactive guide for all programs |

---

## 🚀 Quick Start

### Option 1: Selective Installer (Recommended)

```bash
cd installer
python netguardpro_installer.py
```

Choose which programs to install, set install path, and go.

### Option 2: Launch Everything via Cortex

```bash
cd launchers
# Double-click or run:
LANCER_SENTINEL.bat
```

Cortex starts all agents automatically and provides a unified dashboard on port 8900.

### Option 3: Launch Individual Programs

```bash
cd launchers
LANCER_NETGUARD.bat          # NetGuard Pro
LANCER_CLEANGUARD.bat        # CleanGuard Pro
LANCER_MAILSHIELD.bat        # MailShield Pro
LANCER_VPNGUARD.bat          # VPN Guard Pro
LANCER_SENTINEL_MAPPER.bat   # SentinelOS Mapper
LANCER_HELPAGENT.bat         # Help Agent
```

---

## 🔑 Permission System

NetGuardPro includes an optional role-based permission system. **Disabled by default** — all operations are allowed.

### How to Enable

1. Open any program's settings
2. Go to **Permissions → Enable**
3. Create a master admin account (username + password)
4. **Lock** to require authentication

### Permission Types

| Type | Description | Example |
|------|-------------|---------|
| `read` | View dashboard, see data | View network map |
| `write` | Create rules, add entries | Add firewall rule |
| `modify` | Change settings, edit configs | Edit scan schedule |
| `execute` | Run scans, block IPs | Start packet capture |

### User Management

```python
from permissions import PermissionManager
pm = PermissionManager()

# Enable with master account
pm.enable("admin", "my_password")

# Create restricted user
pm.create_user("my_password", "viewer", "viewer_pass", {
    "netguard": ["read"],
    "sentinel_mapper": ["read", "execute"]
})

# Lock (require auth for operations)
pm.lock("my_password")
```

---

## 🔔 Toast Notifications

Windows 10/11 native notifications for all security alerts.

- 🔴 **Critical threats** — long-duration notification
- 🛡️ **Device blocked/unblocked** — firewall actions
- 🔍 **Scan complete** — results summary
- 🍯 **Honeypot triggered** — intruder detected
- 📁 **File integrity change** — unauthorized modification
- 📢 **General events** — VPN connected, recording started

Requires `winotify` (auto-installed by launchers). Silent no-op if unavailable.

---

## 📋 Feature Details

### NetGuard Pro 🛡️

| Feature | Setting | Admin |
|---------|---------|-------|
| Packet Capture | — | ✅ |
| Intrusion Detection (IDS) | `suricata_enabled` | ❌ |
| Deep Packet Inspection | `dpi_enabled` | ❌ |
| Geo-Blocking | `geo_blocked_countries` | ✅ |
| IP Blocking (Windows FW) | — | ✅ |
| Threat History | — | ❌ |

### SentinelOS Mapper 🗺️

| Feature | Admin | Description |
|---------|-------|-------------|
| Multi-Interface Scan | ❌ | Scans Wi-Fi, Ethernet, VPN simultaneously |
| Device Firewall | ✅ | Block/unblock devices via Windows Firewall |
| Per-Port Blocking | ✅ | Block specific ports on specific devices |
| Device Naming | ❌ | Click to rename any device on the map |
| Deep Scan | ❌ | Detailed port and service analysis |
| Attempt Tracking | — | Counts blocked connection attempts |

### SentinelOS Cortex 🧠

| Feature | Description |
|---------|-------------|
| Agent Management | Auto-starts and monitors all 8 agents |
| Automated Playbooks | Chain actions across agents on triggers |
| Threat Intelligence | Aggregates threat data from all agents |
| Alert System | Telegram / Discord / Windows toast notifications |

### CleanGuard Pro 🧹

| Feature | Description |
|---------|-------------|
| System Clean | Temp files, browser cache, junk removal |
| Malware Scan | Quick / Full / Custom with YARA rules |
| Quarantine | Isolate and manage detected threats |
| Real-time Monitor | File system watchdog |

### MailShield Pro 📧

| Feature | Description |
|---------|-------------|
| Phishing Detection | URL analysis, sender reputation, header checks |
| SPF/DKIM Validation | Automatic email authentication |
| Attachment Scanning | Pre-download threat analysis |
| Encrypted Email | End-to-end encryption support |

### VPN Guard Pro 🔐

| Feature | Description |
|---------|-------------|
| WireGuard VPN | Connect/disconnect, peer management |
| Kill Switch | Block internet on VPN disconnect |
| DNS Leak Protection | Force DNS through VPN tunnel |
| Tunnel Monitoring | Real-time bandwidth and status |

---

## 🌐 Network Ports

| Port | Program | Protocol |
|------|---------|----------|
| 8765 | NetGuard Pro | WebSocket |
| 8801 | MailShield Pro | HTTP/WS |
| 8810 | CleanGuard Pro | HTTP/WS |
| 8820 | VPN Guard Pro | HTTP/WS |
| 8830 | Honeypot | HTTP/WS |
| 8840 | FIM | HTTP/WS |
| 8850 | StrikeBack | HTTP/WS |
| 8860 | Recorder | HTTP/WS |
| 8900 | SentinelOS Cortex | HTTP/WS |

---

## 💻 Requirements

- **OS**: Windows 10 / 11
- **Python**: 3.10+
- **RAM**: 4 GB minimum (8 GB recommended for full suite)
- **Disk**: ~50 MB for all programs

### Required Dependencies

```bash
pip install -r requirements.txt
```

Key packages: `pywebview`, `scapy`, `requests`, `psutil`, `winotify`, `pystray`, `Pillow`

### Optional System Software

| Software | Required For | Download |
|----------|-------------|----------|
| **Npcap** | Packet capture (NetGuard) | [npcap.com](https://npcap.com) |
| **WireGuard** | VPN (VPN Guard) | [wireguard.com](https://www.wireguard.com/install/) |

---

## ⚙️ Configuration

Each program stores its settings in a JSON file:

| Program | Settings File |
|---------|--------------|
| NetGuard Pro | `netguard_settings.json` |
| CleanGuard Pro | `cleanguard/cleanguard_settings.json` |
| MailShield Pro | `mailshield/mailshield_settings.json` |
| VPN Guard Pro | `vpnguard/vpnguard_settings.json` |
| SentinelOS | `sentinel/sentinel_settings.json` |
| Permissions | `permissions_state.json` |

---

## 📁 Project Structure

```
NetGuardPro/
├── netguard.py                 ← NetGuard Pro (main)
├── startup_utils.py            ← Shared: tray + startup
├── permissions.py              ← Shared: permission system
├── toast_notifications.py      ← Shared: Windows notifications
├── requirements.txt            ← All pip dependencies
│
├── cleanguard/                 ← CleanGuard Pro
├── mailshield/                 ← MailShield Pro
├── vpnguard/                   ← VPN Guard Pro
├── sentinel/                   ← SentinelOS (Mapper + Cortex)
├── fim/                        ← File Integrity Monitor
├── honeypot/                   ← Honeypot
├── strikeback/                 ← StrikeBack
├── recorder/                   ← Recorder
├── help_agent/                 ← Help Agent
├── installer/                  ← Selective Installer
├── launchers/                  ← Batch launchers
├── wireguard/                  ← WireGuard configs
├── captures/                   ← Packet captures
└── reports/                    ← Generated reports
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0** — see the [LICENSE](LICENSE) file for details.

---

## 🗺️ Roadmap

- [ ] Linux support
- [ ] macOS support
- [ ] Cloud dashboard
- [ ] Mobile companion app
- [ ] AI-powered threat analysis
- [ ] SIEM integration (Splunk, ELK)
- [ ] Automatic update system
- [ ] Multi-language support (DE, ES, PT)

---

<div align="center">

**NetGuardPro Suite** — Built with 🐍 Python + pywebview

*Cybersecurity for everyone / Cybersécurité pour tous*

</div>
