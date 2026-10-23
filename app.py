"""
Multimodal Construction Intelligence Platform
Capstone Project for Skill Wallet Vibe Coding
Author: Senior Full-Stack AI Engineer
"""

import os
import json
import io
import datetime
from PIL import Image
import streamlit as st
import pandas as pd

# Core Engine Modules
from modules.gemini_service import (
    resolve_api_key,
    is_live_ai_available,
    chat_with_gemini
)
from modules.safety_audit import (
    audit_construction_site_image
)
from modules.crack_diagnostics import (
    diagnose_concrete_image,
    STRUCTURAL_ENGINEERING_DISCLAIMER,
    CRACK_MEASUREMENT_LIMITATION
)
from modules.cost_estimation import (
    STRUCTURE_PRESETS,
    CITY_TIER_MULTIPLIERS,
    FINISHING_LEVELS,
    calculate_project_estimate
)
from modules.weather_assistant import (
    WEATHER_CONDITIONS,
    get_weather_details,
    query_offline_assistant
)
from modules.report_generator import (
    build_consolidated_report,
    export_report_to_json_string
)
from utils.formatting import format_inr, format_inr_compact

# Page Configuration
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Construction Theme
st.markdown("""
<style>
    /* Industrial Construction Theme Enhancements */
    .main-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-left: 6px solid #F59E0B;
        padding: 22px 26px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    }
    .main-title {
        color: #F8FAFC;
        font-size: 26px;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .main-subtitle {
        color: #94A3B8;
        font-size: 14px;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 10px;
    }
    .status-live {
        background-color: #064E3B;
        color: #34D399;
        border: 1px solid #059669;
    }
    .status-demo {
        background-color: #451A03;
        color: #FBBF24;
        border: 1px solid #D97706;
    }
    .metric-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    .metric-val {
        font-size: 24px;
        font-weight: 700;
        color: #F59E0B;
        margin: 4px 0;
    }
    .metric-lbl {
        font-size: 13px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .disclaimer-box {
        background-color: #450A0A;
        border: 1px solid #991B1B;
        border-left: 5px solid #EF4444;
        border-radius: 8px;
        padding: 14px 18px;
        color: #FECACA;
        font-size: 13.5px;
        line-height: 1.5;
        margin: 16px 0;
    }
    .notice-box {
        background-color: #172554;
        border: 1px solid #1E40AF;
        border-left: 5px solid #3B82F6;
        border-radius: 8px;
        padding: 12px 16px;
        color: #BFDBFE;
        font-size: 13.5px;
        margin: 14px 0;
    }
    .demo-ribbon {
        background: #78350F;
        color: #FEF3C7;
        font-size: 12px;
        padding: 6px 12px;
        border-radius: 6px;
        border: 1px dashed #F59E0B;
        margin-bottom: 15px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "api_key" not in st.session_state:
    st.session_state.api_key = os.environ.get("GEMINI_API_KEY", "")
if "safety_result" not in st.session_state:
    st.session_state.safety_result = None
if "crack_result" not in st.session_state:
    st.session_state.crack_result = None
if "cost_result" not in st.session_state:
    st.session_state.cost_result = None
if "weather_condition" not in st.session_state:
    st.session_state.weather_condition = "Normal / Clear Weather"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "project_name" not in st.session_state:
    st.session_state.project_name = "Project Horizon - Commercial Tower Site A"

# Sidebar Configuration
with st.sidebar:
    st.markdown("## 🏗️ Platform Control")
    st.markdown("---")
    
    # Navigation Radio
    selected_page = st.radio(
        "Navigation",
        [
            "🏢 Executive Dashboard",
            "🦺 Module A: Safety & PPE Audit",
            "🔍 Module B: Concrete Crack Diagnostics",
            "📊 Module C: Planning & Cost Estimation",
            "⛅ Module D: Weather-Aware Site Assistant",
            "📑 Module E: Consolidated Reports & Export"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Gemini AI Vision Config")
    user_key_input = st.text_input(
        "Gemini API Key (Optional)",
        value=st.session_state.api_key,
        type="password",
        placeholder="AIzaSy...",
        help="Paste a Google Gemini API Key from Google AI Studio. If left blank, the app runs smoothly in Full Interactive Demo Mode with synthetic analysis."
    )
    if user_key_input != st.session_state.api_key:
        st.session_state.api_key = user_key_input
        st.rerun()

    active_key = resolve_api_key(st.session_state.api_key)
    has_live_ai = is_live_ai_available(active_key)
    
    if has_live_ai:
        st.success("🟢 Gemini Live AI Active")
    else:
        st.warning("🟡 Interactive Demo Mode (Synthetic Analysis)")
        st.caption("No valid API key detected. All modules remain 100% testable and functional with clearly labeled synthetic demo data.")

    st.markdown("---")
    st.markdown("### 📋 Active Project")
    st.session_state.project_name = st.text_input(
        "Project Identifier",
        value=st.session_state.project_name
    )
    
    st.caption("Capstone Project • Multimodal Construction Intelligence • Streamlit + Gemini")


# Top Header Banner
has_live_ai = is_live_ai_available(st.session_state.api_key)
status_html = (
    '<span class="status-badge status-live">🟢 Gemini Live AI Active</span>'
    if has_live_ai else
    '<span class="status-badge status-demo">🟡 Interactive Demo Mode (Simulated AI)</span>'
)

st.markdown(f"""
<div class="main-header">
    <div class="main-title">
        <span>🏗️</span> Multimodal Construction Intelligence Platform
    </div>
    <p class="main-subtitle">
        AI-Powered Construction Site Safety Audit • Structural Crack Diagnostics • Cost Engineering • Weather Advisory
    </p>
    {status_html}
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# PAGE 1: EXECUTIVE DASHBOARD
# ==============================================================================
if selected_page == "🏢 Executive Dashboard":
    st.markdown("### 📋 Executive Project Dashboard")
    st.markdown(f"**Current Site:** `{st.session_state.project_name}`")
    
    # 4 Quick Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        score_display = f"{st.session_state.safety_result['safety_score']}/100" if st.session_state.safety_result else "Pending"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">🦺 Safety Audit Score</div>
            <div class="metric-val">{score_display}</div>
            <small>{st.session_state.safety_result.get('score_rating', 'Audit not conducted') if st.session_state.safety_result else 'Upload site photo'}</small>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        crack_display = st.session_state.crack_result.get("estimated_severity", "None") if st.session_state.crack_result else "Pending"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">🔍 Concrete Defect Risk</div>
            <div class="metric-val">{crack_display}</div>
            <small>{st.session_state.crack_result.get('category', 'Diagnostics pending') if st.session_state.crack_result else 'Upload concrete photo'}</small>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        budget_display = st.session_state.cost_result.get("financial_summary", {}).get("total_cost_compact", "Pending") if st.session_state.cost_result else "Pending"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">📊 Total Project Budget</div>
            <div class="metric-val">{budget_display}</div>
            <small>{st.session_state.cost_result.get('project_metadata', {}).get('current_stage', 'Estimate not computed') if st.session_state.cost_result else 'Configure parameters'}</small>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        weather_info = get_weather_details(st.session_state.weather_condition)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">⛅ Weather Protocol</div>
            <div class="metric-val">{weather_info['icon']} {weather_info['risk_level']}</div>
            <small>{weather_info['selected_condition']}</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Modules Architecture Grid
    st.markdown("#### 🚀 Capstone Modules Overview")
    g1, g2 = st.columns(2)
    with g1:
        with st.container(border=True):
            st.markdown("#### 🦺 Module A: Construction Site Safety & PPE Audit")
            st.write(
                "Automated computer vision audit inspecting hard hats, high-vis vests, steel-toed boots, "
                "and safety harnesses. Calculates a 0-100 safety compliance score, flags OSHA/IS 13416 hazards, "
                "and suggests actionable site rectifications."
            )
            st.markdown("- **Input:** JPG / PNG Site Photographs")
            st.markdown("- **Outputs:** Safety Score, PPE Compliance %, Hazard Register, JSON Audit Report")
            
        with st.container(border=True):
            st.markdown("#### 📊 Module C: Planning & Cost Estimation")
            st.write(
                "Transparent civil engineering cost engine configured for the Indian construction ecosystem. "
                "Calculates total budget, incurred expense, remaining funds, and material estimates "
                "(cement bags, steel metric tonnes, sand, aggregate) formatted in Lakhs (L) and Crores (Cr)."
            )
            st.markdown("- **Inputs:** Structure type, sq.ft. area, city tier, completion %")
            st.markdown("- **Outputs:** Indian INR financial breakdown, milestone stage, material heuristics")

    with g2:
        with st.container(border=True):
            st.markdown("#### 🔍 Module B: Concrete Crack Diagnostics")
            st.write(
                "Visual surface screening identifying hairline shrinkage, structural shear, thermal stress, "
                "and settlement fissures. Features mandatory structural engineering disclaimers and explains "
                "measurement scale boundaries for safe AI usage."
            )
            st.markdown("- **Input:** JPG / PNG Concrete or Wall Surface Photographs")
            st.markdown("- **Outputs:** Defect Category, Probable Causes, Severity/Urgency, NDT Testing Next Steps")

        with st.container(border=True):
            st.markdown("#### ⛅ Module D: Weather-Aware Site Assistant")
            st.write(
                "Adverse weather protocol generator and construction engineering chatbot. Formulates safety rules "
                "for heavy rain, high winds (>40 km/h), and extreme heat (>40°C), adhering to IS 456 concrete and crane limits."
            )
            st.markdown("- **Inputs:** Selectable weather scenarios & engineering questions")
            st.markdown("- **Outputs:** Stoppage rules, hydration guidelines, offline/online assistant answers")

    st.info(
        "💡 **Evaluator Quick Start:** You can test each module immediately using either your own images or "
        "the **'Load Sample Demonstration Image'** buttons included in Modules A and B. No external API key is strictly required!"
    )


# ==============================================================================
# PAGE 2: MODULE A - SAFETY & PPE AUDIT
# ==============================================================================
elif selected_page == "🦺 Module A: Safety & PPE Audit":
    st.markdown("### 🦺 Module A: Construction Site Safety & PPE Audit")
    st.write("Upload construction site photography to evaluate worker PPE compliance and detect critical hazards.")
    
    col_upload, col_preview = st.columns([1, 1])
    
    image_to_analyze = None
    image_source_name = ""
    
    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload Construction Site Image (JPG / PNG)",
            type=["jpg", "jpeg", "png"],
            key="safety_upload"
        )
        
        sample_path = os.path.join(os.path.dirname(__file__), "sample_data", "sample_construction_site.jpg")
        if os.path.exists(sample_path):
            if st.button("📁 Load Built-in Sample Site Photo", use_container_width=True):
                uploaded_file = None
                image_to_analyze = Image.open(sample_path)
                image_source_name = "sample_construction_site.jpg"
                st.session_state.current_safety_img = image_to_analyze
                st.session_state.current_safety_name = image_source_name
        
        if uploaded_file is not None:
            image_to_analyze = Image.open(uploaded_file)
            image_source_name = uploaded_file.name
            st.session_state.current_safety_img = image_to_analyze
            st.session_state.current_safety_name = image_source_name
        elif "current_safety_img" in st.session_state and st.session_state.current_safety_img:
            image_to_analyze = st.session_state.current_safety_img
            image_source_name = st.session_state.current_safety_name
            
        btn_audit = st.button("🚀 Run Safety & PPE Audit", type="primary", use_container_width=True, disabled=(image_to_analyze is None))
        
    with col_preview:
        if image_to_analyze is not None:
            st.image(image_to_analyze, caption=f"Selected Image: {image_source_name}", use_container_width=True)
        else:
            st.markdown(
                """
                <div style="border: 2px dashed #475569; padding: 40px; text-align: center; border-radius: 8px; color: #94A3B8;">
                    📷 Please upload an image or click <b>'Load Built-in Sample Site Photo'</b> to proceed.
                </div>
                """,
                unsafe_allow_html=True
            )

    if btn_audit and image_to_analyze is not None:
        with st.spinner("Analyzing site safety and PPE compliance..."):
            result = audit_construction_site_image(
                image=image_to_analyze,
                filename=image_source_name,
                user_api_key=st.session_state.api_key
            )
            st.session_state.safety_result = result
            st.success("Safety audit complete!")

    # Display Results
    if st.session_state.safety_result:
        res = st.session_state.safety_result
        st.markdown("---")
        st.markdown("### 📋 Site Safety Audit Findings")
        
        # Demo Ribbon if demo mode
        if res.get("is_demo_mode", False):
            st.markdown(f'<div class="demo-ribbon">{res.get("demo_notice")}</div>', unsafe_allow_html=True)
            
        # Top Metrics
        m1, m2, m3, m4 = st.columns(4)
        score = res.get("safety_score", 0)
        with m1:
            st.metric("Safety Compliance Score", f"{score} / 100", delta=f"{res.get('score_rating', 'Rating')}")
        with m2:
            st.metric("Workers Observed", f"{res.get('estimated_workers_visible', 'N/A')}")
        with m3:
            hazards_count = len(res.get("detected_hazards", []))
            st.metric("Hazards Flagged", f"{hazards_count}", delta=f"{'Action Needed' if hazards_count > 0 else 'Clean'}", delta_color="inverse")
        with m4:
            st.metric("Site Housekeeping", f"{res.get('site_cleanliness_housekeeping', 'Satisfactory')}")

        st.progress(min(1.0, max(0.0, score / 100.0)), text=f"Overall Site Safety Index: {score}%")
        
        # Summary Box
        st.markdown(f"**Executive Summary:** {res.get('audit_summary', 'Audit conducted.')}")
        
        # PPE Compliance Breakdown
        st.markdown("#### 🦺 PPE Compliance Breakdown")
        ppe = res.get("ppe_compliance", {})
        p_cols = st.columns(4)
        
        ppe_items = [
            ("Helmets / Hard Hats", ppe.get("helmets", {})),
            ("High-Vis Vests", ppe.get("high_visibility_vests", {})),
            ("Safety Boots", ppe.get("safety_footwear", {})),
            ("Harnesses / Fall Arrest", ppe.get("safety_harnesses", {}))
        ]
        
        for idx, (label, data) in enumerate(ppe_items):
            with p_cols[idx]:
                with st.container(border=True):
                    status = data.get("status", "Unknown")
                    pct = data.get("compliance_rate_percent", 0)
                    st.markdown(f"**{label}**")
                    st.caption(f"Status: **{status}** ({pct}%)")
                    st.write(data.get("observed", "No specific details recorded."))
        
        # Detected Hazards Table
        st.markdown("#### ⚠️ Detected Site Hazards & Corrective Measures")
        hazards = res.get("detected_hazards", [])
        if hazards:
            hazard_rows = []
            for h in hazards:
                hazard_rows.append({
                    "Hazard ID": h.get("id", "HAZ"),
                    "Hazard Description": h.get("hazard_title", ""),
                    "Severity": h.get("severity", "Medium"),
                    "Location": h.get("location", ""),
                    "Standard Reference": h.get("standard_reference", "IS 13416 / OSHA"),
                    "Action Required": h.get("corrective_measure", "")
                })
            df_hazards = pd.DataFrame(hazard_rows)
            st.dataframe(df_hazards, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No critical hazards detected in the submitted photographic frame.")

        # Download Report Button
        st.markdown("<br>", unsafe_allow_html=True)
        json_report = json.dumps(res, indent=2)
        st.download_button(
            label="📥 Download Safety Audit Report (JSON)",
            data=json_report,
            file_name=f"safety_audit_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )


# ==============================================================================
# PAGE 3: MODULE B - CONCRETE CRACK DIAGNOSTICS
# ==============================================================================
elif selected_page == "🔍 Module B: Concrete Crack Diagnostics":
    st.markdown("### 🔍 Module B: Concrete Crack Diagnostics")
    st.write("Perform visual preliminary screening of concrete surfaces, walls, and structural elements.")
    
    # Prominent Structural Disclaimer Alert
    st.markdown(f"""
    <div class="disclaimer-box">
        {STRUCTURAL_ENGINEERING_DISCLAIMER}
    </div>
    """, unsafe_allow_html=True)
    
    col_upload_c, col_preview_c = st.columns([1, 1])
    
    crack_img = None
    crack_img_name = ""
    
    with col_upload_c:
        uploaded_crack = st.file_uploader(
            "Upload Concrete / Wall Image (JPG / PNG)",
            type=["jpg", "jpeg", "png"],
            key="crack_upload"
        )
        
        sample_crack_path = os.path.join(os.path.dirname(__file__), "sample_data", "sample_concrete_crack.jpg")
        if os.path.exists(sample_crack_path):
            if st.button("📁 Load Built-in Sample Crack Photo", use_container_width=True):
                uploaded_crack = None
                crack_img = Image.open(sample_crack_path)
                crack_img_name = "sample_concrete_crack.jpg"
                st.session_state.current_crack_img = crack_img
                st.session_state.current_crack_name = crack_img_name
                
        if uploaded_crack is not None:
            crack_img = Image.open(uploaded_crack)
            crack_img_name = uploaded_crack.name
            st.session_state.current_crack_img = crack_img
            st.session_state.current_crack_name = crack_img_name
        elif "current_crack_img" in st.session_state and st.session_state.current_crack_img:
            crack_img = st.session_state.current_crack_img
            crack_img_name = st.session_state.current_crack_name
            
        btn_diag = st.button("🔬 Diagnose Surface Defects", type="primary", use_container_width=True, disabled=(crack_img is None))
        
    with col_preview_c:
        if crack_img is not None:
            st.image(crack_img, caption=f"Selected Concrete Surface: {crack_img_name}", use_container_width=True)
        else:
            st.markdown(
                """
                <div style="border: 2px dashed #475569; padding: 40px; text-align: center; border-radius: 8px; color: #94A3B8;">
                    🧱 Upload a concrete surface photo or click <b>'Load Built-in Sample Crack Photo'</b> to analyze.
                </div>
                """,
                unsafe_allow_html=True
            )

    if btn_diag and crack_img is not None:
        with st.spinner("Analyzing concrete surface fracture patterns..."):
            result_c = diagnose_concrete_image(
                image=crack_img,
                filename=crack_img_name,
                user_api_key=st.session_state.api_key
            )
            st.session_state.crack_result = result_c
            st.success("Crack diagnostics completed!")

    # Display Crack Diagnostics Findings
    if st.session_state.crack_result:
        rc = st.session_state.crack_result
        st.markdown("---")
        st.markdown("### 🔬 Concrete Diagnostic Evaluation")
        
        if rc.get("is_demo_mode", False):
            st.markdown(f'<div class="demo-ribbon">{rc.get("demo_notice")}</div>', unsafe_allow_html=True)
            
        # Measurement Limitation Callout
        st.markdown(f"""
        <div class="notice-box">
            {CRACK_MEASUREMENT_LIMITATION}
        </div>
        """, unsafe_allow_html=True)
        
        # Diagnostic Metric Cards
        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            st.metric("Defect Category", rc.get("category", "Unspecified"))
        with dc2:
            st.metric("Estimated Severity", rc.get("estimated_severity", "Moderate"))
        with dc3:
            st.metric("Urgency Level", rc.get("urgency_level", "Routine"))

        with st.container(border=True):
            st.markdown(f"#### 🔍 Primary Defect: **{rc.get('defect_identified', 'Concrete Defect')}**")
            st.write(f"**Observed Characteristics:** {rc.get('visible_patterns', 'No pattern details recorded.')}")
            st.write(f"**Engineering Summary:** {rc.get('diagnostic_summary', 'Screening completed.')}")

        # Potential Causes & Associated Symptoms
        ca1, ca2 = st.columns(2)
        with ca1:
            with st.container(border=True):
                st.markdown("#### ⚡ Probable Root Causes")
                causes = rc.get("potential_causes", [])
                if causes:
                    for c in causes:
                        st.markdown(f"- {c}")
                else:
                    st.write("No root causes identified.")
        with ca2:
            with st.container(border=True):
                st.markdown("#### 🧪 Associated Visual Symptoms")
                symp = rc.get("associated_symptoms", [])
                if symp:
                    for s in symp:
                        st.markdown(f"- {s}")
                else:
                    st.write("No secondary chemical or moisture symptoms flagged.")

        # Recommended Next Steps
        st.markdown("#### 🛠️ Recommended Engineering Next Steps & NDT")
        steps = rc.get("recommended_next_steps", [])
        for idx, s in enumerate(steps, 1):
            st.markdown(f"**{idx}.** {s}")

        # Download Report
        st.markdown("<br>", unsafe_allow_html=True)
        json_crack = json.dumps(rc, indent=2)
        st.download_button(
            label="📥 Download Concrete Diagnostics Report (JSON)",
            data=json_crack,
            file_name=f"crack_diagnostics_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )


# ==============================================================================
# PAGE 4: MODULE C - PLANNING & COST ESTIMATION
# ==============================================================================
elif selected_page == "📊 Module C: Planning & Cost Estimation":
    st.markdown("### 📊 Module C: Construction Planning & Cost Estimation")
    st.write(
        "Civil engineering project budget forecasting, work completion expenditure, "
        "and material consumption heuristics with Indian currency formatting (Lakhs / Crores)."
    )
    
    with st.form("cost_estimation_form"):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            structure_choice = st.selectbox(
                "Structure Type",
                options=list(STRUCTURE_PRESETS.keys()),
                index=0
            )
            area_input = st.number_input(
                "Built-Up Area (in Square Feet)",
                min_value=100.0,
                max_value=2000000.0,
                value=3500.0,
                step=100.0,
                help="Total covered plinth area across all structural floors."
            )
            finishing_choice = st.selectbox(
                "Finishing & Specifications Level",
                options=list(FINISHING_LEVELS.keys()),
                index=0
            )

        with col_c2:
            city_tier_choice = st.selectbox(
                "Location / City Tier",
                options=list(CITY_TIER_MULTIPLIERS.keys()),
                index=1
            )
            completion_slider = st.slider(
                "Current Project Completion Percentage (%)",
                min_value=0,
                max_value=100,
                value=35,
                step=1,
                help="Physical progress of construction works on site."
            )
            
        with st.expander("🛠️ Advanced Cost Assumptions & Unit Rates (Customizable)"):
            c_r1, c_r2, c_r3, c_r4 = st.columns(4)
            preset_default = STRUCTURE_PRESETS[structure_choice]["base_rate"]
            with c_r1:
                custom_rate = st.number_input(
                    "Base Rate (₹/sq.ft)",
                    min_value=500.0,
                    max_value=25000.0,
                    value=float(preset_default),
                    step=50.0
                )
            with c_r2:
                cement_rate = st.number_input(
                    "Cement (₹/50kg bag)",
                    min_value=200.0,
                    max_value=1000.0,
                    value=380.0,
                    step=10.0
                )
            with c_r3:
                steel_rate = st.number_input(
                    "Steel TMT (₹/kg)",
                    min_value=40.0,
                    max_value=200.0,
                    value=68.0,
                    step=2.0
                )
            with c_r4:
                sand_rate = st.number_input(
                    "Sand (₹/cft)",
                    min_value=20.0,
                    max_value=150.0,
                    value=55.0,
                    step=5.0
                )

        btn_calculate = st.form_submit_button("📐 Compute Cost & Planning Model", type="primary", use_container_width=True)

    if btn_calculate or st.session_state.cost_result is None:
        est = calculate_project_estimate(
            structure_type=structure_choice,
            built_up_area_sqft=area_input,
            city_tier=city_tier_choice,
            completion_pct=completion_slider,
            finishing_level=finishing_choice,
            custom_base_rate=custom_rate,
            cement_bag_price=cement_rate,
            steel_kg_price=steel_rate,
            sand_cft_price=sand_rate
        )
        st.session_state.cost_result = est

    # Display Financial & Materials Model
    if st.session_state.cost_result:
        res_cost = st.session_state.cost_result
        fin = res_cost["financial_summary"]
        meta = res_cost["project_metadata"]
        
        st.markdown("---")
        st.markdown(f"### 💰 Financial Model — {meta['structure_type']}")
        st.caption(f"Active Milestone: **{meta['current_stage']}** ({meta['completion_percentage']}% Complete)")
        
        # 3 Big Metrics in Indian Currency
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            st.metric("Total Project Cost", fin["total_cost_compact"], help=f"Full Amount: {fin['total_cost_formatted']}")
        with fc2:
            st.metric("Incurred Expenditure", fin["incurred_compact"], help=f"Full Amount: {fin['incurred_formatted']}")
        with fc3:
            st.metric("Remaining Budget Required", fin["remaining_compact"], help=f"Full Amount: {fin['remaining_formatted']}")

        st.progress(meta["completion_percentage"] / 100.0, text=f"Work Completed: {meta['completion_percentage']}%")

        # Two Column Breakdown: Trade Costs & Material Heuristics
        b1, b2 = st.columns(2)
        with b1:
            st.markdown("#### 🏢 Cost Breakdown by Trade")
            bd = res_cost["cost_breakdown"]
            bd_rows = []
            for k, v in bd.items():
                bd_rows.append({
                    "Trade Category": k,
                    "Share (%)": f"{v['percentage']}%",
                    "Amount (Compact)": v["amount_compact"],
                    "Amount (Full ₹)": v["amount_formatted"]
                })
            df_bd = pd.DataFrame(bd_rows)
            st.dataframe(df_bd, use_container_width=True, hide_index=True)
            
            # Simple Matplotlib Bar Chart
            st.caption("Distribution across Structural, Finishes, MEP & Approvals")

        with b2:
            st.markdown("#### 🧱 Illustrative Material Quantities & Heuristics")
            mat = res_cost["material_estimates"]
            mat_rows = [
                {
                    "Material": "Cement (OPC/PPC)",
                    "Estimated Quantity": f"{mat['cement']['quantity_bags']:,} Bags",
                    "Approx Value": mat['cement']['total_cost_formatted'],
                    "Thumb Rule Basis": mat['cement']['assumption_note']
                },
                {
                    "Material": "Steel (TMT Fe 500D)",
                    "Estimated Quantity": f"{mat['steel_rebar']['quantity_metric_tonnes']:,} MT ({mat['steel_rebar']['quantity_kg']:,} kg)",
                    "Approx Value": mat['steel_rebar']['total_cost_formatted'],
                    "Thumb Rule Basis": mat['steel_rebar']['assumption_note']
                },
                {
                    "Material": "River/M-Sand",
                    "Estimated Quantity": f"{mat['fine_aggregate_sand']['quantity_cft']:,} cft",
                    "Approx Value": mat['fine_aggregate_sand']['total_cost_formatted'],
                    "Thumb Rule Basis": mat['fine_aggregate_sand']['assumption_note']
                },
                {
                    "Material": "Coarse Aggregate",
                    "Estimated Quantity": f"{mat['coarse_aggregate']['quantity_cft']:,} cft",
                    "Approx Value": mat['coarse_aggregate']['total_cost_formatted'],
                    "Thumb Rule Basis": mat['coarse_aggregate']['assumption_note']
                }
            ]
            df_mat = pd.DataFrame(mat_rows)
            st.dataframe(df_mat, use_container_width=True, hide_index=True)

        st.caption(f"📌 {res_cost['assumptions_disclaimer']}")

        # Download Cost JSON
        st.markdown("<br>", unsafe_allow_html=True)
        json_cost = json.dumps(res_cost, indent=2)
        st.download_button(
            label="📥 Download Cost Estimate Report (JSON)",
            data=json_cost,
            file_name=f"cost_estimate_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )


# ==============================================================================
# PAGE 5: MODULE D - WEATHER-AWARE SITE ASSISTANT
# ==============================================================================
elif selected_page == "⛅ Module D: Weather-Aware Site Assistant":
    st.markdown("### ⛅ Module D: Weather-Aware Site Assistant")
    st.write(
        "Weather-responsive construction safety protocols, high-risk work stoppage guidelines, "
        "and civil engineering Q&A assistant."
    )
    
    st.markdown("""
    <div class="notice-box">
        ℹ️ <b>DATA SOURCE NOTICE:</b> Weather conditions below are manually selected for site safety simulation and planning. Live automated weather station feeds are not connected.
    </div>
    """, unsafe_allow_html=True)
    
    # Weather Selector
    selected_weather = st.selectbox(
        "Select Simulated Weather Condition for Site",
        options=list(WEATHER_CONDITIONS.keys()),
        index=list(WEATHER_CONDITIONS.keys()).index(st.session_state.weather_condition)
    )
    st.session_state.weather_condition = selected_weather
    
    weather_info = get_weather_details(selected_weather)
    
    # Weather Alert Banner
    st.markdown(f"### {weather_info['icon']} {weather_info['alert_badge']}")
    st.write(f"**Operational Status:** {weather_info['work_status']}")
    st.write(f"**Summary:** {weather_info['summary']}")
    
    # Precautions Grid
    wc1, wc2 = st.columns([1, 1])
    with wc1:
        with st.container(border=True):
            st.markdown("#### 🚨 Mandatory Site Precautions")
            for p in weather_info["key_precautions"]:
                st.markdown(f"- {p}")
                
    with wc2:
        with st.container(border=True):
            st.markdown("#### 🏗️ Activity-Specific Safety Directives")
            for cat, rule in weather_info["category_rules"].items():
                st.markdown(f"**{cat}:** {rule}")

    st.markdown("---")
    st.markdown("### 💬 Construction Engineering Site Assistant")
    st.write("Ask questions regarding curing durations, formwork removal, IS codes, crane operations, or weather safety.")

    # Suggested Prompts
    st.markdown("##### Quick Inquiries:")
    quick_cols = st.columns(3)
    preset_q = ""
    with quick_cols[0]:
        if st.button("🕒 When can slab formwork be removed?"):
            preset_q = "When can formwork and props under a concrete slab be removed as per IS 456?"
    with quick_cols[1]:
        if st.button("💨 Tower crane wind speed cutoff?"):
            preset_q = "What is the maximum wind speed cutoff for operating tower cranes safely?"
    with quick_cols[2]:
        if st.button("🌧️ Precautions for rain during concrete pour?"):
            preset_q = "What should be done if heavy rain starts during a concrete slab pour?"

    user_query = st.text_input(
        "Enter your construction question:",
        value=preset_q if preset_q else "",
        placeholder="e.g., What is the minimum curing period for OPC concrete in hot weather?"
    )

    if st.button("Ask Assistant", type="primary"):
        if user_query.strip():
            with st.spinner("Consulting construction engineering knowledge engine..."):
                active_key = resolve_api_key(st.session_state.api_key)
                if is_live_ai_available(active_key):
                    context = f"Weather Condition: {selected_weather}\nPrecautions: {', '.join(weather_info['key_precautions'])}"
                    success, reply = chat_with_gemini(user_query, context=context, user_api_key=active_key)
                    if not success:
                        reply = query_offline_assistant(user_query, selected_weather)
                else:
                    reply = query_offline_assistant(user_query, selected_weather)
                    
            st.session_state.chat_history.append((user_query, reply))

    # Display Chat History
    if st.session_state.chat_history:
        st.markdown("#### Consultation History")
        for q, a in reversed(st.session_state.chat_history[-5:]):
            with st.chat_message("user"):
                st.write(q)
            with st.chat_message("assistant"):
                st.markdown(a)


# ==============================================================================
# PAGE 6: MODULE E - CONSOLIDATED REPORTS & EXPORT
# ==============================================================================
elif selected_page == "📑 Module E: Consolidated Reports & Export":
    st.markdown("### 📑 Module E: Consolidated Platform Reports & Export")
    st.write("Compile all audit observations, crack diagnostics, financial estimates, and weather logs into a single master project report.")
    
    weather_info = get_weather_details(st.session_state.weather_condition)
    
    consolidated = build_consolidated_report(
        project_name=st.session_state.project_name,
        safety_audit_data=st.session_state.safety_result,
        crack_diagnostic_data=st.session_state.crack_result,
        cost_estimation_data=st.session_state.cost_result,
        weather_data=weather_info
    )
    
    # High Level Site Health Status
    health_status = consolidated["platform_metadata"]["overall_site_health_status"]
    if "Critical" in health_status:
        st.error(f"🚨 Overall Site Status: **{health_status}**")
    elif "Caution" in health_status or "Elevated" in health_status:
        st.warning(f"⚠️ Overall Site Status: **{health_status}**")
    else:
        st.success(f"✅ Overall Site Status: **{health_status}**")

    # Risk Factors Flagged
    st.markdown("#### 🚩 Flagged Risk Factors")
    for rf in consolidated["platform_metadata"]["flagged_risk_factors"]:
        st.markdown(f"- {rf}")
        
    # Module Completion Status Table
    st.markdown("#### 📊 Module Audit Status Summary")
    exec_sum = consolidated["executive_summary"]
    status_table = [
        {"Module": "Module A: Safety & PPE Audit", "Status": "Completed" if exec_sum["safety_audit_completed"] else "Not Run", "Key Finding": f"Score: {exec_sum['safety_score']}/100" if exec_sum['safety_score'] else "No photo analyzed"},
        {"Module": "Module B: Crack Diagnostics", "Status": "Completed" if exec_sum["crack_diagnostics_completed"] else "Not Run", "Key Finding": f"Category: {exec_sum['crack_defect_category']}" if exec_sum['crack_defect_category'] else "No crack photo analyzed"},
        {"Module": "Module C: Cost Estimation", "Status": "Completed" if exec_sum["cost_estimation_completed"] else "Not Run", "Key Finding": f"Budget: {exec_sum['total_budget_inr']}" if exec_sum['total_budget_inr'] else "Estimate pending"},
        {"Module": "Module D: Weather Protocol", "Status": "Configured", "Key Finding": f"Protocol: {exec_sum['weather_protocol_active']}"}
    ]
    st.dataframe(pd.DataFrame(status_table), use_container_width=True, hide_index=True)

    # Full Master JSON Download
    st.markdown("---")
    master_json_str = export_report_to_json_string(consolidated)
    
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        st.download_button(
            label="📥 Download Consolidated Project Audit Report (JSON)",
            data=master_json_str,
            file_name=f"consolidated_audit_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            type="primary",
            use_container_width=True
        )
    with col_d2:
        with st.expander("👁️ View Formatted JSON Report Payload"):
            st.json(consolidated)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Legal & Compliance Disclaimers:")
    for k, v in consolidated["legal_and_compliance_disclaimers"].items():
        st.caption(f"- **{k.replace('_', ' ').title()}:** {v}")
