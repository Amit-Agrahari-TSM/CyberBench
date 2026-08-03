#!/bin/bash
cat << 'EOF' > jwt_utils.py
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

    alg = header.get("alg", "").upper()
    if alg != "HS256":
        raise ValueError(f"Unsupported algorithm: {alg}")

    # Expiration check
    if payload.get("exp") and time.time() > payload["exp"]:
        raise ValueError("Token expired")

    expected_sig = base64.urlsafe_b64encode(
        hmac.new(SECRET_KEY.encode(), f"{header_raw}.{payload_raw}".encode(), hashlib.sha256).digest()
    ).decode().rstrip("=")

    if signature_raw != expected_sig:
        raise ValueError("Invalid signature")

    return payload
EOF

cat << 'EOF' > report.json
{
  "vulnerability_type": "JWT_AUTHENTICATION_BYPASS",
  "vulnerable_file": "jwt_utils.py",
  "none_algorithm_disabled": true,
  "signature_verification_enforced": true,
  "expiration_check_added": true
}
EOF
