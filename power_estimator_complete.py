import streamlit as st
import pandas as pd
import json
from datetime import datetime
import math
import matplotlib.pyplot as plt

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Power Systems Cost Estimator v3.5",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ DARK THEME PREMIUM CSS DESIGN SYSTEM ============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

:root {
    --bg-primary: #0f1419;
    --bg-secondary: #1a2332;
    --bg-tertiary: #252d3d;
    --bg-hover: #2a3549;
    --primary: #2563eb;
    --primary-dark: #1e40af;
    --primary-light: #3b82f6;
    --text-primary: #e8eef5;
    --text-secondary: #a8b5c7;
    --text-tertiary: #7a8696;
    --border: #3a4556;
    --border-light: #2a3549;
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --info: #06b6d4;
}

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg-primary) !important;
    color: var(--text-primary);
    font-size: 14px;
    line-height: 1.6;
}

.main { background: var(--bg-primary) !important; padding-top: 0 !important; }
[data-testid="stMainBlockContainer"] { padding-top: 24px !important; background: var(--bg-primary) !important; }

.header-premium {
    position: sticky; top: 0; z-index: 999; background: var(--bg-secondary); border-bottom: 1px solid var(--border);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4); padding: 0 32px; display: flex; align-items: center; justify-content: space-between;
    height: 64px; margin-bottom: 24px;
}
.header-left { display: flex; align-items: center; gap: 12px; }
.header-icon { font-size: 24px; color: var(--primary-light); }
.header-title { font-size: 16px; font-weight: 600; color: var(--text-primary); margin: 0; }
.header-subtitle { font-size: 12px; color: var(--text-secondary); margin: 0; }
.header-right { display: flex; gap: 24px; align-items: center; }
.header-link { font-size: 12px; color: var(--text-secondary); text-decoration: none; font-weight: 500; transition: color 0.2s ease; }
.header-link:hover { color: var(--primary-light); }

.section-title { font-size: 14px; font-weight: 600; color: var(--text-primary); display: flex; align-items: center; gap: 8px; }
.section-icon { font-size: 16px; }

.card-premium {
    background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px;
    padding: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); margin-bottom: 24px; transition: all 0.3s ease;
}
.card-premium:hover { box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6); border-color: var(--primary-dark); background: var(--bg-tertiary); }

.card-premium-title {
    font-size: 14px; font-weight: 600; color: var(--text-primary); margin-bottom: 16px; display: flex; align-items: center; gap: 8px;
}

input[type="number"], input[type="text"], select, textarea, .stNumberInput > div > div > input, .stSelectbox > div > div > select {
    width: 100% !important; padding: 10px 12px !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; font-size: 14px !important; background: var(--bg-tertiary) !important;
    color: var(--text-primary) !important; font-family: inherit !important; transition: all 0.2s ease !important;
}
input[type="number"]:focus, input[type="text"]:focus, select:focus, textarea:focus {
    outline: none !important; border-color: var(--primary-light) !important; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2) !important;
}

.stButton > button {
    padding: 12px 20px !important; border-radius: 8px !important; font-weight: 600 !important;
    font-size: 14px !important; border: none !important; cursor: pointer !important; transition: all 0.2s ease !important;
    background: var(--primary-light) !important; color: white !important; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4) !important;
}
.stButton > button:hover { background: var(--primary) !important; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5) !important; }
.stButton > button:active { background: var(--primary-dark) !important; }

.stCheckbox > label { font-weight: 400 !important; font-size: 14px !important; display: flex; align-items: center; gap: 8px; color: var(--text-primary) !important; }

.streamlit-expanderHeader {
    background: var(--bg-tertiary) !important; border: 1px solid var(--border) !important; border-radius: 8px !important;
    padding: 12px !important; font-weight: 600 !important; color: var(--text-primary) !important;
}
.streamlit-expanderHeader:hover { background: var(--bg-hover) !important; border-color: var(--primary-dark) !important; }
.streamlit-expanderContent { border: 1px solid var(--border) !important; border-top: none !important; padding: 16px !important; background: var(--bg-secondary) !important; }

.stDataFrame th { background: var(--bg-tertiary) !important; color: var(--text-primary) !important; font-weight: 600 !important; padding: 12px !important; }
.stDataFrame td { padding: 12px !important; color: var(--text-primary) !important; background: var(--bg-secondary) !important; }
.stDataFrame tbody tr:nth-child(even) { background: var(--bg-tertiary) !important; }
.stDataFrame tbody tr:hover { background: var(--bg-hover) !important; }

