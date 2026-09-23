#!/usr/bin/env python3

import os
import stat
import argparse



def audit_path(base_path):
    findings = []
    # Check Directories
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            path = os.path.join(root, d)
            try:
                mode = os.stat(path).st_mode
                if is_world_writable(mode):
                    findings.append(("DIR", path))
            except Exception:
                # If we can't stat in (e.g. permission denied) just skip
                continue
        # Check Files
        for f in files:
            path = os.path.join(root, f)
            try:
                mode = os.stat(path).st_mode
                if is_world_writable(mode):
                    findings.append(("FILE", path))
            except Exception:
                continue
    return findings

def is_world_writable(mode):
    return bool(mode & stat.S_IWOTH)

def main():
    print("Home permission audit starting...")
    
    parser = argparse.ArgumentParser(description="audit for world-writable files/dirs")
    parser.add_argument("--path", default="/home", help="Path to audit (default: /home)")
    parser.add_argument("--out", help="Optional output report file")
    args = parser.parse_args()
    findings = audit_path(args.path)

    lines = []
    lines.append(f"Scanning : {args.path}")
    lines.append(f"World-writable items found: {len(findings)}")
    lines.append("-" * 60)

    for kind, path in findings:
        lines.append(f"{kind}: {path}")

    report = "\n".join(lines)
    print(report)

    if args.out:
        with open(args.out, "w") as f:
            f.write(reports)
        print(f"\n[+] Report save to args: {args.out}")

if __name__ == "__main__":
    main()
