import streamlit as st
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Power Systems Cost Estimator v3.5",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ DARK THEME MINIMAL CSS ============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-primary: #0f1419;
    --bg-secondary: #1a2332;
    --bg-tertiary: #252d3d;
    --primary-light: #3b82f6;
    --text-primary: #e8eef5;
    --text-secondary: #a8b5c7;
    --border: #3a4556;
}

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
    font-family: 'Inter', sans-serif;
    background: var(--bg-primary) !important;
    color: var(--text-primary);
}

.main { background: var(--bg-primary) !important; }
[data-testid="stMainBlockContainer"] { padding-top: 16px !important; background: var(--bg-primary) !important; }

.header-premium {
    position: sticky; top: 0; z-index: 999; background: var(--bg-secondary); border-bottom: 1px solid var(--border);
    padding: 16px 32px; display: flex; align-items: center; gap: 12px; margin-bottom: 16px;
}

.header-icon { font-size: 24px; color: var(--primary-light); }
.header-title { font-size: 16px; font-weight: 600; color: var(--text-primary); }
.header-subtitle { font-size: 12px; color: var(--text-secondary); }

.card-premium {
    background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 8px;
    padding: 16px; margin-bottom: 16px; transition: all 0.3s ease;
}

.card-title { font-size: 14px; font-weight: 600; color: var(--text-primary); margin-bottom: 12px; }

input[type="number"], input[type="text"], select, textarea {
    width: 100% !important; padding: 8px !important; border: 1px solid var(--border) !important;
    border-radius: 6px !important; background: var(--bg-tertiary) !important; color: var(--text-primary) !important;
}

.stButton > button {
    padding: 10px 16px !important; border-radius: 6px !important; font-weight: 600 !important;
    background: var(--primary-light) !important; color: white !important; border: none !important;
}

.stCheckbox > label { font-weight: 400 !important; font-size: 13px !important; }

.stMetric { background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 8px; padding: 12px; }
.stMetricValue { font-size: 16px !important; color: var(--primary-light) !important; }

.highlight-total {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(59, 130, 246, 0.1) 100%);
    border: 2px solid var(--primary-light); border-radius: 8px; padding: 16px; margin: 16px 0; text-align: center;
}

.highlight-value { font-size: 28px; font-weight: 700; color: var(--primary-light); margin: 8px 0; }
.highlight-label { font-size: 12px; color: var(--text-secondary); }

.divider { height: 1px; background: var(--border); margin: 16px 0; }

.footer-premium {
    background: var(--bg-secondary); border-top: 1px solid var(--border);
    padding: 12px 16px; margin-top: 16px; text-align: center; font-size: 11px; color: var(--text-secondary);
}

@media (max-width: 767px) { .header-premium { padding: 12px 16px; } }
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

