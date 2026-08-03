You are a Linux Systems Security Auditor.

Audit the SSH configuration file `sshd_config` in the workspace directory.

Identify the presence of insecure settings and produce a security report named `report.json`.

Your `report.json` must contain the following boolean and integer fields:
- `permit_root_login_allowed`: `true` if `PermitRootLogin` is set to `yes` or allowed, `false` otherwise
- `empty_passwords_allowed`: `true` if `PermitEmptyPasswords` is set to `yes` or allowed, `false` otherwise
- `x11_forwarding_enabled`: `true` if `X11Forwarding` is enabled, `false` otherwise
- `insecure_protocol_enabled`: `true` if SSH Protocol 1 is enabled in `Protocol`, `false` otherwise
- `vulnerability_count`: integer count of distinct security misconfigurations identified in the file (e.g. 5)

Save the result as `report.json` in the following JSON format:

```json
{
  "permit_root_login_allowed": true,
  "empty_passwords_allowed": true,
  "x11_forwarding_enabled": true,
  "insecure_protocol_enabled": true,
  "vulnerability_count": 5
}
```
