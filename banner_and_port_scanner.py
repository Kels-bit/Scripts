#!/usr/bin/env python3

import socket
from concurrent.futures import (ThreadPoolExecutor, as_completed)
import argparse


def scan_range(host, start, end, timeout=1.0, workers=100):
    open_ports = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(scan_port, host, p, timeout): p for p in range(start, end +1) }
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
    return sorted(open_ports)

def banner_grab(host, port, timeout=2.0):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode("utf-8", errors="replace").strip()
        s.close()
        return banner[:200]
    except Exception:
        return ""

def scan_port(host, port, timeout=1.0):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        results = s.connect_ex((host, port))
        s.close()
        return (port, result == 0)
    except Exception:
        return (port, False)

def main():
    print("[+] Banner and port scanning started...")
    
    parser = argparse.ArgumentParser(description="Port scanner  with banner grabbing")
    parser.add_argument("host")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=1024)
    parser.add_argument("--timeout", type=float, default=1.0)
    parser.add_argument("--banners", action="store_true")
    parser.add_argument("--out",)
    args = parser.parse_args()

    print(f"Scanning {args.host}",
          f"{args.start}-{args.end}...")
    ports = scan_range(args.host, args.start, args.end, timeout=args.timeout)


    lines = [f"Host: {args.host}",
          f"Open: {len(ports)}",
          "-" * 50]
    for port in ports:
        banner = ""
        if args.banners:
            banner = banner_grab(args.host, port, 2.0)
        b = f"  | {banner}" if banner else ""
        lines.append( f"  {port:<8} OPEN{b}")
    
    report = "\n".join(lines)
    print(report)
    if args.out:
        with open(args.out, "w") as f:
            f.write(report)
        print(f"\n[+] Saved: {args.out}")


if __name__ == "__main__":
    main()

