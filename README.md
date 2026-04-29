<div align="center">

# 🛡️ NetGuardPro Suite

### 14-Program Cybersecurity Defense Platform for Windows

[![License](https://img.shields.io/badge/License-Commercial-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6.svg)]()
[![Programs](https://img.shields.io/badge/Programs-14-ff6600.svg)]()
[![GPG Signed](https://img.shields.io/badge/Commits-GPG%20Signed-brightgreen.svg)]()

*Protect. Detect. Respond.*

[Quick Start](#-quick-start) | [Programs](#-programs) | [Licensing](#-licensing) | [Architecture](#-architecture) | [Linux Version](#-linux-version)

</div>

---

## 🚀 Overview

NetGuardPro Suite is a comprehensive cybersecurity platform combining **14 integrated security tools** into a single defense ecosystem. Built entirely in Python with native WebSocket communication, every program runs independently or orchestrated through **SentinelOS Cortex** — the central command center that correlates events, triggers automated playbooks, and provides a unified threat dashboard.

Whether you need a network firewall, antivirus scanner, VPN manager, email security gateway, or a full SIEM/SOAR platform — NetGuardPro has you covered.

---

## 📦 Programs

| # | Program | Port | Description |
|---|---------|------|-------------|
| 1 | 🛡️ **NetGuard Pro** | 8765 | Network Firewall & Intrusion Detection System |
| 2 | 🧹 **CleanGuard Pro** | 8810 | Antivirus, Malware Scanner & System Cleaner |
| 3 | 📧 **MailShield Pro** | 8801 | Secure Email Client with Phishing Detection |
| 4 | 🔐 **VPN Guard Pro** | 8820 | WireGuard VPN with Kill Switch & DNS Leak Protection |
| 5 | 🗺️ **SentinelOS Mapper** | — | Interactive Network Map & Device Firewall |
| 6 | 🧠 **SentinelOS Cortex** | 8900 | Central Orchestrator, Playbooks & Threat Intelligence |
| 7 | 📁 **File Integrity Monitor** | 8840 | SHA-256 File Integrity Monitoring |
| 8 | 🍯 **Honeypot** | 8830 | Deception Traps (SSH, FTP, HTTP) |
| 9 | ⚔️ **StrikeBack** | 8850 | Active Defense & Automated Counter-Measures |
| 10 | 🎙️ **Recorder** | 8860 | Forensic Security Event Recording |
| 11 | 🔴 **RedTeam** | — | Offensive Security & Penetration Testing Tools |
| 12 | 🧪 **Sandbox** | — | Isolated Malware Analysis Environment |
| 13 | 📱 **Mobile Gateway** | — | Mobile Device Security Bridge |
| 14 | 📊 **SIEM** | — | Security Information & Event Management |
| + | 🤖 **Help Agent** | — | Interactive Guide for All Programs |

---

## 🖥️ Screenshots

> Screenshots coming soon. Launch any program and visit `http://localhost:<port>` to see the dashboard in action.

---

## ⚡ Quick Start

### Option 1 — Clone & Run

```bat
git clone https://github.com/sxc3030-eng/NetGuardPro.git
cd NetGuardPro
pip install -r requirements.txt
python netguard.py
```

### Option 2 — Selective Installer (Recommended)

```bat
cd installer
python netguardpro_installer.py
```

Choose which programs to install, set your install path, and go.

### Option 3 — Launch Everything via Cortex

```bat
cd launchers
LANCER_SENTINEL.bat
```

Cortex starts all agents automatically and provides a unified dashboard on port **8900**.

### Option 4 — Launch Individual Programs

```bat
cd launchers
LANCER_NETGUARD.bat          :: NetGuard Pro
LANCER_CLEANGUARD.bat        :: CleanGuard Pro
LANCER_MAILSHIELD.bat        :: MailShield Pro
LANCER_VPNGUARD.bat          :: VPN Guard Pro
LANCER_SENTINEL_MAPPER.bat   :: SentinelOS Mapper
LANCER_SIEM.bat              :: SIEM Dashboard
LANCER_REDTEAM.bat           :: RedTeam Tools
LANCER_SANDBOX.bat           :: Sandbox Environment
LANCER_HELPAGENT.bat         :: Help Agent
```

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    SentinelOS Cortex (:8900)                     │
│               Central Orchestrator / Agent Bus                   │
│                    SIEM / SOAR Engine                             │
├────────┬────────┬────────┬────────┬────────┬────────┬────────────┤
│        │        │        │        │        │        │            │
▼        ▼        ▼        ▼        ▼        ▼        ▼            ▼
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌────────┐
│ Net  ││Clean ││Mail  ││ VPN  ││Honey ││ FIM  ││Strk  ││Recorder│
│Guard ││Guard ││Shld  ││Guard ││ pot  ││      ││Back  ││        │
│:8765 ││:8810 ││:8801 ││:8820 ││:8830 ││:8840 ││:8850 ││:8860   │
└──────┘└──────┘└──────┘└──────┘└──────┘└──────┘└──────┘└────────┘

     ┌────────┐ ┌────────┐ ┌─────────┐ ┌──────────────┐
     │RedTeam │ │Sandbox │ │ Mobile  │ │ SIEM / SOAR  │
     │        │ │        │ │ Gateway │ │              │
     └────────┘ └────────┘ └─────────┘ └──────────────┘

  Shared Modules:
  ├── permissions.py         (role-based access control)
  ├── toast_notifications.py (Windows toast alerts)
  ├── startup_utils.py       (system tray + auto-start)
  └── netguard_tray.py       (tray icon management)
```

- All programs communicate via **WebSocket** on localhost
- Shared **permission system** with role-based access control
- **SentinelOS Cortex** = central command center that orchestrates all agents
- **SIEM/SOAR** correlates events across all agents and triggers automated playbooks
- Native **Windows toast notifications** for real-time security alerts

---

## 💰 Licensing

### 🆓 Community (Free)
5 core programs for personal, non-commercial use.

### ⭐ Pro — $29/year
All 14 programs + commercial use license.

### 🎯 Early Bird — $14.99 (Lifetime!)
**Limited to 500 spots** — All 14 programs, all future updates, forever.

### 🏢 Enterprise — $99/year
Unlimited devices + priority support + custom playbooks.

---

## 💻 Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **OS** | Windows 10 | Windows 11 |
| **Python** | 3.8+ | 3.10+ |
| **RAM** | 4 GB | 8 GB (full suite) |
| **Disk** | 50 MB | 100 MB (with captures) |

### Dependencies

```bat
pip install -r requirements.txt
```

Key packages: `pywebview`, `scapy`, `requests`, `psutil`, `winotify`, `pystray`, `Pillow`

### Optional System Software

| Software | Required For | Download |
|----------|-------------|----------|
| **Npcap** | Packet capture (NetGuard) | [npcap.com](https://npcap.com) |
| **WireGuard** | VPN (VPN Guard) | [wireguard.com](https://www.wireguard.com/install/) |

---

## 📁 Project Structure

```
NetGuardPro/
├── netguard.py                 # NetGuard Pro (main firewall/IDS)
├── permissions.py              # Shared: role-based access control
├── toast_notifications.py      # Shared: Windows toast alerts
├── startup_utils.py            # Shared: system tray + auto-start
├── requirements.txt            # All pip dependencies
│
├── cleanguard/                 # CleanGuard Pro
├── mailshield/                 # MailShield Pro
├── vpnguard/                   # VPN Guard Pro
├── sentinel/                   # SentinelOS (Mapper + Cortex)
├── siem/                       # SIEM / SOAR Engine
├── fim/                        # File Integrity Monitor
├── honeypot/                   # Honeypot Deception Traps
├── strikeback/                 # StrikeBack Active Defense
├── recorder/                   # Forensic Recorder
├── redteam/                    # RedTeam Offensive Tools
├── sandbox/                    # Malware Sandbox
├── mobile_gateway/             # Mobile Device Gateway
├── help_agent/                 # Interactive Help Agent
├── installer/                  # Selective Installer
├── launchers/                  # Batch launchers (.bat)
├── wireguard/                  # WireGuard VPN configs
├── captures/                   # Packet capture files
└── reports/                    # Generated security reports
```

---

## 🔑 GPG Verification

All commits in this repository are signed with GPG key **`5C99E502B17F16D5`**.

To verify commit signatures:
```bat
git log --show-signature -1
```

---

## 🔔 Toast Notifications

Windows 10/11 native notifications for all security alerts:

- 🔴 **Critical threats** — high-priority, persistent notification
- 🛡️ **Device blocked/unblocked** — firewall actions in real time
- 🔍 **Scan complete** — results summary with threat count
- 🍯 **Honeypot triggered** — intruder detected on deception trap
- 📁 **File integrity change** — unauthorized file modification
- 📢 **General events** — VPN connected, recording started, and more

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -S -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

All contributions must include GPG-signed commits.

---

## 📜 License

Commercial software. See [LICENSE](LICENSE) for full terms.

---

## 🐧 Linux Version

Looking for Linux? Check out **[Optimus](https://github.com/sxc3030-eng/Optimus)** — our Linux cybersecurity distribution with a custom desktop environment and bootable ISO builder!

---

<div align="center">

**NetGuardPro Suite** — Built with Python + pywebview

*Protect. Detect. Respond.*

Made by [@sxc3030-eng](https://github.com/sxc3030-eng)

</div>

---

### Method

Architecture-first, AI-paired. Designed and shipped over a focused **2-week sprint in March 2026** with **Claude (Opus 4.6)** as paired implementation and audit partner. Each of the 14 programs (firewall/IDS, antivirus scanner, VPN, SIEM/SOAR, honeypot, file-integrity monitor, and more) was cross-audited on every commit: code review, dependency check, threat-model review on the WebSocket bus and shared permissions layer.

---
