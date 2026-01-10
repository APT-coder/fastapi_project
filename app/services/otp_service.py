import random
import time
from typing import Dict

OTP_EXPIRY_SECONDS = 5 * 60  # 5 minutes

# email -> { otp, expires_at }
_otp_store: Dict[str, dict] = {}


def generate_otp() -> str:
    return f"{random.randint(100000, 999999)}"


def save_otp(email: str, otp: str):
    _otp_store[email] = {
        "otp": otp,
        "expires_at": time.time() + OTP_EXPIRY_SECONDS,
    }


def verify_otp(email: str, otp: str) -> bool:
    record = _otp_store.get(email)
    if not record:
        return False

    if time.time() > record["expires_at"]:
        _otp_store.pop(email, None)
        return False

    if record["otp"] != otp:
        return False

    # OTP valid → delete after use
    _otp_store.pop(email, None)
    return True
