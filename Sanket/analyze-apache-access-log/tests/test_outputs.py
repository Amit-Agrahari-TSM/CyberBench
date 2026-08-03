import json
import os

def test_outputs():
    assert os.path.exists("report.json"), "report.json missing"
    with open("report.json", "r", encoding="utf-8") as f:
        report = json.load(f)

    assert report.get("total_requests") == 1500, "total_requests mismatch"
    assert report.get("top_client_ip") == "66.249.73.135", "top_client_ip mismatch"
    assert report.get("status_200_count") == 1367, "status_200_count mismatch"
