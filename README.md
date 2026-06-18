# Dr.Venom
Dr.Venom is an advanced CLI system diagnostics &amp; automated cleanup framework optimized for Linux. It runs deep health checkups on vitals, network, &amp; services with an interactive auto-fix engine.

## 🚀 Key Features

* **📊 Core System Vitals:** Real-time diagnostics of CPU, RAM, Disk utilization, system load averages, uptime, and hardware core temperature sensors using `psutil`.
* **📦 Smart Package Audit:** Scans for pending repository updates, missing patches, or upgradeable applications natively via `apt`.
* **🔋 Deep Battery Profiling:** Discovers battery charge level, real-time power status, and structural design capacity metrics via `upower`.
* **🧹 Smart Auto-Cleanup Engine:** Safely scrubs local APT caches, purges obsolete system configurations (`.dpkg-old`), vacuums historical journal logs, and removes orphaned dependencies.
* **🛠️ Modular Execution:** Fully structured argument parsing to run independent test suites (`--security`, `--network`, `--performance`, `--tips`) or an absolute continuous maintenance scan (`--all --fix`).

**Before installation: install some dependencies:
sudo apt update
sudo apt install python3-psutil -y**

**After this:
## Installation & Setup

Follow these simple steps to download, install dependencies, and configure **Dr.Venom** on your Linux machine:

#Clone the Repository
Open your terminal and clone the repository directly from GitHub:
```bash: git clone [https://github.com/venom-codes1/Dr.Venom.git](https://github.com/venom-codes1/Dr.Venom.git)**

# Grant Execution Permissions
Make the core script execution-ready:

bash: chmod +x healthtool.py

💻 Usage & Command Flags
Dr.Venom comes with flexible CLI arguments so you can run exactly what you need.

Run a Complete Diagnostics & Auto-Cleanup (Recommended)
To run all modules sequentially and trigger the interactive optimization engine:

Bash:
sudo ./healthtool.py --all --fix

**Project Directory Structure**
Dr.Venom/
├── .gitignore          # Safely filters out temporary Python bytecodes (__pycache__/)
├── LICENSE             # MIT Open-Source Permissive License
├── README.md           # Project Documentation and Setup Roadmap
└── healthtool.py       # Main Executable Python Diagnostics Engine
