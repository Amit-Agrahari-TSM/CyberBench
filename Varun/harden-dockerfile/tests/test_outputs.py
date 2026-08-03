import json
import os

def test_outputs():
    assert os.path.exists("report.json"), "report.json does not exist"
    with open("report.json", "r", encoding="utf-8") as f:
        report = json.load(f)

    assert report.get("runs_as_root") is True, f"Expected runs_as_root=True, got {report.get('runs_as_root')}"
    assert report.get("has_hardcoded_secret") is True, f"Expected has_hardcoded_secret=True, got {report.get('has_hardcoded_secret')}"
    assert report.get("uses_latest_tag") is True, f"Expected uses_latest_tag=True, got {report.get('uses_latest_tag')}"
    assert report.get("missing_healthcheck") is True, f"Expected missing_healthcheck=True, got {report.get('missing_healthcheck')}"
    assert report.get("vulnerability_count") >= 4, f"Expected vulnerability_count >= 4, got {report.get('vulnerability_count')}"
