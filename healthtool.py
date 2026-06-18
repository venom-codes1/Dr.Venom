cat > healthtool.py << 'EOF'
#!/usr/bin/env python3
"""
🩺 Full Body Checkup PRO - Dr. Venom Edition
Advanced System Diagnostics & Smart Auto-Fix Tool
"""

import os
import sys
import subprocess
import psutil
import re
import shutil
import json
from datetime import datetime
import argparse
from pathlib import Path

class C:
    HEADER = '\033[95m'
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    GREEN = '\033[32m'
    END = '\033[0m'

ESSENTIAL_SERVICES = ['cron', 'systemd-logind']
OPTIONAL_SERVICES = ['ssh', 'systemd-resolved']

def print_banner():
    banner = r"""
 ╔══════════════════════════════════════════════════════════════════════╗
 ║                                                                      ║
 ║  ██████╗ ██████╗    ██╗   ██╗███████╗███╗   ██╗ ██████╗ ███╗   ███╗  ║
 ║  ██╔══██╗██╔══██╗   ██║   ██║██╔════╝████╗  ██║██╔═══██╗████╗ ████║  ║
 ║  ██║  ██║██████╔╝   ██║   ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║  ║
 ║  ██║  ██║██╔══██╗   ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║  ║
 ║  ██████╔╝██║  ██║    ╚████╔╝ ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║  ║
 ║  ╚═════╝ ╚═╝  ╚═╝ ██  ╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝  ║
 ║                                                                      ║
 ║               🩺 Dr. Venom's Linux Full Body Checkup 🩺              ║
 ║                                                                      ║
 ╚══════════════════════════════════════════════════════════════════════╝
    """
    print(f"{C.HEADER}{C.BOLD}{banner}{C.END}")
    print(f"                Kali Linux Edition - Powered by Dr.Venom\n")

def run(cmd, sudo=False, timeout=90):
    """Execute shell command safely"""
    if sudo and os.geteuid() != 0:
        cmd = f"sudo {cmd}"
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timeout"
    except Exception as e:
        return -1, "", str(e)

def get_deep_health():
    """Get system health metrics"""
    try:
        health = {
            "cpu": psutil.cpu_percent(interval=1.5),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "load": psutil.getloadavg()[0],
            "uptime": str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0],
            "temp": "N/A",
            "swap": psutil.swap_memory().percent
        }
        try:
            for name, entries in psutil.sensors_temperatures().items():
                for entry in entries:
                    if entry.current:
                        health["temp"] = f"{entry.current:.1f}°C"
                        break
        except:
            pass
        return health
    except Exception as e:
        return {}

def check_updates():
    """Check available package updates"""
    print(f"\n{C.BOLD}📦 Package Updates{C.END}")
    run("apt update", sudo=True, timeout=120)
    _, out, _ = run("apt list --upgradable 2>/dev/null")
    updates = len([l for l in out.splitlines() if "upgradable" in l])
    print(f"   Available Updates : {updates}")
    return updates

def deep_battery_health():
    """Check battery health"""
    print(f"\n{C.BOLD}🔋 Deep Battery Health{C.END}")
    try:
        bat = psutil.sensors_battery()
        if bat:
            print(f"   Level     : {bat.percent:.1f}%")
            print(f"   Status    : {'Charging' if bat.power_plugged else 'Discharging'}")
        else:
            print(f"   {C.WARN}No battery detected (Desktop/Server mode){C.END}")
            return
        
        _, out, _ = run("upower -e 2>/dev/null | grep battery")
        if out:
            _, details, _ = run(f"upower -i {out.strip()}")
            for line in details.splitlines():
                if "energy-full:" in line and "design" not in line:
                    print(f"   Health    : {line.strip()}")
    except Exception as e:
        print(f"   {C.WARN}Battery info not available{C.END}")

def disk_cleaner():
    """Analyze disk usage"""
    print(f"\n{C.BOLD}🧹 Disk Cleaner Analysis{C.END}")
    try:
        _, cache, _ = run("du -sh /var/cache/apt 2>/dev/null || echo 'N/A'")
        _, journal, _ = run("journalctl --disk-usage 2>/dev/null || echo 'N/A'")
        print(f"   APT Cache    : {cache}")
        print(f"   Journal Logs : {journal}")
    except Exception as e:
        print(f"   {C.WARN}Could not get disk info{C.END}")

