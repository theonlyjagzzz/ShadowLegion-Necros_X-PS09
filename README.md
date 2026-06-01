# ⚡ NECROS X — Hackathon Edition

> **Autonomous Zombie API Detection & Defense SOC Dashboard**  
> AI-powered API security operations platform for detecting, profiling, and neutralising zombie APIs in banking infrastructure.

---

## 🏆 What is NECROS X?

NECROS X is a production-grade cybersecurity SOC (Security Operations Center) dashboard built to solve a critical gap in API security: **Zombie APIs** — deprecated, forgotten, or unmanaged API endpoints that remain exposed and exploitable long after they should have been decommissioned.

Banks and financial institutions accumulate hundreds of internal API endpoints over years. Legacy payment gateways, deprecated transfer APIs, internal audit endpoints — these endpoints are often:
- No longer actively monitored
- Running with no authentication (`No_Auth`)
- Handling sensitive financial data
- Invisible to modern security tooling

NECROS X autonomously scans, scores, visualises, and defends against these threats in real time.

---

## 🚀 New in Hackathon Edition

### 🎨 UI/UX Overhaul
- **Enterprise dark theme** — Inter + JetBrains Mono typography, deep navy palette
- **Left sidebar navigation** — persistent across all pages, no page refresh on nav
- **Top LED status bar** — real-time green/amber/red/flashing indicators per API
- **Responsive metric cards** — KPI strip across every page
- **Tabbed module views** — no scrolling required to reach AI outputs

### 🔬 API Intelligence Panel (NEW)
Every API is now clickable and opens a full intelligence panel with:
- Zombie probability score (0–100%) with visual progress bar
- Risk score with severity colour coding
- Authentication analysis (No_Auth / Basic / API_Key / OAuth)
- Traffic & attack analysis (events, breach probability, source IPs)
- AI findings list with root cause identification
- Actionable recommendations with **clickable navigation buttons**
- One-click defense actions (kill switch, honeypot, report)

### 📡 Live Monitoring Improvements
- **Session state preserved** — selected API, filters, graph state all survive live ticks
- **Live event feed sidebar** — events appended, never full-page refresh
- **No st.rerun() thrash** — live mode tick uses time-gated delta check
- **Attack history capped** at 150 events with rolling window

### 🔦 LED Status Panel
| Colour | Meaning |
|--------|---------|
| 🟢 Green solid | API healthy and active |
| 🟡 Amber solid | API deprecated |
| 🔴 Red solid | Zombie API detected |
| 🔴 Flashing red | Active attack detected |
| 🌈 RGB cycling | Honeypot active on endpoint |

### 🤖 AI Intelligence Upgrades
- **Zombie probability** calculated per API (not just binary Zombie/Active status)
- **Prediction confidence** shown alongside future risk scores
- **Root cause cards** per predicted target
- **Recommendation confidence** (58–97%) displayed per API
- **MITRE ATT&CK mapping** on pattern analysis (TA0004, TA0008, TA0040…)
- **Clickable recommendations** navigate directly to the relevant module

### 🕸️ Attack Graph Upgrades
- Node colours map to severity (Critical=red, High=amber, Medium=yellow, Low=green)
- Honeypot APIs show 🍯 label and purple glow
- Node tooltips include: API name, severity, attack count, last attack type, source IP
- Click-to-inspect: select any API from dropdown to open Intelligence Panel inline

### ⚡ Defense Upgrades
- **Automated response playbooks** with full step-by-step actions per severity
- **MITRE-mapped escalation paths** (L1 Analyst → Security Engineer → CISO)
- **Manual operator kill switch** — isolate or honeypot any API on demand
- **Honeypot deployment** — redirect any API to honeypot at runtime
- **Defense workflow diagram** — interactive Plotly flow chart

### 🍯 Honeypot Center Upgrades
- Captured payload category classification
- Per-IP threat score aggregation
- Intelligence report generation per attacker
- Attack type distribution chart
- Runtime honeypot deployment to any API

### 📄 Incident Report Upgrades
- ReportLab PDF with executive summary section
- Styled statistics table with alternating row colours
- Full attack event log embedded (last 20 events)
- AI SOC summary included in PDF body

---

## 📁 Project Structure

```
NECROS_X_HACKATHON_EDITION/
├── app.py                          # Main Streamlit SOC dashboard (1,550+ lines)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/
│   └── apis.csv                    # Banking API inventory dataset
├── assets/
│   └── styles.css                  # Enterprise dark theme CSS
└── modules/
    ├── __init__.py
    ├── risk_analyzer.py             # Risk scoring + zombie probability + LED status
    ├── attack_simulator.py          # Mock attack log generator (test data)
    ├── honeypot_engine.py           # Honeypot detection + attacker profiling
    ├── attack_path_visualizer.py    # vis.js interactive network graph
    ├── predictive_threat_engine.py  # Future target prediction + confidence
    ├── ai_recommendation_engine.py  # Security recommendations + API intelligence
    ├── attack_pattern_analysis.py   # Pattern detection + MITRE ATT&CK mapping
    ├── automated_response_system.py # Defense playbooks + escalation paths
    ├── llm_soc_analyst.py           # SOC summary generator
    ├── incident_report_generator.py # ReportLab PDF incident reports
    └── api_kill_switch.py           # API isolation + honeypot redirect
```

---

## 🖥️ Navigation Pages

