"""
CyberBench Test & Benchmark Validation Runner

Runs grader verification across all CyberBench tasks and reports
category breakdown, pass rates, and execution statistics.
"""

import os
import sys
import subprocess
import time
import json

TASKS = [
    "analyze-auth-log",
    "audit-sshd-config",
    "harden-dockerfile",
    "fix-sqli-flask"
]

REFERENCE_OUTPUTS = {
    "analyze-auth-log": {
        "report.json": {
            "failed_logins": 114,
            "successful_logins": 53,
            "top_attacking_ip": "60.30.224.116",
            "root_logins": 1
        }
    },
    "audit-sshd-config": {
        "report.json": {
            "permit_root_login_allowed": True,
            "empty_passwords_allowed": True,
            "x11_forwarding_enabled": True,
            "insecure_protocol_enabled": True,
            "vulnerability_count": 5
        }
    },
    "harden-dockerfile": {
        "report.json": {
            "runs_as_root": True,
            "has_hardcoded_secret": True,
            "uses_latest_tag": True,
            "missing_healthcheck": True,
            "vulnerability_count": 5
        }
    },
    "fix-sqli-flask": {
        "report.json": {
            "vulnerable_file": "app.py",
            "vulnerability_type": "SQL Injection",
            "remediation": "Parameterized Queries",
            "vulnerability_fixed": True
        },
        "app_fixed.py": '''import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return jsonify({"status": "success" if user else "error"})
'''
    }
}

def run_task_solution_and_grade(task_name):
    task_dir = os.path.abspath(os.path.join("tasks", task_name))
    grader_script = os.path.join(task_dir, "grader.py")
    
    print(f"\n==========================================")
    print(f" Testing Task: {task_name}")
    print(f"==========================================")
    
    if not os.path.exists(task_dir):
        print(f"FAIL: Task directory {task_dir} missing")
        return False, 0.0

    start = time.time()
    
    # Generate reference solution output for validation test
    created_files = []
    if task_name in REFERENCE_OUTPUTS:
        for fname, content in REFERENCE_OUTPUTS[task_name].items():
            fpath = os.path.join(task_dir, fname)
            created_files.append(fpath)
            with open(fpath, "w", encoding="utf-8") as f:
                if isinstance(content, dict):
                    json.dump(content, f, indent=2)
                else:
                    f.write(content)

    # Run grader
    try:
        res = subprocess.run([sys.executable, grader_script], cwd=task_dir, capture_output=True, text=True)
        elapsed = time.time() - start
        output = res.stdout.strip() or res.stderr.strip()
        
        # Cleanup generated reference outputs after test
        for fp in created_files:
            if os.path.exists(fp):
                os.remove(fp)

        if res.returncode == 0 and "PASS" in output:
            print(f" Result: PASS ({elapsed:.3f}s)")
            return True, elapsed
        else:
            print(f" Result: FAIL ({elapsed:.3f}s) -> {output}")
            return False, elapsed
    except Exception as e:
        elapsed = time.time() - start
        for fp in created_files:
            if os.path.exists(fp):
                os.remove(fp)
        print(f" Result: ERROR ({elapsed:.3f}s) -> {e}")
        return False, elapsed

def main():
    print("CyberBench Benchmark Suite Validation")
    print("--------------------------------------")
    
    passed = 0
    total = len(TASKS)
    times = []

    for task in TASKS:
        ok, elapsed = run_task_solution_and_grade(task)
        if ok:
            passed += 1
        times.append(elapsed)

    pass_rate = (passed / total) * 100
    avg_time = sum(times) / total if total > 0 else 0

    print("\n==========================================")
    print(" SUMMARY METRICS")
    print("==========================================")
    print(f" Total Tasks Evaluated : {total}")
    print(f" Passed Tasks         : {passed}")
    print(f" Overall Pass Rate    : {pass_rate:.1f}%")
    print(f" Average Execution Time: {avg_time:.3f} seconds/task")
    print("==========================================\n")
    
    if passed == total:
        print("ALL BENCHMARK TASKS PASSED VERIFICATION!")
        sys.exit(0)
    else:
        print("SOME BENCHMARK TASKS FAILED VERIFICATION!")
        sys.exit(1)

if __name__ == "__main__":
    main()
