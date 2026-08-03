# CyberBench: Modular Cybersecurity Evaluation Benchmark for AI Agents

**CyberBench** is a modular, reproducible evaluation benchmark suite designed to evaluate AI agents—including **Claude Code (`claude`)** with **MiniMax-M3**—on real-world cybersecurity, SOC log telemetry analysis, web server access log analysis, container security, cloud baseline auditing, and secure coding / vulnerability remediation tasks.

It integrates natively with the **Harbor Framework** (`harbor run -p tasks -a claude-code`).

---

## 📁 Repository Structure

```
CyberBench/
├── dataset.toml                  # Root Harbor dataset manifest definition
├── datasets/
│   └── cyber-bench.toml          # Modular dataset configuration file
├── tasks/                        # Benchmark Tasks (6 Tasks)
│   ├── analyze-auth-log/         # Task 1: Linux authentication log analysis (SOC)
│   ├── audit-sshd-config/        # Task 2: SSH daemon hardening & audit
│   ├── harden-dockerfile/        # Task 3: Container security & Dockerfile hardening
│   ├── fix-sqli-flask/           # Task 4: Secure coding & SQL injection remediation
│   ├── analyze-apache-access-log/# Task 5 (Hard): Real 1500-line Elastic Apache Web Access log analysis
│   └── remediate-jwt-auth-bypass/# Task 6 (Hard): Python JWT auth bypass & algorithm confusion remediation
│
├── scripts/
│   ├── claude_adapter.py         # Claude Code CLI adapter interface
│   ├── run_claude_bench.py       # CyberBench evaluation runner for Claude Code
│   ├── gemini_adapter.py         # Gemini CLI adapter
│   └── test_runner.py            # Task verifier validation script
└── README.md
```

---

## 🎯 Task Benchmark Suite Overview

| Task ID | Category | Difficulty | Dataset Type | Description | Target Output |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `analyze-auth-log` | Log Analysis | Easy | Real Loghub | Analyze authentic Linux auth.log (500 entries) to compute failed logins, successful logins, top attacking IP, and root logins. | `report.json` |
| `audit-sshd-config` | System Security | Easy/Medium | OpenSSH Config | Audit insecure sshd_config file to detect PermitRootLogin, PermitEmptyPasswords, X11Forwarding, and SSH Protocol 1. | `report.json` |
| `harden-dockerfile` | Container Security | Medium | Dockerfile | Audit insecure Dockerfile for root user execution, hardcoded API secret key in ENV, unpinned :latest tag, and missing HEALTHCHECK. | `report.json` |
| `fix-sqli-flask` | Secure Coding | Medium | Flask / SQLite | Identify SQL injection in Flask app.py and refactor database queries to use safe parameterized SQL placeholders (?). | `app_fixed.py` + `report.json` |
| **`analyze-apache-access-log`** | Log Analysis | **Hard** | **Real Elastic Apache Log (1500 lines)** | Dissect real web server access log (`access.log`) to compute total requests, top client IP, HTTP 200/404/301 status counts, and GET request metrics using **dummy schema prompts**. | `report.json` |
| **`remediate-jwt-auth-bypass`** | Secure Coding | **Hard** | **Multi-File Python App** | Audit `jwt_utils.py` to identify `alg: "none"` algorithm confusion, unverified signatures, and ignored `exp` claims. Refactor code to enforce HMAC-SHA256 and expiration checks using **dummy schema prompts**. | `jwt_utils.py` + `report.json` |

---

## 🚀 Running CyberBench via Harbor Framework

From the `CyberBench` root directory, execute:

### Run All 6 Tasks:
```powershell
harbor run -p tasks -a claude-code `
  -m "MiniMax-M3[1m]" `
  --ae ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic" `
  --ae ANTHROPIC_API_KEY="your_api_key"
```
