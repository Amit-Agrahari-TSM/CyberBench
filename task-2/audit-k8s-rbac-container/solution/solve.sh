#!/bin/bash
cat << 'EOF' > report.json
{
  "wildcard_rbac_permissions": true,
  "docker_socket_mounted": true,
  "privileged_container_mode": true,
  "service_account_token_automounted": true,
  "critical_vulnerability_count": 4
}
EOF