.stMetric { background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px; padding: 16px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4); transition: all 0.3s ease; }
.stMetric:hover { border-color: var(--primary-dark); background: var(--bg-tertiary); }
.stMetricLabel { font-size: 12px !important; color: var(--text-secondary) !important; }
.stMetricValue { font-size: 18px !important; font-weight: 700 !important; color: var(--primary-light) !important; }

.highlight-total {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(59, 130, 246, 0.1) 100%);
    border: 2px solid var(--primary-light);
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
    text-align: center;
}

.highlight-total-value { font-size: 32px; font-weight: 700; color: var(--primary-light); font-family: 'IBM Plex Mono', monospace; margin: 10px 0; }
.highlight-total-label { font-size: 14px; color: var(--text-secondary); }

.section-divider { height: 1px; background: var(--border); margin: 20px 0; border: none; }

.notes-box {
    background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px;
    padding: 16px; margin-top: 12px;
}

.footer-premium {
    background: var(--bg-secondary); border-top: 1px solid var(--border);
    padding: 16px 32px; margin-top: 24px;
    text-align: center; font-size: 11px; color: var(--text-secondary);
}

.credits-box {
    background: var(--bg-tertiary); border-left: 4px solid var(--primary-light);
    border-radius: 8px; padding: 12px 16px; margin-top: 12px;
    font-size: 12px; color: var(--text-secondary);
}

