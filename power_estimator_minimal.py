import streamlit as st
import pandas as pd
import json
from datetime import datetime
import math

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Power Systems Cost Estimator v4.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ PROFESSIONAL DARK THEME - ENGINEERING FOCUSED ============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;600&display=swap');

:root {
    /* Premium Dark Engineering Palette */
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --bg-tertiary: #21262d;
    --bg-hover: #2d333b;
    --bg-active: #388bfd;
    
    /* Primary - Electric Blue (Tech Focus) */
    --primary: #1f6feb;
    --primary-light: #388bfd;
    --primary-dark: #1c5aa0;
    
    /* Accent - Teal (Engineering/Power Systems) */
    --accent: #39c5cf;
    --accent-light: #56d4dd;
    --accent-dark: #2b9da8;
    
    /* Text Colors - High Contrast */
    --text-primary: #f0f6fc;
    --text-secondary: #c9d1d9;
    --text-tertiary: #8b949e;
    --text-muted: #6e7681;
    
    /* Semantic Colors */
    --success: #1a7f37;
    --success-light: #2da44e;
    --warning: #bf8700;
    --warning-light: #d29922;
    --error: #da3633;
    --error-light: #f85149;
    --info: #0969da;
    
    /* Borders */
    --border-subtle: #30363d;
    --border-muted: #21262d;
    
    /* Spacing (8px base) */
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 12px;
    --space-lg: 16px;
    --space-xl: 24px;
    --space-2xl: 32px;
    
    /* Radius */
    --radius-sm: 4px;
    --radius-md: 6px;
    --radius-lg: 8px;
    --radius-xl: 12px;
    
    /* Shadows */
    --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.4);
    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.5);
    --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.6);
    --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.7);
    --shadow-glow: 0 0 16px rgba(56, 139, 253, 0.2);
    
    /* Typography */
    --font-size-xs: 11px;
    --font-size-sm: 12px;
    --font-size-base: 13px;
    --font-size-md: 14px;
    --font-size-lg: 16px;
    --font-size-xl: 18px;
    --font-size-2xl: 20px;
    --font-size-3xl: 24px;
    
    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;
    --font-weight-extrabold: 800;
    
    --line-height-tight: 1.25;
    --line-height-normal: 1.5;
    --line-height-relaxed: 1.75;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg-primary) !important;
    color: var(--text-primary);
    font-size: var(--font-size-base);
    line-height: var(--line-height-normal);
}

.main { 
    background: var(--bg-primary) !important; 
    padding-top: 0 !important; 
}

[data-testid="stMainBlockContainer"] { 
    padding: var(--space-xl) var(--space-xl) var(--space-2xl) var(--space-xl) !important; 
    background: var(--bg-primary) !important; 
    max-width: 1400px;
    margin: 0 auto;
}

/* ============ HEADER STYLES ============ */
.header-premium {
    position: sticky; 
    top: 0; 
    z-index: 999; 
    background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
    border-bottom: 1px solid var(--border-subtle);
    box-shadow: var(--shadow-md);
    padding: var(--space-lg) var(--space-xl);
    margin: -var(--space-xl) -var(--space-xl) var(--space-2xl) -var(--space-xl);
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 70px;
}

.header-left { 
    display: flex; 
    align-items: center; 
    gap: var(--space-lg);
}

.header-icon { 
    font-size: 28px; 
    color: var(--accent-light);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

.header-content h1 { 
    font-size: var(--font-size-xl);
    font-weight: var(--font-weight-extrabold);
    color: var(--text-primary); 
    margin: 0;
    letter-spacing: -0.5px;
}

.header-content p { 
    font-size: var(--font-size-sm);
    color: var(--text-tertiary); 
    margin: 2px 0 0 0;
}

.header-right { 
    display: flex; 
    gap: var(--space-xl);
    align-items: center;
}

.header-link { 
    font-size: var(--font-size-sm);
    color: var(--text-tertiary);
    text-decoration: none;
    font-weight: var(--font-weight-medium);
    transition: all 0.2s ease;
    padding: var(--space-sm) var(--space-md);
    border-radius: var(--radius-md);
}

.header-link:hover { 
    color: var(--accent-light);
    background: rgba(57, 197, 207, 0.1);
}

/* ============ SECTION TITLE STYLES ============ */
.section-title {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-bold);
    color: var(--text-primary);
    margin: var(--space-2xl) 0 var(--space-lg) 0;
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding-bottom: var(--space-md);
    border-bottom: 2px solid var(--border-subtle);
}

