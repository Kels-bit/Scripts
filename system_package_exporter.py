#!/usr/bin/env python3

import argparse
import shutil
import subprocess


def export_packages(manager):
    if manager == "dpkg":
        return run_cmd(["dpkg", "-l"])
    if manager == "dnf":
        return run_cmd(["dnf", "list", "installed"])
    if manager == "rpm":
        return run_cmd(["rp,", "-qa"])
    if manager == "pacman":
        return run_cmd(["pacman", "-Qe"])
    return "Unsupported System."

def detect_manager():
    if shutil.which("dpkg"):
        return "dpkg"
    if shutil.which("dnf"):
        return "dnf"
    if shutil.which("rpm"):
        return "rpm"
    if shutil.which("pacman"):
        return "pacman"
    return None

def run_cmd(cmd):
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT) 

def main():
    print("Package exporter starting...")
    
    parser = argparse.ArgumentParser(description="Export installed packages")
    parser.add_argument("--out", default="installed_packages.txt", help="Output file (default installed_packages.txt)")
    args = parser.parse_args()
    mgr = detect_manager()
    if not mgr:
        print(f"No supported manager found.")
        return
    print(f"[+] Detected package manager: {mgr}")
    data = export_packages(mgr)
    with open(args.out,"w") as f:
        f.write(data)
        print(f"[+] Installed pacjages written to: {args.out}")

if __name__ == "__main__":
     main()
