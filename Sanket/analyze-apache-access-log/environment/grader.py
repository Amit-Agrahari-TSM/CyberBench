import json
import os
import sys

def grade():
    matrix = {
        "task": "analyze-apache-access-log",
        "category": "log-analysis",
        "total_score": 0.0,
        "max_score": 1.0,
        "metrics": {}
    }

    try:
        if not os.path.exists("report.json"):
            raise FileNotFoundError("report.json missing")

        with open("report.json", "r", encoding="utf-8") as f:
            report = json.load(f)

        total_req = report.get("total_requests")
        top_ip = str(report.get("top_client_ip") or "").strip()
        s200 = report.get("status_200_count")
        s404 = report.get("status_404_count")
        s301 = report.get("status_301_count")
        get_cnt = report.get("get_requests_count")

        matrix["metrics"]["total_requests"] = {
            "weight": 0.20,
            "score": 1.0 if total_req == 1500 else 0.0,
            "expected": 1500,
            "actual": total_req
        }

        matrix["metrics"]["top_client_ip"] = {
            "weight": 0.20,
            "score": 1.0 if top_ip == "66.249.73.135" else 0.0,
            "expected": "66.249.73.135",
            "actual": top_ip
        }

        matrix["metrics"]["status_200_count"] = {
            "weight": 0.15,
            "score": 1.0 if s200 == 1367 else 0.0,
            "expected": 1367,
            "actual": s200
        }

        matrix["metrics"]["status_404_count"] = {
            "weight": 0.15,
            "score": 1.0 if s404 == 29 else 0.0,
            "expected": 29,
            "actual": s404
        }

        matrix["metrics"]["status_301_count"] = {
            "weight": 0.15,
            "score": 1.0 if s301 == 60 else 0.0,
            "expected": 60,
            "actual": s301
        }

        matrix["metrics"]["get_requests_count"] = {
            "weight": 0.15,
            "score": 1.0 if get_cnt == 1494 else 0.0,
            "expected": 1494,
            "actual": get_cnt
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