@media (max-width: 767px) {
    .header-premium { padding: 0 16px; } .header-right { display: none; }
}
</style>
""", unsafe_allow_html=True)

# ============ CONSTANTS ============
MEETINGS_RATE = 800
MEETINGS_COUNT = 4
MEETINGS_HRS = 1.5
MODELLING_PERCENT = 0.30
MODELLING_RATE = 1200

PROJECT_FACTORS = {
    'Commercial': 0.85, 'Industrial': 1.10, 'Pharma': 1.20,
    'Hospital': 1.25, 'Metro/Infrastructure': 1.30, 'Oil & Gas': 1.40, 'Business Park': 0.80
}

VOLTAGE_FACTORS = {'11': 1.00, '33': 1.15, '66': 1.30, '132': 1.50, '220': 1.75}
REGION_FACTORS = {'Domestic': 1.00, 'SouthAsia': 1.05, 'SeAsia': 1.35, 'MiddleEast': 1.75, 'APAC': 1.55, 'Europe': 2.00}

DEFAULT_STUDIES = {
    'lf': {'name': 'Load Flow', 'baseHrs': 15, 'complexity': 1.0},
    'sc': {'name': 'Short Circuit', 'baseHrs': 18, 'complexity': 1.1},
    'pdc': {'name': 'Protection Coordination', 'baseHrs': 25, 'complexity': 1.3},
    'af': {'name': 'Arc Flash', 'baseHrs': 16, 'complexity': 1.0},
    'har': {'name': 'Harmonics', 'baseHrs': 22, 'complexity': 1.2},
    'ts': {'name': 'Transient Stability', 'baseHrs': 30, 'complexity': 1.4},
    'ms': {'name': 'Motor Starting', 'baseHrs': 18, 'complexity': 1.05}
}

DEFAULT_TEAM = {
    'L1': {'rate': 2400, 'allocation': 0.15},
    'L2': {'rate': 1200, 'allocation': 0.35},
    'L3': {'rate': 900, 'allocation': 0.50}
}

# ============ HELPER FUNCTIONS ============
def format_currency(amount):
    return f"₹{amount:,.0f}"

def format_number(num):
    return f"{num:,.1f}"

def create_pie_chart(labels, sizes, title, colors=None):
    """Create a pie chart"""
    if colors is None:
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4']
    
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#1a2332')
    ax.set_facecolor('#1a2332')
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    
    for text in texts:
        text.set_color('#e8eef5')
        text.set_fontsize(11)
        text.set_weight('bold')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_weight('bold')
    
    ax.set_title(title, color='#e8eef5', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    return fig

# ============ CALCULATE FUNCTION ============
def calculateAll(facility_mw, mv_buses, lv_buses, project_type, voltage, region,
                mw_exponent, bus_exponent, bus_confidence, buffer_percent,
                report_mode, report_percent, report_fixed, report_complexity,
                custom_studies, custom_team, selected_studies, custom_cost):
    
    total_buses = mv_buses + lv_buses
    mw_per_bus = facility_mw / total_buses
    
    mw_factor = pow(facility_mw / 10, mw_exponent)
    bus_factor = pow(total_buses / 32, bus_exponent)
    project_factor = PROJECT_FACTORS.get(project_type, 1.0)
    voltage_factor = VOLTAGE_FACTORS.get(voltage, 1.0)
    region_factor = REGION_FACTORS.get(region, 1.0)
    
    study_results = []
    total_study_hours = 0
    total_report_hours = 0
    total_study_cost = 0
    
    for code in selected_studies:
        if code not in DEFAULT_STUDIES:
            continue
        
        study = DEFAULT_STUDIES[code]
        base_hrs = custom_studies[code]['baseHrs']
        complexity = custom_studies[code]['complexity']
        
        adjusted_study_hrs = base_hrs * pow(total_buses / 32, bus_exponent) * pow(facility_mw / 10, mw_exponent)
        all_factors = project_factor * voltage_factor * region_factor * bus_confidence * complexity
        final_study_hrs = adjusted_study_hrs * all_factors
        
        l1_hours = final_study_hrs * custom_team['L1']['allocation']
        l2_hours = final_study_hrs * custom_team['L2']['allocation']
        l3_hours = final_study_hrs * custom_team['L3']['allocation']
        
        blended_rate = (l1_hours * custom_team['L1']['rate'] + 
                       l2_hours * custom_team['L2']['rate'] + 
                       l3_hours * custom_team['L3']['rate']) / final_study_hrs if final_study_hrs > 0 else 0
        
        study_cost = final_study_hrs * blended_rate
        
        report_hrs = 0
        if report_mode == "% of Study Cost":
            report_pct = report_percent / 100
            report_hrs = final_study_hrs * report_pct
        
        total_study_hours += final_study_hrs
        total_report_hours += report_hrs
        total_study_cost += study_cost
        
        study_results.append({
            'name': study['name'],
            'studyHrs': final_study_hrs,
            'reportHrs': report_hrs,
            'studyCost': study_cost,
            'reportCost': report_hrs * blended_rate * report_complexity
        })
    
    total_reporting_cost = 0
    if report_mode == "% of Study Cost":
        total_reporting_cost = total_report_hours * 1200 * report_complexity
    else:
        total_reporting_cost = report_fixed * (len(selected_studies) / 7)
    
    total_project_hours = total_study_hours + total_report_hours + (MEETINGS_COUNT * MEETINGS_HRS)
    meetings_cost = MEETINGS_COUNT * MEETINGS_HRS * MEETINGS_RATE
    modelling_hours = total_project_hours * MODELLING_PERCENT
    modelling_cost = modelling_hours * MODELLING_RATE
    
    subtotal = total_study_cost + total_reporting_cost + meetings_cost + modelling_cost + custom_cost
    buffer = subtotal * (buffer_percent / 100)
    grand_total = subtotal + buffer
    
    cost_per_bus = grand_total / total_buses if total_buses > 0 else 0
    
    return {
        'total_buses': total_buses,
        'mw_per_bus': mw_per_bus,
        'total_study_hours': total_study_hours,
        'total_report_hours': total_report_hours,
        'total_project_hours': total_project_hours,
        'modelling_hours': modelling_hours,
        'total_study_cost': total_study_cost,
        'total_reporting_cost': total_reporting_cost,
        'meetings_cost': meetings_cost,
        'modelling_cost': modelling_cost,
        'custom_cost': custom_cost,
        'subtotal': subtotal,
        'buffer': buffer,
        'grand_total': grand_total,
        'cost_per_bus': cost_per_bus,
        'study_results': study_results
    }

# ============ HEADER ============
st.markdown("""
<div class="header-premium">
    <div class="header-left">
        <div class="header-icon">⚡</div>
        <div>
            <div class="header-title">Power Systems</div>
            <div class="header-subtitle">Cost Estimator v3.5</div>
        </div>
    </div>
    <div class="header-right">
        <a href="#" class="header-link">Documentation</a>
        <a href="#" class="header-link">Settings</a>
        <a href="#" class="header-link">Help</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ============ SESSION STATE ============
