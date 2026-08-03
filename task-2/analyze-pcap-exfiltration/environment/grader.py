import json
import sys
import os

def grade():
    matrix = {
        "task": "analyze-pcap-exfiltration",
        "category": "network-analysis",
        "total_score": 0.0,
        "max_score": 1.0,
        "metrics": {}
    }

    try:
        if not os.path.exists("report.json"):
            raise FileNotFoundError("report.json not found")

        with open("report.json", "r", encoding="utf-8") as f:
            report = json.load(f)

        victim_ip = str(report.get("victim_ip", "")).strip()
        c2_ip = str(report.get("attacker_c2_ip") or report.get("c2_ip") or "").strip()
        proto = str(report.get("exfiltration_protocol", "")).upper().strip()
        secret = str(report.get("exfiltrated_secret", "")).strip()
        chunks = report.get("chunk_count")

        matrix["metrics"]["attacker_c2_ip"] = {
            "weight": 0.25,
            "score": 1.0 if c2_ip == "10.0.0.99" else 0.0,
            "expected": "10.0.0.99",
            "actual": c2_ip
        }

        matrix["metrics"]["victim_ip"] = {
            "weight": 0.15,
            "score": 1.0 if victim_ip == "192.168.1.105" else 0.0,
            "expected": "192.168.1.105",
            "actual": victim_ip
        }

        matrix["metrics"]["exfiltration_protocol"] = {
            "weight": 0.15,
            "score": 1.0 if "DNS" in proto or "UDP" in proto else 0.0,
            "expected": "DNS",
            "actual": proto
        }

        matrix["metrics"]["exfiltrated_secret"] = {
            "weight": 0.35,
            "score": 1.0 if secret == "FLAG{k8s_secret_auth_token_9981}" else 0.0,
            "expected": "FLAG{k8s_secret_auth_token_9981}",
            "actual": secret
        }

        matrix["metrics"]["chunk_count"] = {
            "weight": 0.10,
            "score": 1.0 if chunks == 4 else 0.0,
            "expected": 4,
            "actual": chunks
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
