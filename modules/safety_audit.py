"""
Module A: Construction Site Safety & PPE Audit
Analyzes construction site photographs for PPE compliance (helmets, vests,
footwear, harnesses), identifies site hazards, calculates safety scores,
and generates structured JSON audit reports.
"""

import datetime
from typing import Dict, Any, Optional
from PIL import Image

from modules.gemini_service import (
    analyze_image_with_gemini,
    is_live_ai_available
)

SAFETY_AUDIT_PROMPT = """
You are a Senior Construction Safety Auditor and OSHA/IS 13416 Compliance Inspector.
Examine this construction site photograph and perform a thorough PPE and hazards safety audit.

You must respond ONLY with a valid, raw JSON object matching this schema exactly (no markdown formatting, no conversational preamble):
{
  "safety_score": 75,
  "score_rating": "Good Compliance",
  "estimated_workers_visible": 3,
  "ppe_compliance": {
    "helmets": {
      "status": "Compliant | Non-Compliant | Partially Compliant | Not Applicable / Obscured",
      "observed": "Detailed description of hard hats observed or missing",
      "compliance_rate_percent": 100
    },
    "high_visibility_vests": {
      "status": "Compliant | Non-Compliant | Partially Compliant | Not Applicable / Obscured",
      "observed": "Detailed description of high-vis vests observed or missing",
      "compliance_rate_percent": 66
    },
    "safety_footwear": {
      "status": "Compliant | Non-Compliant | Partially Compliant | Not Applicable / Obscured",
      "observed": "Detailed description of boots/footwear observed",
      "compliance_rate_percent": 100
    },
    "safety_harnesses": {
      "status": "Compliant | Non-Compliant | Partially Compliant | Not Applicable (Ground Level)",
      "observed": "Observations on fall protection, lanyards, or anchor points",
      "compliance_rate_percent": 100
    }
  },
  "detected_hazards": [
    {
      "id": "HAZ-001",
      "hazard_title": "Short descriptive title",
      "severity": "Critical | High | Medium | Low",
      "location": "Specific location in photo (e.g., upper left scaffolding, floor center)",
      "standard_reference": "Relevant standard (e.g., IS 13416 / OSHA 1926.501)",
      "corrective_measure": "Specific corrective action needed"
    }
  ],
  "site_cleanliness_housekeeping": "Satisfactory | Moderate | Poor",
  "audit_summary": "Professional concise summary of the safety posture on site"
}
"""


