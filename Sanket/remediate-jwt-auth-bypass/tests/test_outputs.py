import json
import os

def test_outputs():
    assert os.path.exists("report.json"), "report.json missing"
    with open("report.json", "r", encoding="utf-8") as f:
        report = json.load(f)

    assert report.get("none_algorithm_disabled") is True, "None algorithm not disabled"
    assert report.get("signature_verification_enforced") is True, "Signature verification not enforced"
