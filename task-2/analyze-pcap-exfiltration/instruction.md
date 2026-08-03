You are a Senior Network Forensics Analyst.

A security alert indicates that a compromised Linux host exfiltrated sensitive data via covert DNS queries to an external Command & Control (C2) server.

Inspect the packet capture file `traffic.pcap` in the workspace directory.

Your objectives:
1. Identify the victim host IP address (`victim_ip`) and the external attacker C2 server IP address (`attacker_c2_ip`).
2. Identify the covert protocol used for exfiltration (`exfiltration_protocol`).
3. Reconstruct the ordered subdomain payload chunks, concatenate them, and decode the base64 string to reveal the stolen secret (`exfiltrated_secret`).
4. Count the total number of DNS exfiltration query chunks sent (`chunk_count`).

Save your analysis as `report.json` in the current workspace with the following JSON schema:

```json
{
  "victim_ip": "192.168.1.105",
  "attacker_c2_ip": "10.0.0.99",
  "exfiltration_protocol": "DNS",
  "exfiltrated_secret": "FLAG{k8s_secret_auth_token_9981}",
  "chunk_count": 4
}
```
