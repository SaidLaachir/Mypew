import os
import shutil
import datetime

BASE_DIR = os.path.expanduser("~/.mypew")
PASS_FILE = os.path.join(BASE_DIR, "password.hash")
TOTP_FILE = os.path.join(BASE_DIR, "totp.secret")
SESSION_FILE = os.path.join(BASE_DIR, "mfa.session")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")


def ensure_storage():
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)


# ---------- PASSWORD ----------

def save_password_hash(hash_value: str):
    ensure_storage()
    with open(PASS_FILE, "w") as f:
        f.write(hash_value)


def load_password_hash():
    if not os.path.exists(PASS_FILE):
        return None
    with open(PASS_FILE, "r") as f:
        return f.read().strip()


# ---------- TOTP ----------

def save_totp_secret(secret: str):
    ensure_storage()
    with open(TOTP_FILE, "w") as f:
        f.write(secret)


def load_totp_secret():
    if not os.path.exists(TOTP_FILE):
        return None
    with open(TOTP_FILE, "r") as f:
        return f.read().strip()


# ---------- MFA SESSION ----------

def save_mfa_session():
    ensure_storage()
    with open(SESSION_FILE, "w") as f:
        f.write(datetime.datetime.now().isoformat())


def load_mfa_session(timeout_minutes=5) -> bool:
    if not os.path.exists(SESSION_FILE):
        return False

    with open(SESSION_FILE, "r") as f:
        timestamp = f.read().strip()

    try:
        session_time = datetime.datetime.fromisoformat(timestamp)
    except ValueError:
        return False

    delta = datetime.datetime.now() - session_time
    return delta.total_seconds() <= timeout_minutes * 60


def clear_mfa_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)


# ---------- AUDIT ----------

def backup_session_files():
    ensure_storage()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    target_dir = os.path.join(BACKUP_DIR, timestamp)
    os.makedirs(target_dir, exist_ok=True)

    logs = [
        "/var/log/auth.log",
        "/var/log/syslog"
    ]

    for log in logs:
        if os.path.exists(log):
            try:
                shutil.copy(log, target_dir)
            except PermissionError:
                pass
