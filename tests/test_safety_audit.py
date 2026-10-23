"""
Tests for Module A: Construction Site Safety & PPE Audit.
"""

from PIL import Image
from modules.safety_audit import (
    generate_simulated_safety_audit,
    audit_construction_site_image
)


def test_simulated_safety_audit_structure():
    # Create a dummy image
    img = Image.new("RGB", (800, 600), color=(100, 100, 100))
    result = generate_simulated_safety_audit(img, "test_site.jpg")
    
    assert result["is_demo_mode"] is True
    assert "DEMO" in result["data_source"]
    assert "safety_score" in result
    assert 0 <= result["safety_score"] <= 100
    assert "ppe_compliance" in result
    
    ppe = result["ppe_compliance"]
    for key in ["helmets", "high_visibility_vests", "safety_footwear", "safety_harnesses"]:
        assert key in ppe
        assert "status" in ppe[key]
        assert "compliance_rate_percent" in ppe[key]
        
    assert "detected_hazards" in result
    assert len(result["detected_hazards"]) >= 1
    for h in result["detected_hazards"]:
        assert "severity" in h
        assert "corrective_measure" in h


def test_audit_without_api_key_runs_demo():
    img = Image.new("RGB", (600, 800), color=(120, 120, 120))
    result = audit_construction_site_image(img, "portrait.jpg", user_api_key=None)
    assert result["is_demo_mode"] is True
    assert "safety_score" in result
