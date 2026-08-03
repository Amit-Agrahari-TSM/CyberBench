# CyberBench: Modular Cybersecurity Evaluation Benchmark for AI Agents

**CyberBench** is a modular, reproducible evaluation benchmark suite designed to evaluate AI agents—including **Claude Code (`claude`)** powered by **MiniMax-M3**—on real-world cybersecurity, SOC log analysis, system hardening, container security, and secure coding tasks.

It integrates natively with the **Harbor Framework** (`harbor run -p tasks -a claude-code`).

---

## 📁 Repository Structure

```
CyberBench/
├── dataset.toml                  # Harbor dataset manifest definition
├── datasets/
│   └── cyber-bench.toml          # Modular dataset configuration file
├── tasks/                        # Evaluation task benchmarks
│   ├── analyze-auth-log/         # Task 1: Linux authentication log analysis (SOC)
│   ├── audit-sshd-config/        # Task 2: SSH daemon hardening & audit
│   ├── harden-dockerfile/        # Task 3: Container security & Dockerfile hardening
│   └── fix-sqli-flask/           # Task 4: Secure coding & SQL injection remediation
├── scripts/
│   ├── claude_adapter.py         # Claude Code CLI adapter interface
│   ├── run_claude_bench.py       # CyberBench evaluation runner for Claude Code
│   ├── gemini_adapter.py         # Gemini CLI adapter
│   └── test_runner.py            # Task verifier validation script
└── README.md
```

---

## 🚀 Running CyberBench via Harbor Framework with Claude Code & MiniMax

From the `CyberBench` root directory, execute:

### 1. Standard Harbor Execution
```powershell
harbor run -p tasks -a claude-code
```

### 2. Specifying MiniMax Model
```powershell
harbor run -p tasks -a claude-code -m MiniMax-M3
```

---

## 🎯 Task Benchmark Suite Overview

| Task ID | Category | Difficulty | Description | Target Output |
| :--- | :--- | :--- | :--- | :--- |
| `analyze-auth-log` | Log Analysis | Easy | Analyze real Linux authentication log (`auth.log`) to compute failed logins, successful logins, top attacking IP, and root logins. | `report.json` |
| `audit-sshd-config` | System Security | Easy/Medium | Audit insecure SSH daemon config (`sshd_config`) to detect root login, empty passwords, X11 forwarding, and weak protocols. | `report.json` |
| `harden-dockerfile` | Container Security | Medium | Audit insecure `Dockerfile` for root user execution, hardcoded secrets, unpinned tags, and missing healthchecks. | `report.json` |
| `fix-sqli-flask` | Secure Coding | Medium | Identify and remediate SQL injection vulnerability in a Flask web application using parameterized SQL queries (`?`). | `app_fixed.py` + `report.json` |