if 'custom_studies' not in st.session_state:
    st.session_state.custom_studies = {code: {'baseHrs': study['baseHrs'], 'complexity': study['complexity']} 
                                       for code, study in DEFAULT_STUDIES.items()}
if 'custom_team' not in st.session_state:
    st.session_state.custom_team = DEFAULT_TEAM.copy()

# ============ MAIN CONTENT ============
# SECTION 1: PROJECT BASICS
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="card-premium"><div class="card-premium-title"><span class="section-icon">📋</span> Project Basics</div>', unsafe_allow_html=True)
    
    project_name = st.text_input("Project Name", value="Project-Alpha", placeholder="Enter project name")
    
    facility_mw = st.number_input("Facility Capacity (MW)", value=10.0, min_value=0.5, max_value=500.0, step=0.5)
    col1, col2 = st.columns(2)
    with col1:
        mv_buses = st.number_input("MV Buses", value=24, min_value=1, max_value=200)
    with col2:
        lv_buses = st.number_input("LV Buses", value=54, min_value=1, max_value=300)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="card-premium"><div class="card-premium-title"><span class="section-icon">⚙️</span> Configuration</div>', unsafe_allow_html=True)
    
    project_type = st.selectbox("Project Type", list(PROJECT_FACTORS.keys()), index=0)
    voltage = st.selectbox("Highest Voltage (kV)", list(VOLTAGE_FACTORS.keys()), index=1)
    region = st.selectbox("Region", list(REGION_FACTORS.keys()), index=0)
    
    st.markdown('</div>', unsafe_allow_html=True)

# SECTION 2: STUDIES
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="card-premium"><div class="card-premium-title"><span class="section-icon">✓</span> Studies to Include</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    chk_lf = st.checkbox("Load Flow", value=True)
    chk_sc = st.checkbox("Short Circuit", value=True)
    chk_pdc = st.checkbox("Protection Coordination", value=True)
    chk_af = st.checkbox("Arc Flash", value=True)

with col2:
    chk_har = st.checkbox("Harmonics", value=False)
    chk_ts = st.checkbox("Transient Stability", value=False)
    chk_ms = st.checkbox("Motor Starting", value=False)

selected_studies = []
if chk_lf: selected_studies.append('lf')
if chk_sc: selected_studies.append('sc')
if chk_pdc: selected_studies.append('pdc')
if chk_af: selected_studies.append('af')
if chk_har: selected_studies.append('har')
if chk_ts: selected_studies.append('ts')
if chk_ms: selected_studies.append('ms')

col_calc, col_reset = st.columns(2)
with col_calc:
    calc_button = st.button("🔄 Calculate Estimate", use_container_width=True)
