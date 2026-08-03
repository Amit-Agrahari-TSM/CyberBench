import json
import os

def test_outputs():
    assert os.path.exists("report.json"), "report.json does not exist"
    with open("report.json", "r", encoding="utf-8") as f:
        report = json.load(f)

    assert report.get("vulnerable_file") == "app.py", f"Expected vulnerable_file 'app.py', got {report.get('vulnerable_file')}"
    assert "SQL" in str(report.get("vulnerability_type")), f"Expected SQL Injection in vulnerability_type, got {report.get('vulnerability_type')}"
    assert report.get("vulnerability_fixed") is True, f"Expected vulnerability_fixed=True, got {report.get('vulnerability_fixed')}"

    assert os.path.exists("app_fixed.py"), "app_fixed.py does not exist"
    with open("app_fixed.py", "r", encoding="utf-8") as f:
        code = f.read()

    assert "?" in code, "Parameterized query placeholder '?' missing in app_fixed.py"
