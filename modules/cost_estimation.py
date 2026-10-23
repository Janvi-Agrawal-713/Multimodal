"""
Module C: Construction Planning & Cost Estimation
Implements transparent civil engineering cost estimation, material heuristics,
completion progress tracking, and Indian numbering/currency formatting.
"""

from typing import Dict, Any, Optional
from utils.formatting import format_inr, format_inr_compact, format_number_inr

# Standard Structural Baseline Presets (per sq. ft. in INR)
STRUCTURE_PRESETS = {
    "Residential: Independent Villa / Duplex": {
        "base_rate": 1850.0,
        "steel_kg_per_sqft": 3.8,
        "cement_bags_per_sqft": 0.40,
        "sand_cft_per_sqft": 1.7,
        "aggregate_cft_per_sqft": 1.2,
        "description": "G+1 or G+2 framed residential structure with standard foundation."
    },
    "Residential: Multi-Storey Apartment (RCC Frame)": {
        "base_rate": 2200.0,
        "steel_kg_per_sqft": 4.5,
        "cement_bags_per_sqft": 0.44,
        "sand_cft_per_sqft": 1.9,
        "aggregate_cft_per_sqft": 1.35,
        "description": "Multi-floor RCC shear-wall / framed building with deep footings or raft."
    },
    "Commercial: Office / Retail Complex": {
        "base_rate": 2600.0,
        "steel_kg_per_sqft": 5.0,
        "cement_bags_per_sqft": 0.46,
        "sand_cft_per_sqft": 2.0,
        "aggregate_cft_per_sqft": 1.45,
        "description": "High ceiling commercial space with heavy live load and MEP provisions."
    },
    "Industrial: PEB Warehouse / Factory Shed": {
        "base_rate": 1450.0,
        "steel_kg_per_sqft": 3.2,
        "cement_bags_per_sqft": 0.30,
        "sand_cft_per_sqft": 1.4,
        "aggregate_cft_per_sqft": 1.1,
        "description": "Pre-Engineered Building with concrete plinth, industrial VDF flooring and steel truss."
    },
    "Institutional: School / Hospital / Clinic": {
        "base_rate": 2400.0,
        "steel_kg_per_sqft": 4.6,
        "cement_bags_per_sqft": 0.43,
        "sand_cft_per_sqft": 1.85,
        "aggregate_cft_per_sqft": 1.3,
        "description": "Institutional building with wide corridors, heavy structural specs and specialized MEP."
    }
}

# City/Location Cost Indices (Relative to National Baseline)
CITY_TIER_MULTIPLIERS = {
    "Tier 1 Metro (Mumbai, Delhi-NCR, Bengaluru, Hyderabad, Chennai, Kolkata)": {
        "multiplier": 1.25,
        "tier_name": "Tier 1 Metro",
        "description": "High labor wages, strict transit regulations, higher logistics and compliance overhead."
    },
    "Tier 2 Urban (Pune, Ahmedabad, Jaipur, Lucknow, Kochi, Chandigarh, Surat)": {
        "multiplier": 1.05,
        "tier_name": "Tier 2 Urban",
        "description": "Balanced material availability and competitive skilled labor rates."
    },
    "Tier 3 / Semi-Urban / Rural": {
        "multiplier": 0.90,
        "tier_name": "Tier 3 / Rural",
        "description": "Lower local labor costs, though specialized materials may incur transport premiums."
    }
}

# Finishing Quality Multipliers
FINISHING_LEVELS = {
    "Standard": {
        "multiplier": 1.00,
        "description": "Ceramic tiles, standard CP fittings, emulsion paints, flush doors."
    },
    "Premium": {
        "multiplier": 1.20,
        "description": "Vitrified tiles, branded sanitaryware (Kohler/Jaquar), weather-shield paints, teak veneer doors."
    },
    "Luxury": {
        "multiplier": 1.55,
        "description": "Italian marble flooring, VRV air conditioning, automated smart lighting, high-end imported fixtures."
    }
}