.section-icon { 
    font-size: var(--font-size-xl);
    color: var(--accent-light);
}

.section-divider { 
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-subtle), transparent);
    margin: var(--space-2xl) 0;
    border: none;
}

/* ============ CARD & CONTAINER STYLES ============ */
.card-premium {
    background: var(--bg-secondary);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    box-shadow: var(--shadow-sm);
    margin-bottom: var(--space-lg);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
}

.card-premium:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--primary-light);
    background: rgba(31, 111, 235, 0.02);
    transform: translateY(-2px);
}

.card-content {
    display: flex;
    flex-direction: column;
    gap: var(--space-lg);
}

/* ============ INPUT & FORM STYLES ============ */
input[type="number"], 
input[type="text"], 
select, 
.stNumberInput > div > div > input, 
.stSelectbox > div > div > select {
    width: 100% !important;
    padding: var(--space-md) var(--space-lg) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    font-size: var(--font-size-sm) !important;
    background: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
    font-family: inherit !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

input[type="number"]:focus, 
input[type="text"]:focus, 
select:focus, 
.stNumberInput > div > div > input:focus, 
.stSelectbox > div > div > select:focus {
    outline: none !important;
    border-color: var(--primary-light) !important;
    box-shadow: 0 0 0 3px rgba(56, 139, 253, 0.15) !important;
    background: var(--bg-tertiary) !important;
}

input::placeholder { 
    color: var(--text-muted) !important;
}

label {
    display: block;
    font-weight: var(--font-weight-semibold);
    font-size: var(--font-size-sm);
    color: var(--text-primary);
    margin-bottom: var(--space-md) !important;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.help-text {
    font-size: var(--font-size-xs);
    color: var(--text-tertiary);
    margin-top: var(--space-sm);
    display: block;
}

/* ============ BUTTON STYLES ============ */
.stButton > button {
    padding: var(--space-md) var(--space-lg) !important;
    border-radius: var(--radius-md) !important;
    font-weight: var(--font-weight-semibold) !important;
    font-size: var(--font-size-sm) !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-family: inherit !important;
    background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%) !important;
    color: #ffffff !important;
    box-shadow: var(--shadow-sm) !important;
    position: relative;
    overflow: hidden;
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%) !important;
    box-shadow: var(--shadow-lg), var(--shadow-glow) !important;
    transform: translateY(-2px);
}

.stButton > button:active {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    transform: translateY(0);
}

/* ============ CHECKBOX & RADIO STYLES ============ */
.stCheckbox > label {
    font-weight: var(--font-weight-normal) !important;
    font-size: var(--font-size-md) !important;
    margin-bottom: var(--space-md) !important;
    display: flex !important;
    align-items: center;
    gap: var(--space-md);
    color: var(--text-primary) !important;
    cursor: pointer;
}

.stRadio > label {
    font-weight: var(--font-weight-medium) !important;
    font-size: var(--font-size-sm) !important;
    color: var(--text-primary) !important;
}

/* ============ EXPANDER STYLES ============ */
.streamlit-expanderHeader {
    background: linear-gradient(90deg, var(--bg-tertiary) 0%, var(--bg-hover) 100%) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    padding: var(--space-lg) !important;
    font-weight: var(--font-weight-semibold) !important;
    color: var(--text-primary) !important;
    transition: all 0.2s ease !important;
    font-size: var(--font-size-md) !important;
}

.streamlit-expanderHeader:hover {
    background: linear-gradient(90deg, var(--bg-hover) 0%, rgba(56, 139, 253, 0.1) 100%) !important;
    border-color: var(--primary-light) !important;
    box-shadow: var(--shadow-sm) !important;
}

.streamlit-expanderContent {
    border: 1px solid var(--border-subtle) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
    padding: var(--space-xl) !important;
    background: var(--bg-secondary) !important;
}

/* ============ SLIDER STYLES ============ */
.stSlider > div > div > div {
    color: var(--text-primary) !important;
}

.stSlider [role="slider"] {
    background: var(--primary-light) !important;
}

/* ============ TABLE & DATAFRAME STYLES ============ */
.stDataFrame {
    width: 100%;
    border-radius: var(--radius-lg);
    overflow: hidden;
    border: 1px solid var(--border-subtle);
}

