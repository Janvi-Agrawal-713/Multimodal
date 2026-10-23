"""
Tests for Module C: Construction Planning & Cost Estimation.
"""

import pytest
from modules.cost_estimation import (
    calculate_project_estimate,
    get_current_stage,
    STRUCTURE_PRESETS,
    CITY_TIER_MULTIPLIERS
)


def test_calculate_project_estimate_basic():
    area = 2000.0
    structure = "Residential: Independent Villa / Duplex"
    tier = "Tier 2 Urban (Pune, Ahmedabad, Jaipur, Lucknow, Kochi, Chandigarh, Surat)"
    completion = 40.0
    
    result = calculate_project_estimate(
        structure_type=structure,
        built_up_area_sqft=area,
        city_tier=tier,
        completion_pct=completion
    )
    
    # Preset base rate = 1850, Tier 2 multiplier = 1.05 -> rate = 1942.50
    expected_rate = 1850.0 * 1.05
    expected_total = area * expected_rate
    expected_incurred = expected_total * 0.40
    expected_remaining = expected_total - expected_incurred
    
    fin = result["financial_summary"]
    assert fin["total_estimated_cost"] == pytest.approx(expected_total, 0.01)
    assert fin["incurred_expenditure"] == pytest.approx(expected_incurred, 0.01)
    assert fin["remaining_budget"] == pytest.approx(expected_remaining, 0.01)
    assert "₹" in fin["total_cost_formatted"]
    assert "Cr" in fin["total_cost_compact"] or "Lakhs" in fin["total_cost_compact"]


def test_material_heuristics():
    area = 1000.0
    structure = "Residential: Multi-Storey Apartment (RCC Frame)"
    tier = "Tier 1 Metro (Mumbai, Delhi-NCR, Bengaluru, Hyderabad, Chennai, Kolkata)"
    
    result = calculate_project_estimate(
        structure_type=structure,
        built_up_area_sqft=area,
        city_tier=tier,
        completion_pct=50.0
    )
    
    mat = result["material_estimates"]
    # Check cement bags: 1000 * 0.44 = 440 bags
    assert mat["cement"]["quantity_bags"] == 440.0
    assert mat["cement"]["total_cost"] == 440.0 * 380.0
    
    # Check steel: 1000 * 4.5 = 4500 kg = 4.5 MT
    assert mat["steel_rebar"]["quantity_kg"] == 4500.0
    assert mat["steel_rebar"]["quantity_metric_tonnes"] == 4.5


def test_invalid_area_raises():
    with pytest.raises(ValueError):
        calculate_project_estimate(
            structure_type="Residential: Independent Villa / Duplex",
            built_up_area_sqft=-100,
            city_tier="Tier 1 Metro (Mumbai, Delhi-NCR, Bengaluru, Hyderabad, Chennai, Kolkata)",
            completion_pct=10
        )


def test_milestone_stages():
    assert "Substructure" in get_current_stage(5.0)
    assert "Superstructure" in get_current_stage(35.0)
    assert "Masonry" in get_current_stage(55.0)
    assert "Final Polish" in get_current_stage(95.0)
