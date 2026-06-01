# NECROS X — Intelligent Zombie API Security Platform

## Problem Statement

This project addresses **PS9: Zombie API Discovery** from the **PSBs Hackathon Series 2026 (iDEA 2.0)**.

NECROS X helps financial institutions discover unmanaged APIs, classify them as Active, Deprecated, or Zombie, assess security risks, visualize attack paths, simulate cyberattacks, deploy honeypot defenses, and provide automated response recommendations through a centralized Security Operations Center (SOC) dashboard.

Unlike traditional API security tools that focus only on known APIs, NECROS X identifies hidden attack surfaces and transforms vulnerable zombie APIs into monitored defensive assets.

---

## Live Demo

🔗 **Live Demo:** [https://kp5w4bpbhwfksmjneumuab.streamlit.app/](https://kp5w4bpbhwfksmjneumuab.streamlit.app/)  
🎥 **Demo Video:** [https://youtu.be/vfpytiUcflE?si=TKeA3Iokj9kCqU16](https://youtu.be/vfpytiUcflE?si=TKeA3Iokj9kCqU16)

---

## Tech Stack

| Category | Technologies |
|----------|--------------|
| **Frontend** | Streamlit, Plotly, PyVis |
| **Backend** | Python 3.x, Pandas, NumPy |
| **Security & Analytics** | NetworkX, Custom Risk Scoring Engine, Predictive Threat Analytics, Attack Simulation Engine, Honeypot Intelligence Framework |
| **Reporting** | ReportLab |
| **Data** | Synthetic Banking API Dataset (CSV) |

---

## How to Run Locally

### 1. Clone Repository
```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd NECROS_X
2. Create Virtual Environment
bash
python -m venv venv
3. Activate Environment
Windows:

bash
venv\Scripts\activate
Linux / macOS:

bash
source venv/bin/activate
4. Install Dependencies
bash
pip install -r requirements.txt
5. Launch Application
bash
streamlit run app.py
6. Open Browser
text
http://localhost:8501
Project Structure
text
NECROS_X/
├── app.py
├── data/
│   └── apis.csv
├── modules/
│   ├── risk_analyzer.py
│   ├── attack_simulator.py
│   ├── attack_path_visualizer.py
│   ├── honeypot_engine.py
│   ├── predictive_threat_engine.py
│   ├── automated_response_system.py
│   ├── api_kill_switch.py
│   └── incident_report_generator.py
├── assets/
├── reports/
├── requirements.txt
└── README.md
Dataset
NECROS X uses a synthetic banking API inventory created solely for demonstration and testing purposes.

The dataset contains simulated APIs across multiple banking domains:

Authentication APIs

Payment APIs

Customer APIs

Account APIs

Loan APIs

Administrative APIs

Each API record contains: API Name, Endpoint, API Status (Active / Deprecated / Zombie), Authentication Method, Exposure Level, Last Activity Timestamp, Owner Information, Threat Indicators, and Risk Attributes.

No real customer data, production infrastructure, or bank systems were used.

Core Features
API Discovery & Inventory Analysis – Simulated discovery, enumeration, lifecycle identification

Zombie API Detection – Classifies APIs as Active, Deprecated, or Zombie

Security Risk Analysis – Risk score (0–100), threat categorization, critical asset identification

Predictive Threat Analytics – Future high-risk API identification, risk forecasting

Attack Path Visualization – Interactive API relationship graph, attacker movement paths

Attack Simulation Engine – SQL injection, token hijacking, brute force, lateral movement

Honeypot Defense System – Converts zombie APIs into decoys, attacker profiling, threat intelligence

Automated Response Engine – API quarantine recommendations, kill switch activation, alerting

SOC Dashboard – API inventory, zombie statistics, threat monitoring, risk analysis

Incident Reporting – PDF reports with executive summaries and attack logs

New in Hackathon Edition (Detailed Enhancements)
🎨 UI/UX Overhaul
Enterprise dark theme (Inter + JetBrains Mono, deep navy palette)

Persistent left sidebar navigation (no page refresh)

Top LED status bar (real-time green/amber/red/flashing indicators per API)

Responsive metric cards (KPI strip across all pages)

Tabbed module views (no scrolling to reach AI outputs)

🔬 API Intelligence Panel (NEW)
Every API is clickable and opens a full panel with:

Zombie probability score (0–100%) + visual progress bar

Risk score + severity colour coding

Authentication analysis (No_Auth / Basic / API_Key / OAuth)

Traffic & attack analysis (events, breach probability, source IPs)

AI findings list with root cause identification

Actionable recommendations with clickable navigation buttons

One-click defense actions (kill switch, honeypot, report)

📡 Live Monitoring Improvements
Session state preserved (selected API, filters, graph state survive live ticks)

Live event feed sidebar (events appended, no full-page refresh)

Attack history capped at 150 events (rolling window)

🔦 LED Status Panel
Colour	Meaning
🟢 Green solid	API healthy and active
🟡 Amber solid	API deprecated
🔴 Red solid	Zombie API detected
🔴 Flashing red	Active attack detected
🌈 RGB cycling	Honeypot active on endpoint
🤖 AI Intelligence Upgrades
Zombie probability per API (not just binary status)

Prediction confidence alongside future risk scores

Root cause cards per predicted target

Recommendation confidence (58–97%) displayed per API

MITRE ATT&CK mapping (TA0004, TA0008, TA0040…)

Clickable recommendations navigate directly to relevant module

🕸️ Attack Graph Upgrades
Node colours map to severity (Critical=red, High=amber, Medium=yellow, Low=green)

Honeypot APIs show 🍯 label and purple glow

Node tooltips include API name, severity, attack count, last attack type, source IP

Click-to-inspect: select API from dropdown to open Intelligence Panel inline

⚡ Defense Upgrades
Automated response playbooks with step-by-step actions per severity

MITRE-mapped escalation paths (L1 Analyst → Security Engineer → CISO)

Manual operator kill switch (isolate or honeypot any API on demand)

Runtime honeypot deployment to any API

Defense workflow diagram (interactive Plotly flow chart)

🍯 Honeypot Center Upgrades
Captured payload category classification

Per-IP threat score aggregation

Intelligence report generation per attacker

Attack type distribution chart

Runtime honeypot deployment

📄 Incident Report Upgrades
ReportLab PDF with executive summary section

Styled statistics table (alternating row colours)

Full attack event log embedded (last 20 events)

AI SOC summary included in PDF body

Architecture Overview
text
API Inventory
      │
      ▼
API Discovery & Classification
      │
      ▼
Risk Scoring Engine
      │
      ▼
Predictive Threat Analytics
      │
      ▼
Attack Path Analysis
      │
      ▼
Attack Simulation
      │
      ▼
Honeypot Defense System
      │
      ▼
Automated Response Engine
      │
      ▼
SOC Dashboard & Reports
Known Limitations
Uses synthetic banking API inventory data

Discovery operates on structured datasets, not live infrastructure

Attack simulations are generated scenarios, not real attacks

Threat analytics uses heuristic-based prediction

No direct integration with API gateways, SIEM platforms, or production banking systems

Automated responses are simulated and do not execute real containment actions

Designed as a hackathon proof-of-concept

Future Enhancements
Real-time API discovery from live traffic

API gateway integration (Kong / Apigee)

Machine learning-based zombie API prediction

SIEM & SOC platform integration

Automated threat response orchestration

Multi-bank threat intelligence sharing

Enterprise RBAC & audit logging

Compliance & regulatory reporting

Team
Team Name: Shadow Legion

Member	Role
Utkarsh Dodmise	ML Lead
Mayuresh Jha	Backend Developer
Jagriti Prasad	Frontend Developer
Ishwari Chaudhari	Domain Research
Hackathon Details
Field	Detail
Project	NECROS X — Intelligent Zombie API Security Platform
Problem Statement	PS9 — Zombie API Discovery
Hackathon	PSBs Hackathon Series 2026 (iDEA 2.0)
License
This project was developed for educational and hackathon purposes. All datasets used are synthetic and created solely for demonstration.

NECROS X — Because zombie APIs don't die on their own.
