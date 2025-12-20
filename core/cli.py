import argparse
from core.auth import setup_user, authenticate_user
from mfa.totp import verify_totp
from security.executor import execute_command
from security.policy import is_critical
from utils.storage import save_mfa_session

def run_cli():
    parser = argparse.ArgumentParser(
        description="myPew - Secure CLI with MFA/TOTP"
    )

    parser.add_argument("--setup", action="store_true")
    parser.add_argument("--login", action="store_true")
    parser.add_argument("--exec", type=str)

    args = parser.parse_args()

    if args.setup:
        setup_user()
        return

    if args.login:
        if not authenticate_user():
            print("[-] Authentication failed")
            return

        code = input("Enter TOTP code: ")
        if not verify_totp(code):
            print("[-] Invalid TOTP code")
            return

        save_mfa_session()
        print("[+] MFA session opened")
        return

    if args.exec:
        command = args.exec

        if is_critical(command):
            if not authenticate_user():
                print("[-] Authentication failed")
                return

            code = input("Enter TOTP code: ")
            if not verify_totp(code):
                print("[-] Invalid TOTP code")
                return

            save_mfa_session()

        execute_command(command)
        return

    parser.print_help()
