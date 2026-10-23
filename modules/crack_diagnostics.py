"""
Module B: Concrete Crack Diagnostics
Performs visual screening of concrete walls, slabs, and structural surfaces.
Identifies defect types, categories, probable root causes, urgency, and engineering remedies,
with mandatory structural disclaimers and measurement limitations.
"""

import datetime
from typing import Dict, Any, Optional
from PIL import Image

from modules.gemini_service import (
    analyze_image_with_gemini,
    is_live_ai_available
)

STRUCTURAL_ENGINEERING_DISCLAIMER = (
    "⚠️ CRITICAL STRUCTURAL DISCLAIMER: This computer-vision screening is an AI-assisted preliminary "
    "diagnostic tool and does NOT substitute for an on-site structural audit by a licensed Civil or "
    "Structural Engineer. Standard 2D photography cannot evaluate subsurface rebar corrosion, rebar yield "
    "capacity, concrete core compressive strength, or soil strata stability. Always commission on-site "
    "Non-Destructive Testing (NDT) such as Ultrasonic Pulse Velocity (IS 13311 Part 1) and Rebound Hammer "
    "(IS 13311 Part 2) for authoritative assessment."
)

CRACK_MEASUREMENT_LIMITATION = (
    "📏 CALIBRATION & MEASUREMENT NOTICE: Standard photographs without a calibrated physical reference "
    "scale (such as a certified crack comparator gauge or millimeter optical target placed flush on the "
    "surface) cannot provide certified millimeter crack width or depth measurements. All dimensional "
    "assessments herein are qualitative visual observations."
)

CRACK_DIAGNOSTICS_PROMPT = f"""
You are a Senior Forensic Structural Engineer and Concrete Petrography Specialist.
Analyze this photograph of a concrete surface, wall, beam, or masonry element for defects.

Strict Guidelines:
1. Identify visible crack patterns, orientations (diagonal, horizontal, vertical, map-cracking), and secondary symptoms (efflorescence, spalling, rust stains).
2. Categorize strictly as: "Structural Defect", "Non-Structural / Surface Defect", or "Environmental / Chemical Deterioration".
3. State likely causes (thermal shrinkage, shear stress, differential settlement, rebar corrosion, overload).
4. Assign estimated severity ("Low", "Moderate", "High", "Severe") and urgency.
5. NEVER claim precise millimeter crack dimensions unless a calibrated scale is explicitly visible in the photo.

Respond ONLY with a valid JSON object matching this schema exactly (no markdown formatting, no conversational text):
{{
  "defect_identified": "e.g. Diagonal Shear Crack in Reinforced Concrete Beam",
  "category": "Structural Defect | Non-Structural / Surface Defect | Environmental / Chemical Deterioration",
  "estimated_severity": "Low | Moderate | High | Severe",
  "urgency_level": "Immediate Structural Evacuation & Shoring (<24h) | High Priority Inspection (within 7 days) | Moderate Priority (within 30 days) | Routine Monitoring (3-6 months)",
  "visible_patterns": "Detailed description of orientation, branching, path, and surface texture",
  "potential_causes": [
    "Primary cause 1",
    "Secondary factor 2"
  ],
  "associated_symptoms": [
    "e.g., Efflorescence (calcium leaching), spalling concrete cover, rust staining"
  ],
  "recommended_next_steps": [
    "Install Avongard crack width monitor / tell-tale gauge to track active displacement",
    "Commission on-site Non-Destructive Testing (UPV and Rebound Hammer)",
    "Recommended repair approach (e.g. low-viscosity epoxy injection vs elastomeric sealant)"
  ],
  "measurement_scale_detected": false,
  "diagnostic_summary": "Concise engineering summary of the observed defect"
}}
"""


