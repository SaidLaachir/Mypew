import qrcode

def generate_qr(uri: str):
    img = qrcode.make(uri)
    img.save("mfa_qr.png")
    print("[+] QR code saved as mfa_qr.png")
