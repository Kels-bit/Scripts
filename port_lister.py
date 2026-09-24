#!/usr/bin/env python3

import subprocess


def get_listening_ports():
    # -l = listening, -n = numeric, -t = TCP, -u = UDP, -p = show process
    cmd = ["ss", "-lntup"]
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)

    lines = out.splitlines()
    results = []

    for line in lines:
        # Skip header or any empty lines
        if line.startswith("Netid") or not line.strip():
             continue
        parts = line.split()
        if len(parts) < 5:
            continue
        
        protocol = parts[0]
        local_addr = parts[4]

        # If the line contains 'users:' info, the process is usually at the end
        process = parts[-1] if "users:" in line else "unknown"
        
        results.append({
            "protocol": protocol,
            "local": local_addr,
            "process": process
            })
    return results

def main():
    print("Port lister starting...")

    ports = get_listening_ports()
    
    print(f"Listening ports found: {len(ports)}")
    print("-" * 90)
    for p in ports:
        print(f"{p['protocol']:>4} {p['local']:<45} {p['process']}")
          
if __name__ == "__main__":
    main()
