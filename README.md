# 🏗️ Multimodal Construction Intelligence Platform
> **Skill Wallet Vibe Coding Capstone Project**  
> *AI-Powered Site Safety Audit • Concrete Diagnostics • Cost Engineering • Weather Advisory*

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google-Gemini%20API-4285F4.svg)](https://ai.google.dev/)
[![Tests Passing](https://img.shields.io/badge/Tests-19%20Passed-brightgreen.svg)]()

---

## 🌟 Overview

The **Multimodal Construction Intelligence Platform** is an enterprise-grade, beginner-friendly web application engineered to address primary pain points in modern civil infrastructure and construction management:
1. **Accident Prevention & PPE Enforcement:** Visual monitoring of personal protective equipment (PPE) and environmental site hazards.
2. **Structural Health Diagnostics:** Preliminary image screening of concrete cracks, spalling, and surface defects with forensic civil engineering guidelines.
3. **Transparent Financial & Material Estimation:** Cost estimation and material quantity heuristics (cement, steel, aggregates) tailored to Indian market indices with Indian numbering (`₹ Lakhs` & `₹ Crores`).
4. **Weather-Resilient Operations:** Safety stoppage protocols and advisory assistance for extreme rain, wind gusts (>40 km/h), and heatwaves (>40°C).
5. **Consolidated Auditing:** Single-click JSON compliance and risk reporting across all project modules.

---

## 🏗️ Architecture & Project Structure

The project adheres to a clean, modular architecture:

```text
multimodal-construction-platform/
│
├── app.py                          # Main Streamlit web application & unified dashboard
├── requirements.txt                # Production and development dependencies
├── README.md                       # Comprehensive documentation & deployment guide
├── .gitignore                      # Git exclusion rules (secrets, venv, pycache)
│
├── .streamlit/
│   └── config.toml                 # Construction industrial theme & server settings
│
├── modules/
│   ├── __init__.py
│   ├── gemini_service.py           # Gemini Multimodal API client & robust JSON parser
│   ├── safety_audit.py             # Module A: Safety scoring, PPE audit & hazard detection
│   ├── crack_diagnostics.py        # Module B: Concrete defect diagnostics & disclaimers
│   ├── cost_estimation.py          # Module C: Indian cost engine & material heuristics
│   ├── weather_assistant.py        # Module D: Weather protocols & civil Q&A assistant
│   └── report_generator.py         # Module E: Consolidated JSON audit report generator
│
├── utils/
│   ├── __init__.py
│   └── formatting.py               # Indian currency formatting (Lakhs/Crores, ₹)
│
├── sample_data/
│   ├── create_sample_images.py     # Script to generate sample photographic assets
│   ├── sample_construction_site.jpg # Built-in sample image for PPE audit
│   └── sample_concrete_crack.jpg    # Built-in sample image for crack diagnostics
│
└── tests/
    ├── __init__.py
    ├── test_formatting.py          # Unit tests for Indian numbering system
    ├── test_cost_estimation.py     # Tests for cost math, tiers, and materials
    ├── test_weather_assistant.py   # Tests for weather rules and knowledge engine
    ├── test_safety_audit.py        # Tests for safety score & PPE compliance logic
    ├── test_crack_diagnostics.py   # Tests for crack defect classification & disclaimers
    ├── test_gemini_service.py      # Tests for API key resolution & JSON extractors
    └── test_report_generator.py    # Tests for consolidated report assembly
```

---

## 🚀 Key Features by Module

### 🦺 Module A: Construction Site Safety & PPE Audit
- **Photographic Upload:** Supports standard `.jpg`, `.jpeg`, and `.png` site photos, or 1-click loading of bundled sample site photography.
- **PPE Verification:** Analyzes hard hats/helmets, high-visibility reflective vests, steel-toed boots, and safety harnesses.
- **Safety Scoring (0–100):** Evaluates compliance percentage and assigns health bands (*Critical Risk*, *Needs Attention*, *Good Compliance*, *Excellent*).
- **Hazard Register:** Flags specific site hazards with standard references (IS 13416 / OSHA 1926) and actionable corrective measures.
- **Export:** Instant download of `safety_audit.json`.
- **Demo Mode Transparency:** Clearly labels all synthetic evaluations with `[DEMO MODE]` badges when no API key is provided.

### 🔍 Module B: Concrete Crack Diagnostics
- **Surface Fracture Screening:** Evaluates cracks on walls, beams, columns, and slabs (shear cracks, shrinkage fissures, settlement cracks, spalling, efflorescence).
- **Engineering Categorization:** Separates *Structural Defects* from *Non-Structural / Surface Defects*.
- **Urgency & Severity:** Distinguishes immediate evacuation/shoring alerts from scheduled maintenance or routine 3-month monitoring.
- **Actionable Remediation:** Advises on Avongard tell-tale crack monitors, low-viscosity epoxy pressure injection, polyurethane elastomeric sealants, and Ultrasonic Pulse Velocity (UPV / IS 13311) testing.
- **Mandatory Structural Disclaimer:** Prominently states that visual analysis is a preliminary screening aid and is **not a substitute for assessment by a licensed civil/structural engineer**.
- **Measurement Limitation Notice:** Clarifies that precise millimeter crack width or subsurface depth **cannot be certified from 2D photos without a physical optical scale**.

### 📊 Module C: Construction Planning & Cost Estimation
- **Civil Engineering Model:** Parametric calculations for 5 structure categories (Villas, Multi-Storey Apartments, Commercial Offices, Industrial Warehouses, Institutional Buildings).
- **Location Multipliers:** Configured for Indian Metro (Tier 1: 1.25x), Urban (Tier 2: 1.05x), and Semi-Urban/Rural (Tier 3: 0.90x) markets.
- **Indian Number Formatting:** Seamless presentation in ₹ Lakhs (`₹ 45.00 Lakhs`) and ₹ Crores (`₹ 1.50 Cr`) using standard Indian comma separation (`₹ 1,23,45,678`).
- **Milestone Progress Tracking:** Automatically detects active construction stage (Substructure, Superstructure, Masonry, Finishing, Handover) based on completion percentage.
- **Transparent Material Heuristics:**
  - Cement bags: ~0.38 - 0.46 bags / sq.ft.
  - Steel rebar: ~3.2 - 5.0 kg / sq.ft. (Fe 500D TMT)
  - Sand / Aggregates: Cubic feet (cft) volume heuristics.
- **Editable Cost Rates:** Allows custom overrides for base rate per sq.ft., cement bag rates, and steel per-kg pricing.

### ⛅ Module D: Weather-Aware Site Assistant
- **Selectable Weather Scenarios:** Normal/Clear, Heavy Rain/Monsoon, High Wind (>40 km/h), Extreme Heat (>40°C).
- **Transparent Data Notice:** Explicitly indicates manual simulation mode (no fabricated live sensor feeds).
- **Operational Directives:** Concrete pour halting rules, tower crane cutoff limits (38–40 km/h), outrigger ground stability, trench dewatering, and worker hydration protocols (IS 456 / OSHA).
- **Engineering Q&A Assistant:** Dual-engine assistant combining Google Gemini Generative AI (live mode) and a built-in Indian Standards Knowledge Engine (IS 456, IS 13416, NBC 2016) in demo mode.

### 📑 Module E: Consolidated Reports & Export
- **Multi-Module Master Report:** Gathers audit scores, crack evaluations, financial models, and weather states into a single unified JSON document.
- **Overall Site Health Index:** Computes a composite site safety and structural risk status (*Satisfactory*, *Moderate Caution*, *Elevated Caution*, *Critical Alert*).
- **Compliance & Legal Disclaimers:** Incorporates formal civil engineering disclaimers in the downloadable payload.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9, 3.10, 3.11, or 3.12
- `pip` package manager

### 1. Clone or Open the Repository
```bash
cd C:\Users\LENOVO\.gemini\antigravity-ide\scratch\multimodal-construction-platform
```

### 2. Create and Activate a Virtual Environment (Recommended)
```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Gemini API Key Configuration (Optional)

The platform is designed to be **100% usable without an API key** in Interactive Demo Mode. To enable live multimodal computer vision analysis:

### Option A: Enter in the Streamlit Sidebar (Easiest)
Paste your key starting with `AIzaSy...` directly into the sidebar text field in the web app.

### Option B: Set an Environment Variable
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="AIzaSyYourActualKeyHere"

# Windows Command Prompt
set GEMINI_API_KEY=AIzaSyYourActualKeyHere

# Linux / macOS
export GEMINI_API_KEY="AIzaSyYourActualKeyHere"
```

### Option C: Use Streamlit Secrets
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "AIzaSyYourActualKeyHere"
```

*(Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/app/apikey).)*

---

## 💻 Running the Application

Launch the Streamlit web dashboard:
```bash
streamlit run app.py
```
The interface will automatically open in your default browser at `http://localhost:8501`.

---

## 🧪 Automated Testing

A comprehensive test suite of 19 automated tests verifies calculations, formatting, demo modes, and disclaimers.

Run tests using pytest:
```bash
pytest tests/
```

### Test Coverage Summary:
- `tests/test_formatting.py`: Validates Indian numbering, Lakhs, Crores, decimals, and thousands separation.
- `tests/test_cost_estimation.py`: Validates base rates, tier multipliers, progress milestone strings, material quantities, and error validation on invalid input.
- `tests/test_weather_assistant.py`: Validates all weather protocols, hazard rules, and offline knowledge assistant keyword matching.
- `tests/test_safety_audit.py`: Validates safety scoring, PPE compliance schema, hazard identification, and demo tags.
- `tests/test_crack_diagnostics.py`: Validates crack defect classifications, structural disclaimers, and measurement limitation statements.
- `tests/test_gemini_service.py`: Validates JSON extraction from raw strings and markdown code fences.
- `tests/test_report_generator.py`: Validates consolidated report construction and JSON serialization.

**Execution Result:**
```text
======================= 19 passed in 10.01s ========================
```

---

## 📦 Deploying to Streamlit Community Cloud (Free)

Follow these steps to deploy your project to the free Streamlit Community Cloud:

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Multimodal Construction Intelligence Platform"
git branch -M main
git remote add origin https://github.com/<your-username>/multimodal-construction-platform.git
git push -u origin main
```

### 2. Deploy on Streamlit Community Cloud
1. Sign in to [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
2. Click **"New app"**.
3. Select your repository: `<your-username>/multimodal-construction-platform`.
4. Branch: `main`.
5. Main file path: `app.py`.
6. (Optional) Under **Advanced settings -> Secrets**, add your Gemini API key:
   ```toml
   GEMINI_API_KEY = "AIzaSyYourKeyHere"
   ```
7. Click **"Deploy!"**. Your application will be live in 1-2 minutes with a public HTTPS URL.

---

## ⚖️ Engineering Disclaimers & Ethics

- **Structural Safety Notice:** This software provides preliminary computer-vision screening and algorithmic estimations for educational, research, and site-planning assistance. It does **not** constitute a certified structural audit or engineering sign-off.
- **Physical Scale Requirement:** Visual photography without physical reference targets cannot produce certified millimeter crack dimensions.
- **Weather Simulation Notice:** Weather scenarios are selected manually for simulation and do not represent a real-time IoT meteorological station.
- **Simulated Demo Data:** Any result generated without an active API key is clearly identified and watermarked as simulated demo data.

---

## 👨‍💻 Capstone Information
- **Project Name:** Multimodal Construction Intelligence Platform
- **Course / Requirement:** Skill Wallet Vibe Coding Capstone Project
- **Status:** Complete, Fully Functional, and Tested
