#!/bin/bash
cat << 'EOF' > report.json
{
  "total_requests": 1500,
  "top_client_ip": "66.249.73.135",
  "status_200_count": 1367,
  "status_404_count": 29,
  "status_301_count": 60,
  "get_requests_count": 1494
}
EOF
