import json
import sys

def grade():
    matrix = {
        "task": "analyze-auth-log",
        "category": "log-analysis",
        "total_score": 0.0,
        "max_score": 1.0,
        "metrics": {}
    }
    
    try:
        with open("report.json", "r", encoding="utf-8") as f:
            report = json.load(f)

        failed = report.get("failed_logins")
        successful = report.get("successful_logins")
        top_ip = str(report.get("top_attacking_ip") or report.get("top_ip") or "").strip()
        root_logins = report.get("root_logins") or report.get("root_login")

        # Metric 1: Failed Logins Count (Weight: 0.25)
        failed_score = 1.0 if failed == 114 else (0.5 if isinstance(failed, int) else 0.0)
        matrix["metrics"]["failed_logins"] = {
            "weight": 0.25,
            "score": failed_score,
            "expected": 114,
            "actual": failed
        }

        # Metric 2: Successful Logins Count (Weight: 0.25)
        success_score = 1.0 if successful == 53 else (0.5 if isinstance(successful, int) else 0.0)
        matrix["metrics"]["successful_logins"] = {
            "weight": 0.25,
            "score": success_score,
            "expected": 53,
            "actual": successful
        }

        # Metric 3: Top Attacking IP (Weight: 0.25)
        top_ip_score = 1.0 if top_ip == "60.30.224.116" else 0.0
        matrix["metrics"]["top_attacking_ip"] = {
            "weight": 0.25,
            "score": top_ip_score,
            "expected": "60.30.224.116",
            "actual": top_ip
        }

        # Metric 4: Root Logins (Weight: 0.25)
        root_score = 1.0 if (root_logins == 1 or root_logins is True) else 0.0
        matrix["metrics"]["root_logins"] = {
            "weight": 0.25,
            "score": root_score,
            "expected": 1,
            "actual": root_logins
        }

        # Calculate weighted total score
        total_score = sum(m["weight"] * m["score"] for m in matrix["metrics"].values())
        matrix["total_score"] = round(total_score, 2)

    except Exception as e:
        matrix["error"] = str(e)
        matrix["total_score"] = 0.0

    # Save detailed evaluation matrix
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
