#!/usr/bin/env python3

import argparse
import csv


def parse_group():
    groups = []
    with open("/etc/group", "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) < 4:
                continue
            name = parts[0]
            gid = int(parts[2])
            members = parts[3].split(",") if parts[3] else []
            groups.append({
                "group" : name,
                "gid" : gid,
                "members" : members})
            return groups

def parse_passwd():
    users = []
    with open("/etc/passwd", "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) < 7:
                continue
            username = parts[0]
            uid = int(parts[2])
            gid = int(parts[3])
            home = parts[5]
            shell = parts[6]

            users.append({
                "username" : username,
                "uid" : uid,
                "gid" : gid,
                "home": home,
                "shell" : shell,
                "type" : "human" if uid >= 1000 else "system"
                })
        return users


def main():
    print("User & group enumerator starting...")
    parser = argparse.ArgumentParser(description="Enumerate users and group")
    parser.add_argument("--csv", help="Optinal CSV output file")
    args = parser.parse_args()
    
    system_users = parse_passwd()
    system_groups = parse_group()
    
    print(f"Users found: {len(system_users)}")
    print("-" * 60)
    for u in system_users:
        print(f"{u['username']:<18} UID={u['uid']:5} "
              f"Type={u['type']:<6} Shell={u['shell']}")

    print(f"\nGroups found: {len(system_groups)}")
    print("-" * 60)
    for g in system_groups[:20]:
        print(f"{g['group']:<18} GID={g['gid']:<5} Members={','.join(g['members'])}")

    if args.csv:
        with open(args.csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["kind", "name", "id", "extra"])
            for u in system_users:
                write.writerow(["user", u["username"], u["uid"], u["shell"]])
            for g in system_groups:
                writer.writerow(["group", g["group"], g["gid"], ",".join(g["members"])])
        print(f"\n[+] CSV written to: {args.csv}")
if __name__ == "__main__":
    main()
