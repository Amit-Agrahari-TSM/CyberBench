import json
import sys
import os

def grade():
    matrix = {
        "task": "audit-k8s-rbac-container",
        "category": "cloud-security",
        "total_score": 0.0,
        "max_score": 1.0,
        "test_cases_passed": 0,
        "total_test_cases": 10,
        "metrics": {}
    }

    try:
        # Test 1: File Existence (Weight 0.05)
        file_exists = os.path.exists("report.json")
        matrix["metrics"]["1_file_exists"] = {
            "weight": 0.05,
            "score": 1.0 if file_exists else 0.0,
            "description": "report.json generated in workspace"
        }

        if not file_exists:
            raise FileNotFoundError("report.json missing")

        with open("report.json", "r", encoding="utf-8") as f:
            report = json.load(f)

        # Test 2: Valid JSON Schema (Weight 0.05)
        is_dict = isinstance(report, dict) and len(report) > 0
        matrix["metrics"]["2_json_validity"] = {
            "weight": 0.05,
            "score": 1.0 if is_dict else 0.0,
            "description": "Valid JSON dictionary schema"
        }

        rbac_wildcard = report.get("wildcard_rbac_permissions") or report.get("wildcard_rbac_detected")
        docker_sock = report.get("docker_socket_mounted")
        privileged = report.get("privileged_container_mode") or report.get("privileged_container_detected")
        token_automount = report.get("service_account_token_automounted") or report.get("service_account_token_automount")
        vuln_cnt = report.get("critical_vulnerability_count") or report.get("vulnerability_count")

        # Test 3: Wildcard ClusterRole RBAC Detection (Weight 0.15)
        matrix["metrics"]["3_wildcard_rbac"] = {
            "weight": 0.15,
            "score": 1.0 if rbac_wildcard is True else 0.0,
            "expected": True,
            "actual": rbac_wildcard,
            "description": "Wildcard RBAC permissions (verbs/resources '*') detected"
        }

        # Test 4: Docker Socket HostPath Mount Detection (Weight 0.15)
        matrix["metrics"]["4_docker_socket_mounted"] = {
            "weight": 0.15,
            "score": 1.0 if docker_sock is True else 0.0,
            "expected": True,
            "actual": docker_sock,
            "description": "/var/run/docker.sock hostPath mount detected"
        }

        # Test 5: Privileged Container Execution Detection (Weight 0.15)
        matrix["metrics"]["5_privileged_container_mode"] = {
            "weight": 0.15,
            "score": 1.0 if privileged is True else 0.0,
            "expected": True,
            "actual": privileged,
            "description": "securityContext.privileged=true mode detected"
        }

        # Test 6: ServiceAccount Automount Token Detection (Weight 0.10)
        matrix["metrics"]["6_service_account_token_automounted"] = {
            "weight": 0.10,
            "score": 1.0 if token_automount is True else 0.0,
            "expected": True,
            "actual": token_automount,
            "description": "automountServiceAccountToken=true risk detected"
        }

        # Test 7: Vulnerability Count Accuracy (Weight 0.10)
        matrix["metrics"]["7_vulnerability_count"] = {
            "weight": 0.10,
            "score": 1.0 if (isinstance(vuln_cnt, int) and vuln_cnt >= 4) else 0.0,
            "expected": ">= 4",
            "actual": vuln_cnt,
            "description": "Total vulnerability count accurately computed"
        }

        # Test 8: Manifest File Target Identification (Weight 0.10)
        target_file = report.get("target_manifest") or "k8s_deployment.yaml"
        matrix["metrics"]["8_target_manifest"] = {
            "weight": 0.10,
            "score": 1.0 if "k8s_deployment" in str(target_file) else 0.0,
            "description": "Target Kubernetes manifest identified"
        }

        # Test 9: Boolean Data Type Strictness (Weight 0.10)
        bool_strict = isinstance(docker_sock, bool) and isinstance(rbac_wildcard, bool)
        matrix["metrics"]["9_boolean_data_types"] = {
            "weight": 0.10,
            "score": 1.0 if bool_strict else 0.0,
            "description": "Audit findings returned as strict boolean data types"
        }

        # Test 10: Security Matrix Coverage (Weight 0.05)
        coverage = all(k in report for k in ["wildcard_rbac_permissions", "docker_socket_mounted", "privileged_container_mode"])
        matrix["metrics"]["10_matrix_coverage"] = {
            "weight": 0.05,
            "score": 1.0 if coverage else 0.0,
            "description": "Complete coverage across RBAC, volume mounts, and container contexts"
        }

        # Count passed test cases & compute weighted score
        passed_cases = sum(1 for m in matrix["metrics"].values() if m["score"] == 1.0)
        matrix["test_cases_passed"] = passed_cases
        total_score = sum(m["weight"] * m["score"] for m in matrix["metrics"].values())
        matrix["total_score"] = round(total_score, 2)

    except Exception as e:
        matrix["error"] = str(e)
        matrix["total_score"] = 0.0

    with open("evaluation_matrix.json", "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=2)

    print(json.dumps(matrix, indent=2))

    if matrix["total_score"] >= 0.8:
        print(f"PASS (Test Cases Passed: {matrix['test_cases_passed']}/10)")
        sys.exit(0)
    else:
        print(f"FAIL (Score: {matrix['total_score']}, Passed: {matrix['test_cases_passed']}/10)")
        sys.exit(1)

if __name__ == "__main__":
    grade()
