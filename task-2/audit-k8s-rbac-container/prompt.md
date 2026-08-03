You are a Principal Kubernetes Cloud Security Architect.

Audit the multi-document Kubernetes manifest file `k8s_deployment.yaml` in the current workspace directory.

Identify critical cloud infrastructure vulnerabilities across RBAC permissions, service account configurations, and container spec definitions.

Your `report.json` must analyze the following security fields:
1. `wildcard_rbac_permissions`: `true` if ClusterRole assigns wildcard (`*`) apiGroups, resources, or verbs
2. `docker_socket_mounted`: `true` if Docker socket (`/var/run/docker.sock`) is mounted into the pod via hostPath
3. `privileged_container_mode`: `true` if container runs with `privileged: true` or `runAsUser: 0`
4. `service_account_token_automounted`: `true` if `automountServiceAccountToken` is set to `true`
5. `critical_vulnerability_count`: integer count of distinct security vulnerabilities identified (e.g. 4)

Save the result as `report.json` in the current workspace in the following JSON format:

```json
{
  "wildcard_rbac_permissions": true,
  "docker_socket_mounted": true,
  "privileged_container_mode": true,
  "service_account_token_automounted": true,
  "critical_vulnerability_count": 4
}
```
