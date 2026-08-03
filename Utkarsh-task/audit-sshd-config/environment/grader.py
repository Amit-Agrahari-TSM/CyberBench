import json
import sys

def grade():
    matrix = {
        "task": "audit-sshd-config",
        "category": "system-security",
        "total_score": 0.0,
        "max_score": 1.0,
        "metrics": {}
    }

    try:
        with open("report.json", "r", encoding="utf-8") as f:
            report = json.load(f)

        permit_root = report.get("permit_root_login_allowed")
        empty_pass = report.get("empty_passwords_allowed")
        x11 = report.get("x11_forwarding_enabled")
        insecure_proto = report.get("insecure_protocol_enabled")
        vuln_cnt = report.get("vulnerability_count")

        matrix["metrics"]["permit_root_login"] = {
            "weight": 0.20,
            "score": 1.0 if permit_root is True else 0.0,
            "expected": True,
            "actual": permit_root
        }

        matrix["metrics"]["empty_passwords"] = {
            "weight": 0.20,
            "score": 1.0 if empty_pass is True else 0.0,
            "expected": True,
            "actual": empty_pass
        }

        matrix["metrics"]["x11_forwarding"] = {
            "weight": 0.20,
            "score": 1.0 if x11 is True else 0.0,
            "expected": True,
            "actual": x11
        }

        matrix["metrics"]["insecure_protocol"] = {
            "weight": 0.20,
            "score": 1.0 if insecure_proto is True else 0.0,
            "expected": True,
            "actual": insecure_proto
        }

        matrix["metrics"]["vulnerability_count"] = {
            "weight": 0.20,
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
