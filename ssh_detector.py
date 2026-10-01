#!/usr/bin/env python3

import re
from collections import Counter
import argparse


LOG_FILE = "/var/log/auth.log"


def block_ips(flagged_ips, deny_file="/etc/host.deny"):
    try:
        with open(deny_file, "r") as f:
            existing = f.read()
    except FileNotFoundError:
        existing = ""

    newly_blocked = []
    with open(deny_file, "a") as f:
        for ip in flagged_ips:
            entry = f"sshd: {ip}"
            if entry not in existing:
                f.write(f"{entry}\n")
                newly_blocked.append(ip)
    return newly_blocked


def get_flagged_ips(counts, threshold=5):
    return {ip: count for ip, count in counts.items()
            if count >= threshold}

def count_failures(attempts):
    ips = []
    for line in attempts:
        ip = extract_IP(line)
        if ip:
            ips.append(ips)
    return Counter(ips)

def extract_ip(line):
    match = re.search(r"from\s+([\d\.]+)", line)
    if match:
        return match.group(1)
    return None

def read_failed_attempts(log_path):
    failed = []
    try:
        with open(log_path, "r", errors="replace") as f:
            for line in f:
                if "Failed password" in line:
                    failed.append(line.strip())
    except FileNotFoundError:
            print(f"Log file not found: (log_path)")
    except PermissionError:
            print("Permission denied. Try running with sudo.")
    return failed

def main():
    print("[+] SSH brute brute-force detector starting...")
    
    parser = argparse.ArgumentParser(description="Detect SSH brute-force attempts")
    parser.add_argument("--log", default="/var/log/auth.log")
    parser.add_argument("--threshold", type=int, default=5)
    parser.add_argument("--block", action="store_true", help="Write flagged IPs to /etc/hosts.deny")
    args = parser.parse_args()

    attempts = read_failed_attempts(LOG_FILE)
    counts = count_failures(attempts)
    flagged = get_flagged_ips(counts, args.threshold)

    print(f"Log: {args.log}")
    print(f"Threshold: {args.threshold}")
    print(f"Total:   {len(attempts)}")
    print("-" * 50)

    for ip, count in sorted(flagged.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ip:<20} {count} [FLAGGED]") 
    if args.block:
        blocked= block_ips(flagged)
        print(f"\n[+] Blocked: {len(blocked)} IP(s)")
        for ip in blocked:
            priint(f"   {ip}")


if __name__ == "__main__":
    main()

