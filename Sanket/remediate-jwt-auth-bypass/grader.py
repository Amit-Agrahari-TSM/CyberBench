import json
import sys
import os
import time
import base64

def grade():
    matrix = {
        "task": "remediate-jwt-auth-bypass",
        "category": "secure-coding",
        "total_score": 0.0,
        "max_score": 1.0,
        "metrics": {}
    }

    try:
        # Check report.json
        if not os.path.exists("report.json"):
            raise FileNotFoundError("report.json missing")

        with open("report.json", "r", encoding="utf-8") as f:
            report = json.load(f)

        none_dis = report.get("none_algorithm_disabled")
        sig_enf = report.get("signature_verification_enforced")
        exp_add = report.get("expiration_check_added")

        matrix["metrics"]["report_fields"] = {
            "weight": 0.25,
            "score": 1.0 if (none_dis is True and sig_enf is True and exp_add is True) else 0.0,
            "description": "report.json confirms remediation of all 3 JWT flaws"
        }

        # Import updated jwt_utils
        sys.path.insert(0, os.getcwd())
        import jwt_utils

        def b64url(s):
            return base64.urlsafe_b64encode(s.encode()).decode().rstrip("=")

        # Test 1: Alg None Rejection
        header_none = b64url(json.dumps({"alg": "none", "typ": "JWT"}))
        payload_test = b64url(json.dumps({"user": "admin", "exp": int(time.time()) + 3600}))
        none_token = f"{header_none}.{payload_test}."

        try:
            jwt_utils.decode_token(none_token)
            none_rejected = False
        except Exception:
            none_rejected = True

        matrix["metrics"]["none_alg_rejection"] = {
            "weight": 0.25,
            "score": 1.0 if none_rejected else 0.0,
            "description": "Token with alg=none rejected with Exception"
        }

        # Test 2: Forged Signature Rejection
        header_hs = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}))
        forged_token = f"{header_hs}.{payload_test}.invalid_signature_hash"

        try:
            jwt_utils.decode_token(forged_token)
            forged_rejected = False
        except Exception:
            forged_rejected = True

        matrix["metrics"]["forged_sig_rejection"] = {
            "weight": 0.25,
            "score": 1.0 if forged_rejected else 0.0,
            "description": "Token with invalid signature rejected"
        }

        # Test 3: Expired Token Rejection
        expired_payload = b64url(json.dumps({"user": "admin", "exp": int(time.time()) - 3600}))
        expired_token = f"{header_hs}.{expired_payload}.invalid"

        try:
            jwt_utils.decode_token(expired_token)
            expired_rejected = False
        except Exception:
            expired_rejected = True

        matrix["metrics"]["expired_token_rejection"] = {
            "weight": 0.25,
            "score": 1.0 if expired_rejected else 0.0,
            "description": "Expired token rejected"
        }

        total_score = sum(m["weight"] * m["score"] for m in matrix["metrics"].values())
        matrix["total_score"] = round(total_score, 2)

    except Exception as e:
        matrix["error"] = str(e)
        matrix["total_score"] = 0.0

    with open("evaluation_matrix.json", "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=2)

    print(json.dumps(matrix, indent=2))

    if matrix["total_score"] >= 0.8:
        print("PASS")
        sys.exit(0)
    else:
        print(f"FAIL (Score: {matrix['total_score']})")
        sys.exit(1)

if __name__ == "__main__":
    grade()
