#!/bin/bash
cat << 'EOF' > report.json
{
  "victim_ip": "192.168.1.105",
  "attacker_c2_ip": "10.0.0.99",
  "exfiltration_protocol": "DNS",
  "exfiltrated_secret": "FLAG{k8s_secret_auth_token_9981}",
  "chunk_count": 4
}
EOF
