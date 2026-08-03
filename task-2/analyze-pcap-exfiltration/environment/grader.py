import json
import sys
import os

def grade():
    matrix = {
        "task": "analyze-pcap-exfiltration",
        "category": "network-analysis",
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
            "description": "report.json file generated in workspace"
        }

        if not file_exists:
            raise FileNotFoundError("report.json not found")

        with open("report.json", "r", encoding="utf-8") as f:
            report = json.load(f)

        # Test 2: Valid JSON Object (Weight 0.05)
        is_dict = isinstance(report, dict) and len(report) > 0
        matrix["metrics"]["2_json_validity"] = {
            "weight": 0.05,
            "score": 1.0 if is_dict else 0.0,
            "description": "Valid JSON dictionary format"
        }

        victim_ip = str(report.get("victim_ip", "")).strip()
        c2_ip = str(report.get("attacker_c2_ip") or report.get("c2_ip") or "").strip()
        proto = str(report.get("exfiltration_protocol", "")).upper().strip()
        secret = str(report.get("exfiltrated_secret", "")).strip()
        chunks = report.get("chunk_count")

        # Test 3: Victim IP Identification (Weight 0.10)
        matrix["metrics"]["3_victim_ip"] = {
            "weight": 0.10,
            "score": 1.0 if victim_ip == "192.168.1.105" else 0.0,
            "expected": "192.168.1.105",
            "actual": victim_ip,
            "description": "Victim host IP correctly identified"
        }

        # Test 4: Attacker C2 IP Identification (Weight 0.15)
        matrix["metrics"]["4_attacker_c2_ip"] = {
            "weight": 0.15,
            "score": 1.0 if c2_ip == "10.0.0.99" else 0.0,
            "expected": "10.0.0.99",
            "actual": c2_ip,
            "description": "Attacker C2 server IP correctly identified"
        }

        # Test 5: Exfiltration Protocol Detection (Weight 0.10)
        matrix["metrics"]["5_exfiltration_protocol"] = {
            "weight": 0.10,
            "score": 1.0 if ("DNS" in proto or "UDP" in proto) else 0.0,
            "expected": "DNS",
            "actual": proto,
            "description": "Exfiltration transport protocol detected"
        }

        # Test 6: Chunk Count Accuracy (Weight 0.10)
        matrix["metrics"]["6_chunk_count"] = {
            "weight": 0.10,
            "score": 1.0 if chunks == 4 else 0.0,
            "expected": 4,
            "actual": chunks,
            "description": "Exact exfiltration packet chunk count"
        }

        # Test 7: Secret Flag Format (Weight 0.10)
        flag_fmt = secret.startswith("FLAG{") and secret.endswith("}")
        matrix["metrics"]["7_flag_format"] = {
            "weight": 0.10,
            "score": 1.0 if flag_fmt else 0.0,
            "description": "Exfiltrated secret complies with FLAG{...} syntax"
        }

        # Test 8: Secret Payload Decoding (Weight 0.20)
        matrix["metrics"]["8_secret_payload_decoded"] = {
            "weight": 0.20,
            "score": 1.0 if secret == "FLAG{k8s_secret_auth_token_9981}" else 0.0,
            "expected": "FLAG{k8s_secret_auth_token_9981}",
            "actual": secret,
            "description": "Stolen authentication token base64 payload decoded"
        }

        # Test 9: False Positive Noise Filter (Weight 0.10)
        no_fp = (c2_ip != "8.8.8.8" and c2_ip != "192.168.1.50")
        matrix["metrics"]["9_noise_filtering"] = {
            "weight": 0.10,
            "score": 1.0 if no_fp else 0.0,
            "description": "Background DNS resolvers filtered out"
        }

        # Test 10: Complete Diagnostic Summary (Weight 0.05)
        complete = all(k in report for k in ["victim_ip", "attacker_c2_ip", "exfiltrated_secret"])
        matrix["metrics"]["10_complete_report"] = {
            "weight": 0.05,
            "score": 1.0 if complete else 0.0,
            "description": "Report contains all required diagnostic fields"
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