| Page | Description |
|------|-------------|
| 🏠 Dashboard Overview | API inventory, LED panel, risk charts, API Intelligence |
| 📡 Threat Monitoring | Live event feed, attack table, severity timeline |
| 🍯 Honeypot Intelligence | Captured intrusions, attacker profiles, deployment |
| 🕸️ Attack Visualization | Interactive attack path graph (vis.js) |
| 🤖 AI Intelligence | Predictions, heatmap, recommendations, patterns |
| ⚡ Autonomous Response | Playbooks, kill switch, defense workflow |
| 🔍 SOC Analyst | AI-generated intelligence summary |
| 📄 Incident Reports | PDF report generation & download |
| 📊 Executive Summary | C-suite security posture overview |

---

## ⚙️ Installation & Running

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the dashboard

```bash
streamlit run app.py
```

### 3. Open in browser

```
http://localhost:8501
```

---

## 🧪 Generating Test Data

The platform ships with a **mock attack simulator** for testing and demonstration:

- **Sidebar → `＋1 Attack`** — inject a single simulated attack event
- **Sidebar → `＋10 Attacks`** — inject a coordinated attack burst
- **Sidebar → `🔴 LIVE MONITORING`** — stream attack events continuously (2.5s interval)
- **Sidebar → `🗑 Clear Events`** — reset all attack history

> All attack data is randomly generated from a fixed set of API targets, attack types, source IPs and severity levels. No real network requests are made.

---

## 🔒 Core Security Features

### Zombie API Detection
APIs are scored using a weighted risk model:
- **+40** — Zombie status
- **+25** — Deprecated status  
- **+30** — No authentication (`No_Auth`)
- **+20** — Handles sensitive data
- **+10–20** — Last used > 100 / 300 days ago

### Automated Kill Switch
APIs receiving **≥5 attack events** are automatically isolated and added to the blocked list.

### Honeypot APIs (Default)
Five zombie APIs are pre-configured as honeypots:
- `legacy_transfer_api`
- `old_payment_gateway`
- `internal_audit_api`
- `debug_api`
- `test_admin_api`

Any attacker probing these endpoints is profiled and scored.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Dashboard framework | Streamlit |
| Data processing | Pandas, NumPy |
| Visualisation | Plotly, pyvis (vis.js) |
| PDF generation | ReportLab |
| Network graphs | pyvis (vis.js NetworkX wrapper) |
| Styling | CSS3 custom (Inter + JetBrains Mono) |
| Language | Python 3.10+ |

---

## 📊 Sample API Dataset

The platform ships with 15 banking APIs:

| API | Status | Risk | Auth |
|-----|--------|------|------|
| login_api | Active | Medium | OAuth |
| payment_api | Active | Medium | OAuth |
| legacy_transfer_api | Deprecated | Critical | No_Auth |
| old_payment_gateway | Zombie | Critical | No_Auth |
| test_admin_api | Zombie | Critical | No_Auth |
| debug_api | Zombie | High | No_Auth |
| internal_audit_api | Zombie | Critical | No_Auth |
| sandbox_api | Deprecated | High | No_Auth |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│                   NECROS X SOC DASHBOARD              │
│                      (Streamlit)                      │
├──────────────────┬───────────────────────────────────┤
│   LEFT SIDEBAR   │        MAIN CONTENT AREA          │
│  ─────────────   │  ──────────────────────────────   │
│  Logo + Status   │  Top LED Status Bar               │
│  Navigation      │  Page-specific content            │
│  Live Controls   │  API Intelligence Panel           │
│  Sim Controls    │  Live Event Feed                  │
└──────────────────┴───────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   Risk Engine        Attack Engine      Defense Engine
  ─────────────      ──────────────     ──────────────
  risk_analyzer      attack_simulator   api_kill_switch
  predictive_        attack_path_       automated_
  threat_engine      visualizer         response_system
  ai_recommendation  attack_pattern_    honeypot_engine
  _engine            analysis
                           │
                    ┌──────┴──────┐
                    ▼             ▼
              SOC Analyst    Incident Reports
             ────────────   ───────────────
             llm_soc_       incident_report_
             analyst        generator
```

---

## 📝 Change Log (Hackathon Edition)

### UI
- [NEW] Enterprise dark theme with Inter + JetBrains Mono typography
- [NEW] Left sidebar with persistent navigation and status summary
- [NEW] Top LED status bar (green/amber/red/flashing/RGB)
- [NEW] Tabbed views eliminating scroll depth
- [NEW] Animated LED indicators per API in Dashboard
- [IMPROVED] All charts use dark transparent backgrounds

### Intelligence
- [NEW] API Intelligence Panel (zombie prob, breach prob, auth analysis, findings)
- [NEW] Clickable API selector on every page → opens Intelligence Panel inline
- [NEW] Recommendation confidence scores
- [NEW] Prediction confidence scores
- [NEW] Root cause analysis cards
- [NEW] MITRE ATT&CK mapping on attack patterns
- [IMPROVED] Honeypot engine enriches captures with attack category + threat score

### Monitoring
- [NEW] Live event feed (appends only, no full-page refresh)
- [NEW] Session-preserved selected API across live ticks
- [NEW] Time-gated live mode (2.5s delta, no thrash)
- [IMPROVED] Attack history capped + rolling at 150 events

### Defense
- [NEW] Playbook steps per response (not just action label)
- [NEW] Manual operator kill switch UI
- [NEW] Runtime honeypot deployment to any API
- [NEW] Defense workflow diagram (Plotly flow chart)
- [IMPROVED] Kill switch tracks isolation method and timestamp

### Reports
- [NEW] Executive summary section in PDF
- [NEW] Styled statistics table in PDF
- [NEW] Attack event log table in PDF
- [IMPROVED] ReportLab custom paragraph styles

---

## 👥 Credits

Built for the Akto Hackathon 2025.  
Platform architecture inspired by enterprise API security tools including Akto, Salt Security, and Traceable AI.

---

*NECROS X — Because zombie APIs don't die on their own.*
