#!/usr/bin/env python3

import platform
import socket
from datetime import datetime, timezone
import shutil
import json
import argparse

def build_snapshot():
    return {
            "timestamp_utc": get_timestamp_utc(),
            "hostname": get_hostname(),
            "os_info": get_os_info(),
            "uptime_seconds": get_uptime_seconds(),
            "disk_root": get_disk_info(),
            "memory_info": get_memory_info(),
            "users": get_users(),
            "ip_addresses": get_ip_addresses(),
           }

def get_ip_addresses():
    ips = set()
   #Method 1
    try:
        hostname = socket.gethostname()
        host_ips = socket.gethostbyname_ex(hostname)[2]
        ips.update(host_ips)
    except Exception:
        pass
    #Method 2
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return sorted(list(ips))

def get_users():
    users = []
    try:
        with open("/etc/passwd", "r") as f:
         for line in f:
             parts = line.strip().split(":")
             if len(parts) >= 3:
                 username = parts[0]
                 uid = int(parts[2])
                 user_type = "human" if uid >= 1000 else "system"
                 users.append({"username": username, "uid": uid, "type": user_type})
    except Exception as e:
        print("Could not read passwd:", e)
    return users

def get_memory_info():
    mem = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                key, val = line.split(":", 1)
                mem[key.strip()] = val.strip()
    except Exception as e:
        print("Could not read meminfo:", e)
    return mem

def get_disk_info():
    usage = shutil.disk_usage("/")
    return {
            "total_gb": round(usage.total / (1024 ** 3), 2),
            "used_gb": round(usage.used / (1024 ** 3), 2),
            "free_gb": round(usage.free / (1024 ** 3), 2),
            "percent_used": round((usage.used / usage.total) * 100, 2),
            }

def get_uptime_seconds():
    try:
        with open("/proc/uptime", "r") as f:
            uptime_str = f.read().split()[0]
        return float(uptime_str)
    except Exception as e:
        print("Could not read uptime:", e)
        return None

def get_hostname():
    return socket.gethostname()

def get_timestamp_utc():
    return datetime.now().isoformat() + "Z"

def get_os_info():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
         }


def main():
    parser = argparse.ArgumentParser(description="System Snapshot Reporter")
    parser.add_argument("--out", help="Output JSON path. Default snapshot_<date>,json")
    args = parser.parse_args()

    snap = build_snapshot()
    
    if args.out:
        out_path = args.out
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = f"snapshot_{stamp}.json"
    with open(out_path, "w") as f:
        json.dump(snap, f, indent=2)

    print(f"[+] System snapshot written to: {out_path}")

if __name__ == "__main__":
    main()
