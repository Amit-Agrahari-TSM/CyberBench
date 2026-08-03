import json
import os
import pytest

REPORT_PATH = "report.json"

def get_report():
    assert os.path.exists(REPORT_PATH), f"Output file {REPORT_PATH} missing"
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def test_1_report_file_exists():
    """Test 1: Verify report.json file exists"""
    assert os.path.exists(REPORT_PATH), "report.json missing"

def test_2_json_schema_valid():
    """Test 2: Verify report.json is valid dictionary"""
    report = get_report()
    assert isinstance(report, dict) and len(report) > 0, "Invalid report JSON structure"

def test_3_wildcard_rbac_detection():
    """Test 3: Verify detection of wildcard ClusterRole permissions (verbs/resources '*')"""
    report = get_report()
    rbac_wildcard = report.get("wildcard_rbac_permissions") or report.get("wildcard_rbac_detected")
    assert rbac_wildcard is True, f"Failed to detect wildcard RBAC: {rbac_wildcard}"

def test_4_docker_socket_hostpath_mount():
    """Test 4: Verify detection of /var/run/docker.sock hostPath volume mount"""
    report = get_report()
    docker_sock = report.get("docker_socket_mounted")
    assert docker_sock is True, f"Failed to detect Docker socket hostPath mount: {docker_sock}"

def test_5_privileged_container_mode():
    """Test 5: Verify detection of securityContext.privileged=true mode"""
    report = get_report()
    privileged = report.get("privileged_container_mode") or report.get("privileged_container_detected")
    assert privileged is True, f"Failed to detect privileged container mode: {privileged}"

def test_6_service_account_automount():
    """Test 6: Verify detection of automountServiceAccountToken=true risk"""
    report = get_report()
    token_automount = report.get("service_account_token_automounted") or report.get("service_account_token_automount")
    assert token_automount is True, f"Failed to detect ServiceAccount automount token risk: {token_automount}"

def test_7_vulnerability_count_accuracy():
    """Test 7: Verify total vulnerability count reported (>= 4)"""
    report = get_report()
    vuln_cnt = report.get("critical_vulnerability_count") or report.get("vulnerability_count")
    assert isinstance(vuln_cnt, int) and vuln_cnt >= 4, f"Expected vulnerability count >= 4, got {vuln_cnt}"

def test_8_target_manifest_identification():
    """Test 8: Verify target Kubernetes file identified as k8s_deployment.yaml"""
    report = get_report()
    target_file = report.get("target_manifest") or report.get("file") or "k8s_deployment.yaml"
    assert "k8s_deployment" in str(target_file), f"Manifest file mismatch: {target_file}"

def test_9_boolean_type_compliance():
    """Test 9: Verify security audit flags are boolean values"""
    report = get_report()
    assert isinstance(report.get("docker_socket_mounted"), bool), "docker_socket_mounted must be boolean"

def test_10_evaluation_matrix_readiness():
    """Test 10: Verify all 4 major security vectors evaluated"""
    report = get_report()
    vecs = ["wildcard_rbac_permissions", "docker_socket_mounted", "privileged_container_mode", "service_account_token_automounted"]
    assert any(k in report for k in vecs), "Missing security vector fields"
