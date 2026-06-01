```markdown
# ⚡ NECROS X — Hackathon Edition
> **Autonomous Zombie API Detection & Defense SOC Dashboard**
> AI-powered API security operations platform for detecting, profiling, and neutralising zombie APIs in banking infrastructure.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://kp5w4bpbhwfksmjneumuab.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Educational](https://img.shields.io/badge/License-Educational-lightgrey.svg)]()

---

## 🏆 What is NECROS X?

NECROS X is a production-grade cybersecurity SOC (Security Operations Center) dashboard built to solve a critical gap in API security: **Zombie APIs** — deprecated, forgotten, or unmanaged API endpoints that remain exposed and exploitable long after they should have been decommissioned.

Built for **PS9: Zombie API Discovery** from the **PSBs Hackathon Series 2026 (iDEA 2.0)**.

Banks and financial institutions accumulate hundreds of internal API endpoints over years. Legacy payment gateways, deprecated transfer APIs, internal audit endpoints — these endpoints are often:
- No longer actively monitored
- Running with no authentication (`No_Auth`)
- Handling sensitive financial data
- Invisible to modern security tooling

NECROS X autonomously scans, scores, visualises, and defends against these threats in real time.

---

## 🔗 Links

- 🌐 **Live Demo:** [https://kp5w4bpbhwfksmjneumuab.streamlit.app/](https://kp5w4bpbhwfksmjneumuab.streamlit.app/)
- 🎥 **Demo Video:** [https://youtu.be/vfpytiUcflE?si=TKeA3Iokj9kCqU16](https://youtu.be/vfpytiUcflE?si=TKeA3Iokj9kCqU16)

---

## 📚 Table of Contents

- [What is NECROS X?](#-what-is-necros-x)
- [Links](#-links)
- [New in Hackathon Edition](#-new-in-hackathon-edition)
- [Navigation Pages](#️-navigation-pages)
- [How to Run Locally](#-how-to-run-locally)
- [Project Structure](#-project-structure)
- [Tech Stack](#️-tech-stack)
- [Dataset](#-dataset)
- [Core Security Features](#-core-security-features)
- [Known Limitations](#-known-limitations)
- [Future Enhancements](#-future-enhancements)
- [Team](#-team)
- [Hackathon Details](#-hackathon-details)
- [License](#-license)

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

## ⚙️ How to Run Locally

### Prerequisites
- Python 3.8 or higher
- pip package manager

### 1. Clone Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd NECROS_X_HACKATHON_EDITION
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Launch Application

```bash
# Standard
streamlit run app.py

# Windows (if streamlit not found in PATH)
python -m streamlit run app.py
```

### 6. Open Browser

Navigate to `http://localhost:8501`

---

## 📁 Project Structure

```
NECROS_X_HACKATHON_EDITION/
├── app.py                          # Main Streamlit SOC dashboard
├── requirements.txt
├── README.md
├── data/
│   └── apis.csv                    # Synthetic banking API dataset
├── assets/
│   └── styles.css                  # Enterprise dark theme
└── modules/
    ├── risk_analyzer.py
    ├── attack_simulator.py
    ├── honeypot_engine.py
    ├── attack_path_visualizer.py
    ├── predictive_threat_engine.py
    ├── ai_recommendation_engine.py
    ├── attack_pattern_analysis.py
    ├── automated_response_system.py
    ├── llm_soc_analyst.py
    ├── incident_report_generator.py
    └── api_kill_switch.py
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Dashboard framework | Streamlit |
| Data processing | Pandas, NumPy |
| Visualisation | Plotly, PyVis (vis.js) |
| Network analysis | NetworkX |
| PDF generation | ReportLab |
| Language | Python 3.x |

---

## 📊 Dataset

NECROS X uses a **synthetic banking API inventory** created solely for demonstration and testing purposes. The dataset contains simulated APIs across:

- Authentication APIs
- Payment APIs
- Customer APIs
- Account APIs
- Loan APIs
- Administrative APIs

Each record contains: API name, status (Active / Deprecated / Zombie), authentication method, exposure level, last activity, threat indicators, and risk attributes.

> No real customer data, production infrastructure, or bank systems were used.

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
APIs receiving **≥5 attack events** are automatically isolated.

### Honeypot APIs (Default)
Five zombie APIs are pre-configured as honeypots:
- `legacy_transfer_api`
- `old_payment_gateway`
- `internal_audit_api`
- `debug_api`
- `test_admin_api`

---

## ⚠️ Known Limitations

- Uses synthetic banking API inventory data
- Discovery operates on structured datasets, not live infrastructure
- Attack simulations are generated scenarios, not real attacks
- Threat analytics uses heuristic-based prediction
- No direct integration with API gateways, SIEM platforms, or production systems
- Automated responses are simulated and do not execute real containment actions
- Designed as a hackathon proof-of-concept

---

## 🔮 Future Enhancements

- Real-time API discovery from live traffic
- API gateway integration (Kong / Apigee)
- Machine learning-based zombie prediction
- SIEM & SOC platform integration
- Automated threat response orchestration
- Multi-bank threat intelligence sharing
- Enterprise RBAC & audit logging
- Compliance & regulatory reporting

---

## 👥 Team

**Team Name:** Shadow Legion

| Member | Role |
|--------|------|
| Utkarsh Dodmise | ML Lead |
| Mayuresh Jha | Backend Developer |
| Jagriti Prasad | Frontend Developer |
| Ishwari Chaudhari | Domain Research |

---

## 🏆 Hackathon Details

| Field | Detail |
|-------|--------|
| Project | NECROS X — Intelligent Zombie API Security Platform |
| Problem Statement | PS9 — Zombie API Discovery |
| Hackathon | PSBs Hackathon Series 2026 (iDEA 2.0) |

---

## 📝 License

Developed for educational and hackathon purposes. All datasets are synthetic and created solely for demonstration.

---

*NECROS X — Because zombie APIs don't die on their own.*
```
