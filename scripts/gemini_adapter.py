"""
CyberBench Gemini CLI Adapter for Harbor Framework

This adapter allows the Harbor benchmark framework to dispatch task prompts
to the Gemini CLI agent interface.
"""

import sys
import os
import subprocess
import argparse
import time

def run_gemini_task(task_dir, model="gemini-2.5-flash"):
    prompt_file = os.path.join(task_dir, "prompt.md")
    if not os.path.exists(prompt_file):
        prompt_file = os.path.join(task_dir, "instruction.md")
        
    if not os.path.exists(prompt_file):
        print(f"Error: Prompt file not found in {task_dir}")
        return False

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    print(f"Executing Gemini CLI for task: {os.path.basename(task_dir)}...")
    start_time = time.time()
    
    # Execute gemini CLI command
    cmd = ["gemini", "--model", model, "prompt", prompt_text]
    try:
        res = subprocess.run(cmd, cwd=task_dir, capture_output=True, text=True, timeout=300)
        elapsed = time.time() - start_time
        print(f"Gemini CLI completed in {elapsed:.2f}s with returncode {res.returncode}")
        return res.returncode == 0
    except Exception as e:
        print(f"Failed to execute Gemini CLI: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CyberBench Gemini CLI Task Adapter")
    parser.add_argument("--task-dir", required=True, help="Path to the task directory")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini model name")
    args = parser.parse_args()
    
    success = run_gemini_task(args.task-dir, args.model)
    sys.exit(0 if success else 1)
