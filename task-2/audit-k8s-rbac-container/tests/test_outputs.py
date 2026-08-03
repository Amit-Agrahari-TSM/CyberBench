import json
import os

def test_outputs():
    assert os.path.exists("report.json"), "report.json missing"
    with open("report.json", "r", encoding="utf-8") as f:
        report = json.load(f)

    assert report.get("wildcard_rbac_permissions") is True, "Wildcard RBAC undetected"
    assert report.get("docker_socket_mounted") is True, "Docker socket mount undetected"