.stDataFrame thead {
    background: linear-gradient(90deg, var(--bg-tertiary) 0%, var(--bg-hover) 100%) !important;
}

.stDataFrame th {
    background: linear-gradient(90deg, var(--bg-tertiary) 0%, var(--bg-hover) 100%) !important;
    color: var(--text-primary) !important;
    font-weight: var(--font-weight-bold) !important;
    font-size: var(--font-size-sm) !important;
    border-bottom: 2px solid var(--border-subtle) !important;
    padding: var(--space-lg) !important;
    text-align: left !important;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.stDataFrame td {
    padding: var(--space-lg) !important;
    border-bottom: 1px solid var(--border-muted) !important;
    font-size: var(--font-size-sm) !important;
    color: var(--text-secondary) !important;
    background: var(--bg-secondary) !important;
}

.stDataFrame tbody tr:nth-child(even) {
    background: rgba(30, 64, 175, 0.03) !important;
}

.stDataFrame tbody tr:hover {
    background: rgba(56, 139, 253, 0.08) !important;
}

/* ============ METRIC STYLES ============ */
.stMetric {
    background: var(--bg-secondary);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: var(--space-xl);
    box-shadow: var(--shadow-sm);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.stMetric::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--primary-light), var(--accent-light));
}

.stMetric:hover {
    border-color: var(--primary-light);
    background: rgba(31, 111, 235, 0.02);
    box-shadow: var(--shadow-md), var(--shadow-glow);
    transform: translateY(-2px);
}

.stMetricLabel {
    font-size: var(--font-size-xs) !important;
    font-weight: var(--font-weight-semibold) !important;
    color: var(--text-tertiary) !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stMetricValue {
    font-size: var(--font-size-2xl) !important;
    font-weight: var(--font-weight-extrabold) !important;
    color: var(--primary-light) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    letter-spacing: -0.5px;
}

/* ============ ALERT STYLES ============ */
.stAlert {
    border-radius: var(--radius-lg) !important;
    padding: var(--space-lg) var(--space-xl) !important;
    font-size: var(--font-size-sm) !important;
    border-left: 4px solid !important;
    background: rgba(56, 139, 253, 0.08) !important;
    border-left-color: var(--primary-light) !important;
}

.stAlert > div {
    color: var(--text-primary) !important;
}

/* ============ FOOTER STYLES ============ */
.footer-premium {
    position: sticky;
    bottom: 0;
    background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
    border-top: 1px solid var(--border-subtle);
    padding: var(--space-lg) var(--space-xl);
    margin: var(--space-2xl) -var(--space-xl) -var(--space-xl) -var(--space-xl);
    height: auto;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: var(--space-xl);
    align-items: center;
    font-size: var(--font-size-xs);
    color: var(--text-tertiary);
    z-index: 100;
}

.footer-left {
    font-weight: var(--font-weight-semibold);
    color: var(--text-secondary);
}

.footer-center {
    text-align: center;
    color: var(--text-tertiary);
}

.footer-right {
    display: flex;
    gap: var(--space-lg);
    justify-content: flex-end;
}

.footer-link {
    color: var(--text-tertiary);
    text-decoration: none;
    transition: color 0.2s ease;
}

.footer-link:hover {
    color: var(--accent-light);
}

/* ============ LAYOUT UTILITIES ============ */
.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-xl);
    margin-bottom: var(--space-lg);
}

.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-xl);
    margin-bottom: var(--space-lg);
}

.grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-xl);
    margin-bottom: var(--space-lg);
}

/* ============ RESPONSIVE DESIGN ============ */
@media (max-width: 1199px) {
    .grid-4 { grid-template-columns: repeat(2, 1fr); }
    .header-premium { padding: var(--space-md) var(--space-lg); }
    .footer-premium { grid-template-columns: 1fr; gap: var(--space-md); text-align: center; }
}

@media (max-width: 767px) {
    [data-testid="stMainBlockContainer"] { 
        padding: var(--space-lg) var(--space-md) var(--space-2xl) var(--space-md) !important; 
    }
    
    .header-premium {
        padding: var(--space-md) var(--space-lg);
        height: auto;
        flex-direction: column;
        gap: var(--space-lg);
    }
    
    .header-right { display: none; }
    
    .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
    
    .section-title { font-size: var(--font-size-md); }
    
    .card-premium { padding: var(--space-md); }
    
    .stMetric { padding: var(--space-lg); }
    
    .footer-premium { margin: var(--space-xl) -var(--space-md) -var(--space-md) -var(--space-md); }
}

