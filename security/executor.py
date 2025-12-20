import subprocess
from security.policy import is_critical
from security.session import session_valid
from utils.logger import log_event
from utils.storage import backup_session_files

def execute_command(command: str):
    log_event(f"Command requested: {command}")

    if is_critical(command) and not session_valid():
        print("[-] MFA session invalid or expired")
        log_event("Blocked critical command (no MFA session)")
        return

    # Force sudo + disable pager for systemctl
    if command.startswith("systemctl"):
        command = f"sudo SYSTEMD_PAGER=cat {command}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        log_event(f"Command executed: {command}")
        backup_session_files()

    except Exception as e:
        print(str(e))
        log_event(f"Execution error: {e}")
