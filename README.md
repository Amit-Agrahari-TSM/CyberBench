# CyberBench: Modular Cybersecurity Evaluation Benchmark for AI Agents

**CyberBench** is a modular, reproducible evaluation benchmark suite designed to evaluate AI agents—including **Claude Code (`claude`)** with **MiniMax-M3**—on real-world cybersecurity, SOC log telemetry analysis, web server access log analysis, container security, cloud baseline auditing, and secure coding / vulnerability remediation tasks.

---

## 📁 Repository & Folder Structure

```
CyberBench/
├── dataset.toml                  # Root Harbor dataset manifest definition
│
├── Utkarsh-task/                 # Utkarsh's Task Folder (2 Unique Tasks)
│   ├── dataset.toml
│   ├── analyze-auth-log/         # Task 1: Real Linux Auth Log Analysis (SOC)
│   └── audit-sshd-config/        # Task 2: OpenSSH Daemon Security Audit
│
├── Varun/                        # Varun's Task Folder (2 Unique Tasks)
│   ├── dataset.toml
│   ├── harden-dockerfile/        # Task 3: Container Security & Dockerfile Audit
│   └── fix-sqli-flask/           # Task 4: Secure Coding / Flask SQL Injection Fix
│
├── Sanket/                       # Sanket's Task Folder (2 Unique Tasks)
│   ├── dataset.toml
│   ├── analyze-apache-access-log/# Task 5 (Hard): Real 1500-Line Elastic Apache Access Log Analysis
│   └── remediate-jwt-auth-bypass/# Task 6 (Hard): Multi-File Python JWT Auth Bypass Remediation
│
├── tasks/                        # Master Task Directory (All 6 Tasks)
├── scripts/                      # Evaluation Adapters & Test Runner Scripts
└── README.md
```

---

## 🚀 Running Harbor Commands by Folder

You can navigate into any individual folder and execute `harbor run -p . -a claude-code` to run the 2 unique tasks assigned to that folder:

### 1. Utkarsh's Folder (`Utkarsh-task`)
```powershell
cd Utkarsh-task
harbor run -p . -a claude-code `
  -m "MiniMax-M3[1m]" `
  --ae ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic" `
  --ae ANTHROPIC_API_KEY="your_api_key"
```

### 2. Varun's Folder (`Varun`)
```powershell
cd Varun
harbor run -p . -a claude-code `
  -m "MiniMax-M3[1m]" `
  --ae ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic" `
  --ae ANTHROPIC_API_KEY="your_api_key"
```

### 3. Sanket's Folder (`Sanket`)
```powershell
cd Sanket
harbor run -p . -a claude-code `
  -m "MiniMax-M3[1m]" `
  --ae ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic" `
  --ae ANTHROPIC_API_KEY="your_api_key"
```