/* ============ SCROLLBAR STYLES ============ */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: var(--border-subtle);
    border-radius: var(--radius-md);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary-light);
}

/* ============ ACCESSIBILITY ============ */
:focus-visible {
    outline: 2px solid var(--primary-light);
    outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* ============ TYPOGRAPHY ============ */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary);
    font-weight: var(--font-weight-bold);
    margin: 0;
    line-height: var(--line-height-tight);
}

p {
    color: var(--text-secondary);
    margin: 0 0 var(--space-md) 0;
}

code {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    background: var(--bg-tertiary);
    color: var(--accent-light);
    padding: 2px 4px;
    border-radius: var(--radius-sm);
}

</style>
""", unsafe_allow_html=True)

# ============ ORIGINAL CONSTANTS & CALCULATIONS ============
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

# ============ ORIGINAL CALCULATE FUNCTION ============
def calculateAll(facility_mw, mv_buses, lv_buses, project_type, voltage, region,
                mw_exponent, bus_exponent, bus_confidence, buffer_percent,
                report_mode, report_percent, report_fixed, report_complexity,
                custom_studies, custom_team, selected_studies):
    
    total_buses = mv_buses + lv_buses
    mw_per_bus = facility_mw / total_buses
    
    # Calculate factors
    mw_factor = pow(facility_mw / 10, mw_exponent)
    bus_factor = pow(total_buses / 32, bus_exponent)
    project_factor = PROJECT_FACTORS.get(project_type, 1.0)
    voltage_factor = VOLTAGE_FACTORS.get(voltage, 1.0)
    region_factor = REGION_FACTORS.get(region, 1.0)
    
    # Calculate studies
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
        
        # Team allocation for this study
        l1_hours = final_study_hrs * custom_team['L1']['allocation']
        l2_hours = final_study_hrs * custom_team['L2']['allocation']
        l3_hours = final_study_hrs * custom_team['L3']['allocation']
        
        blended_rate = (l1_hours * custom_team['L1']['rate'] + 
                       l2_hours * custom_team['L2']['rate'] + 
                       l3_hours * custom_team['L3']['rate']) / final_study_hrs if final_study_hrs > 0 else 0
        
        study_cost = final_study_hrs * blended_rate
        
        # Reporting
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
    
    # Reporting cost
    total_reporting_cost = 0
    if report_mode == "% of Study Cost":
        total_reporting_cost = total_report_hours * 1200 * report_complexity
    else:
        total_reporting_cost = report_fixed * (len(selected_studies) / 7)
    
    # Additional costs
    total_project_hours = total_study_hours + total_report_hours + (MEETINGS_COUNT * MEETINGS_HRS)
    meetings_cost = MEETINGS_COUNT * MEETINGS_HRS * MEETINGS_RATE
    modelling_hours = total_project_hours * MODELLING_PERCENT
    modelling_cost = modelling_hours * MODELLING_RATE
    
    # Final costs
    subtotal = total_study_cost + total_reporting_cost + meetings_cost + modelling_cost
    buffer = subtotal * (buffer_percent / 100)
    grand_total = subtotal + buffer
    
    cost_per_bus = grand_total / total_buses if total_buses > 0 else 0
    
    return {
        'total_buses': total_buses,
        'mw_per_bus': mw_per_bus,
        'total_study_hours': total_study_hours,
        'total_report_hours': total_report_hours,
        'total_project_hours': total_project_hours,
        'total_study_cost': total_study_cost,
        'total_reporting_cost': total_reporting_cost,
        'meetings_cost': meetings_cost,
        'modelling_cost': modelling_cost,
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
        <div class="header-content">
            <h1>Power Systems</h1>
            <p>Cost Estimator v4.0</p>
        </div>
    </div>
    <div class="header-right">
        <a href="#" class="header-link">📖 Documentation</a>
        <a href="#" class="header-link">⚙️ Settings</a>
        <a href="#" class="header-link">❓ Help</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ============ SESSION STATE ============
if 'custom_studies' not in st.session_state:
    st.session_state.custom_studies = {code: {'baseHrs': study['baseHrs'], 'complexity': study['complexity']} 
                                       for code, study in DEFAULT_STUDIES.items()}
if 'custom_team' not in st.session_state:
    st.session_state.custom_team = DEFAULT_TEAM.copy()

# ============ SECTION 1: PROJECT BASICS & CONFIGURATION ============
st.markdown('<div class="section-title"><span class="section-icon">📋</span> Project Parameters</div>', unsafe_allow_html=True)

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown('<div class="card-premium"><div class="card-content">', unsafe_allow_html=True)
    facility_mw = st.number_input("🔌 Facility Capacity (MW)", value=10.0, min_value=0.5, max_value=500.0, step=0.5)
    col_mv, col_lv = st.columns(2)
    with col_mv:
        mv_buses = st.number_input("MV Buses", value=24, min_value=1, max_value=200)
    with col_lv:
        lv_buses = st.number_input("LV Buses", value=54, min_value=1, max_value=300)
    st.markdown('</div></div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="card-premium"><div class="card-content">', unsafe_allow_html=True)
    project_type = st.selectbox("🏢 Project Type", list(PROJECT_FACTORS.keys()), index=0)
    voltage = st.selectbox("⚡ Highest Voltage (kV)", list(VOLTAGE_FACTORS.keys()), index=1)
    region = st.selectbox("🌍 Region", list(REGION_FACTORS.keys()), index=0)
    st.markdown('</div></div>', unsafe_allow_html=True)

# ============ SECTION 2: STUDIES SELECTION ============
st.markdown('<div class="section-title"><span class="section-icon">✓</span> Studies to Include</div>', unsafe_allow_html=True)
st.markdown('<div class="card-premium"><div class="card-content">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    chk_lf = st.checkbox("📊 Load Flow", value=True)
    chk_sc = st.checkbox("⚠️ Short Circuit", value=True)
    chk_pdc = st.checkbox("🔒 Protection Coordination", value=True)
    chk_af = st.checkbox("🔥 Arc Flash", value=True)

with col2:
    chk_har = st.checkbox("〰️ Harmonics", value=False)
    chk_ts = st.checkbox("📈 Transient Stability", value=False)
    chk_ms = st.checkbox("⚙️ Motor Starting", value=False)

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
    calc_button = st.button("🔄 Calculate Costs", use_container_width=True)
with col_reset:
    reset_button = st.button("↻ Reset Form", use_container_width=True)

st.markdown('</div></div>', unsafe_allow_html=True)

if reset_button:
    st.rerun()

# ============ SECTION 3: ADVANCED CUSTOMIZATION ============
st.markdown('<div class="section-title"><span class="section-icon">⚙️</span> Advanced Customization (35+ Parameters)</div>', unsafe_allow_html=True)
st.markdown('<div class="card-premium"><div class="card-content">', unsafe_allow_html=True)

with st.expander("▼ Scaling Factors", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        mw_exponent = st.slider("🔋 MW Exponent (0.5 - 1.2)", 0.5, 1.2, 0.8, 0.05)
    with col2:
        bus_exponent = st.slider("📍 Bus Exponent (0.7 - 1.3)", 0.7, 1.3, 0.9, 0.05)

with st.expander("▼ Base Hours per Study"):
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

with st.expander("▼ Reporting Configuration"):
    report_mode = st.radio("Reporting Cost Mode", ["% of Study Cost", "Fixed Amount ₹"], horizontal=True)
    if report_mode == "% of Study Cost":
        report_percent = st.slider("Report Cost %", 10, 50, 35, 5)
        report_fixed = 30000
    else:
        report_fixed = st.number_input("Fixed Cost (₹)", value=30000, min_value=5000, max_value=100000, step=5000)
        report_percent = 35
    report_complexity = st.slider("Report Complexity Factor", 0.8, 1.5, 1.0, 0.1)

with st.expander("▼ Team Cost Allocation"):
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

with st.expander("▼ Confidence & Buffers"):
    col1, col2 = st.columns(2)
    with col1:
        bus_confidence = st.slider("📊 Bus Confidence Level", 0.9, 2.5, 1.0, 0.1)
    with col2:
        buffer_percent = st.slider("📈 Contingency Buffer %", 5, 25, 15, 1)

st.markdown('</div></div>', unsafe_allow_html=True)

# ============ SECTION 4: RESULTS & ANALYTICS ============
if len(selected_studies) > 0:
    results = calculateAll(facility_mw, mv_buses, lv_buses, project_type, voltage, region,
                          mw_exponent, bus_exponent, bus_confidence, buffer_percent,
                          report_mode, report_percent, report_fixed, report_complexity,
                          st.session_state.custom_studies, st.session_state.custom_team, selected_studies)
    
    # KPI METRICS
    st.markdown('<div class="section-title"><span class="section-icon">💰</span> Cost Estimation Results</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Study Hours", format_number(results['total_study_hours']))
    with col2:
        st.metric("Report Hours", format_number(results['total_report_hours']))
    with col3:
        st.metric("Total Hours", format_number(results['total_project_hours']))
    with col4:
        st.metric("Grand Total", format_currency(results['grand_total']))
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Study Cost", format_currency(results['total_study_cost']))
    with col2:
        st.metric("Report Cost", format_currency(results['total_reporting_cost']))
    with col3:
        st.metric("Modelling Cost", format_currency(results['modelling_cost']))
    with col4:
        st.metric("Cost/Bus", format_currency(results['cost_per_bus']))
    
    # PER-BUS BREAKDOWN
    st.markdown('<div class="section-title"><span class="section-icon">📍</span> Per-Bus Cost Breakdown</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-premium">', unsafe_allow_html=True)
    
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
            'Component': 'Buffer',
            'Total Cost': format_currency(results['buffer']),
            'Cost Per Bus': format_currency(results['buffer']/results['total_buses']),
            '% of Total': f"{(results['buffer']/results['grand_total']*100):.1f}%"
        },
    ]
    
    st.dataframe(pd.DataFrame(breakdown_data), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("ℹ️ **Reporting cost calculated separately. All costs include:** Study + Reporting + Modelling ÷ Buses")
    
    # STUDIES BREAKDOWN
    st.markdown('<div class="section-title"><span class="section-icon">📊</span> Studies Breakdown</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-premium">', unsafe_allow_html=True)
    
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
    
    # CONTRACTUAL PRICING
    st.markdown('<div class="section-title"><span class="section-icon">💼</span> Contractual Pricing</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Buses", results['total_buses'])
    with col2:
        st.metric("Cost Per Bus", format_currency(results['cost_per_bus']))
    with col3:
        st.metric("With 20% Margin", format_currency(results['cost_per_bus'] * 1.20))
    with col4:
        st.metric("Total Revenue", format_currency(results['cost_per_bus'] * 1.20 * results['total_buses']))
    
    # EXPORT
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span class="section-icon">📥</span> Export & Download</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-premium"><div class="card-content">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    export_data = {
        'timestamp': datetime.now().isoformat(),
        'grandTotal': results['grand_total'],
        'costPerBus': results['cost_per_bus']
    }
    
    with col1:
        st.download_button("📥 JSON", json.dumps(export_data, indent=2),
                          file_name=f"estimate-{datetime.now().strftime('%Y%m%d')}.json", mime="application/json", use_container_width=True)
    
    with col2:
        csv_data = f"Grand Total,{results['grand_total']}\nCost Per Bus,{results['cost_per_bus']}\nTotal Buses,{results['total_buses']}"
        st.download_button("📊 CSV", csv_data, file_name=f"estimate-{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
    
    with col3:
        summary = f"Grand Total: {format_currency(results['grand_total'])}\nCost Per Bus: {format_currency(results['cost_per_bus'])}\nBuses: {results['total_buses']}"
        st.download_button("📋 TXT", summary, file_name=f"estimate-{datetime.now().strftime('%Y%m%d')}.txt", mime="text/plain", use_container_width=True)
    
    with col4:
        if st.button("↻ Start Over", use_container_width=True):
            st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)

else:
    st.info("👈 **Please select at least one study to calculate costs**")

# ============ FOOTER ============
st.markdown("""
<div class="footer-premium">
    <div class="footer-left">© 2024 Power Systems Estimator | v4.0</div>
    <div class="footer-center">🚀 Built with Streamlit | Professional Engineering Dashboard</div>
    <div class="footer-right">
        <a href="#" class="footer-link">📖 Docs</a> | <a href="#" class="footer-link">💬 Support</a> | <a href="#" class="footer-link">📋 Terms</a>
    </div>
</div>
""", unsafe_allow_html=True)
