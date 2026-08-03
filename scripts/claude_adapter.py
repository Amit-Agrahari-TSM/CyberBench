"""
CyberBench Claude Code CLI Adapter for Harbor Framework

This adapter allows the Harbor benchmark framework and CyberBench test runners
to dispatch task prompts to the Claude Code CLI interface (`claude`).
"""

import sys
import os
import subprocess
import argparse
import time

def run_claude_task(task_dir, model="sonnet", permission_mode="bypassPermissions", timeout=300):
    prompt_file = os.path.join(task_dir, "prompt.md")
    if not os.path.exists(prompt_file):
        prompt_file = os.path.join(task_dir, "instruction.md")
        
    if not os.path.exists(prompt_file):
        print(f"Error: Prompt file not found in {task_dir}")
        return False

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_text = f.read().strip()

    print(f"==================================================")
    print(f" Launching Claude Code CLI for Task: {os.path.basename(task_dir)}")
    print(f" Model: {model} | Permission Mode: {permission_mode}")
    print(f"==================================================")
    
    start_time = time.time()
    
    # Construct claude CLI command
    cmd = [
        "claude",
        "-p", prompt_text,
        "--permission-mode", permission_mode,
        "--model", model
    ]
    
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    
    try:
        res = subprocess.run(
            cmd,
            cwd=task_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env
        )
        elapsed = time.time() - start_time
        print(f"Claude Code finished in {elapsed:.2f}s (Exit Code: {res.returncode})")
        if res.stdout:
            print("--- Output Summary ---")
            lines = res.stdout.strip().splitlines()
            print("\n".join(lines[-15:]))
        return res.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"Error: Claude Code timed out after {timeout} seconds")
        return False
    except Exception as e:
        print(f"Error executing Claude Code CLI: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CyberBench Claude Code CLI Task Adapter")
    parser.add_argument("--task-dir", required=True, help="Path to the task directory")
    parser.add_argument("--model", default="sonnet", help="Claude model (e.g. sonnet, opus, haiku)")
    parser.add_argument("--permission-mode", default="bypassPermissions", help="Permission mode for Claude Code")
    parser.add_argument("--timeout", type=int, default=300, help="Task timeout in seconds")
    args = parser.parse_args()
    
    success = run_claude_task(args.task_dir, args.model, args.permission_mode, args.timeout)
    sys.exit(0 if success else 1)
