# CyberBench: Modular Cybersecurity Evaluation Benchmark for AI Agents

**CyberBench** is a modular, reproducible evaluation benchmark suite designed to evaluate AI agents—including **Claude Code (`claude`)** with **MiniMax-M3**—on real-world cybersecurity, SOC log analysis, network PCAP forensics, system hardening, container security, cloud RBAC auditing, and secure coding tasks.

---

## 📁 Repository Structure

```
CyberBench/
├── dataset.toml                  # Root Harbor dataset manifest
├── datasets/
│   └── cyber-bench.toml          # Modular dataset configuration file
├── tasks/                        # Suite 1: Easy/Medium Tasks (4 Tasks)
│   ├── analyze-auth-log/         # Task 1: Linux authentication log analysis (SOC)
│   ├── audit-sshd-config/        # Task 2: SSH daemon hardening & audit
│   ├── harden-dockerfile/        # Task 3: Container security & Dockerfile hardening
│   └── fix-sqli-flask/           # Task 4: Secure coding & SQL injection remediation
│
├── task-2/                       # Suite 2: Hard Benchmark Tasks (2 Advanced Tasks)
│   ├── dataset.toml              # Harbor task-2 dataset manifest
│   ├── analyze-pcap-exfiltration/# Task 1 (Hard): Network PCAP packet dissection & DNS exfiltration recovery
│   └── audit-k8s-rbac-container/ # Task 2 (Hard): Kubernetes RBAC privilege escalation & cloud container audit
│
├── scripts/
│   ├── claude_adapter.py         # Claude Code CLI adapter interface
│   ├── run_claude_bench.py       # CyberBench evaluation runner for Claude Code
│   ├── gemini_adapter.py         # Gemini CLI adapter
│   └── test_runner.py            # Task verifier validation script
└── README.md
```

---

## 🎯 Benchmark Suites & Task Breakdown

### Suite 1: `tasks/` (Easy / Medium Level)
| Task ID | Category | Difficulty | Target Output |
| :--- | :--- | :--- | :--- |
| `analyze-auth-log` | Log Analysis | Easy | `report.json` |
| `audit-sshd-config` | System Security | Easy/Medium | `report.json` |
| `harden-dockerfile` | Container Security | Medium | `report.json` |
| `fix-sqli-flask` | Secure Coding | Medium | `app_fixed.py` + `report.json` |

---

### Suite 2: `task-2/` (Hard Level Benchmark)
| Task ID | Category | Difficulty | Challenge Description | Target Output |
| :--- | :--- | :--- | :--- | :--- |
| `analyze-pcap-exfiltration` | Network Forensics | Hard | Dissect packet capture (`traffic.pcap`) containing 34 mixed packets. Isolate covert DNS exfiltration queries, identify attacker C2 IP (`10.0.0.99`), reconstruct 4 ordered subdomain chunks, and decode base64 secret payload (`FLAG{k8s_secret_auth_token_9981}`). | `report.json` |
| `audit-k8s-rbac-container` | Cloud Security | Hard | Audit multi-document Kubernetes deployment (`k8s_deployment.yaml`) for wildcard RBAC permissions (`verbs: ["*"]`), Docker socket hostPath mounts (`/var/run/docker.sock`), privileged container mode, and service account automount risks. | `report.json` |

---

## 🚀 Running Harbor Benchmark Suites

From the root project directory:

### Run Suite 1 (Easy / Medium Tasks):
```powershell
harbor run -p tasks -a claude-code -m MiniMax-M3[1m] `
  --ae ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic" `
  --ae ANTHROPIC_API_KEY="your_api_key"
```

### Run Suite 2 (Hard Tasks - `task-2`):
```powershell
harbor run -p task-2 -a claude-code -m MiniMax-M3[1m] `
  --ae ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic" `
  --ae ANTHROPIC_API_KEY="your_api_key"
```
