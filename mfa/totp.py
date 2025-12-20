import pyotp
from utils.storage import save_totp_secret, load_totp_secret
from mfa.qr import generate_qr

def setup_totp():
    secret = pyotp.random_base32()
    save_totp_secret(secret)
    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name="myPew-user",
        issuer_name="myPew SecureCLI"
    )
    generate_qr(uri)
    print("[+] Scan the QR code with your authenticator app")

def verify_totp(code: str) -> bool:
    secret = load_totp_secret()
    if not secret:
        return False

    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)

