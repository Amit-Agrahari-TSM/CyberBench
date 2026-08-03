import json
import os

def test_outputs():
    assert os.path.exists("report.json"), "report.json missing"
    with open("report.json", "r", encoding="utf-8") as f:
        report = json.load(f)

    assert report.get("attacker_c2_ip") == "10.0.0.99", "Incorrect C2 IP"
    assert report.get("exfiltrated_secret") == "FLAG{k8s_secret_auth_token_9981}", "Incorrect secret token"
