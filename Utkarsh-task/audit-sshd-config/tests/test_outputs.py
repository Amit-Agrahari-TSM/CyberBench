import json
import os

def test_outputs():
    assert os.path.exists("report.json"), "report.json does not exist"
    with open("report.json", "r", encoding="utf-8") as f:
        report = json.load(f)

    assert report.get("permit_root_login_allowed") is True, f"Expected permit_root_login_allowed=True, got {report.get('permit_root_login_allowed')}"
    assert report.get("empty_passwords_allowed") is True, f"Expected empty_passwords_allowed=True, got {report.get('empty_passwords_allowed')}"
    assert report.get("x11_forwarding_enabled") is True, f"Expected x11_forwarding_enabled=True, got {report.get('x11_forwarding_enabled')}"
    assert report.get("insecure_protocol_enabled") is True, f"Expected insecure_protocol_enabled=True, got {report.get('insecure_protocol_enabled')}"
    assert report.get("vulnerability_count") >= 4, f"Expected vulnerability_count >= 4, got {report.get('vulnerability_count')}"
