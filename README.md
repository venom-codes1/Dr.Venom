# 🩺 Dr.Venom

[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Kali-blueviolet?style=flat-square&logo=linux)](https://www.kali.org/)
[![Language](https://img.shields.io/badge/Language-Python%203-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://opensource.org/licenses/MIT)

**Dr.Venom** is an advanced command-line system diagnostics, security audit, and automated optimization framework tailored for Linux environments (optimized for Kali Linux). Built in Python, it performs deep health checks—tracking core vitals, tracking battery health, evaluating disk leaks, checking network hygiene, and auditing services—backed by an interactive auto-fix and smart cleanup engine to maintain peak system performance.

---

## 🚀 Key Features

* **📊 Core System Vitals:** Real-time diagnostics of CPU, RAM, Disk utilization, system load averages, uptime, and hardware core temperature sensors using `psutil`.
* **📦 Smart Package Audit:** Scans for pending repository updates, missing patches, or upgradeable applications natively via `apt`.
* **🔋 Deep Battery Profiling:** Discovers battery charge level, real-time power status, and structural design capacity metrics via `upower`.
* **🧹 Smart Auto-Cleanup Engine:** Safely scrubs local APT caches, purges obsolete system configurations (`.dpkg-old`), vacuums historical journal logs, and removes orphaned dependencies.
* **🛠️ Modular Execution:** Fully structured argument parsing to run independent test suites (`--security`, `--network`, `--performance`, `--tips`) or an absolute continuous maintenance scan (`--all --fix`).

---
## **Before installation: install some dependencies:
#bash: sudo apt update    
#bash: sudo apt install python3-psutil -y**

**After this:

## Installation & Setup

Follow these simple steps to download, install dependencies, and configure **Dr.Venom** on your Linux machine:

# Clone the Repository
Open your terminal and clone the repository directly from GitHub:
bash:  git clone [https://github.com/venom-codes1/Dr.Venom.git](https://github.com/venom-codes1/Dr.Venom.git)

## Grant Execution Permissions
Make the core script execution-ready:

bash: chmod +x healthtool.py

## All Rounder command (Recommended)
Bash: 
sudo ./healthtool.py --all --fix

#Run a Complete Diagnostics & Auto-Cleanup 
To run all modules sequentially and trigger the interactive optimization engine.


## 💻 Usage & Command Flags
Dr.Venom comes with flexible CLI arguments so you can run exactly what you need.
If you want to isolate specific checkups, run the tool with any of these flags:
           #Command Flag                                #Description
1. python3 healthtool.py --security         Triggers a selective standalone Security and Audit verification.
2. python3 healthtool.py --network          Inspects gateway loops, active interface sockets, and connection hygiene.
3. python3 healthtool.py --performance     Evaluates resource overhead bottlenecks and active service performance.
4. python3 healthtool.py --tips             Displays proactive system optimization configurations and suggestions.









Project Directory Structure
Dr.Venom/
├── .gitignore          # Safely filters out temporary Python bytecodes (__pycache__/)
├── LICENSE             # MIT Open-Source Permissive License
├── README.md           # Project Documentation and Setup Roadmap
└── healthtool.py       # Main Executable Python Diagnostics Engine
