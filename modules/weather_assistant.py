"""
Module D: Weather-Aware Site Assistant
Provides weather-specific construction precautions, work stoppage guidelines,
operational recommendations, and an engineering Q&A assistant.
"""

from typing import Dict, Any, List

# Standard Weather Condition Protocols
WEATHER_CONDITIONS = {
    "Normal / Clear Weather": {
        "status_code": "NORMAL",
        "icon": "☀️",
        "work_status": "All standard construction activities permitted.",
        "risk_level": "Low",
        "alert_badge": "🟢 Normal Site Operations",
        "summary": "Standard operational parameters with routine PPE and housekeeping requirements.",
        "key_precautions": [
            "Perform standard morning toolbox talks and safety harness inspections before height work.",
            "Ensure routine curing schedule (minimum 7-14 days for OPC/PPC as per IS 456).",
            "Maintain unobstructed primary emergency egress and access paths.",
            "Verify standard PPE compliance: safety helmet, steel-toed boots, high-vis vest."
        ],
        "category_rules": {
            "Working at Height": "Permitted with standard fall arrest systems and certified scaffolding (IS 13416).",
            "Concreting & Pouring": "Ideal for structural pours. Maintain standard slump testing and moist curing.",
            "Excavation & Shoring": "Safe for standard trenching. Ensure spoil piles are kept >1.5m away from edge.",
            "Crane & Lifting": "Standard lifting procedures up to equipment manufacturer wind rating (~38 km/h).",
            "Electrical & Welding": "Standard hot work permits and dry ground connections."
        }
    },
    "Heavy Rain / Monsoon": {
        "status_code": "HEAVY_RAIN",
        "icon": "🌧️",
        "work_status": "High caution: Halt open-air concreting, electrical hot work, and deep trenching.",
        "risk_level": "High",
        "alert_badge": "🔴 High Risk — Severe Monsoon / Wet Hazards",
        "summary": "Waterlogging, electrical conductivity, soil collapse, and concrete wash-out risks are elevated.",
        "key_precautions": [
            "STRICTLY HALT open-air concrete pouring; rainwater will dilute water-cement ratio and wash away cement paste.",
            "De-energize non-essential electrical equipment. Keep DB boards elevated and waterproofed with IP65 enclosures.",
            "Inspect all trenches and deep excavations for slope slippage, soil liquefaction, and water accumulation.",
            "Deploy submersible dewatering pumps with heavy-duty hoses before resuming any basement/footing work.",
            "Re-inspect scaffolding base plates and sole boards for foundation subsidence or soil wash-out before re-entry.",
            "Enforce anti-slip footwear and secure wet walking platforms with non-slip duckboards."
        ],
        "category_rules": {
            "Working at Height": "SUSPEND outdoor roof/scaffold work during heavy rainfall due to severe slip and fall hazards.",
            "Concreting & Pouring": "Cover newly poured slabs immediately with polythene sheeting. Never pour during active rain.",
            "Excavation & Shoring": "MANDATORY trench inspection before worker entry. Install trench boxes or benching.",
            "Crane & Lifting": "Inspect ground bearing under crane outriggers. Wet mud can cause outrigger punch-through.",
            "Electrical & Welding": "PROHIBIT outdoor arc welding. All cables must be elevated above pooling water."
        }
    },
    "High Wind (>40 km/h) / Storm": {
        "status_code": "HIGH_WIND",
        "icon": "💨",
        "work_status": "Severe caution: Cease tower crane lifts and external scaffolding/cladding works.",
        "risk_level": "Severe",
        "alert_badge": "🟠 Severe Risk — High Wind Velocity (>40 km/h)",
        "summary": "Crane jib windage, falling objects, scaffold instability, and worker displacement at elevations.",
        "key_precautions": [
            "IMMEDIATELY CEASE tower crane, mobile crane, and passenger hoist operations (Standard cutoff: 38-40 km/h).",
            "Place tower crane jibs into free-weather-vaning mode as per manufacturer safety protocol.",
            "Tie down or lower loose sheet metal, plywood formwork, tin roofing, and perimeter safety netting.",
            "Evacuate workers from suspended cradles, external mast climbers, and perimeter scaffolding.",
            "Secure loose debris, trash bins, rebar bundles, and lightweight tools from elevated floors.",
            "Check barricades, hoardings, and temporary perimeter fencing for wind damage."
        ],
        "category_rules": {
            "Working at Height": "PROHIBITED on external perimeters, suspended cradles, and roofs until gusts subside below 28 km/h.",
            "Concreting & Pouring": "Permitted at ground/internal areas. High winds accelerate plastic shrinkage cracking; apply anti-evaporant or cover promptly.",
            "Excavation & Shoring": "Beware of airborne dust and debris blinding machine operators. Wear sealed safety goggles.",
            "Crane & Lifting": "ABSOLUTELY HALTED. Taglines are insufficient to control sail effect on formwork or sheet panels.",
            "Electrical & Welding": "Shield welding areas from draft to avoid shielding gas dispersion."
        }
    },
    "Extreme Heat (>40°C / Heatwave)": {
        "status_code": "EXTREME_HEAT",
        "icon": "🔥",
        "work_status": "Caution: Shift schedule adjustments, mandatory hydration, and cold-joint prevention.",
        "risk_level": "Moderate to High",
        "alert_badge": "🟠 Heatwave Warning — Thermal Stress & Rapid Evaporation",
        "summary": "Worker dehydration, heat exhaustion, rapid concrete slump loss, and plastic shrinkage cracking.",
        "key_precautions": [
            "Shift strenuous heavy work to cooler hours (early morning 6 AM - 11 AM and late afternoon 4 PM - 7 PM).",
            "Establish shaded rest stations with cool potable drinking water, ORS (oral rehydration salts), and electrolyte packs.",
            "Mandate 15-minute hydration breaks every hour for outdoor workers.",
            "Pre-chill concrete mixing water with chilled water or flaked ice to maintain placing temperature <32°C (IS 456).",
            "Sprinkle water on aggregates and wet formwork/reinforcement before pouring to prevent moisture absorption.",
            "Start wet curing immediately after initial set and cover with wet hessian cloth to prevent plastic shrinkage cracks."
        ],
        "category_rules": {
            "Working at Height": "Limit continuous exposure under direct sun; metal railings and ladders reach burn temperatures (>60°C).",
            "Concreting & Pouring": "Add retarder admixtures to prevent rapid setting and cold joints. Pour in early morning or evening.",
            "Excavation & Shoring": "Dust control: spray water on haul roads to suppress silica dust inhalation.",
            "Crane & Lifting": "Check hydraulic fluid temperatures and cabin air-conditioning for operator alertness.",
            "Electrical & Welding": "Provide lightweight, breathable flame-resistant cotton workwear; prevent heat stroke under leather jackets."
        }
    }
}