def create_bar_chart(labels, values, title, color='#3b82f6'):
    """Create a lightweight bar chart"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#1a2332')
    ax.set_facecolor('#1a2332')
    
    bars = ax.bar(labels, values, color=color, edgecolor='#3a4556', linewidth=1.5)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'₹{height/100000:.1f}L', ha='center', va='bottom', color='#e8eef5', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('', color='#e8eef5')
    ax.set_ylabel('Amount (₹)', color='#e8eef5', fontweight='bold')
    ax.set_title(title, color='#e8eef5', fontsize=14, fontweight='bold', pad=15)
    ax.tick_params(colors='#a8b5c7', labelsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#3a4556')
    ax.spines['bottom'].set_color('#3a4556')
    ax.grid(axis='y', alpha=0.2, color='#3a4556', linestyle='--')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

# ============ CALCULATE FUNCTION ============
def calculateAll(facility_mw, mv_buses, lv_buses, project_type, voltage, region,
                mw_exponent, bus_exponent, bus_confidence, buffer_percent,
                report_mode, report_percent, report_fixed, report_complexity,
                custom_studies, custom_team, selected_studies, custom_cost):
    
    total_buses = mv_buses + lv_buses
    mw_per_bus = facility_mw / total_buses if total_buses > 0 else 0
    
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
    <div class="header-icon">⚡</div>
    <div>
        <div class="header-title">Power Systems Cost Estimator</div>
        <div class="header-subtitle">v3.5 - Lightweight Version</div>
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
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="card-premium"><div class="card-title">📋 Project Basics</div>', unsafe_allow_html=True)
    project_name = st.text_input("Project Name", value="Project-Alpha", placeholder="Enter project name")
    facility_mw = st.number_input("Facility Capacity (MW)", value=10.0, min_value=0.5, max_value=500.0, step=0.5)
    col1, col2 = st.columns(2)
    with col1:
        mv_buses = st.number_input("MV Buses", value=24, min_value=1, max_value=200)
    with col2:
        lv_buses = st.number_input("LV Buses", value=54, min_value=1, max_value=300)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="card-premium"><div class="card-title">⚙️ Configuration</div>', unsafe_allow_html=True)
    project_type = st.selectbox("Project Type", list(PROJECT_FACTORS.keys()), index=0)
    voltage = st.selectbox("Highest Voltage (kV)", list(VOLTAGE_FACTORS.keys()), index=1)
    region = st.selectbox("Region", list(REGION_FACTORS.keys()), index=0)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="card-premium"><div class="card-title">✓ Studies to Include</div>', unsafe_allow_html=True)

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
    calc_button = st.button("🔄 Calculate", use_container_width=True)
with col_reset:
    reset_button = st.button("↻ Reset", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

if reset_button:
    st.rerun()

# ============ ADVANCED CUSTOMIZATION ============
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="card-premium"><div class="card-title">⚙️ Advanced Settings</div>', unsafe_allow_html=True)

with st.expander("▼ Scaling Parameters"):
    col1, col2 = st.columns(2)
    with col1:
        mw_exponent = st.slider("MW Exponent", 0.5, 1.2, 0.8, 0.05)
    with col2:
        bus_exponent = st.slider("Bus Exponent", 0.7, 1.3, 0.9, 0.05)

with st.expander("▼ Base Study Hours"):
    for code in DEFAULT_STUDIES.keys():
        custom_hrs = st.number_input(f"{DEFAULT_STUDIES[code]['name']}", value=st.session_state.custom_studies[code]['baseHrs'],
                                     min_value=5, max_value=50, step=1, key=f"hrs_{code}")
        st.session_state.custom_studies[code]['baseHrs'] = custom_hrs

with st.expander("▼ Complexity Factors"):
    for code in DEFAULT_STUDIES.keys():
        complexity = st.slider(f"{DEFAULT_STUDIES[code]['name']}", 0.5, 2.0, 
                              st.session_state.custom_studies[code]['complexity'], 0.05, key=f"cplx_{code}")
        st.session_state.custom_studies[code]['complexity'] = complexity

with st.expander("▼ Reporting Settings"):
    report_mode = st.radio("Mode", ["% of Study Cost", "Fixed Amount ₹"], horizontal=True)
    if report_mode == "% of Study Cost":
        report_percent = st.slider("Report Cost %", 10, 50, 35, 5)
        report_fixed = 30000
    else:
        report_fixed = st.number_input("Fixed Cost (₹)", value=30000, min_value=5000, max_value=100000, step=5000)
        report_percent = 35
    report_complexity = st.slider("Complexity Factor", 0.8, 1.5, 1.0, 0.1)

with st.expander("▼ Team Rates"):
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
            alloc = st.slider(f"{level} %", min_alloc, max_alloc, int(st.session_state.custom_team[level]['allocation']*100), 1, key=f"alloc_{level}")
            st.session_state.custom_team[level]['allocation'] = alloc / 100

with st.expander("▼ Additional Costs"):
    custom_cost = st.number_input("Custom Cost (₹)", value=0, min_value=0, max_value=500000, step=1000)

with st.expander("▼ Buffer & Confidence"):
    col1, col2 = st.columns(2)
    with col1:
        bus_confidence = st.slider("Bus Confidence", 0.9, 2.5, 1.0, 0.1)
    with col2:
        buffer_percent = st.slider("Contingency Buffer %", 5, 25, 15, 1)

st.markdown('</div>', unsafe_allow_html=True)

# ============ REMARKS & NOTES ============
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="card-premium"><div class="card-title">📝 Remarks & Notes</div>', unsafe_allow_html=True)
remarks = st.text_area("Add remarks or special requirements", placeholder="Type here...", height=60)
st.markdown('</div>', unsafe_allow_html=True)

# ============ RESULTS ============
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if len(selected_studies) > 0:
    results = calculateAll(facility_mw, mv_buses, lv_buses, project_type, voltage, region,
                          mw_exponent, bus_exponent, bus_confidence, buffer_percent,
                          report_mode, report_percent, report_fixed, report_complexity,
                          st.session_state.custom_studies, st.session_state.custom_team, 
                          selected_studies, custom_cost)
    
    # HIGHLIGHTED TOTAL
    st.markdown(f"""
    <div class="highlight-total">
        <div class="highlight-label">📊 TOTAL PROJECT COST</div>
        <div class="highlight-label" style="font-size: 12px;">Project: {project_name}</div>
        <div class="highlight-value">{format_currency(results['grand_total'])}</div>
        <div class="highlight-label">Cost Per Bus: {format_currency(results['cost_per_bus'])} | Buses: {results['total_buses']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # COST METRICS
    st.markdown('<div class="card-premium"><div class="card-title">💰 Cost Breakdown</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Study", format_currency(results['total_study_cost']))
    with col2:
        st.metric("Report", format_currency(results['total_reporting_cost']))
    with col3:
        st.metric("Modelling", format_currency(results['modelling_cost']))
    with col4:
        st.metric("Meetings", format_currency(results['meetings_cost']))
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Custom", format_currency(results['custom_cost']))
    with col2:
        st.metric("Subtotal", format_currency(results['subtotal']))
    with col3:
        st.metric("Buffer", format_currency(results['buffer']))
    with col4:
        st.metric("Total", format_currency(results['grand_total']))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # TIME METRICS
    st.markdown('<div class="card-premium"><div class="card-title">⏱️ Time Breakdown (Hours)</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Study", format_number(results['total_study_hours']))
    with col2:
        st.metric("Report", format_number(results['total_report_hours']))
    with col3:
        st.metric("Modelling", format_number(results['modelling_hours']))
    with col4:
        st.metric("Total", format_number(results['total_project_hours']))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # BAR CHARTS
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        cost_labels = ['Study', 'Report', 'Modelling', 'Meetings', 'Custom', 'Buffer']
        cost_values = [
            results['total_study_cost'],
            results['total_reporting_cost'],
            results['modelling_cost'],
            results['meetings_cost'],
            results['custom_cost'],
            results['buffer']
        ]
        fig_cost = create_bar_chart(cost_labels, cost_values, "Cost Breakdown")
        st.pyplot(fig_cost, use_container_width=True)
    
    with col2:
        time_labels = ['Study', 'Report', 'Modelling', 'Meetings']
        time_values = [
            results['total_study_hours'],
            results['total_report_hours'],
            results['modelling_hours'],
            MEETINGS_COUNT * MEETINGS_HRS
        ]
        fig_time = create_bar_chart(time_labels, time_values, "Time Breakdown (Hours)", '#10b981')
        st.pyplot(fig_time, use_container_width=True)
    
    # PER-BUS BREAKDOWN
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-premium"><div class="card-title">📍 Per-Bus Breakdown</div>', unsafe_allow_html=True)
    
    breakdown_data = [
        {'Component': 'Studies', 'Total': format_currency(results['total_study_cost']), 
         'Per Bus': format_currency(results['total_study_cost']/results['total_buses']),
         '%': f"{(results['total_study_cost']/results['grand_total']*100):.1f}%"},
        {'Component': 'Reporting', 'Total': format_currency(results['total_reporting_cost']),
         'Per Bus': format_currency(results['total_reporting_cost']/results['total_buses']),
         '%': f"{(results['total_reporting_cost']/results['grand_total']*100):.1f}%"},
        {'Component': 'Modelling', 'Total': format_currency(results['modelling_cost']),
         'Per Bus': format_currency(results['modelling_cost']/results['total_buses']),
         '%': f"{(results['modelling_cost']/results['grand_total']*100):.1f}%"},
        {'Component': 'Meetings', 'Total': format_currency(results['meetings_cost']),
         'Per Bus': format_currency(results['meetings_cost']/results['total_buses']),
         '%': f"{(results['meetings_cost']/results['grand_total']*100):.1f}%"},
        {'Component': 'Custom', 'Total': format_currency(results['custom_cost']),
         'Per Bus': format_currency(results['custom_cost']/results['total_buses']) if results['total_buses'] > 0 else "₹0",
         '%': f"{(results['custom_cost']/results['grand_total']*100):.1f}%" if results['grand_total'] > 0 else "0%"},
        {'Component': 'Buffer', 'Total': format_currency(results['buffer']),
         'Per Bus': format_currency(results['buffer']/results['total_buses']),
         '%': f"{(results['buffer']/results['grand_total']*100):.1f}%"},
    ]
    st.dataframe(pd.DataFrame(breakdown_data), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # STUDIES BREAKDOWN
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-premium"><div class="card-title">📊 Studies Summary</div>', unsafe_allow_html=True)
    
    studies_df = pd.DataFrame([
        {'Study': s['name'], 'Study Hrs': format_number(s['studyHrs']), 'Report Hrs': format_number(s['reportHrs']),
         'Total Hrs': format_number(s['studyHrs'] + s['reportHrs']), 'Cost': format_currency(s['studyCost'] + s['reportCost'])}
        for s in results['study_results']
    ])
    st.dataframe(studies_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # EXPORT
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-premium"><div class="card-title">📥 Export & Download</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        export_data = {
            'projectName': project_name,
            'grandTotal': results['grand_total'],
            'costPerBus': results['cost_per_bus'],
            'timestamp': datetime.now().isoformat(),
            'remarks': remarks
        }
        st.download_button("📥 JSON", json.dumps(export_data, indent=2),
                          file_name=f"estimate-{project_name}.json", mime="application/json", use_container_width=True)
    
    with col2:
        csv_data = f"Project,{project_name}\nTotal,{results['grand_total']}\nPer Bus,{results['cost_per_bus']}\nBuses,{results['total_buses']}"
        st.download_button("📊 CSV", csv_data, file_name=f"estimate-{project_name}.csv", mime="text/csv", use_container_width=True)
    
    with col3:
        summary = f"PROJECT: {project_name}\nTOTAL: {format_currency(results['grand_total'])}\nPER BUS: {format_currency(results['cost_per_bus'])}\nBUSES: {results['total_buses']}\nREMARKS: {remarks}"
        st.download_button("📋 TXT", summary, file_name=f"estimate-{project_name}.txt", mime="text/plain", use_container_width=True)
    
    with col4:
        if st.button("↻ New Estimate", use_container_width=True):
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👈 Select at least one study to calculate")

# ============ FOOTER ============
st.markdown("""
<div class="footer-premium">
    © 2024 Power Systems Cost Estimator v3.5 | Lightweight Version | Developed by A.D
</div>
""", unsafe_allow_html=True)
