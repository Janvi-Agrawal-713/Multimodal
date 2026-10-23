"""
Module E: Consolidated Reports and Export
Consolidates audit results, structural diagnostics, cost estimates, and weather protocols
into standardized, downloadable JSON reports and executive summaries.
"""

import json
import datetime
from typing import Dict, Any, Optional


def build_consolidated_report(
    project_name: str,
    safety_audit_data: Optional[Dict[str, Any]] = None,
    crack_diagnostic_data: Optional[Dict[str, Any]] = None,
    cost_estimation_data: Optional[Dict[str, Any]] = None,
    weather_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Assembles a unified, multi-module project audit report for stakeholder sign-off and archiving.
    """
    timestamp = datetime.datetime.now().isoformat()
    
    # Calculate an Overall Platform Risk Index
    risk_factors = []
    
    safety_score = None
    if safety_audit_data and "safety_score" in safety_audit_data:
        safety_score = safety_audit_data["safety_score"]
        if safety_score < 60:
            risk_factors.append("CRITICAL: Safety & PPE compliance below acceptable OSHA/IS threshold.")
        elif safety_score < 75:
            risk_factors.append("MODERATE: PPE non-compliance or minor site hazards detected.")
            
    crack_severity = None
    if crack_diagnostic_data and "estimated_severity" in crack_diagnostic_data:
        crack_severity = crack_diagnostic_data["estimated_severity"]
        if crack_severity in ["High", "Severe"]:
            risk_factors.append(f"HIGH: Structural defect detected ({crack_diagnostic_data.get('defect_identified', 'Severe Crack')}).")
            
    weather_risk = None
    if weather_data and "risk_level" in weather_data:
        weather_risk = weather_data["risk_level"]
        if weather_risk in ["High", "Severe"]:
            risk_factors.append(f"ENVIRONMENTAL: Adverse weather protocols active ({weather_data.get('selected_condition', 'Adverse Weather')}).")
            
    overall_health = "Satisfactory / Low Risk"
    if any("CRITICAL" in r for r in risk_factors) or (crack_severity == "Severe"):
        overall_health = "Critical Alert / Immediate Action Mandated"
    elif len(risk_factors) >= 2 or any("HIGH" in r for r in risk_factors):
        overall_health = "Elevated Caution / Supervised Operations"
    elif len(risk_factors) == 1:
        overall_health = "Moderate Caution / Corrective Tasks Pending"

    report = {
        "platform_metadata": {
            "application_title": "Multimodal Construction Intelligence Platform",
            "version": "1.0.0-capstone",
            "project_name": project_name or "Project Horizon - Site Alpha",
            "generated_at": timestamp,
            "overall_site_health_status": overall_health,
            "flagged_risk_factors": risk_factors if risk_factors else ["No immediate critical hazards flagged."]
        },
        "executive_summary": {
            "safety_audit_completed": safety_audit_data is not None,
            "safety_score": safety_score,
            "crack_diagnostics_completed": crack_diagnostic_data is not None,
            "crack_defect_category": crack_diagnostic_data.get("category") if crack_diagnostic_data else None,
            "cost_estimation_completed": cost_estimation_data is not None,
            "total_budget_inr": cost_estimation_data.get("financial_summary", {}).get("total_cost_formatted") if cost_estimation_data else None,
            "weather_protocol_active": weather_data.get("selected_condition") if weather_data else "Not configured"
        },
        "modules": {
            "module_a_safety_audit": safety_audit_data,
            "module_b_crack_diagnostics": crack_diagnostic_data,
            "module_c_cost_estimation": cost_estimation_data,
            "module_d_weather_protocol": weather_data
        },
        "legal_and_compliance_disclaimers": {
            "structural_disclaimer": (
                "Visual crack evaluations are AI-assisted screening indicators only and do not replace "
                "formal non-destructive testing or structural audits by a registered civil/structural engineer."
            ),
            "safety_disclaimer": (
                "Site safety audits reflect image-based observations and should be validated via physical "
                "daily site inspections conforming to IS 13416 and OSHA guidelines."
            ),
            "cost_disclaimer": (
                "Financial estimates are algorithmic approximations based on standard CPWD/NBC empirical heuristics. "
                "Contractor quotations, site topography, and material market volatility must be verified locally."
            )
        }
    }
    
    return report


def export_report_to_json_string(report_data: Dict[str, Any], indent: int = 2) -> str:
    """Serializes a report dictionary to an indented UTF-8 JSON string."""
    return json.dumps(report_data, indent=indent, default=str, ensure_ascii=False)