# Knowledge Base for Offline/Demo Mode Construction Assistant
OFFLINE_CONSTRUCTION_KNOWLEDGE = [
    {
        "keywords": ["curing", "cure", "water", "days"],
        "answer": (
            "**Concrete Curing Standards (IS 456:2000 Clause 13.5):**\n"
            "- For Ordinary Portland Cement (OPC): Minimum **7 days** of moist curing under normal conditions.\n"
            "- For Mineral Admixtures / Blended Cements (PPC / PSC) or hot/dry weather: Minimum **10 to 14 days**.\n"
            "- Curing methods: Ponding on slabs, continuously wet hessian / burlap coverings, or membrane-forming curing compounds.\n"
            "- Under extreme heat (>40°C), start moist curing as soon as the concrete surface resists indentation to stop plastic shrinkage cracking."
        )
    },
    {
        "keywords": ["striking", "formwork", "shuttering", "deshuttering", "removal"],
        "answer": (
            "**Formwork Striking Times (IS 456:2000 Clause 11.3):**\n"
            "- Walls, columns, and vertical faces of beams: **16 to 24 hours** (ensure concrete is hard).\n"
            "- Slab soffits (props left under): **3 days**.\n"
            "- Beam soffits (props left under): **7 days**.\n"
            "- Removal of props under slabs (spanning up to 4.5m): **7 days**; spanning >4.5m: **14 days**.\n"
            "- Removal of props under beams/arches (spanning up to 6m): **14 days**; spanning >6m: **21 days**."
        )
    },
    {
        "keywords": ["wind", "crane", "gust", "storm"],
        "answer": (
            "**Wind Speed Limits for Lifting & Scaffolding:**\n"
            "- **38 km/h (~10.5 m/s or Beaufort 6):** Standard manufacturer cutoff to halt all tower crane and mobile crane lifting operations.\n"
            "- **45 km/h:** All suspended work platforms (cradles) must be evacuated and lashed to building columns.\n"
            "- When storm warnings are issued, disengage tower crane slewing brakes into free-wheeling (weather-vaning) to prevent structural mast twisting."
        )
    },
    {
        "keywords": ["rain", "monsoon", "pouring", "wet"],
        "answer": (
            "**Monsoon & Rain Concreting Protocols:**\n"
            "- Do not initiate open-air concrete pours if rain is imminent.\n"
            "- If rain begins mid-pour, halt immediately, create a planned construction joint with shear keys / dowels, and cover fresh concrete with heavy polythene sheets.\n"
            "- Rainwater increases the water-cement ratio, drastically lowering compressive strength (up to 30-40% reduction) and causing severe surface dusting."
        )
    },
    {
        "keywords": ["ppe", "helmet", "vest", "boots", "safety"],
        "answer": (
            "**Mandatory Site PPE Standards:**\n"
            "- **Safety Helmets:** Conforming to IS 2925 / EN 397 (inspected for cracks, UV degradation, and fitted with chinstraps).\n"
            "- **High-Visibility Vests:** Conforming to EN ISO 20471 (Class 2 for general site, Class 3 near heavy highway traffic).\n"
            "- **Safety Footwear:** Steel or composite toe-cap boots with puncture-resistant midsole (IS 15298 / EN ISO 20345 S3).\n"
            "- **Fall Protection:** Full-body harness (IS 3521 / EN 361) mandatory for any work above **1.8 meters (6 feet)**."
        )
    },
    {
        "keywords": ["slump", "workability", "test"],
        "answer": (
            "**Concrete Slump Recommendations (IS 456:2000):**\n"
            "- Shallow sections, pavements: **25 - 75 mm**.\n"
            "- Normal reinforced concrete (slabs, beams, columns): **75 - 100 mm**.\n"
            "- Heavily reinforced sections, pumpable concrete: **100 - 150 mm**.\n"
            "- Tremie / underwater / bored piles: **150 - 200 mm**."
        )
    }
]


