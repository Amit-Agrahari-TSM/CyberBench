"""
CyberBench - Claude Code Evaluation Runner with Granular Matrix Metrics

Runs Claude Code CLI (`claude`) against all CyberBench benchmark tasks,
evaluates responses using sub-metric evaluation matrices, and reports final metrics.
"""

import os
import sys
import subprocess
import time
import json
import argparse

TASKS = [
    ("analyze-auth-log", "Log Analysis", "Easy"),
    ("audit-sshd-config", "System Hardening", "Easy/Medium"),
    ("harden-dockerfile", "Container Security", "Medium"),
    ("fix-sqli-flask", "Secure Coding", "Medium")
]

def run_claude_benchmark(model="sonnet", permission_mode="bypassPermissions", timeout=300):
    print("==================================================================")
    print(" CYBERBENCH EVALUATION SUITE: CLAUDE CODE BENCHMARK")
    print(f" Agent: Claude Code (`claude`) | Model: {model}")
    print("==================================================================")

    results = []

    for task_name, category, difficulty in TASKS:
        task_dir = os.path.abspath(os.path.join("tasks", task_name))
        grader_script = os.path.join(task_dir, "grader.py")
        matrix_file = os.path.join(task_dir, "evaluation_matrix.json")

        print(f"\n------------------------------------------------------------------")
        print(f" Task: {task_name} | Category: {category} | Difficulty: {difficulty}")
        print(f"------------------------------------------------------------------")

        if not os.path.exists(task_dir):
            print(f"FAIL: Task directory missing: {task_dir}")
            results.append({"task": task_name, "category": category, "passed": False, "score": 0.0, "time": 0.0, "metrics": {}})
            continue

        start_time = time.time()

        # Step 1: Run Claude Code adapter on task
        cmd = [
            sys.executable,
            os.path.join("scripts", "claude_adapter.py"),
            "--task-dir", task_dir,
            "--model", model,
            "--permission-mode", permission_mode,
            "--timeout", str(timeout)
        ]

        subprocess.run(cmd)
        
        # Step 2: Run task grader & matrix generator
        grader_res = subprocess.run(
            [sys.executable, grader_script],
            cwd=task_dir,
            capture_output=True,
            text=True
        )
        elapsed = time.time() - start_time

        # Read generated evaluation_matrix.json
        matrix_data = {}
        total_score = 0.0
        if os.path.exists(matrix_file):
            try:
                with open(matrix_file, "r", encoding="utf-8") as f:
                    matrix_data = json.load(f)
                total_score = matrix_data.get("total_score", 0.0)
            except Exception:
                pass

        passed = (grader_res.returncode == 0 and total_score >= 0.8)
        
        if passed:
            print(f" STATUS: PASSED | Matrix Score: {total_score * 100:.1f}% ({elapsed:.2f}s)")
        else:
            print(f" STATUS: FAILED | Matrix Score: {total_score * 100:.1f}% ({elapsed:.2f}s)")

        results.append({
            "task": task_name,
            "category": category,
            "difficulty": difficulty,
            "passed": passed,
            "score": total_score,
            "time": elapsed,
            "metrics": matrix_data.get("metrics", {})
        })

    # Print Summary & Evaluation Matrix Report
    print("\n" + "=" * 76)
    print(" CYBERBENCH GRANULAR EVALUATION MATRIX REPORT")
    print("=" * 76)
    print(f"{'Task Name':<20} | {'Category':<18} | {'Score':<8} | {'Status':<8} | {'Time (s)':<8}")
    print("-" * 76)

    passed_count = 0
    total_count = len(results)
    total_time = 0.0
    sum_score = 0.0

    for r in results:
        status_str = "PASS" if r["passed"] else "FAIL"
        if r["passed"]:
            passed_count += 1
        total_time += r["time"]
        sum_score += r["score"]
        score_pct = f"{r['score'] * 100:.1f}%"
        print(f"{r['task']:<20} | {r['category']:<18} | {score_pct:<8} | {status_str:<8} | {r['time']:<8.2f}")

    avg_score_pct = (sum_score / total_count * 100) if total_count > 0 else 0
    pass_rate = (passed_count / total_count * 100) if total_count > 0 else 0

    print("-" * 76)
    print(f" Overall Benchmark Score : {avg_score_pct:.1f}% average task quality score")
    print(f" Pass Rate (Score >= 80%): {passed_count}/{total_count} tasks ({pass_rate:.1f}%)")
    print(f" Total Benchmark Time    : {total_time:.2f} seconds")
    print("=" * 76 + "\n")

    return passed_count == total_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run CyberBench Benchmark Suite with Claude Code")
    parser.add_argument("--model", default="sonnet", help="Claude model (e.g., sonnet, opus, haiku)")
    parser.add_argument("--permission-mode", default="bypassPermissions", help="Claude Code permission mode")
    parser.add_argument("--timeout", type=int, default=300, help="Per-task timeout in seconds")
    args = parser.parse_args()

    success = run_claude_benchmark(args.model, args.permission_mode, args.timeout)
    sys.exit(0 if success else 1)
