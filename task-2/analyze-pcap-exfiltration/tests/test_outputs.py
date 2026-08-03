import json
import os
import re
import pytest

REPORT_PATH = "report.json"

def get_report():
    assert os.path.exists(REPORT_PATH), f"Output file {REPORT_PATH} missing"
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def test_1_report_file_exists():
    """Test 1: Verify report.json exists in workspace"""
    assert os.path.exists(REPORT_PATH), "report.json does not exist in workspace"

def test_2_json_syntax_validity():
    """Test 2: Verify report.json is valid JSON dictionary"""
    report = get_report()
    assert isinstance(report, dict), "report.json must be a JSON object"
    assert len(report.keys()) > 0, "report.json is empty"

def test_3_victim_ip_identification():
    """Test 3: Verify victim host IP (192.168.1.105) is identified"""
    report = get_report()
    victim_ip = str(report.get("victim_ip", "")).strip()
    assert victim_ip == "192.168.1.105", f"Expected victim_ip 192.168.1.105, got {victim_ip}"

def test_4_attacker_c2_ip_identification():
    """Test 4: Verify external attacker C2 IP (10.0.0.99) is identified"""
    report = get_report()
    c2_ip = str(report.get("attacker_c2_ip") or report.get("c2_ip") or "").strip()
    assert c2_ip == "10.0.0.99", f"Expected attacker_c2_ip 10.0.0.99, got {c2_ip}"

def test_5_exfiltration_protocol_detection():
    """Test 5: Verify exfiltration protocol is identified as DNS or UDP"""
    report = get_report()
    proto = str(report.get("exfiltration_protocol", "")).upper().strip()
    assert "DNS" in proto or "UDP" in proto, f"Expected DNS/UDP protocol, got {proto}"

def test_6_exfiltration_chunk_count():
    """Test 6: Verify chunk count of 4 packets is detected"""
    report = get_report()
    chunks = report.get("chunk_count")
    assert chunks == 4, f"Expected chunk_count 4, got {chunks}"

def test_7_flag_format_syntax():
    """Test 7: Verify exfiltrated secret matches FLAG{...} format"""
    report = get_report()
    secret = str(report.get("exfiltrated_secret", "")).strip()
    assert secret.startswith("FLAG{") and secret.endswith("}"), f"Secret format invalid: {secret}"

def test_8_exfiltrated_secret_decoding():
    """Test 8: Verify exact exfiltrated secret value payload"""
    report = get_report()
    secret = str(report.get("exfiltrated_secret", "")).strip()
    assert secret == "FLAG{k8s_secret_auth_token_9981}", f"Secret mismatch: {secret}"

def test_9_no_false_positive_background_ips():
    """Test 9: Verify background DNS resolvers (8.8.8.8) are not flagged as C2"""
    report = get_report()
    c2_ip = str(report.get("attacker_c2_ip") or report.get("c2_ip") or "").strip()
    assert c2_ip != "8.8.8.8" and c2_ip != "192.168.1.50", f"Background IP false positive: {c2_ip}"

def test_10_evaluation_matrix_generated():
    """Test 10: Verify evaluation matrix file is present or computable"""
    report = get_report()
    assert "exfiltrated_secret" in report and "attacker_c2_ip" in report, "Missing core metrics"
