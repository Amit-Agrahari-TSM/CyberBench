import json
import os
import sys

def grade():
    matrix = {
        "task": "fix-sqli-flask",
        "category": "web-security",
        "total_score": 0.0,
        "max_score": 1.0,
        "metrics": {}
    }

    try:
        if not os.path.exists("report.json") or not os.path.exists("app_fixed.py"):
            raise FileNotFoundError("Missing report.json or app_fixed.py")

        with open("report.json", "r", encoding="utf-8") as f:
            report = json.load(f)

        vulnerable_file = report.get("vulnerable_file")
        vulnerability_type = report.get("vulnerability_type")
        vulnerability_fixed = report.get("vulnerability_fixed")

        with open("app_fixed.py", "r", encoding="utf-8") as f:
            code = f.read()

        has_placeholder = "?" in code
        no_fmt = "%" not in code and "f\"" not in (code.split("cursor.execute")[1].split(")")[0] if "cursor.execute" in code else "")

        matrix["metrics"]["vulnerable_file_reported"] = {
            "weight": 0.20,
            "score": 1.0 if vulnerable_file == "app.py" else 0.0,
            "expected": "app.py",
            "actual": vulnerable_file
        }

        matrix["metrics"]["vulnerability_type_reported"] = {
            "weight": 0.20,
            "score": 1.0 if "SQL" in str(vulnerability_type) else 0.0,
            "expected": "SQL Injection",
            "actual": vulnerability_type
        }

        matrix["metrics"]["vulnerability_fixed_flag"] = {
            "weight": 0.20,
            "score": 1.0 if vulnerability_fixed is True else 0.0,
            "expected": True,
            "actual": vulnerability_fixed
        }

        matrix["metrics"]["parameterized_queries_used"] = {
            "weight": 0.20,
            "score": 1.0 if has_placeholder else 0.0,
            "expected": "SQL ? placeholder present",
            "actual": has_placeholder
        }

        matrix["metrics"]["raw_string_formatting_removed"] = {
            "weight": 0.20,
            "score": 1.0 if no_fmt else 0.0,
            "expected": "No string formatting in cursor.execute",
            "actual": no_fmt
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