def security_audit():
    print(f"\n{C.BOLD}🛡️ Security & Integrity Audit{C.END}")
    # Check failed logins
    _, out, _ = run("grep 'failed' /var/log/auth.log 2>/dev/null | wc -l")
    print(f"   Failed Login Attempts: {out if out else '0'}")
    # Check if root login is allowed via SSH
    if os.path.exists("/etc/ssh/sshd_config"):
        _, out, _ = run("grep '^PermitRootLogin' /etc/ssh/sshd_config")
        print(f"   SSH Root Login Configuration: {out if out else 'Default (Managed)'}")
    else:
        print("   SSH Service config not found.")

def network_health(auto_fix=False):
    print(f"\n{C.BOLD}🌐 Network Hygiene Status{C.END}")
    # Check internet connectivity
    ret, _, _ = run("ping -c 1 8.8.8.8", timeout=5)
    if ret == 0:
        print(f"   Internet Connectivity: {C.OK}ONLINE{C.END}")
    else:
        print(f"   Internet Connectivity: {C.FAIL}OFFLINE{C.END}")
        if auto_fix:
            print("   [🛠️ Auto-Fix] Attempting to restart networking service...")
            run("systemctl restart networking", sudo=True)

def performance_analysis():
    print(f"\n{C.BOLD}⚡ Performance & Resource Bottlenecks{C.END}")
    zombies = [p for p in psutil.process_iter(['status']) if p.info['status'] == psutil.STATUS_ZOMBIE]
    print(f"   Zombie Processes Detected: {len(zombies)}")
    if len(zombies) > 0:
        print(f"   {C.WARN}Warning: {len(zombies)} idle/zombie processes lingering.{C.END}")

def service_status(auto_fix=False):
    print(f"\n{C.BOLD}⚙️ Essential System Services Core{C.END}")
    for svc in ESSENTIAL_SERVICES:
        ret, _, _ = run(f"systemctl is-active {svc}")
        if ret == 0:
            print(f"   {svc:<18}: {C.OK}ACTIVE{C.END}")
        else:
            print(f"   {svc:<18}: {C.FAIL}INACTIVE{C.END}")
            if auto_fix:
                print(f"   [🛠️ Auto-Fix] Booting up required service: {svc}")
                run(f"systemctl start {svc}", sudo=True)

def filesystem_integrity():
    print(f"\n{C.BOLD}📂 Filesystem Integrity Verification{C.END}")
    _, out, _ = run("mount | grep 'ro,'")
    if out:
        print(f"   {C.FAIL}Alert! Read-only partitions detected:{C.END}\n{out}")
    else:
        print(f"   All active partitions are mounted clean with {C.OK}Read/Write privileges{C.END}")

def dependency_check(auto_fix=False):
    print(f"\n{C.BOLD}🧩 Package Dependency Verifications{C.END}")
    ret, out, _ = run("dpkg --configure -a", sudo=True)
    if ret == 0:
        print(f"   Broken configurations: {C.OK}None found{C.END}")
    else:
        print(f"   {C.WARN}Unconfigured dependencies detected.{C.END}")

def performance_recommendations():
    print(f"\n{C.BOLD}💡 Engine Performance Tuning Overview{C.END}")
    swappiness = "/proc/sys/vm/swappiness"
    if os.path.exists(swappiness):
        with open(swappiness, 'r') as f:
            val = f.read().strip()
        print(f"   Current System Linux Swappiness Value: {val}")

def system_optimization_tips(health):
    print(f"\n{C.BOLD}💡 Dr. Venom's Pro Custom Optimization Tips{C.END}")
    if health.get('ram', 0) > 80:
        print("   - [RAM] Memory limits exceeding 80%. Clean runtime leaks using: 'sync; echo 3 > /proc/sys/vm/drop_caches'")
    if health.get('disk', 0) > 85:
        print("   - [DISK] Storage highly constraints. Purge unused tool cache or purge packages using '--fix'")
    else:
        print("   - System vitals stable. Keep your repositories updated regularly.")

def check_files_for_update():
    # Looks for stale configurations
    _, out, _ = run("find /etc -name '*.dpkg-old' -o -name '*.dpkg-dist' 2>/dev/null")
    found = bool(out.strip())
    return found, out

