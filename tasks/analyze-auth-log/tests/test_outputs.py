import json
import os

def test_outputs():
    assert os.path.exists("report.json"), "report.json does not exist"
    with open("report.json", "r", encoding="utf-8") as f:
        report = json.load(f)
    
    failed = report.get("failed_logins")
    successful = report.get("successful_logins")
    top_ip = str(report.get("top_attacking_ip") or report.get("top_ip")).strip()
    root_logins = report.get("root_logins") or report.get("root_login")

    assert failed == 114, f"Expected 114 failed logins, got {failed}"
    assert successful == 53, f"Expected 53 successful logins, got {successful}"
    assert top_ip == "60.30.224.116", f"Expected top_attacking_ip '60.30.224.116', got '{top_ip}'"
    assert root_logins == 1 or root_logins is True, f"Expected root_logins 1 or True, got {root_logins}"