def generate_simulated_safety_audit(image: Image.Image, filename: str) -> Dict[str, Any]:
    """
    Generates a realistic, deterministic simulated audit for demo purposes.
    Clearly labeled with DEMO flags as mandated by project requirements.
    """
    width, height = image.size
    aspect_ratio = width / max(1, height)
    
    # Deterministic variation based on image aspect ratio and dimensions
    if aspect_ratio > 1.2:
        # Wide angle shot scenario: Scaffolding and edge hazards
        score = 68
        rating = "Needs Attention"
        workers = 4
        helmets_stat = "Partially Compliant"
        helmets_obs = "3 of 4 workers visible wearing safety helmets; 1 worker in background lacks headgear."
        helmets_pct = 75
        vests_stat = "Compliant"
        vests_obs = "All workers wearing fluorescent high-visibility reflective vests."
        vests_pct = 100
        boots_stat = "Compliant"
        boots_obs = "Steel-toed construction boots observed on foreground personnel."
        boots_pct = 100
        harness_stat = "Partially Compliant"
        harness_obs = "Worker at elevated scaffolding tier lacks anchored dual lanyard."
        harness_pct = 50
        hazards = [
            {
                "id": "HAZ-001",
                "hazard_title": "Worker at Height Without Anchored Fall Arrest",
                "severity": "Critical",
                "location": "Upper elevated platform / scaffolding tier",
                "standard_reference": "IS 13416 (Part 2) / OSHA 1926.501",
                "corrective_measure": "Immediately halt work at height; verify 100% tie-off to certified life-lines with energy-absorbing lanyards."
            },
            {
                "id": "HAZ-002",
                "hazard_title": "Uncapped Vertical Rebar Starter Bars",
                "severity": "High",
                "location": "Ground perimeter walkway near column base",
                "standard_reference": "OSHA 1926.701(b) / IS 456",
                "corrective_measure": "Install certified OSHA-rated plastic rebar mushroom caps or wooden troughs over protruding rebar."
            },
            {
                "id": "HAZ-003",
                "hazard_title": "Unorganized Electrical Cables on Floor",
                "severity": "Medium",
                "location": "Center walkway / staging zone",
                "standard_reference": "IS 13416 (Part 4) / NFPA 70",
                "corrective_measure": "Elevate all 230V power supply cables with non-conductive S-hooks above ground clearance (>2.1m)."
            }
        ]
        housekeeping = "Moderate"
        summary = (
            "Site demonstrates strong high-vis vest compliance, but critical height fall-protection "
            "deficiencies and exposed vertical rebar bars require immediate corrective intervention before work continues."
        )
    else:
        # Standard portrait / close-up framing
        score = 88
        rating = "Good Compliance"
        workers = 2
        helmets_stat = "Compliant"
        helmets_obs = "All active workers properly wearing EN 397/IS 2925 industrial hard hats with fastened chinstraps."
        helmets_pct = 100
        vests_stat = "Compliant"
        vests_obs = "High-visibility Class 2 reflective vests equipped on all personnel."
        vests_pct = 100
        boots_stat = "Compliant"
        boots_obs = "Standard heavy-duty safety footwear with ankle support verified."
        boots_pct = 100
        harness_stat = "Not Applicable (Ground Level)"
        harness_obs = "Operations currently conducted at grade level; no fall arrest mandated for this activity."
        harness_pct = 100
        hazards = [
            {
                "id": "HAZ-001",
                "hazard_title": "Minor Trip Hazard: Scattered Timber Offcuts",
                "severity": "Low",
                "location": "Staging corridor adjacent to formwork stack",
                "standard_reference": "IS 13416 (Part 1) General Safety",
                "corrective_measure": "Implement daily 5S housekeeping sweep and deposit scrap wood into designated skip bins."
            }
        ]
        housekeeping = "Satisfactory"
        summary = (
            "High standard of PPE compliance observed. Workers are properly equipped with helmets, "
            "vests, and safety boots. Continue routine daily safety monitoring."
        )
        
    return {
        "is_demo_mode": True,
        "data_source": "SIMULATED_DEMO_DATA (Interactive Demo Mode - No Gemini API Key)",
        "demo_notice": "⚠️ DEMO MODE ACTIVE: This safety audit report is simulated demo data for evaluation and testing purposes. To perform live multimodal AI vision analysis, enter your Gemini API key.",
        "audit_timestamp": datetime.datetime.now().isoformat(),
        "image_filename": filename,
        "image_resolution": f"{width}x{height}",
        "safety_score": score,
        "score_rating": rating,
        "estimated_workers_visible": workers,
        "ppe_compliance": {
            "helmets": {
                "status": helmets_stat,
                "observed": helmets_obs,
                "compliance_rate_percent": helmets_pct
            },
            "high_visibility_vests": {
                "status": vests_stat,
                "observed": vests_obs,
                "compliance_rate_percent": vests_pct
            },
            "safety_footwear": {
                "status": boots_stat,
                "observed": boots_obs,
                "compliance_rate_percent": boots_pct
            },
            "safety_harnesses": {
                "status": harness_stat,
                "observed": harness_obs,
                "compliance_rate_percent": harness_pct
            }
        },
        "detected_hazards": hazards,
        "site_cleanliness_housekeeping": housekeeping,
        "audit_summary": summary
    }


def audit_construction_site_image(
    image: Image.Image,
    filename: str,
    user_api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main audit entry point. If live Gemini API is available, executes vision analysis;
    otherwise gracefully falls back to structured, clearly labeled demo simulation.
    """
    if not is_live_ai_available(user_api_key):
        return generate_simulated_safety_audit(image, filename)
        
    # Attempt live Gemini AI Vision
    success, data, message = analyze_image_with_gemini(
        image=image,
        prompt=SAFETY_AUDIT_PROMPT,
        user_api_key=user_api_key
    )
    
    if success and data and isinstance(data, dict) and "safety_score" in data:
        data["is_demo_mode"] = False
        data["data_source"] = "LIVE_GEMINI_AI_VISION"
        data["demo_notice"] = "🟢 LIVE AI ANALYSIS: Generated via Gemini Multimodal Vision API."
        data["audit_timestamp"] = datetime.datetime.now().isoformat(),
        data["image_filename"] = filename
        data["image_resolution"] = f"{image.width}x{image.height}"
        return data
        
    # If API call failed or couldn't parse schema, fallback to demo mode with informative explanation
    fallback = generate_simulated_safety_audit(image, filename)
    fallback["demo_notice"] = f"⚠️ FALLBACK DEMO MODE: Live API request encountered an issue ({message}). Displaying illustrative demo analysis."
    return fallback
