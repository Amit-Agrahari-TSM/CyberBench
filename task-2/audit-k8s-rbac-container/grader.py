import json
import sys
import os

def grade():
    matrix = {
        "task": "audit-k8s-rbac-container",
        "category": "cloud-security",
        "total_score": 0.0,
        "max_score": 1.0,
        "metrics": {}
    }

    try:
        if not os.path.exists("report.json"):
            raise FileNotFoundError("report.json not found")

        with open("report.json", "r", encoding="utf-8") as f:
            report = json.load(f)

        rbac_wildcard = report.get("wildcard_rbac_permissions") or report.get("wildcard_rbac_detected")
        docker_sock = report.get("docker_socket_mounted")
        privileged = report.get("privileged_container_mode") or report.get("privileged_container_detected")
        token_automount = report.get("service_account_token_automounted") or report.get("service_account_token_automount")
        vuln_cnt = report.get("critical_vulnerability_count") or report.get("vulnerability_count")

        matrix["metrics"]["wildcard_rbac"] = {
            "weight": 0.25,
            "score": 1.0 if rbac_wildcard is True else 0.0,
            "expected": True,
            "actual": rbac_wildcard
        }

        matrix["metrics"]["docker_socket_mounted"] = {
            "weight": 0.25,
            "score": 1.0 if docker_sock is True else 0.0,
            "expected": True,
            "actual": docker_sock
        }

        matrix["metrics"]["privileged_container_mode"] = {
            "weight": 0.20,
            "score": 1.0 if privileged is True else 0.0,
            "expected": True,
            "actual": privileged
        }

        matrix["metrics"]["service_account_token_automounted"] = {
            "weight": 0.15,
            "score": 1.0 if token_automount is True else 0.0,
            "expected": True,
            "actual": token_automount
        }

        matrix["metrics"]["critical_vulnerability_count"] = {
            "weight": 0.15,
            "score": 1.0 if (isinstance(vuln_cnt, int) and vuln_cnt >= 4) else 0.0,
            "expected": ">= 4",
            "actual": vuln_cnt
        }

        total_score = sum(m["weight"] * m["score"] for m in matrix["metrics"].values())
        matrix["total_score"] = round(total_score, 2)

    except Exception as e:
        matrix["error"] = str(e)
        matrix["total_score"] = 0.0

    with open("evaluation_matrix.json", "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=2)

    print(json.dumps(matrix, indent=2))

    if matrix["total_score"] >= 0.8:
        print("PASS")
        sys.exit(0)
    else:
        print(f"FAIL (Score: {matrix['total_score']})")
        sys.exit(1)

if __name__ == "__main__":
    grade()
