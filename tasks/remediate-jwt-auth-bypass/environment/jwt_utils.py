import json
import base64
import hmac
import hashlib
import time

SECRET_KEY = "super-secret-jwt-key-2026"

def base64url_decode(input_str):
    rem = len(input_str) % 4
    if rem > 0:
        input_str += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input_str)

def decode_token(token):
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid token format")

    header_raw, payload_raw, signature_raw = parts
    header = json.loads(base64url_decode(header_raw).decode('utf-8'))
    payload = json.loads(base64url_decode(payload_raw).decode('utf-8'))

    # VULNERABILITY 1: Insecurely allowing 'none' algorithm bypass
    alg = header.get("alg", "").lower()
    if alg == "none":
        return payload  # Accepts unsigned tokens!

    # VULNERABILITY 2: Ignoring token expiration claim (exp)
    # Missing: if payload.get("exp") and time.time() > payload["exp"]: raise ValueError("Token expired")

    # VULNERABILITY 3: Weak signature verification fallback
    expected_sig = base64.urlsafe_b64encode(
        hmac.new(SECRET_KEY.encode(), f"{header_raw}.{payload_raw}".encode(), hashlib.sha256).digest()
    ).decode().rstrip("=")

    # Unchecked signature parsing
    return payload
