"""
Tests for Module E: Consolidated Report Generation.
"""

from modules.report_generator import (
    build_consolidated_report,
    export_report_to_json_string
)


def test_consolidated_report_structure():
    safety_mock = {"safety_score": 82, "score_rating": "Good"}
    crack_mock = {"category": "Structural Defect", "estimated_severity": "High"}
    cost_mock = {"financial_summary": {"total_cost_formatted": "₹ 1,50,00,000"}}
    weather_mock = {"selected_condition": "Heavy Rain / Monsoon", "risk_level": "High"}
    
    report = build_consolidated_report(
        project_name="Metro Station Pier 14",
        safety_audit_data=safety_mock,
        crack_diagnostic_data=crack_mock,
        cost_estimation_data=cost_mock,
        weather_data=weather_mock
    )
    
    assert report["platform_metadata"]["project_name"] == "Metro Station Pier 14"
    assert "modules" in report
    assert report["executive_summary"]["safety_score"] == 82
    assert "legal_and_compliance_disclaimers" in report
    
    # JSON serialization test
    json_str = export_report_to_json_string(report)
    assert "Metro Station Pier 14" in json_str
    assert "₹ 1,50,00,000" in json_str
