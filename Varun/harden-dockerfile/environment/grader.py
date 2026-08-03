import json
import sys

def grade():
    matrix = {
        "task": "harden-dockerfile",
        "category": "docker-security",
        "total_score": 0.0,
        "max_score": 1.0,
        "metrics": {}
    }

    try:
        with open("report.json", "r", encoding="utf-8") as f:
            report = json.load(f)

        runs_root = report.get("runs_as_root")
        secret = report.get("has_hardcoded_secret")
        latest = report.get("uses_latest_tag")
        health = report.get("missing_healthcheck")
        vuln_cnt = report.get("vulnerability_count")

        matrix["metrics"]["runs_as_root"] = {
            "weight": 0.20,
            "score": 1.0 if runs_root is True else 0.0,
            "expected": True,
            "actual": runs_root
        }

        matrix["metrics"]["has_hardcoded_secret"] = {
            "weight": 0.20,
            "score": 1.0 if secret is True else 0.0,
            "expected": True,
            "actual": secret
        }

        matrix["metrics"]["uses_latest_tag"] = {
            "weight": 0.20,
            "score": 1.0 if latest is True else 0.0,
            "expected": True,
            "actual": latest
        }

        matrix["metrics"]["missing_healthcheck"] = {
            "weight": 0.20,
            "score": 1.0 if health is True else 0.0,
            "expected": True,
            "actual": health
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
