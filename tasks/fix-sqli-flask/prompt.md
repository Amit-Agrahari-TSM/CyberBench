You are an Application Security Engineer.

Analyze `app.py` in the current workspace directory for SQL Injection vulnerabilities.

Perform the following:
1. Fix `app.py` by converting all raw SQL string format/concatenation into safe parameterized queries using SQLite placeholders (`?`). Save the fixed code as `app_fixed.py`.
2. Generate a security report named `report.json` with the following fields:
   - `vulnerable_file`: `"app.py"`
   - `vulnerability_type`: `"SQL Injection"`
   - `remediation`: `"Parameterized Queries"`
   - `vulnerability_fixed`: `true`

Save `report.json` in the following JSON format:

```json
{
  "vulnerable_file": "app.py",
  "vulnerability_type": "SQL Injection",
  "remediation": "Parameterized Queries",
  "vulnerability_fixed": true
}
```
