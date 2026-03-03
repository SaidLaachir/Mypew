# myPew – Secure CLI with MFA (TOTP)

myPew is a security-oriented CLI tool for Linux systems that protects critical system commands using multi-factor authentication (password + TOTP).

## Features
- Password-based authentication
- TOTP (RFC 6238) MFA
- MFA session with expiration
- Protection of critical Linux commands
- Command execution auditing
- Designed for Kali / Linux systems

## Installation

```bash
git clone https://github.com/SaidLaachir/myPew.git
cd myPew
pip install -r requirements.txt