def get_weather_details(condition_name: str) -> Dict[str, Any]:
    """Retrieve full safety and operational details for a selected weather condition."""
    details = WEATHER_CONDITIONS.get(condition_name, WEATHER_CONDITIONS["Normal / Clear Weather"])
    return {
        "selected_condition": condition_name,
        "is_simulated_selection": True,
        "data_source_notice": "Manually selected condition for site planning simulation (No live IoT/API feed connected).",
        **details
    }


def query_offline_assistant(query: str, current_weather: str) -> str:
    """Fallback local knowledge assistant when Gemini API key is not present."""
    q_lower = query.lower()
    
    # Check for direct keyword matches in knowledge base
    for item in OFFLINE_CONSTRUCTION_KNOWLEDGE:
        if any(kw in q_lower for kw in item["keywords"]):
            weather_note = f"\n\n> ⛅ **Current Selected Weather Context ({current_weather}):** Please verify that conditions comply with local safety thresholds before proceeding."
            return f"*(Knowledge Engine Response - Demo Mode)*\n\n{item['answer']}{weather_note}"
    
    # Generic intelligent construction assistant response
    weather_info = WEATHER_CONDITIONS.get(current_weather, WEATHER_CONDITIONS["Normal / Clear Weather"])
    return (
        f"*(Knowledge Engine Response - Demo Mode)*\n\n"
        f"Regarding your query on **'{query.strip()}'** under **{current_weather}** conditions:\n\n"
        f"1. **Safety First:** Maintain strict adherence to site safety guidelines ({weather_info['work_status']}).\n"
        f"2. **Codes & Standards:** Refer to IS 456:2000 (Plain & Reinforced Concrete Code of Practice), "
        f"IS 13416 (Construction Safety Recommendations), and NBC 2016 Part 7 (Construction Management).\n"
        f"3. **Immediate Action:** Consult with the resident Project Manager / Safety Officer before modifying any structural or lifting activities.\n\n"
        f"*(Tip: To get personalized generative AI answers, configure your Gemini API Key in the settings sidebar!)*"
    )
