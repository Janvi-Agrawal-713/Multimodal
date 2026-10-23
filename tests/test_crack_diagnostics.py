"""
Tests for Module B: Concrete Crack Diagnostics.
"""

from PIL import Image
from modules.crack_diagnostics import (
    generate_simulated_crack_diagnostics,
    diagnose_concrete_image,
    STRUCTURAL_ENGINEERING_DISCLAIMER,
    CRACK_MEASUREMENT_LIMITATION
)


def test_simulated_crack_diagnostics_structure():
    img = Image.new("RGB", (700, 500), color=(150, 150, 150))
    result = generate_simulated_crack_diagnostics(img, "crack.jpg")
    
    assert result["is_demo_mode"] is True
    assert "DEMO" in result["data_source"]
    assert "defect_identified" in result
    assert "category" in result
    assert "estimated_severity" in result
    assert "urgency_level" in result
    assert len(result["potential_causes"]) >= 1
    assert len(result["recommended_next_steps"]) >= 1
    
    # Verify mandatory engineering disclaimer and measurement notice
    assert STRUCTURAL_ENGINEERING_DISCLAIMER in result["engineering_disclaimer"]
    assert CRACK_MEASUREMENT_LIMITATION in result["measurement_limitation_notice"]
    assert result["measurement_scale_detected"] is False


def test_diagnose_without_api_key_runs_demo():
    img = Image.new("RGB", (500, 700), color=(180, 180, 180))
    result = diagnose_concrete_image(img, "vertical_crack.jpg", user_api_key=None)
    assert result["is_demo_mode"] is True
    assert "Non-Structural" in result["category"] or "Structural" in result["category"]