def generate_simulated_crack_diagnostics(image: Image.Image, filename: str) -> Dict[str, Any]:
    """
    Generates a deterministic, high-fidelity simulated diagnostic report for demo mode.
    Fully tagged with demo badges and structural disclaimers.
    """
    width, height = image.size
    aspect_ratio = width / max(1, height)
    
    if aspect_ratio >= 1.0:
        # Scenario 1: Diagonal structural shear crack
        defect_name = "Diagonal Shear Crack at Beam-Column / Lintel Junction"
        category = "Structural Defect"
        severity = "High"
        urgency = "High Priority Inspection (within 7 days)"
        patterns = (
            "Pronounced diagonal fissure propagating at approximately a 40–45 degree inclination, "
            "typical of principal tensile stresses exceeding concrete tensile resistance in shear zones."
        )
        causes = [
            "Excessive shear stresses exceeding beam web reinforcement capacity (stirrups).",
            "Differential settlement of adjacent structural columns or footings.",
            "Load redistribution from dead load or unforeseen live load increments."
        ]
        symptoms = [
            "Noticeable diagonal fracture path.",
            "Minor aggregate interlock loss along the fracture plane.",
            "Potential loss of concrete shear transfer capacity."
        ]
        steps = [
            "Install a calibrated optical tell-tale crack monitor (Avongard gauge) immediately to record movement over 14 days.",
            "Engage a registered structural engineer to perform structural load checks and verify stirrup spacing.",
            "Conduct Ultrasonic Pulse Velocity (UPV) test (IS 13311 Part 1) across the crack to evaluate depth penetration.",
            "If dormant: structural low-viscosity epoxy pressure injection; if active: structural underpinning and steel jacketing."
        ]
        summary = (
            "Screening indicates a potentially active diagonal shear crack in a load-bearing zone. "
            "Requires prompt structural engineering inspection and continuous displacement monitoring."
        )
    else:
        # Scenario 2: Vertical / Map hairline shrinkage defect
        defect_name = "Plastic Shrinkage & Thermal Surface Hairline Cracking"
        category = "Non-Structural / Surface Defect"
        severity = "Low"
        urgency = "Routine Monitoring (3-6 months)"
        patterns = (
            "Fine, shallow, irregular interconnected 'map-cracking' pattern confined to the surface render/paste layer."
        )
        causes = [
            "Rapid surface moisture evaporation during early hydration (inadequate early moist curing or windy dry weather).",
            "High water-cement ratio or rich cement mortar mix causing excessive drying shrinkage.",
            "Thermal differential between concrete core and surface exposed to sun."
        ]
        symptoms = [
            "Superficial craze cracking.",
            "No evidence of structural displacement or rebar corrosion staining."
        ]
        steps = [
            "Mark boundary benchmarks with date stamps and photograph at 30-day intervals to verify crack dormancy.",
            "Clean surface thoroughly with wire brush and compressed air.",
            "Apply high-grade elastomeric waterproofing acrylic coating or crystalline penetration sealer.",
            "Ensure future concreting adheres strictly to IS 456 minimum 10-14 days curing protocols."
        ]
        summary = (
            "Visual characteristics correspond to non-structural plastic shrinkage or drying crazing. "
            "Integrity of primary structural elements appears uncompromised. Treat for water ingress prevention."
        )

    return {
        "is_demo_mode": True,
        "data_source": "SIMULATED_DEMO_DATA (Interactive Demo Mode - No Gemini API Key)",
        "demo_notice": "⚠️ DEMO MODE ACTIVE: This concrete diagnostic report is simulated demo data. To analyze real photographs with generative AI vision, enter your Gemini API key in the settings panel.",
        "engineering_disclaimer": STRUCTURAL_ENGINEERING_DISCLAIMER,
        "measurement_limitation_notice": CRACK_MEASUREMENT_LIMITATION,
        "audit_timestamp": datetime.datetime.now().isoformat(),
        "image_filename": filename,
        "image_resolution": f"{width}x{height}",
        "defect_identified": defect_name,
        "category": category,
        "estimated_severity": severity,
        "urgency_level": urgency,
        "visible_patterns": patterns,
        "potential_causes": causes,
        "associated_symptoms": symptoms,
        "recommended_next_steps": steps,
        "measurement_scale_detected": False,
        "diagnostic_summary": summary
    }


def diagnose_concrete_image(
    image: Image.Image,
    filename: str,
    user_api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main diagnostic entry point. Calls Gemini Vision when configured,
    or falls back gracefully to structured, labeled simulated diagnostics.
    """
    if not is_live_ai_available(user_api_key):
        return generate_simulated_crack_diagnostics(image, filename)
        
    success, data, message = analyze_image_with_gemini(
        image=image,
        prompt=CRACK_DIAGNOSTICS_PROMPT,
        user_api_key=user_api_key
    )
    
    if success and data and isinstance(data, dict) and "defect_identified" in data:
        data["is_demo_mode"] = False
        data["data_source"] = "LIVE_GEMINI_AI_VISION"
        data["demo_notice"] = "🟢 LIVE AI ANALYSIS: Evaluated via Gemini Multimodal Vision API."
        data["engineering_disclaimer"] = STRUCTURAL_ENGINEERING_DISCLAIMER
        data["measurement_limitation_notice"] = CRACK_MEASUREMENT_LIMITATION
        data["audit_timestamp"] = datetime.datetime.now().isoformat()
        data["image_filename"] = filename
        data["image_resolution"] = f"{image.width}x{image.height}"
        return data
        
    fallback = generate_simulated_crack_diagnostics(image, filename)
    fallback["demo_notice"] = f"⚠️ FALLBACK DEMO MODE: Vision API request could not complete ({message}). Presenting illustrative diagnostic report."
    return fallback
