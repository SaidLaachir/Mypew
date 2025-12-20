from utils.storage import load_mfa_session

def session_valid() -> bool:
    return load_mfa_session()
