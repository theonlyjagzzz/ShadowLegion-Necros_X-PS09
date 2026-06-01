"""
NECROS X — Hackathon Edition
Autonomous Zombie API Detection & Defense SOC Dashboard
Upgraded: Enterprise dark theme, API Intelligence Panel, live event feed,
clickable nodes, LED status panel, session-preserving monitoring.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import time
import numpy as np
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NECROS X — SOC Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# MODULE IMPORTS
# ─────────────────────────────────────────────
from modules.risk_analyzer import (
    calculate_risk_score,
    classify_threat_level,
    calculate_zombie_probability,
    get_severity_color,
    get_led_status,
)
from modules.attack_simulator import generate_attack, generate_multiple_attacks
from modules.honeypot_engine import analyze_honeypot_activity, generate_attacker_profile, get_honeypot_apis
from modules.attack_path_visualizer import generate_attack_path_graph
from modules.predictive_threat_engine import predict_future_targets
from modules.ai_recommendation_engine import generate_security_recommendations, get_api_intelligence
from modules.attack_pattern_analysis import analyze_attack_patterns
from modules.automated_response_system import automated_threat_response
from modules.llm_soc_analyst import generate_soc_summary
from modules.incident_report_generator import generate_incident_report
from modules.api_kill_switch import activate_kill_switch, manual_isolate_api, deploy_honeypot_redirect

# ─────────────────────────────────────────────
# CSS — ENTERPRISE DARK THEME
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── GLOBAL ───────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.stApp {
    background-color: #060b18 !important;
    color: #e2e8f0 !important;
}

/* ── SIDEBAR ──────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1020 0%, #080e1c 100%) !important;
    border-right: 1px solid rgba(99,179,237,0.1) !important;
    width: 240px !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
[data-testid="stSidebarHeader"] { height: 0px !important; padding: 0 !important; }

/* ── SIDEBAR LOGO ─────────────────────────── */
.necros-logo {
    padding: 20px 16px 12px;
    border-bottom: 1px solid rgba(99,179,237,0.08);
    margin-bottom: 8px;
}
.necros-logo-text {
    font-size: 22px; font-weight: 800; letter-spacing: 3px;
    background: linear-gradient(135deg, #63b3ed, #fc8181);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.necros-logo-sub {
    font-size: 10px; color: #4a5568; letter-spacing: 1.5px;
    text-transform: uppercase; margin-top: 2px; font-family: 'JetBrains Mono', monospace;
}

/* ── NAV SECTION LABEL ────────────────────── */
.nav-section {
    font-size: 10px; color: #4a5568; letter-spacing: 2px;
    text-transform: uppercase; padding: 12px 16px 4px;
    font-weight: 600;
}

/* ── NAV BUTTONS ──────────────────────────── */
section[data-testid="stSidebar"] .stButton button {
    width: 100% !important; background: transparent !important;
    border: none !important; border-radius: 6px !important;
    padding: 9px 14px !important; margin-bottom: 1px !important;
    color: #718096 !important; font-size: 13px !important;
    font-weight: 500 !important; text-align: left !important;
    transition: all 0.15s ease !important;
    min-height: 36px !important; box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(99,179,237,0.08) !important;
    color: #e2e8f0 !important; transform: none !important;
    border-left: 2px solid #63b3ed !important;
}

/* ── METRIC CARDS ─────────────────────────── */
div[data-testid="metric-container"] {
    background: #0d1526 !important;
    border-radius: 10px !important; padding: 16px !important;
    border: 1px solid rgba(99,179,237,0.1) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important;
}
div[data-testid="metric-container"] label {
    color: #718096 !important; font-size: 11px !important;
    font-weight: 600 !important; letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e2e8f0 !important; font-size: 28px !important; font-weight: 700 !important;
}

/* ── MAIN BUTTONS ─────────────────────────── */
.stButton button {
    background: #0d1526 !important; color: #e2e8f0 !important;
    border-radius: 8px !important;
    border: 1px solid rgba(99,179,237,0.2) !important;
    padding: 8px 16px !important; font-weight: 600 !important;
    font-size: 13px !important; transition: all 0.15s !important;
}
.stButton button:hover {
    background: #1a2540 !important;
    border-color: rgba(99,179,237,0.5) !important;
}

/* ── HEADERS ──────────────────────────────── */
h1, h2, h3, h4 { color: #e2e8f0 !important; }
h1 { font-size: 28px !important; font-weight: 700 !important; letter-spacing: -0.5px !important; }
h2 { font-size: 20px !important; font-weight: 600 !important; }
h3 { font-size: 16px !important; font-weight: 600 !important; }

/* ── DATAFRAMES ───────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 10px !important; overflow: hidden !important;
    border: 1px solid rgba(99,179,237,0.1) !important;
}
[data-testid="stDataFrame"] thead th {
    background: #0d1526 !important; color: #718096 !important;
    font-size: 11px !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: 0.5px !important;
}

/* ── CARDS ────────────────────────────────── */
.soc-card {
    background: #0d1526; border-radius: 10px;
    border: 1px solid rgba(99,179,237,0.1);
    padding: 18px; margin-bottom: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
}
.soc-card-title {
    font-size: 11px; color: #4a5568; text-transform: uppercase;
    letter-spacing: 1.5px; font-weight: 600; margin-bottom: 6px;
}
.soc-card-value {
    font-size: 26px; font-weight: 700; color: #e2e8f0;
}
.soc-card-sub { font-size: 12px; color: #718096; margin-top: 4px; }

/* ── STATUS BADGES ────────────────────────── */
.badge {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.5px;
    text-transform: uppercase;
}
.badge-critical { background: rgba(252,129,129,0.15); color: #fc8181; border: 1px solid rgba(252,129,129,0.3); }
.badge-high     { background: rgba(251,189,35,0.15);  color: #f6ad55; border: 1px solid rgba(251,189,35,0.3); }
.badge-medium   { background: rgba(246,224,94,0.15);  color: #f6e05e; border: 1px solid rgba(246,224,94,0.3); }
.badge-low      { background: rgba(104,211,145,0.15); color: #68d391; border: 1px solid rgba(104,211,145,0.3); }
.badge-zombie   { background: rgba(252,129,129,0.12); color: #fc8181; border: 1px solid rgba(252,129,129,0.25); }
.badge-active   { background: rgba(104,211,145,0.12); color: #68d391; border: 1px solid rgba(104,211,145,0.25); }
.badge-deprecated { background: rgba(251,189,35,0.12); color: #f6ad55; border: 1px solid rgba(251,189,35,0.25); }

/* ── LED STATUS DOTS ──────────────────────── */
.led { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }
.led-green  { background: #68d391; box-shadow: 0 0 6px #68d391; }
.led-amber  { background: #f6ad55; box-shadow: 0 0 6px #f6ad55; }
.led-red    { background: #fc8181; box-shadow: 0 0 6px #fc8181; }
.led-flash  { background: #fc8181; box-shadow: 0 0 6px #fc8181;
    animation: flash 0.7s infinite alternate; }
.led-honeypot { background: #9f7aea;
    animation: rgb-cycle 1.2s infinite; }
@keyframes flash { from { opacity: 1; } to { opacity: 0.15; } }
@keyframes rgb-cycle {
    0%   { background: #fc8181; box-shadow: 0 0 8px #fc8181; }
    33%  { background: #68d391; box-shadow: 0 0 8px #68d391; }
    66%  { background: #63b3ed; box-shadow: 0 0 8px #63b3ed; }
    100% { background: #fc8181; box-shadow: 0 0 8px #fc8181; }
}

/* ── API INTELLIGENCE PANEL ───────────────── */
.intel-panel {
    background: linear-gradient(135deg, #0d1526, #0a1020);
    border-radius: 12px; border: 1px solid rgba(99,179,237,0.2);
    padding: 22px; margin-top: 8px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.intel-header {
    font-size: 16px; font-weight: 700; color: #e2e8f0;
    margin-bottom: 14px; padding-bottom: 10px;
    border-bottom: 1px solid rgba(99,179,237,0.1);
    display: flex; align-items: center; gap: 8px;
}
.intel-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 13px;
}
.intel-label { color: #718096; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.intel-value { color: #e2e8f0; font-weight: 600; font-size: 13px; }
.intel-section { margin-top: 14px; margin-bottom: 6px; font-size: 10px; color: #4a5568; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; }

/* ── PROGRESS BARS ────────────────────────── */
.progress-bar-track {
    background: rgba(255,255,255,0.06); border-radius: 4px;
    height: 8px; margin: 4px 0; overflow: hidden;
}
.progress-bar-fill {
    height: 100%; border-radius: 4px;
    transition: width 0.4s ease;
}

/* ── EVENT FEED ───────────────────────────── */
.event-feed { max-height: 420px; overflow-y: auto; }
.event-item {
    padding: 10px 14px; border-radius: 8px;
    margin-bottom: 6px; border-left: 3px solid;
    font-size: 12px; font-family: 'JetBrains Mono', monospace;
    background: rgba(255,255,255,0.03);
}
.event-critical { border-color: #fc8181; }
.event-high     { border-color: #f6ad55; }
.event-medium   { border-color: #f6e05e; }
.event-low      { border-color: #68d391; }
.event-time     { color: #4a5568; font-size: 10px; }
.event-api      { color: #63b3ed; }
.event-type     { color: #a0aec0; }

/* ── PAGE HEADER BAR ──────────────────────── */
.page-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 20px; padding-bottom: 14px;
    border-bottom: 1px solid rgba(99,179,237,0.08);
}
.page-title { font-size: 22px; font-weight: 700; color: #e2e8f0; }
.page-subtitle { font-size: 12px; color: #718096; margin-top: 2px; }

/* ── TOP STATUS BAR ───────────────────────── */
.status-bar {
    background: #0a1020; border-radius: 8px; padding: 10px 18px;
    border: 1px solid rgba(99,179,237,0.08); margin-bottom: 18px;
    display: flex; align-items: center; gap: 24px; font-size: 12px;
}
.status-item { display: flex; align-items: center; gap: 6px; color: #718096; }
.status-item strong { color: #e2e8f0; }

/* ── TOGGLE ───────────────────────────────── */
[data-testid="stToggle"] { margin-top: 6px; }

/* ── ALERTS ───────────────────────────────── */
.stAlert { border-radius: 8px !important; font-size: 13px !important; }

/* ── TABS ─────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1526 !important; border-radius: 8px !important;
    gap: 4px !important; padding: 4px !important;
    border: 1px solid rgba(99,179,237,0.1) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px !important; color: #718096 !important;
    font-size: 12px !important; font-weight: 600 !important;
    padding: 6px 14px !important;
}
.stTabs [aria-selected="true"] {
    background: #1a2540 !important; color: #e2e8f0 !important;
}

/* ── EXPANDER ─────────────────────────────── */
.streamlit-expanderHeader {
    background: #0d1526 !important; border-radius: 8px !important;
    color: #e2e8f0 !important; font-weight: 600 !important;
    border: 1px solid rgba(99,179,237,0.1) !important;
}

/* ── SCROLLBAR ────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #060b18; }
::-webkit-scrollbar-thumb { background: #1a2540; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2d3748; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
def init_session():
    defaults = {
        "page": "dashboard",
        "attack_history": [],
        "blocked_apis": [],
        "live_mode": False,
        "selected_api": None,
        "enable_colors": True,
        "event_feed": [],
        "honeypot_deployed": [],
        "show_intel": False,
        "last_live_tick": 0.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ─────────────────────────────────────────────
# LOAD & PROCESS DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_api_data():
    df = pd.read_csv("data/apis.csv")
    return df

api_data_raw = load_api_data().copy()
api_data_raw["risk_score"] = api_data_raw.apply(calculate_risk_score, axis=1)
api_data_raw["threat_level"] = api_data_raw["risk_score"].apply(classify_threat_level)
api_data_raw["zombie_probability"] = api_data_raw.apply(calculate_zombie_probability, axis=1)
api_data_raw["led_status"] = api_data_raw.apply(get_led_status, axis=1)
api_data = api_data_raw

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def _count_attacks():
    counts = {}
    for a in st.session_state.attack_history:
        api = a["api_target"]
        counts[api] = counts.get(api, 0) + 1
    return counts

# ─────────────────────────────────────────────
# LIVE MODE — append event without full rerun
# ─────────────────────────────────────────────
if st.session_state.live_mode:
    now = time.time()
    if now - st.session_state.last_live_tick >= 2.5:
        new_attack = generate_attack()
        st.session_state.attack_history.append(new_attack)
        st.session_state.event_feed.append(new_attack)
        if len(st.session_state.attack_history) > 150:
            st.session_state.attack_history = st.session_state.attack_history[-150:]
        if len(st.session_state.event_feed) > 80:
            st.session_state.event_feed = st.session_state.event_feed[-80:]
        st.session_state.last_live_tick = now
        # Auto kill-switch
        for api, count in _count_attacks().items():
            if count >= 5 and api not in st.session_state.blocked_apis:
                st.session_state.blocked_apis.append(api)
        time.sleep(0.05)
        st.rerun()

def _count_attacks():
    counts = {}
    for a in st.session_state.attack_history:
        api = a["api_target"]
        counts[api] = counts.get(api, 0) + 1
    return counts

# Auto kill-switch check (passive)
for api, count in _count_attacks().items():
    if count >= 5 and api not in st.session_state.blocked_apis:
        st.session_state.blocked_apis.append(api)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
SEVERITY_ORDER = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}

def severity_badge(level):
    cls = {"Critical": "badge-critical", "High": "badge-high",
           "Medium": "badge-medium", "Low": "badge-low"}.get(level, "badge-low")
    return f"<span class='badge {cls}'>{level}</span>"

def status_badge(status):
    cls = {"Zombie": "badge-zombie", "Active": "badge-active",
           "Deprecated": "badge-deprecated"}.get(status, "badge-low")
    return f"<span class='badge {cls}'>{status}</span>"

def led_html(led_status):
    cls = {
        "green": "led-green", "amber": "led-amber",
        "red": "led-red", "flashing_red": "led-flash",
        "honeypot": "led-honeypot",
    }.get(led_status, "led-green")
    return f"<span class='led {cls}'></span>"

def progress_bar(value, max_val=100, color="#fc8181"):
    pct = min(int((value / max_val) * 100), 100)
    return f"""
    <div class='progress-bar-track'>
      <div class='progress-bar-fill' style='width:{pct}%;background:{color};'></div>
    </div>
    <div style='font-size:11px;color:#718096;'>{value}/{max_val}</div>
    """

def color_risk(row):
    level = row.get("threat_level") or row.get("severity") or row.get("future_risk", "Low")
    palette = {
        "Critical": "background-color:rgba(252,129,129,0.18)",
        "High":     "background-color:rgba(246,173,85,0.18)",
        "Medium":   "background-color:rgba(246,224,94,0.15)",
        "Low":      "background-color:rgba(104,211,145,0.12)",
    }
    return [palette.get(level, "")] * len(row)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='necros-logo'>
      <div class='necros-logo-text'>NECROS X</div>
      <div class='necros-logo-sub'>SOC · API Security Platform</div>
    </div>
    """, unsafe_allow_html=True)

    # Status summary
    total_a = len(api_data)
    zombie_a = len(api_data[api_data["status"] == "Zombie"])
    attack_c = len(st.session_state.attack_history)
    crit_c = len([x for x in st.session_state.attack_history if x.get("severity") == "Critical"])

    overall_led = "led-flash" if crit_c > 0 else ("led-red" if zombie_a > 0 else "led-green")
    overall_label = "CRITICAL" if crit_c > 0 else ("ELEVATED" if zombie_a > 0 else "STABLE")
    overall_color = "#fc8181" if crit_c > 0 else ("#f6ad55" if zombie_a > 0 else "#68d391")

    st.markdown(f"""
    <div style='padding:10px 14px;margin-bottom:8px;background:rgba(0,0,0,0.3);
         border-radius:8px;border:1px solid rgba(255,255,255,0.05);'>
      <div style='display:flex;align-items:center;gap:8px;'>
        <span class='led {overall_led}'></span>
        <span style='font-size:13px;font-weight:700;color:{overall_color};'>{overall_label}</span>
      </div>
      <div style='font-size:11px;color:#4a5568;margin-top:4px;'>
        {attack_c} events · {crit_c} critical · {zombie_a} zombies
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='nav-section'>Monitoring</div>", unsafe_allow_html=True)

    nav_items = [
        ("dashboard",    "🏠  Dashboard Overview"),
        ("monitoring",   "📡  Threat Monitoring"),
        ("honeypot",     "🍯  Honeypot Intelligence"),
    ]
    for key, label in nav_items:
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.session_state.show_intel = False

    st.markdown("<div class='nav-section'>Intelligence</div>", unsafe_allow_html=True)
    intel_items = [
        ("attack_viz",   "🕸️  Attack Visualization"),
        ("ai_intel",     "🤖  AI Intelligence"),
    ]
    for key, label in intel_items:
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.session_state.show_intel = False

    st.markdown("<div class='nav-section'>Defense</div>", unsafe_allow_html=True)
    def_items = [
        ("response",     "⚡  Autonomous Response"),
        ("soc_analyst",  "🔍  SOC Analyst"),
    ]
    for key, label in def_items:
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.session_state.show_intel = False

    st.markdown("<div class='nav-section'>Reports</div>", unsafe_allow_html=True)
    rep_items = [
        ("incidents",    "📄  Incident Reports"),
        ("executive",    "📊  Executive Summary"),
    ]
    for key, label in rep_items:
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.session_state.show_intel = False

    st.markdown("---")
    # Live mode toggle
    st.session_state.live_mode = st.toggle(
        "🔴  LIVE MONITORING",
        value=st.session_state.live_mode,
        help="Streams simulated attack events. State is preserved."
    )
    st.session_state.enable_colors = st.toggle(
        "🎨  Color Coding",
        value=st.session_state.enable_colors,
    )

    st.markdown("<div class='nav-section'>Simulation</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("＋1 Attack", use_container_width=True):
            a = generate_attack()
            st.session_state.attack_history.append(a)
            st.session_state.event_feed.append(a)
            st.rerun()
    with c2:
        if st.button("＋10 Attacks", use_container_width=True):
            attacks = generate_multiple_attacks(10)
            st.session_state.attack_history.extend(attacks)
            st.session_state.event_feed.extend(attacks)
            st.rerun()
    if st.button("🗑  Clear Events", use_container_width=True):
        st.session_state.attack_history = []
        st.session_state.event_feed = []
        st.session_state.blocked_apis = []
        st.rerun()

# ─────────────────────────────────────────────
# TOP STATUS BAR
# ─────────────────────────────────────────────
total_apis    = len(api_data)
active_apis   = len(api_data[api_data["status"] == "Active"])
zombie_apis   = len(api_data[api_data["status"] == "Zombie"])
deprecated_apis = len(api_data[api_data["status"] == "Deprecated"])
critical_apis = len(api_data[api_data["threat_level"] == "Critical"])
total_attacks_count = len(st.session_state.attack_history)
critical_attacks_count = len([x for x in st.session_state.attack_history if x.get("severity") == "Critical"])
blocked_count = len(st.session_state.blocked_apis)

st.markdown(f"""
<div class='status-bar'>
  <div class='status-item'>
    <span class='led led-green'></span>
    <strong>{active_apis}</strong> Active APIs
  </div>
  <div class='status-item'>
    <span class='led led-amber'></span>
    <strong>{deprecated_apis}</strong> Deprecated
  </div>
  <div class='status-item'>
    <span class='led {"led-flash" if zombie_apis > 0 else "led-red"}'></span>
    <strong>{zombie_apis}</strong> Zombies
  </div>
  <div class='status-item' style='margin-left:auto;'>
    <span class='led {"led-flash" if critical_attacks_count > 0 else "led-green"}'></span>
    <strong style='color:{"#fc8181" if critical_attacks_count > 0 else "#68d391"};'>
      {critical_attacks_count} Critical Events
    </strong>
  </div>
  <div class='status-item'>
    <strong>{total_attacks_count}</strong> Total Events
  </div>
  <div class='status-item'>
    <span style='color:{"#fc8181" if blocked_count > 0 else "#718096"};'>
      🔒 <strong>{blocked_count}</strong> Blocked
    </span>
  </div>
  <div class='status-item'>
    <span style='color:{"#9f7aea" if st.session_state.live_mode else "#4a5568"};'>
      {"🔴 LIVE" if st.session_state.live_mode else "⚫ PAUSED"}
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# API INTELLIGENCE PANEL (shown when API selected)
# ─────────────────────────────────────────────
def render_intel_panel(api_name):
    row = api_data[api_data["api_name"] == api_name]
    if row.empty:
        st.warning(f"API '{api_name}' not found in database.")
        return
    api_row = row.iloc[0].to_dict()
    intel = get_api_intelligence(api_row, st.session_state.attack_history)

    severity_color = get_severity_color(intel["threat_level"])
    is_honeypot = api_name in get_honeypot_apis() or api_name in st.session_state.honeypot_deployed

    st.markdown(f"""
    <div class='intel-panel'>
      <div class='intel-header'>
        {led_html(intel.get("led_status", get_led_status(api_row)))}
        🔬 API Intelligence: <span style='color:#63b3ed;'>{api_name}</span>
        {severity_badge(intel["threat_level"])}
        {"<span class='badge' style='background:rgba(159,122,234,0.15);color:#9f7aea;border:1px solid rgba(159,122,234,0.3);'>🍯 HONEYPOT</span>" if is_honeypot else ""}
      </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='intel-section'>RISK METRICS</div>
        <div class='intel-row'><span class='intel-label'>Risk Score</span>
          <span class='intel-value' style='color:{severity_color};'>{intel["risk_score"]}/100</span></div>
        """, unsafe_allow_html=True)
        st.markdown(progress_bar(intel["risk_score"], 100, severity_color), unsafe_allow_html=True)
        st.markdown(f"""
        <div class='intel-row'><span class='intel-label'>Zombie Probability</span>
          <span class='intel-value' style='color:#f6ad55;'>{intel["zombie_probability"]}%</span></div>
        """, unsafe_allow_html=True)
        st.markdown(progress_bar(intel["zombie_probability"], 100, "#f6ad55"), unsafe_allow_html=True)
        st.markdown(f"""
        <div class='intel-row'><span class='intel-label'>Threat Level</span>
          <span class='intel-value'>{severity_badge(intel["threat_level"])}</span></div>
        <div class='intel-row'><span class='intel-label'>Status</span>
          <span class='intel-value'>{status_badge(intel["status"])}</span></div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='intel-section'>TRAFFIC & ATTACK ANALYSIS</div>
        <div class='intel-row'><span class='intel-label'>API Traffic</span>
          <span class='intel-value'>{intel["traffic"]}</span></div>
        <div class='intel-row'><span class='intel-label'>Last Used</span>
          <span class='intel-value'>{intel["last_used_days"]} days ago</span></div>
        <div class='intel-row'><span class='intel-label'>Attack Events</span>
          <span class='intel-value' style='color:{"#fc8181" if intel["traffic_events"]>0 else "#68d391"};'>
            {intel["traffic_events"]}
          </span></div>
        <div class='intel-row'><span class='intel-label'>Avg Breach Probability</span>
          <span class='intel-value' style='color:#f6ad55;'>{intel["avg_breach_probability"]}%</span></div>
        <div class='intel-row'><span class='intel-label'>Source IPs Detected</span>
          <span class='intel-value'>{len(intel["source_ips"])}</span></div>
        """, unsafe_allow_html=True)
        if intel["attack_types"]:
            types_html = " ".join([f"<span style='background:rgba(99,179,237,0.1);color:#63b3ed;padding:2px 7px;border-radius:4px;font-size:10px;margin:2px;display:inline-block;'>{t}</span>" for t in intel["attack_types"][:4]])
            st.markdown(f"<div style='margin-top:8px;'>{types_html}</div>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='intel-section'>AUTH & EXPOSURE</div>
        <div class='intel-row'><span class='intel-label'>Authentication</span>
          <span class='intel-value'>{intel["authentication"]}</span></div>
        <div class='intel-row'><span class='intel-label'>Sensitive Data</span>
          <span class='intel-value' style='color:{"#fc8181" if intel["sensitive_data"]=="Yes" else "#68d391"};'>
            {intel["sensitive_data"]}
          </span></div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class='intel-section'>AUTH ANALYSIS</div>
        <div style='font-size:12px;color:#a0aec0;line-height:1.5;'>{intel["auth_analysis"]}</div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class='intel-section'>AI CONFIDENCE</div>
        """, unsafe_allow_html=True)
        st.markdown(progress_bar(intel["confidence"], 100, "#63b3ed"), unsafe_allow_html=True)

    # Findings
    if intel["findings"]:
        st.markdown("<div class='intel-section'>⚠ FINDINGS</div>", unsafe_allow_html=True)
        findings_html = "".join([
            f"<div style='padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:12px;color:#a0aec0;'>• {f}</div>"
            for f in intel["findings"]
        ])
        st.markdown(findings_html, unsafe_allow_html=True)

    # Recommendations
    st.markdown("<div class='intel-section'>🤖 AI RECOMMENDATION</div>", unsafe_allow_html=True)
    rec_text = intel["recommendation"].replace("\n", "<br/>")
    st.markdown(f"<div style='font-size:12px;color:#a0aec0;line-height:1.7;font-family:\"JetBrains Mono\",monospace;'>{rec_text}</div>", unsafe_allow_html=True)

    # Action buttons
    if intel["actions"]:
        st.markdown("<div class='intel-section'>🚀 DEFENSE ACTIONS</div>", unsafe_allow_html=True)
        action_cols = st.columns(len(intel["actions"][:4]))
        for i, act in enumerate(intel["actions"][:4]):
            with action_cols[i]:
                if st.button(f"{act['icon']} {act['action']}", key=f"act_{api_name}_{i}", use_container_width=True):
                    st.session_state.page = {
                        "Autonomous Response": "response",
                        "Honeypot Intelligence": "honeypot",
                        "Attack Visualization": "attack_viz",
                        "AI Intelligence": "ai_intel",
                        "Incident Reports": "incidents",
                        "Threat Monitoring": "monitoring",
                        "SOC Analyst": "soc_analyst",
                    }.get(act["module"], "dashboard")
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SHARED: API SELECTOR WIDGET
# ─────────────────────────────────────────────
def render_api_selector(prefix=""):
    api_names = sorted(api_data["api_name"].tolist())
    # Pre-select preserved selected API
    default_idx = 0
    if st.session_state.selected_api in api_names:
        default_idx = api_names.index(st.session_state.selected_api)
    selected = st.selectbox(
        "🔎 Select API for Intelligence",
        api_names,
        index=default_idx,
        key=f"api_selector_{prefix}",
    )
    if selected != st.session_state.selected_api:
        st.session_state.selected_api = selected
        st.session_state.show_intel = True
    if st.button("🔬 Open API Intelligence Panel", key=f"open_intel_{prefix}"):
        st.session_state.show_intel = True
        st.session_state.selected_api = selected
    if st.session_state.show_intel and st.session_state.selected_api:
        render_intel_panel(st.session_state.selected_api)

# ─────────────────────────────────────────────
# PAGE: DASHBOARD OVERVIEW
# ─────────────────────────────────────────────
page = st.session_state.page

if page == "dashboard":
    st.markdown("""
    <div class='page-header'>
      <div>
        <div class='page-title'>API Infrastructure Dashboard</div>
        <div class='page-subtitle'>Real-time overview of your API security posture</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total APIs", total_apis)
    col2.metric("Active", active_apis, delta=None)
    col3.metric("Zombie APIs", zombie_apis, delta=f"+{zombie_apis}" if zombie_apis else None,
                delta_color="inverse")
    col4.metric("Deprecated", deprecated_apis)
    col5.metric("Critical Risk", critical_apis, delta=f"🔴 {critical_apis}" if critical_apis else None,
                delta_color="inverse")

    st.markdown("---")

    # LED Status Panel
    st.subheader("🔦 LED Status Panel")
    led_cols = st.columns(min(len(api_data), 7))
    for i, (_, row) in enumerate(api_data.iterrows()):
        col_idx = i % 7
        with led_cols[col_idx]:
            led_s = row["led_status"]
            is_hp = row["api_name"] in get_honeypot_apis()
            if is_hp:
                led_s = "honeypot"
            st.markdown(f"""
            <div style='text-align:center;padding:8px 4px;background:#0d1526;
                 border-radius:8px;margin:2px;border:1px solid rgba(255,255,255,0.05);
                 cursor:pointer;'>
              {led_html(led_s)}
              <div style='font-size:10px;color:#718096;margin-top:3px;
                   white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
                   max-width:90px;' title='{row["api_name"]}'>{row["api_name"]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style='display:flex;gap:20px;margin-top:8px;margin-bottom:16px;font-size:11px;color:#718096;'>
      <span><span class='led led-green'></span>Active</span>
      <span><span class='led led-amber'></span>Deprecated</span>
      <span><span class='led led-red'></span>Zombie</span>
      <span><span class='led led-flash'></span>Attack Detected</span>
      <span><span class='led led-honeypot'></span>Honeypot Active</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # API table + intelligence panel
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("Discovered API Infrastructure")
        display_df = api_data[["api_name","status","last_used_days","authentication",
                                "sensitive_data","risk_score","threat_level","zombie_probability"]].copy()
        display_df = display_df.sort_values("risk_score", ascending=False).reset_index(drop=True)
        display_df.index += 1

        if st.session_state.enable_colors:
            st.dataframe(
                display_df.style.apply(color_risk, axis=1),
                use_container_width=True, height=380,
            )
        else:
            st.dataframe(display_df, use_container_width=True, height=380)

        # Click an API name to open intelligence
        st.caption("💡 Select an API below to open the Intelligence Panel")
        clicked_api = st.selectbox("Click API to Inspect", api_data["api_name"].tolist(),
                                   key="dashboard_api_select", label_visibility="collapsed")
        if st.button("🔬 Open Intelligence Panel", key="dash_open_intel"):
            st.session_state.selected_api = clicked_api
            st.session_state.show_intel = True

    with right_col:
        st.subheader("Risk Distribution")
        status_counts = api_data["status"].value_counts()
        pie = px.pie(
            values=status_counts.values, names=status_counts.index,
            color_discrete_map={"Active":"#68d391","Zombie":"#fc8181","Deprecated":"#f6ad55"},
            hole=0.6,
        )
        pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", showlegend=True,
            legend=dict(orientation="v", x=0.6, y=0.5, font=dict(size=11)),
            margin=dict(l=0,r=0,t=10,b=0), height=220,
        )
        st.plotly_chart(pie, use_container_width=True)

        st.subheader("Risk Scores")
        bar = px.bar(
            api_data.sort_values("risk_score", ascending=True),
            x="risk_score", y="api_name", orientation="h",
            color="threat_level",
            color_discrete_map={"Critical":"#fc8181","High":"#f6ad55","Medium":"#f6e05e","Low":"#68d391"},
        )
        bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", margin=dict(l=0,r=0,t=10,b=0), height=300,
            yaxis=dict(tickfont=dict(size=10)), xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            showlegend=False,
        )
        st.plotly_chart(bar, use_container_width=True)

    # Show intel panel below
    if st.session_state.show_intel and st.session_state.selected_api:
        st.markdown("---")
        render_intel_panel(st.session_state.selected_api)

# ─────────────────────────────────────────────
# PAGE: THREAT MONITORING
# ─────────────────────────────────────────────
elif page == "monitoring":
    st.markdown("""
    <div class='page-header'>
      <div>
        <div class='page-title'>📡 Live Threat Intelligence Feed</div>
        <div class='page-subtitle'>Real-time attack event monitoring with session-preserved state</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    main_col, feed_col = st.columns([3, 1])

    with main_col:
        if len(st.session_state.attack_history) == 0:
            st.success("✅ No active attacks detected. System is monitoring.")
        else:
            attack_df = pd.DataFrame(st.session_state.attack_history)
            attack_df = attack_df.reset_index(drop=True)
            attack_df.index += 1

            # Severity timeline
            st.subheader("Threat Severity Timeline")
            timeline_df = attack_df.copy()
            timeline_df["timestamp"] = pd.to_datetime(timeline_df["timestamp"])
            severity_map = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
            timeline_df["severity_score"] = timeline_df["severity"].map(severity_map)
            tl_fig = px.area(
                timeline_df, x="timestamp", y="severity_score", color="severity",
                color_discrete_map={"Critical":"#fc8181","High":"#f6ad55","Medium":"#f6e05e","Low":"#68d391"},
                title="Threat Escalation Over Time",
            )
            tl_fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0", margin=dict(l=0,r=0,t=30,b=0),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickvals=[1,2,3,4],
                           ticktext=["Low","Med","High","Crit"]),
            )
            st.plotly_chart(tl_fig, use_container_width=True)

            # Attack table
            st.subheader("Attack Event Log")
            display_cols = [c for c in ["timestamp","api_target","attack_type","source_ip","severity","status","breach_probability"] if c in attack_df.columns]
            if st.session_state.enable_colors:
                st.dataframe(
                    attack_df[display_cols].style.apply(color_risk, axis=1),
                    use_container_width=True, height=320,
                )
            else:
                st.dataframe(attack_df[display_cols], use_container_width=True, height=320)

            # Critical alerts
            critical_df = attack_df[attack_df["severity"] == "Critical"]
            if not critical_df.empty:
                st.subheader(f"🔴 Critical Alerts ({len(critical_df)})")
                for _, row in critical_df.tail(5).iterrows():
                    st.error(
                        f"**{row['attack_type']}** on `{row['api_target']}` "
                        f"from `{row['source_ip']}` at {row['timestamp']}"
                    )

        # API Intelligence
        st.markdown("---")
        st.subheader("API Intelligence")
        render_api_selector("monitoring")

    with feed_col:
        st.subheader("⚡ Live Event Feed")
        if not st.session_state.event_feed:
            st.markdown("<div style='color:#4a5568;font-size:12px;'>No events yet. Launch an attack or enable Live Mode.</div>", unsafe_allow_html=True)
        else:
            feed_html = "<div class='event-feed'>"
            for ev in reversed(st.session_state.event_feed[-40:]):
                sev = ev.get("severity","Low")
                cls = f"event-{sev.lower()}"
                feed_html += f"""
                <div class='event-item {cls}'>
                  <div class='event-time'>{ev.get("timestamp","")}</div>
                  <div><span class='event-api'>{ev.get("api_target","")}</span></div>
                  <div class='event-type'>{ev.get("attack_type","")}</div>
                  <div style='color:#718096;font-size:10px;'>{ev.get("source_ip","")}</div>
                </div>
                """
            feed_html += "</div>"
            st.markdown(feed_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: HONEYPOT INTELLIGENCE
# ─────────────────────────────────────────────
elif page == "honeypot":
    st.markdown("""
    <div class='page-header'>
      <div>
        <div class='page-title'>🍯 Honeypot Defense Intelligence</div>
        <div class='page-subtitle'>Attacker profiling from honeypot API interactions</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    honeypot_apis_list = get_honeypot_apis()

    # Honeypot status cards
    st.subheader("Honeypot Deployment Status")
    hp_cols = st.columns(len(honeypot_apis_list))
    for i, api in enumerate(honeypot_apis_list):
        with hp_cols[i]:
            is_active = api in st.session_state.honeypot_deployed or True  # all are active by default
            st.markdown(f"""
            <div class='soc-card' style='text-align:center;'>
              <span class='led led-honeypot'></span>
              <div style='font-size:11px;color:#9f7aea;margin-top:4px;font-weight:600;'>ACTIVE</div>
              <div style='font-size:12px;color:#a0aec0;margin-top:2px;
                   word-break:break-all;'>{api}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📋 Inspect", key=f"hp_inspect_{i}", use_container_width=True):
                st.session_state.selected_api = api
                st.session_state.show_intel = True

    st.markdown("---")

    honeypot_logs = analyze_honeypot_activity(st.session_state.attack_history)

    if honeypot_logs.empty:
        st.info("🍯 Honeypots are active. No intrusion attempts captured yet. Generate attacks to populate intelligence.")
    else:
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader(f"Captured Intrusions ({len(honeypot_logs)})")
            display_cols = [c for c in ["timestamp","api_target","attack_type","source_ip",
                                         "severity","attack_category","threat_score","intelligence_report"]
                            if c in honeypot_logs.columns]
            if st.session_state.enable_colors:
                st.dataframe(
                    honeypot_logs[display_cols].style.apply(color_risk, axis=1),
                    use_container_width=True, height=320,
                )
            else:
                st.dataframe(honeypot_logs[display_cols], use_container_width=True, height=320)

        with col_right:
            # Attack type distribution
            if "attack_type" in honeypot_logs.columns:
                type_counts = honeypot_logs["attack_type"].value_counts()
                fig_hp = px.bar(
                    x=type_counts.values, y=type_counts.index, orientation="h",
                    title="Attack Types Captured",
                    color=type_counts.values,
                    color_continuous_scale=["#68d391","#f6ad55","#fc8181"],
                )
                fig_hp.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0", margin=dict(l=0,r=0,t=30,b=0),
                    showlegend=False, coloraxis_showscale=False,
                    yaxis=dict(tickfont=dict(size=10)),
                )
                st.plotly_chart(fig_hp, use_container_width=True)

        # Attacker profiles
        attacker_profiles = generate_attacker_profile(honeypot_logs)
        if not attacker_profiles.empty:
            st.subheader("🕵️ Attacker Threat Profiles")
            profile_cols = [c for c in ["source_ip","honeypot_hits","avg_threat_score",
                                          "threat_level","intel_summary","last_seen"]
                            if c in attacker_profiles.columns]
            if st.session_state.enable_colors:
                st.dataframe(
                    attacker_profiles[profile_cols].style.apply(color_risk, axis=1),
                    use_container_width=True,
                )
            else:
                st.dataframe(attacker_profiles[profile_cols], use_container_width=True)

    st.markdown("---")
    st.subheader("Deploy Honeypot to API")
    hp_target = st.selectbox("Select API to Honeypot-ify", api_data["api_name"].tolist(), key="hp_deploy_select")
    if st.button("🍯 Deploy Honeypot", key="hp_deploy_btn"):
        result = deploy_honeypot_redirect(hp_target)
        if hp_target not in st.session_state.honeypot_deployed:
            st.session_state.honeypot_deployed.append(hp_target)
        st.success(f"✅ Honeypot deployed on `{hp_target}` — {result['action']}")

    if st.session_state.show_intel and st.session_state.selected_api:
        st.markdown("---")
        render_intel_panel(st.session_state.selected_api)

# ─────────────────────────────────────────────
# PAGE: ATTACK VISUALIZATION
# ─────────────────────────────────────────────
elif page == "attack_viz":
    st.markdown("""
    <div class='page-header'>
      <div>
        <div class='page-title'>🕸️ Attack Path Visualization</div>
        <div class='page-subtitle'>Interactive graph — click nodes to open API Intelligence</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if len(st.session_state.attack_history) == 0:
        st.info("No attack data yet. Generate attacks using the sidebar controls to visualize the attack graph.")
    else:
        # Inline API selector to keep graph state
        selected_for_intel = st.selectbox(
            "🔬 Click node OR select API for Intelligence",
            ["— none —"] + sorted(api_data["api_name"].tolist()),
            key="viz_api_select",
            index=0,
        )
        if selected_for_intel != "— none —":
            st.session_state.selected_api = selected_for_intel
            st.session_state.show_intel = True

        graph_html = generate_attack_path_graph(st.session_state.attack_history)

        # Inject postMessage listener
        listener_script = """
        <script>
        window.addEventListener("message", function(event) {
          if (event.data && event.data.type === "necros_node_click") {
            var api = event.data.api;
            // Streamlit doesn't support cross-frame postMessage natively,
            // so we show a tooltip overlay instead
            var overlay = document.getElementById('node-tooltip');
            if (!overlay) {
              overlay = document.createElement('div');
              overlay.id = 'node-tooltip';
              overlay.style.cssText = 'position:fixed;top:20px;right:20px;background:#0d1526;' +
                'border:1px solid rgba(99,179,237,0.3);border-radius:8px;padding:12px 16px;' +
                'color:#e2e8f0;font-size:13px;z-index:9999;font-family:monospace;' +
                'box-shadow:0 8px 32px rgba(0,0,0,0.6);';
              document.body.appendChild(overlay);
            }
            overlay.innerHTML = '🔬 <b>' + api + '</b> — Use selector above to open Intelligence Panel';
            setTimeout(function(){ overlay.style.display='none'; }, 4000);
            overlay.style.display = 'block';
          }
        });
        </script>
        """
        components.html(graph_html + listener_script, height=820, scrolling=False)

        if st.session_state.show_intel and st.session_state.selected_api:
            st.markdown("---")
            render_intel_panel(st.session_state.selected_api)

# ─────────────────────────────────────────────
# PAGE: AI INTELLIGENCE
# ─────────────────────────────────────────────
elif page == "ai_intel":
    st.markdown("""
    <div class='page-header'>
      <div>
        <div class='page-title'>🤖 AI Predictive Threat Intelligence</div>
        <div class='page-subtitle'>Future attack target prediction, root cause analysis, and pattern recognition</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Predictions", "🗺 Heatmap", "💡 Recommendations", "🔍 Patterns"])

    with tab1:
        prediction_df = predict_future_targets(st.session_state.attack_history)
        if prediction_df.empty:
            st.info("Not enough attack data for predictions. Generate at least 3 attacks.")
        else:
            prediction_df = prediction_df.sort_values("prediction_score", ascending=False).reset_index(drop=True)

            # Prediction cards
            st.subheader("Future Threat Predictions")
            pred_cols = st.columns(min(len(prediction_df), 4))
            for i, (_, row) in enumerate(prediction_df.head(4).iterrows()):
                with pred_cols[i]:
                    color = get_severity_color(row["future_risk"])
                    st.markdown(f"""
                    <div class='soc-card'>
                      <div class='soc-card-title'>{row["api_name"]}</div>
                      <div class='soc-card-value' style='color:{color};'>{row["prediction_score"]:.0f}%</div>
                      <div style='margin:6px 0;'>
                        {severity_badge(row["future_risk"])}
                        <span style='font-size:10px;color:#718096;margin-left:6px;'>
                          Confidence: {row.get("confidence",60):.0f}%
                        </span>
                      </div>
                      <div style='font-size:11px;color:#718096;margin-top:4px;line-height:1.4;'>
                        {row.get("root_cause","")[:80]}...
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("🔬 Inspect", key=f"pred_inspect_{i}", use_container_width=True):
                        st.session_state.selected_api = row["api_name"]
                        st.session_state.show_intel = True

            st.markdown("---")
            # Root cause cards
            st.subheader("Root Cause Analysis")
            for _, row in prediction_df.iterrows():
                color = get_severity_color(row["future_risk"])
                with st.expander(f"{led_html(row['future_risk'].lower())} {row['api_name']} — {row['future_risk']} Risk", expanded=False):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Prediction Score", f"{row['prediction_score']:.1f}%")
                    c2.metric("Confidence", f"{row.get('confidence',60):.0f}%")
                    c3.metric("Attack Count", row["attack_count"])
                    st.markdown(f"**Root Cause:** {row.get('root_cause','')}")

            # Full prediction table
            st.subheader("Full Prediction Table")
            display_pred = prediction_df.copy()
            display_pred["prediction_score"] = display_pred["prediction_score"].round(1).astype(str) + "%"
            display_pred["confidence"] = display_pred["confidence"].round(1).astype(str) + "%"
            if st.session_state.enable_colors:
                st.dataframe(display_pred.style.apply(color_risk, axis=1), use_container_width=True)
            else:
                st.dataframe(display_pred, use_container_width=True)

        if st.session_state.show_intel and st.session_state.selected_api:
            st.markdown("---")
            render_intel_panel(st.session_state.selected_api)

    with tab2:
        if len(st.session_state.attack_history) > 0:
            heatmap_df = pd.DataFrame(st.session_state.attack_history)
            attack_counts_hm = (
                heatmap_df.groupby(["api_target","attack_type"]).size().reset_index(name="count")
            )
            heatmap = px.density_heatmap(
                attack_counts_hm, x="api_target", y="attack_type", z="count",
                title="Attack Concentration Heatmap",
                color_continuous_scale=["#060b18","#1a2540","#f6ad55","#fc8181"],
            )
            heatmap.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                xaxis=dict(tickangle=-30, tickfont=dict(size=10)),
                yaxis=dict(tickfont=dict(size=10)),
            )
            st.plotly_chart(heatmap, use_container_width=True)
        else:
            st.info("No attack data for heatmap.")

    with tab3:
        recommendations = generate_security_recommendations(api_data)
        st.subheader(f"AI Security Recommendations ({len(recommendations)} APIs)")
        for rec in sorted(recommendations, key=lambda r: SEVERITY_ORDER.get(r["threat_level"], 0), reverse=True):
            color_map = {"Critical":"#fc8181","High":"#f6ad55","Medium":"#f6e05e","Low":"#68d391"}
            color = color_map.get(rec["threat_level"], "#68d391")
            with st.expander(
                f"{led_html(rec['threat_level'].lower())} {rec['api_name']} — {rec['threat_level']}  (Confidence: {rec['confidence']}%)",
                expanded=(rec["threat_level"] == "Critical"),
            ):
                # Findings
                if rec["findings"]:
                    st.markdown("**🔍 Findings:**")
                    for f in rec["findings"]:
                        st.markdown(f"  - {f}")

                st.markdown(f"**💡 Recommendation:**")
                rec_text = rec["recommendation"].replace("\n", "  \n")
                st.code(rec_text, language=None)

                # Action buttons
                if rec["actions"]:
                    st.markdown("**🚀 Quick Actions:**")
                    act_cols = st.columns(len(rec["actions"][:4]))
                    for i, act in enumerate(rec["actions"][:4]):
                        with act_cols[i]:
                            if st.button(
                                f"{act['icon']} {act['action']}",
                                key=f"rec_act_{rec['api_name']}_{i}",
                                use_container_width=True,
                            ):
                                page_map = {
                                    "Autonomous Response": "response",
                                    "Honeypot Intelligence": "honeypot",
                                    "Attack Visualization": "attack_viz",
                                    "AI Intelligence": "ai_intel",
                                    "Incident Reports": "incidents",
                                    "Threat Monitoring": "monitoring",
                                    "SOC Analyst": "soc_analyst",
                                }
                                st.session_state.page = page_map.get(act["module"], "dashboard")
                                st.session_state.selected_api = rec["api_name"]
                                st.rerun()

    with tab4:
        patterns = analyze_attack_patterns(st.session_state.attack_history)
        if not patterns:
            st.info("Insufficient attack data for pattern analysis. Need at least 3 attack events.")
        else:
            st.subheader(f"Detected Attack Patterns ({len(patterns)})")
            for p in sorted(patterns, key=lambda x: SEVERITY_ORDER.get(x["risk_level"], 0), reverse=True)[:20]:
                color = get_severity_color(p["risk_level"])
                with st.expander(
                    f"{severity_badge(p['risk_level'])} {p['behavior_type']}",
                    expanded=(p["risk_level"] == "Critical"),
                ):
                    st.markdown(f"**Attack Chain:** `{p['attack_pattern']}`")
                    st.markdown(f"**MITRE Technique:** `{p.get('mitre_technique','')}`")
                    st.markdown(f"**Description:** {p.get('description','')}")

# ─────────────────────────────────────────────
# PAGE: AUTONOMOUS RESPONSE
# ─────────────────────────────────────────────
elif page == "response":
    st.markdown("""
    <div class='page-header'>
      <div>
        <div class='page-title'>⚡ Autonomous Threat Response Engine</div>
        <div class='page-subtitle'>Automated defense playbooks, kill switch, and traffic isolation</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🤖 Automated Responses", "🔒 Kill Switch", "🛡 Defense Workflow"])

    with tab1:
        responses = automated_threat_response(st.session_state.attack_history)
        if not responses:
            st.success("✅ No active automated responses. System is on standby.")
        else:
            # Summary metrics
            c1,c2,c3,c4 = st.columns(4)
            crit_r = len([r for r in responses if r["severity"]=="Critical"])
            high_r = len([r for r in responses if r["severity"]=="High"])
            c1.metric("Total Responses", len(responses))
            c2.metric("Critical Actions", crit_r)
            c3.metric("High Actions", high_r)
            c4.metric("APIs Affected", len(set(r["target_api"] for r in responses)))

            st.markdown("---")
            st.subheader("Response Log")
            response_df = pd.DataFrame(responses)[["timestamp","target_api","attack_type","severity","automated_action","escalation_path","status"]]
            if st.session_state.enable_colors:
                st.dataframe(response_df.style.apply(color_risk, axis=1), use_container_width=True, height=300)
            else:
                st.dataframe(response_df, use_container_width=True, height=300)

            # Detailed response cards (critical only)
            crit_responses = [r for r in responses if r["severity"] == "Critical"]
            if crit_responses:
                st.subheader("🔴 Critical Response Playbooks")
                for r in crit_responses[:5]:
                    with st.expander(f"🔴 {r['target_api']} — {r['attack_type']}", expanded=False):
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f"**Action:** `{r['automated_action']}`")
                            st.markdown(f"**Escalation:** {r['escalation_path']}")
                            st.markdown(f"**ETA:** {r['estimated_time']}")
                        with c2:
                            st.markdown("**Response Steps:**")
                            for i, step in enumerate(r.get("response_steps", []), 1):
                                st.markdown(f"  {i}. {step}")

    with tab2:
        st.subheader("🔒 API Kill Switch")
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("**Automatically Isolated APIs** (≥5 attacks detected)")
            if not st.session_state.blocked_apis:
                st.success("✅ No APIs currently isolated.")
            else:
                blocked_df = pd.DataFrame({
                    "API": st.session_state.blocked_apis,
                    "Status": ["BLOCKED"] * len(st.session_state.blocked_apis),
                    "Containment": ["Traffic Terminated"] * len(st.session_state.blocked_apis),
                })
                st.error(f"⚠️ {len(st.session_state.blocked_apis)} API(s) have been automatically isolated.")
                st.dataframe(blocked_df, use_container_width=True)

        with col_right:
            st.markdown("**Manual Operator Control**")
            manual_target = st.selectbox("Select API to isolate", api_data["api_name"].tolist(), key="kill_switch_select")
            action_choice = st.radio("Action", ["Isolate API", "Redirect to Honeypot"], key="kill_action")
            if st.button("⚡ Execute", key="kill_execute", use_container_width=True):
                if action_choice == "Isolate API":
                    result = manual_isolate_api(manual_target)
                    if manual_target not in st.session_state.blocked_apis:
                        st.session_state.blocked_apis.append(manual_target)
                    st.error(f"🔒 `{manual_target}` isolated via {result['isolation_method']}")
                else:
                    result = deploy_honeypot_redirect(manual_target)
                    if manual_target not in st.session_state.honeypot_deployed:
                        st.session_state.honeypot_deployed.append(manual_target)
                    st.warning(f"🍯 `{manual_target}` redirected to honeypot")

            if st.button("🔓 Release All Blocks", key="release_all"):
                st.session_state.blocked_apis = []
                st.success("All API blocks released.")

    with tab3:
        st.subheader("🛡 Automated Defense Workflow")
        st.markdown("""
        <div class='intel-panel'>
        <div style='font-size:13px;color:#a0aec0;line-height:2;'>
        <b style='color:#63b3ed;'>Detection →</b> Risk scoring + zombie classification engine runs on all API traffic<br/>
        <b style='color:#f6ad55;'>Analysis →</b> Pattern analysis identifies lateral movement and escalation paths<br/>
        <b style='color:#f6e05e;'>Response →</b> Automated playbooks trigger based on severity threshold<br/>
        <b style='color:#fc8181;'>Containment →</b> Kill switch isolates APIs with ≥5 detected attack events<br/>
        <b style='color:#9f7aea;'>Intelligence →</b> Honeypot data enriches attacker profiling<br/>
        <b style='color:#68d391;'>Recovery →</b> Operator reviews incident report and releases blocks after remediation
        </div>
        </div>
        """, unsafe_allow_html=True)

        fig_flow = go.Figure()
        stages = ["Detect", "Analyze", "Respond", "Contain", "Enrich", "Recover"]
        colors_flow = ["#63b3ed","#f6ad55","#f6e05e","#fc8181","#9f7aea","#68d391"]
        for i, (stage, color) in enumerate(zip(stages, colors_flow)):
            fig_flow.add_trace(go.Scatter(
                x=[i], y=[0], mode="markers+text",
                text=[stage], textposition="top center",
                marker=dict(size=40, color=color, line=dict(color="#060b18", width=3)),
                textfont=dict(color="#e2e8f0", size=12),
            ))
            if i > 0:
                fig_flow.add_shape(type="line", x0=i-1, y0=0, x1=i, y1=0,
                                   line=dict(color="rgba(255,255,255,0.15)", width=2, dash="dot"))
        fig_flow.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False, height=180,
            xaxis=dict(visible=False), yaxis=dict(visible=False, range=[-0.5, 0.6]),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_flow, use_container_width=True)

# ─────────────────────────────────────────────
# PAGE: SOC ANALYST
# ─────────────────────────────────────────────
elif page == "soc_analyst":
    st.markdown("""
    <div class='page-header'>
      <div>
        <div class='page-title'>🔍 LLM SOC Analyst</div>
        <div class='page-subtitle'>AI-generated threat intelligence summary for security operations</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    soc_summary = generate_soc_summary(st.session_state.attack_history)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("SOC Intelligence Report")
        st.code(soc_summary, language=None)
    with col_right:
        st.subheader("Session Statistics")
        attacks = st.session_state.attack_history
        if attacks:
            sev_counts = pd.Series([a["severity"] for a in attacks]).value_counts()
            fig_donut = px.pie(
                values=sev_counts.values, names=sev_counts.index,
                color_discrete_map={"Critical":"#fc8181","High":"#f6ad55","Medium":"#f6e05e","Low":"#68d391"},
                hole=0.6, title="Severity Breakdown",
            )
            fig_donut.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0",
                margin=dict(l=0,r=0,t=30,b=0), height=240,
                legend=dict(font=dict(size=11)),
            )
            st.plotly_chart(fig_donut, use_container_width=True)

            api_target_counts = pd.Series([a["api_target"] for a in attacks]).value_counts().head(6)
            fig_bar = px.bar(
                x=api_target_counts.values, y=api_target_counts.index, orientation="h",
                title="Top Targeted APIs",
                color=api_target_counts.values,
                color_continuous_scale=["#1a2540","#f6ad55","#fc8181"],
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0", margin=dict(l=0,r=0,t=30,b=0),
                showlegend=False, coloraxis_showscale=False,
                yaxis=dict(tickfont=dict(size=10)),
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No attack data yet.")

    st.markdown("---")
    render_api_selector("soc")

# ─────────────────────────────────────────────
# PAGE: INCIDENT REPORTS
# ─────────────────────────────────────────────
elif page == "incidents":
    st.markdown("""
    <div class='page-header'>
      <div>
        <div class='page-title'>📄 AI Incident Report Generator</div>
        <div class='page-subtitle'>Generate professional PDF compliance reports for SOC teams</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    soc_summary = generate_soc_summary(st.session_state.attack_history)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Report Configuration")
        st.markdown(f"""
        <div class='soc-card'>
          <div class='soc-card-title'>Session Data</div>
          <div class='intel-row'><span class='intel-label'>Total Events</span><span class='intel-value'>{len(st.session_state.attack_history)}</span></div>
          <div class='intel-row'><span class='intel-label'>Critical</span><span class='intel-value' style='color:#fc8181;'>{len([x for x in st.session_state.attack_history if x.get("severity")=="Critical"])}</span></div>
          <div class='intel-row'><span class='intel-label'>Blocked APIs</span><span class='intel-value'>{len(st.session_state.blocked_apis)}</span></div>
          <div class='intel-row'><span class='intel-label'>Generated</span><span class='intel-value'>{datetime.now().strftime("%Y-%m-%d %H:%M")}</span></div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📄 Generate PDF Report", use_container_width=True, type="primary"):
            with st.spinner("Generating incident report..."):
                report_path = generate_incident_report(st.session_state.attack_history, soc_summary)
            with open(report_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=f,
                    file_name=report_path,
                    mime="application/pdf",
                    use_container_width=True,
                )
            st.success("✅ Incident report generated successfully.")

    with col2:
        st.subheader("Report Preview")
        st.code(soc_summary, language=None)

# ─────────────────────────────────────────────
# PAGE: EXECUTIVE SUMMARY
# ─────────────────────────────────────────────
elif page == "executive":
    st.markdown("""
    <div class='page-header'>
      <div>
        <div class='page-title'>📊 Executive SOC Intelligence Summary</div>
        <div class='page-subtitle'>C-suite security posture overview</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    attacks = st.session_state.attack_history
    total_atk = len(attacks)
    crit_atk = len([x for x in attacks if x.get("severity") == "Critical"])
    high_atk  = len([x for x in attacks if x.get("severity") == "High"])
    blocked   = len(st.session_state.blocked_apis)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Total APIs", total_apis)
    c2.metric("Zombie APIs", zombie_apis, delta=f"+{zombie_apis}" if zombie_apis else None, delta_color="inverse")
    c3.metric("Attack Events", total_atk)
    c4.metric("Critical Threats", crit_atk, delta=None)
    c5.metric("Blocked APIs", blocked)
    c6.metric("Risk Score (Avg)", f"{int(api_data['risk_score'].mean())}/100")

    st.markdown("---")

    left, right = st.columns(2)
    with left:
        # Risk distribution bar
        threat_counts = api_data["threat_level"].value_counts().reindex(["Critical","High","Medium","Low"]).fillna(0)
        fig_risk = px.bar(
            x=threat_counts.index, y=threat_counts.values,
            color=threat_counts.index,
            color_discrete_map={"Critical":"#fc8181","High":"#f6ad55","Medium":"#f6e05e","Low":"#68d391"},
            title="API Risk Distribution",
        )
        fig_risk.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", showlegend=False,
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    with right:
        if attacks:
            sev_series = pd.Series([a["severity"] for a in attacks]).value_counts()
            fig_sev = px.pie(
                values=sev_series.values, names=sev_series.index,
                color_discrete_map={"Critical":"#fc8181","High":"#f6ad55","Medium":"#f6e05e","Low":"#68d391"},
                hole=0.55, title="Attack Severity Distribution",
            )
            fig_sev.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0",
                margin=dict(l=0,r=0,t=30,b=0),
            )
            st.plotly_chart(fig_sev, use_container_width=True)
        else:
            st.info("No attack data yet.")

    # Executive brief
    posture = "Critical" if crit_atk > 3 else ("High" if high_atk > 5 else "Elevated" if total_atk > 0 else "Stable")
    color = "#fc8181" if posture == "Critical" else ("#f6ad55" if posture in ("High","Elevated") else "#68d391")
    st.markdown(f"""
    <div class='intel-panel' style='margin-top:16px;'>
      <div class='intel-header'>📊 Executive Security Brief</div>
      <div style='font-size:14px;color:#a0aec0;line-height:2.0;'>
        <b>Security Posture:</b> <span style='color:{color};font-weight:700;'>{posture}</span><br/>
        NECROS X has autonomously analyzed the API infrastructure across <b>{total_apis}</b> endpoints.
        <b style='color:#fc8181;'>{zombie_apis}</b> zombie APIs were identified as unmanaged and exposed.
        {"A total of <b style='color:#fc8181;'>" + str(total_atk) + "</b> attack events were detected, with <b>" + str(crit_atk) + "</b> classified as critical severity." if total_atk > 0 else "No attack events have been detected in this session."}
        {"<br/><b style='color:#fc8181;'>" + str(blocked) + "</b> APIs have been automatically isolated by the kill-switch engine." if blocked > 0 else ""}
        <br/><br/>
        <b>Recommended Executive Action:</b>
        Enforce Zero Trust architecture across all legacy API endpoints.
        Prioritize decommissioning of zombie APIs with no active ownership.
        Mandate OAuth2/JWT on all APIs handling sensitive financial data.
      </div>
    </div>
    """, unsafe_allow_html=True)