with col_reset:
    reset_button = st.button("↻ Reset All", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

if reset_button:
    st.rerun()

# SECTION 3: ADVANCED CUSTOMIZATION
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="card-premium"><div class="card-premium-title"><span class="section-icon">⚙️</span> Advanced Customization (35+ Parameters)</div>', unsafe_allow_html=True)

with st.expander("▼ Scaling", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        mw_exponent = st.slider("MW Exponent (0.5 - 1.2)", 0.5, 1.2, 0.8, 0.05)
    with col2:
        bus_exponent = st.slider("Bus Exponent (0.7 - 1.3)", 0.7, 1.3, 0.9, 0.05)

with st.expander("▼ Base Hours"):
    for code in DEFAULT_STUDIES.keys():
        custom_hrs = st.number_input(f"{DEFAULT_STUDIES[code]['name']} Base Hours",
                                     value=st.session_state.custom_studies[code]['baseHrs'],
                                     min_value=5, max_value=50, step=1, key=f"hrs_{code}")
        st.session_state.custom_studies[code]['baseHrs'] = custom_hrs

with st.expander("▼ Complexity Factors"):
    for code in DEFAULT_STUDIES.keys():
        complexity = st.slider(f"{DEFAULT_STUDIES[code]['name']} Complexity",
                              0.5, 2.0, st.session_state.custom_studies[code]['complexity'], 0.05,
                              key=f"cplx_{code}")
        st.session_state.custom_studies[code]['complexity'] = complexity

with st.expander("▼ Reporting"):
    report_mode = st.radio("Reporting Cost Mode", ["% of Study Cost", "Fixed Amount ₹"], horizontal=True)
    if report_mode == "% of Study Cost":
        report_percent = st.slider("Report Cost %", 10, 50, 35, 5)
        report_fixed = 30000
    else:
        report_fixed = st.number_input("Fixed Cost (₹)", value=30000, min_value=5000, max_value=100000, step=5000)
        report_percent = 35
    report_complexity = st.slider("Report Complexity Factor", 0.8, 1.5, 1.0, 0.1)

with st.expander("▼ Team Costs"):
    for level in DEFAULT_TEAM.keys():
        col1, col2 = st.columns(2)
        with col1:
            min_rate = 1200 if level == 'L1' else (600 if level == 'L2' else 450)
            max_rate = 3600 if level == 'L1' else (1800 if level == 'L2' else 1350)
            rate = st.number_input(f"{level} Rate (₹/hr)", value=st.session_state.custom_team[level]['rate'],
                                  min_value=min_rate, max_value=max_rate, step=100)
            st.session_state.custom_team[level]['rate'] = rate
        with col2:
            min_alloc = 5 if level == 'L1' else (20 if level == 'L2' else 30)
            max_alloc = 25 if level == 'L1' else (50 if level == 'L2' else 70)
            alloc = st.slider(f"{level} Allocation %", min_alloc, max_alloc,
                             int(st.session_state.custom_team[level]['allocation']*100), 1, key=f"alloc_{level}")
            st.session_state.custom_team[level]['allocation'] = alloc / 100

with st.expander("▼ Additional Costs"):
    custom_cost = st.number_input("Custom Cost (Any Additional Cost)", value=0, min_value=0, max_value=500000, step=1000,
                                  help="Add any additional costs to the final project cost")

with st.expander("▼ Buffers"):
    col1, col2 = st.columns(2)
    with col1:
        bus_confidence = st.slider("Bus Confidence Level", 0.9, 2.5, 1.0, 0.1)
    with col2:
        buffer_percent = st.slider("Contingency Buffer %", 5, 25, 15, 1)

st.markdown('</div>', unsafe_allow_html=True)

# SECTION 4: REMARKS & NOTES
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="card-premium"><div class="card-premium-title"><span class="section-icon">📝</span> Remarks & Notes</div>', unsafe_allow_html=True)

remarks = st.text_area("Add any remarks, notes, or special requirements for this project",
                       placeholder="Type your remarks here...", height=80)

st.markdown('</div>', unsafe_allow_html=True)

# ============ CALCULATE & RESULTS ============
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

if len(selected_studies) > 0:
    results = calculateAll(facility_mw, mv_buses, lv_buses, project_type, voltage, region,
                          mw_exponent, bus_exponent, bus_confidence, buffer_percent,
                          report_mode, report_percent, report_fixed, report_complexity,
                          st.session_state.custom_studies, st.session_state.custom_team, 
                          selected_studies, custom_cost)
    
    # ========== HIGHLIGHTED TOTAL PROJECT COST ==========
    st.markdown(f"""
    <div class="highlight-total">
        <div class="highlight-total-label">📊 TOTAL PROJECT COST</div>
        <div class="highlight-total-label" style="font-size: 12px; color: #a8b5c7;">Project: {project_name}</div>
        <div class="highlight-total-value">{format_currency(results['grand_total'])}</div>
        <div class="highlight-total-label">Cost Per Bus: {format_currency(results['cost_per_bus'])} | Total Buses: {results['total_buses']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== KPI METRICS ROW 1 ==========
    st.markdown('<div class="card-premium"><div class="card-premium-title"><span class="section-icon">💰</span> Cost Estimation Results</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Study Cost", format_currency(results['total_study_cost']))
    with col2:
        st.metric("Report Cost", format_currency(results['total_reporting_cost']))
    with col3:
        st.metric("Modelling Cost", format_currency(results['modelling_cost']))
    with col4:
        st.metric("Meetings Cost", format_currency(results['meetings_cost']))
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Custom Cost", format_currency(results['custom_cost']))
    with col2:
        st.metric("Subtotal", format_currency(results['subtotal']))
    with col3:
        st.metric("Buffer", format_currency(results['buffer']))
    with col4:
        st.metric("Grand Total", format_currency(results['grand_total']))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== TIME BREAKDOWN ==========
    st.markdown('<div class="card-premium"><div class="card-premium-title"><span class="section-icon">⏱️</span> Project Time Breakdown</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Study Hours", format_number(results['total_study_hours']))
    with col2:
        st.metric("Report Hours", format_number(results['total_report_hours']))
    with col3:
        st.metric("Modelling Hours", format_number(results['modelling_hours']))
    with col4:
        st.metric("Total Hours", format_number(results['total_project_hours']))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== PIE CHARTS ==========
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost Composition Pie Chart
        cost_labels = ['Study Cost', 'Report Cost', 'Modelling', 'Meetings', 'Custom Cost', 'Buffer']
        cost_values = [
            results['total_study_cost'],
            results['total_reporting_cost'],
            results['modelling_cost'],
            results['meetings_cost'],
            results['custom_cost'],
            results['buffer']
        ]
        # Filter out zero values
        cost_labels = [l for l, v in zip(cost_labels, cost_values) if v > 0]
        cost_values = [v for v in cost_values if v > 0]
        
        fig_cost = create_pie_chart(cost_labels, cost_values, "Total Cost Composition")
        st.pyplot(fig_cost)
    
    with col2:
        # Time Breakdown Pie Chart
        time_labels = ['Study Hours', 'Report Hours', 'Modelling Hours', 'Meetings Hours']
        time_values = [
            results['total_study_hours'],
            results['total_report_hours'],
            results['modelling_hours'],
            MEETINGS_COUNT * MEETINGS_HRS
        ]
        time_labels = [l for l, v in zip(time_labels, time_values) if v > 0]
        time_values = [v for v in time_values if v > 0]
        
        fig_time = create_pie_chart(time_labels, time_values, "Total Project Time Breakdown (Hours)")
        st.pyplot(fig_time)
    
    # ========== PER-BUS BREAKDOWN TABLE ==========
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-premium"><div class="card-premium-title"><span class="section-icon">📍</span> Per-Bus Cost Breakdown</div>', unsafe_allow_html=True)
    
    breakdown_data = [
        {
            'Component': 'Studies',
            'Total Cost': format_currency(results['total_study_cost']),
            'Cost Per Bus': format_currency(results['total_study_cost']/results['total_buses']),
            '% of Total': f"{(results['total_study_cost']/results['grand_total']*100):.1f}%"
        },
        {
            'Component': 'Reporting',
            'Total Cost': format_currency(results['total_reporting_cost']),
            'Cost Per Bus': format_currency(results['total_reporting_cost']/results['total_buses']),
            '% of Total': f"{(results['total_reporting_cost']/results['grand_total']*100):.1f}%"
        },
        {
            'Component': 'Modelling (30%)',
            'Total Cost': format_currency(results['modelling_cost']),
            'Cost Per Bus': format_currency(results['modelling_cost']/results['total_buses']),
            '% of Total': f"{(results['modelling_cost']/results['grand_total']*100):.1f}%"
        },
        {
            'Component': 'Meetings',
            'Total Cost': format_currency(results['meetings_cost']),
            'Cost Per Bus': format_currency(results['meetings_cost']/results['total_buses']),
            '% of Total': f"{(results['meetings_cost']/results['grand_total']*100):.1f}%"
        },
        {
            'Component': 'Custom Cost',
            'Total Cost': format_currency(results['custom_cost']),
            'Cost Per Bus': format_currency(results['custom_cost']/results['total_buses']) if results['total_buses'] > 0 else "₹0",
            '% of Total': f"{(results['custom_cost']/results['grand_total']*100):.1f}%" if results['grand_total'] > 0 else "0.0%"
        },
        {
            'Component': 'Buffer',
            'Total Cost': format_currency(results['buffer']),
            'Cost Per Bus': format_currency(results['buffer']/results['total_buses']),
            '% of Total': f"{(results['buffer']/results['grand_total']*100):.1f}%"
        },
    ]
    
    st.dataframe(pd.DataFrame(breakdown_data), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== STUDIES BREAKDOWN ==========
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-premium"><div class="card-premium-title"><span class="section-icon">📊</span> Studies Breakdown</div>', unsafe_allow_html=True)
    
    studies_df = pd.DataFrame([
        {
            'Study': s['name'],
            'Study Hrs': format_number(s['studyHrs']),
            'Report Hrs': format_number(s['reportHrs']),
            'Total Hrs': format_number(s['studyHrs'] + s['reportHrs']),
            'Study Cost': format_currency(s['studyCost']),
            'Report Cost': format_currency(s['reportCost']),
            'Total': format_currency(s['studyCost'] + s['reportCost'])
        }
        for s in results['study_results']
    ])
    
    st.dataframe(studies_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== CONTRACTUAL PRICING ==========
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-premium"><div class="card-premium-title"><span class="section-icon">💼</span> Contractual Pricing</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Buses", results['total_buses'])
    with col2:
        st.metric("Cost Per Bus", format_currency(results['cost_per_bus']))
    with col3:
        st.metric("With 20% Margin", format_currency(results['cost_per_bus'] * 1.20))
    with col4:
        st.metric("Total Revenue", format_currency(results['cost_per_bus'] * 1.20 * results['total_buses']))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== EXPORT ==========
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-premium"><div class="card-premium-title"><span class="section-icon">📥</span> Export & Download</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'projectName': project_name,
            'grandTotal': results['grand_total'],
            'costPerBus': results['cost_per_bus'],
            'remarks': remarks
        }
        st.download_button("📥 JSON", json.dumps(export_data, indent=2),
                          file_name=f"estimate-{project_name}-{datetime.now().strftime('%Y%m%d')}.json",
                          mime="application/json", use_container_width=True)
    
    with col2:
        csv_data = f"Project,{project_name}\nGrand Total,{results['grand_total']}\nCost Per Bus,{results['cost_per_bus']}\nBuses,{results['total_buses']}"
        st.download_button("📊 CSV", csv_data,
                          file_name=f"estimate-{project_name}-{datetime.now().strftime('%Y%m%d')}.csv",
                          mime="text/csv", use_container_width=True)
    
    with col3:
        summary = f"PROJECT: {project_name}\nGrand Total: {format_currency(results['grand_total'])}\nCost Per Bus: {format_currency(results['cost_per_bus'])}\nBuses: {results['total_buses']}\nRemarks: {remarks}"
        st.download_button("📋 TXT", summary,
                          file_name=f"estimate-{project_name}-{datetime.now().strftime('%Y%m%d')}.txt",
                          mime="text/plain", use_container_width=True)
    
    with col4:
        if st.button("↻ Start Over", use_container_width=True):
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👈 **Please select at least one study to calculate costs**")

# ========== CREDITS & FUTURE ENHANCEMENTS ==========
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="card-premium">
    <div class="card-premium-title"><span class="section-icon">👥</span> Credits & Future Enhancements</div>
    
    <div class="credits-box">
        <strong>🏆 Developed By:</strong><br>
        A.D | Power Systems Studies Department<br><br>
        
        <strong>🔧 Current Version: v3.5</strong><br>
        Dark Theme UI | Advanced Cost Estimation | Per-Bus Analysis<br><br>
        
        <strong>📋 Current Features:</strong><br>
        ✓ 7 Power System Studies | ✓ Custom Team Allocation | ✓ Multi-Region Support<br>
        ✓ 35+ Customizable Parameters | ✓ Real-time Cost Breakdown | ✓ Pie Chart Analytics<br>
        ✓ Remarks & Notes | ✓ Multiple Export Formats | ✓ Dark Theme Professional UI<br><br>
        
        <strong>🚀 Future Enhancements (Roadmap):</strong><br>
        • Bus Count Estimation Tool Integration<br>
        • Advanced Report Generation (PDF/DOCX)<br>
        • Historical Project Database & Analytics<br>
        • Team Resource Planning Module<br>
        • Client Portal & Quotation Sharing<br>
        • Budget Variance Analysis<br>
        • AI-Based Cost Prediction<br>
        • Multi-Project Dashboard<br><br>
        
        <strong>📧 Support & Feedback:</strong><br>
        For issues, suggestions, or collaborations contact the development team.<br>
        Built with ❤️ using Streamlit | Last Updated: December 2024
    </div>
</div>
""", unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer-premium">
    © 2024 Power Systems Cost Estimator v3.5 | Developed by A.D | Power Systems Studies Department<br>
    Built with Streamlit | Professional Consulting Tool for Data Center & Industrial Power Systems
</div>
""", unsafe_allow_html=True)
