# security/policy.py

CRITICAL_COMMANDS = {
    "passwd",
    "useradd",
    "usermod",
    "userdel",
    "iptables",
    "systemctl",
    "mount",
    "umount",
    "shutdown",
    "reboot"
}

def is_critical(command: str) -> bool:
    base = command.strip().split()[0]
    return base in CRITICAL_COMMANDS

