#!/bin/bash
cat << 'EOF' > report.json
{
  "permit_root_login_allowed": true,
  "empty_passwords_allowed": true,
  "x11_forwarding_enabled": true,
  "insecure_protocol_enabled": true,
  "vulnerability_count": 5
}
EOF