# Construction Milestone Stages
MILESTONE_STAGES = [
    (0, 10, "Substructure: Excavation, Anti-termite, PCC & Raft/Isolated Footings"),
    (11, 25, "Plinth & RCC Columns: Plinth beam casting, backfilling, column casting"),
    (26, 45, "Superstructure: RCC Slab casting, beams, staircases"),
    (46, 65, "Masonry & Plastering: AAC Blockwork / Brickwork, internal & external plaster"),
    (66, 80, "Services & MEP: Electrical conduiting, plumbing lines, HVAC rough-ins"),
    (81, 92, "Finishing: Flooring, wall putty, prime paint, door/window frames"),
    (93, 100, "Final Polish: Final paint coats, sanitary/electrical fixtures, testing, snagging & handover")
]


def get_current_stage(completion_pct: float) -> str:
    """Determine the physical construction stage for a given completion percentage."""
    pct = max(0.0, min(100.0, float(completion_pct)))
    for min_pct, max_pct, stage_name in MILESTONE_STAGES:
        if min_pct <= pct <= max_pct:
            return stage_name
    return "Project Commissioned and Handed Over"


def calculate_project_estimate(
    structure_type: str,
    built_up_area_sqft: float,
    city_tier: str,
    completion_pct: float,
    finishing_level: str = "Standard",
    custom_base_rate: Optional[float] = None,
    cement_bag_price: float = 380.0,
    steel_kg_price: float = 68.0,
    sand_cft_price: float = 55.0,
    aggregate_cft_price: float = 42.0
) -> Dict[str, Any]:
    """
    Compute comprehensive project cost, incurred expenditure, remaining budget,
    and material quantity heuristics.
    """
    if built_up_area_sqft <= 0:
        raise ValueError("Built-up area must be greater than zero.")
    
    completion_pct = max(0.0, min(100.0, float(completion_pct)))
    
    preset = STRUCTURE_PRESETS.get(structure_type, STRUCTURE_PRESETS["Residential: Independent Villa / Duplex"])
    tier_info = CITY_TIER_MULTIPLIERS.get(city_tier, CITY_TIER_MULTIPLIERS["Tier 2 Urban (Pune, Ahmedabad, Jaipur, Lucknow, Kochi, Chandigarh, Surat)"])
    finishing_info = FINISHING_LEVELS.get(finishing_level, FINISHING_LEVELS["Standard"])
    
    # Determine base rate (user override or preset)
    effective_base_rate = float(custom_base_rate) if custom_base_rate and custom_base_rate > 0 else preset["base_rate"]
    
    # Effective rate per sq ft considering location and finish
    effective_rate_per_sqft = effective_base_rate * tier_info["multiplier"] * finishing_info["multiplier"]
    
    # Total Project Cost
    total_project_cost = built_up_area_sqft * effective_rate_per_sqft
    
    # Incurred Expenditure & Remaining Budget
    incurred_expenditure = total_project_cost * (completion_pct / 100.0)
    remaining_budget = total_project_cost - incurred_expenditure
    
    # Stage description
    current_stage = get_current_stage(completion_pct)
    
    # Cost Breakdown by Trade (Standard industry rule of thumb)
    # Civil Structure (52%), Finishes (22%), MEP (16%), Approvals & Contingency (10%)
    cost_breakdown = {
        "Civil & Structural Works": {
            "percentage": 52.0,
            "amount": total_project_cost * 0.52,
            "description": "Earthwork, concrete, rebar, shuttering, masonry, and plastering."
        },
        "Architectural Finishes": {
            "percentage": 22.0,
            "amount": total_project_cost * 0.22,
            "description": "Flooring, wall finishes, paint, doors, windows, and waterproofing."
        },
        "MEP Services (Mechanical, Electrical, Plumbing)": {
            "percentage": 16.0,
            "amount": total_project_cost * 0.16,
            "description": "Conduits, wiring, switches, drainage, supply pipes, sanitary fixtures."
        },
        "Management, Approvals & Contingency": {
            "percentage": 10.0,
            "amount": total_project_cost * 0.10,
            "description": "Municipal sanction fees, site supervision, insurance, unforeseen contingencies."
        }
    }
    
    # Material Heuristics (based on IS thumb rules)
    cement_bags = built_up_area_sqft * preset["cement_bags_per_sqft"]
    cement_cost = cement_bags * cement_bag_price
    
    steel_kg = built_up_area_sqft * preset["steel_kg_per_sqft"]
    steel_tonnes = steel_kg / 1000.0
    steel_cost = steel_kg * steel_kg_price
    
    sand_cft = built_up_area_sqft * preset["sand_cft_per_sqft"]
    sand_cost = sand_cft * sand_cft_price
    
    aggregate_cft = built_up_area_sqft * preset["aggregate_cft_per_sqft"]
    aggregate_cost = aggregate_cft * aggregate_cft_price
    
    # Format strings for Indian presentation
    return {
        "project_metadata": {
            "structure_type": structure_type,
            "built_up_area_sqft": built_up_area_sqft,
            "city_tier": tier_info["tier_name"],
            "finishing_level": finishing_level,
            "completion_percentage": completion_pct,
            "current_stage": current_stage
        },
        "rates_applied": {
            "base_rate_per_sqft": effective_base_rate,
            "location_multiplier": tier_info["multiplier"],
            "finishing_multiplier": finishing_info["multiplier"],
            "effective_rate_per_sqft": round(effective_rate_per_sqft, 2),
            "cement_bag_price": cement_bag_price,
            "steel_kg_price": steel_kg_price
        },
        "financial_summary": {
            "total_estimated_cost": round(total_project_cost, 2),
            "total_cost_formatted": format_inr(total_project_cost),
            "total_cost_compact": format_inr_compact(total_project_cost),
            "incurred_expenditure": round(incurred_expenditure, 2),
            "incurred_formatted": format_inr(incurred_expenditure),
            "incurred_compact": format_inr_compact(incurred_expenditure),
            "remaining_budget": round(remaining_budget, 2),
            "remaining_formatted": format_inr(remaining_budget),
            "remaining_compact": format_inr_compact(remaining_budget),
            "currency": "INR (₹)"
        },
        "cost_breakdown": {
            k: {
                "percentage": v["percentage"],
                "amount": round(v["amount"], 2),
                "amount_formatted": format_inr(v["amount"]),
                "amount_compact": format_inr_compact(v["amount"]),
                "description": v["description"]
            }
            for k, v in cost_breakdown.items()
        },
        "material_estimates": {
            "cement": {
                "quantity_bags": round(cement_bags, 1),
                "unit": "Bags (50 kg)",
                "rate_per_unit": cement_bag_price,
                "total_cost": round(cement_cost, 2),
                "total_cost_formatted": format_inr(cement_cost),
                "assumption_note": f"Estimated at ~{preset['cement_bags_per_sqft']} bags/sq.ft. for {structure_type}"
            },
            "steel_rebar": {
                "quantity_kg": round(steel_kg, 1),
                "quantity_metric_tonnes": round(steel_tonnes, 2),
                "unit": "Metric Tonnes (MT)",
                "rate_per_kg": steel_kg_price,
                "total_cost": round(steel_cost, 2),
                "total_cost_formatted": format_inr(steel_cost),
                "assumption_note": f"Estimated at ~{preset['steel_kg_per_sqft']} kg/sq.ft. (Fe 500D TMT bars)"
            },
            "fine_aggregate_sand": {
                "quantity_cft": round(sand_cft, 1),
                "unit": "Cubic Feet (cft)",
                "rate_per_cft": sand_cft_price,
                "total_cost": round(sand_cost, 2),
                "total_cost_formatted": format_inr(sand_cost),
                "assumption_note": f"Estimated at ~{preset['sand_cft_per_sqft']} cft/sq.ft. (Zone II / M-Sand)"
            },
            "coarse_aggregate": {
                "quantity_cft": round(aggregate_cft, 1),
                "unit": "Cubic Feet (cft)",
                "rate_per_cft": aggregate_cft_price,
                "total_cost": round(aggregate_cost, 2),
                "total_cost_formatted": format_inr(aggregate_cost),
                "assumption_note": f"Estimated at ~{preset['aggregate_cft_per_sqft']} cft/sq.ft. (10mm/20mm crushed stone)"
            }
        },
        "assumptions_disclaimer": (
            "All estimates are illustrative based on standard Indian civil engineering empirical heuristics (CPWD & NBC guidelines). "
            "Actual material quantities and contractor bids will vary depending on soil strata, structural engineer designs, "
            "seismic zone, and market price fluctuations."
        )
    }