def check_files_for_delete():
    # Looks for older cache structures
    _, out, _ = run("find /var/cache -type f -mtime +30 2>/dev/null")
    found = bool(out.strip())
    return found, out

def auto_clean(updates, files_update_found, files_delete_found):
    """Auto cleanup and optimization"""
    print(f"\n{C.BOLD}🧹 Dr. Venom Auto Cleanup Engine{C.END}")
    
    if files_update_found:
        update_choice = input("   Apply file updates (.dpkg-old)? (y/n): ").strip().lower()
        if update_choice == 'y':
            run("find /etc -name '*.dpkg-old' -o -name '*.dpkg-dist' 2>/dev/null | xargs rm -f", sudo=True)
            print(f"   {C.OK}File updates processed!{C.END}")
    
    if files_delete_found:
        delete_choice = input("   Delete old cache/log files? (y/n): ").strip().lower()
        if delete_choice == 'y':
            run("find /var/cache -type f -mtime +30 -delete 2>/dev/null", sudo=True)
            run("find /var/log -type f -mtime +60 -name '*.log' -delete 2>/dev/null", sudo=True)
            print(f"   {C.OK}Old files cleaned!{C.END}")
    
    choice = input("   Perform full cleanup (Cache + Logs)? (y/n): ").strip().lower()
    if choice == 'y':
        print(f"{C.WARN}   Starting cleanup...{C.END}")
        run("apt autoremove -y", sudo=True)
        run("apt clean", sudo=True)
        run("journalctl --vacuum-time=10d", sudo=True)
        print(f"{C.OK}   ✅ Disk Cleanup Completed!{C.END}")
    
    if updates > 0:
        up_choice = input(f"   {updates} updates available. Upgrade now? (y/n): ").strip().lower()
        if up_choice == 'y':
            print("   Running full upgrade...")
            run("apt full-upgrade -y", sudo=True)
            print(f"{C.OK}   ✅ System Upgraded!{C.END}")

def main():
    parser = argparse.ArgumentParser(description="Dr. Venom's Full Body Checkup")
    parser.add_argument("--all", action="store_true", help="Deep Full Checkup")
    parser.add_argument("--fix", action="store_true", help="Run Auto Fix + Clean")
    parser.add_argument("--security", action="store_true", help="Security Audit Only")
    parser.add_argument("--network", action="store_true", help="Network Only")
    parser.add_argument("--performance", action="store_true", help="Performance Only")
    parser.add_argument("--tips", action="store_true", help="Tips Only")
    args = parser.parse_args()

    print_banner()

    h = get_deep_health()
    
    print(f"{C.BOLD}1. Core System Vitals{C.END}")
    print(f"   CPU     : {h.get('cpu', 0)}%")
    print(f"   RAM     : {h.get('ram', 0)}%")
    print(f"   Disk    : {h.get('disk', 0)}%")
    print(f"   Temp    : {h.get('temp', 'N/A')}")
    print(f"   Load    : {h.get('load', 0):.2f}")
    print(f"   Uptime  : {h.get('uptime', 'N/A')}")

    updates = check_updates()
    deep_battery_health()
    disk_cleaner()

    auto_fix_enabled = args.all or args.fix

    if args.security or args.all:
        security_audit()
    if args.network or args.all:
        network_health(auto_fix=auto_fix_enabled)
    if args.performance or args.all:
        performance_analysis()
    if args.all:
        service_status(auto_fix=auto_fix_enabled)
        filesystem_integrity()
        dependency_check(auto_fix=auto_fix_enabled)
        performance_recommendations()
    if args.tips or args.all:
        system_optimization_tips(h)

    files_update_found, _ = check_files_for_update()
    files_delete_found, _ = check_files_for_delete()

    if args.fix or args.all:
        auto_clean(updates, files_update_found, files_delete_found)
    
    print(f"\n{C.OK}{C.BOLD}✅ Dr. Venom's Full Body Checkup Completed!{C.END}\n")

if __name__ == "__main__":
    if os.geteuid() != 0 and any([sys.argv[i] in ['--all', '--fix'] for i in range(1, len(sys.argv))]):
        print(f"{C.WARN}Run with sudo for full power: sudo ./healthtool.py --all --fix{C.END}\n")
    main()
EOF
