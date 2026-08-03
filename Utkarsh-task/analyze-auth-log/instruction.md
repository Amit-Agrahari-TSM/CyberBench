You are a SOC analyst.

Analyze `auth.log` in the current workspace directory.

Identify:
1. `failed_logins`: Total number of failed login attempts
2. `successful_logins`: Total number of successful logins
3. `top_attacking_ip`: The IP address with the highest number of failed login attempts
4. `root_logins`: Total number of successful logins as the `root` user

Save the answer as `report.json` in the workspace in the following JSON format:

```json
{
  "failed_logins": 114,
  "successful_logins": 53,
  "top_attacking_ip": "60.30.224.116",
  "root_logins": 1
}
```
