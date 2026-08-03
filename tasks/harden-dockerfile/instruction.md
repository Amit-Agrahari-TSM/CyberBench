You are a DevSecOps Security Engineer.

Audit the container configuration `Dockerfile.insecure` in the current workspace.

Identify container security anti-patterns and save your audit as `report.json`.

Your `report.json` must contain the following boolean and integer fields:
- `runs_as_root`: `true` if the container runs as root without creating/switching to a non-root `USER`, `false` otherwise
- `has_hardcoded_secret`: `true` if hardcoded secrets/passwords are declared in `ENV`, `false` otherwise
- `uses_latest_tag`: `true` if the base image relies on `:latest` or unpinned image tag, `false` otherwise
- `missing_healthcheck`: `true` if container lacks a `HEALTHCHECK` instruction, `false` otherwise
- `vulnerability_count`: integer count of distinct security misconfigurations identified (e.g. 5)

Save the answer as `report.json` in the following JSON format:

```json
{
  "runs_as_root": true,
  "has_hardcoded_secret": true,
  "uses_latest_tag": true,
  "missing_healthcheck": true,
  "vulnerability_count": 5
}
```
