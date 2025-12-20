import getpass
import hashlib
from utils.storage import save_password_hash, load_password_hash
from mfa.totp import setup_totp

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def setup_user():
    password = getpass.getpass("Create password: ")
    confirm = getpass.getpass("Confirm password: ")

    if password != confirm:
        print("Passwords do not match")
        return

    save_password_hash(hash_password(password))
    setup_totp()
    print("[+] User and MFA configured")

def authenticate_user() -> bool:
    stored_hash = load_password_hash()
    if not stored_hash:
        print("No user configured")
        return False

    password = getpass.getpass("Password: ")
    return hash_password(password) == stored_hash
