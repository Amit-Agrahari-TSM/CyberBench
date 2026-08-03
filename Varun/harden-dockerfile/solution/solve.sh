#!/bin/bash
cat << 'EOF' > report.json
{
  "runs_as_root": true,
  "has_hardcoded_secret": true,
  "uses_latest_tag": true,
  "missing_healthcheck": true,
  "vulnerability_count": 5
}
EOF
EOF
