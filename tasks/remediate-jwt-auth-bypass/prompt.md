You are a Senior Application Security Engineer.

Audit the Python JWT authentication handler `jwt_utils.py` in the workspace directory.

`jwt_utils.py` contains severe authentication bypass flaws:
1. Algorithm confusion vulnerability: accepts `{"alg": "none"}` unsigned JWT tokens
2. Missing signature verification: returns payload without validating HMAC-SHA256 signature against `SECRET_KEY`
3. Missing expiration validation: ignores the `exp` claim in token payload

Your tasks:
1. Refactor `jwt_utils.py` in place to:
   - Explicitly reject tokens with `alg: "none"` or unapproved algorithms (raise `ValueError`)
   - Strictly verify HMAC-SHA256 signature using `SECRET_KEY` (raise `ValueError` if signature is invalid)
   - Validate token expiration (`exp` claim); raise `ValueError` if current time exceeds `exp`
2. Create `report.json` in the current workspace with your audit findings.

**Output JSON Schema (Use actual audit findings, NOT the dummy values below):**

```json
{
  "vulnerability_type": "DUMMY_VULNERABILITY",
  "vulnerable_file": "dummy_file.py",
  "none_algorithm_disabled": false,
  "signature_verification_enforced": false,
  "expiration_check_added": false
}
```
