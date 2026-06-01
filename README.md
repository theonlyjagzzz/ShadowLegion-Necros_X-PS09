# NECROS X — Intelligent Zombie API Security Platform

## Problem Statement

This project addresses **PS9: Zombie API Discovery** from the PSBs Hackathon Series 2026.

NECROS X helps financial institutions discover unmanaged APIs, classify them as Active, Deprecated, or Zombie, assess security risks, visualize attack paths, simulate cyberattacks, deploy honeypot defenses, and provide automated response recommendations through a centralized Security Operations Center (SOC) dashboard.

Unlike traditional API security tools that focus only on known APIs, NECROS X identifies hidden attack surfaces and transforms vulnerable zombie APIs into monitored defensive assets.

---

## Live Demo

🔗 Live Demo: https://kp5w4bpbhwfksmjneumuab.streamlit.app/

🎥 Demo Video: https://youtu.be/vfpytiUcflE?si=TKeA3Iokj9kCqU16

---

## Tech Stack

### Frontend

* Streamlit
* Plotly
* PyVis

### Backend

* Python 3.x
* Pandas
* NumPy

### Security & Analytics

* NetworkX
* Custom Risk Scoring Engine
* Predictive Threat Analytics
* Attack Simulation Engine
* Honeypot Intelligence Framework

### Reporting

* ReportLab

### Data

* Synthetic Banking API Dataset (CSV)

---

## How to Run Locally

### 1. Clone Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd NECROS_X
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Launch Application

```bash
streamlit run app.py
```

### 6. Open Browser

```text
http://localhost:8501
```

---

## Project Structure

```text
NECROS_X/

├── app.py
├── data/
│   └── apis.csv
│
├── modules/
│   ├── risk_analyzer.py
│   ├── attack_simulator.py
│   ├── attack_path_visualizer.py
│   ├── honeypot_engine.py
│   ├── predictive_threat_engine.py
│   ├── automated_response_system.py
│   ├── api_kill_switch.py
│   └── incident_report_generator.py
│
├── assets/
├── reports/
├── requirements.txt
└── README.md
```

---

## Dataset

NECROS X uses a synthetic banking API inventory created solely for demonstration and testing purposes.

The dataset contains simulated APIs across multiple banking domains:

* Authentication APIs
* Payment APIs
* Customer APIs
* Account APIs
* Loan APIs
* Administrative APIs

Each API record contains:

* API Name
* Endpoint
* API Status (Active / Deprecated / Zombie)
* Authentication Method
* Exposure Level
* Last Activity Timestamp
* Owner Information
* Threat Indicators
* Risk Attributes

No real customer data, production infrastructure, or Union Bank systems were used.

---

## Core Features

### API Discovery & Inventory Analysis

* Simulated API Discovery
* API Enumeration
* Inventory Processing
* Lifecycle Identification

### Zombie API Detection

* Active API Classification
* Deprecated API Classification
* Zombie API Classification

### Security Risk Analysis

* Risk Score Generation (0–100)
* Threat Categorization
* Critical Asset Identification
* Security Prioritization

### Predictive Threat Analytics

* Future High-Risk API Identification
* Zombie API Risk Forecasting
* Threat Trend Analysis

### Attack Path Visualization

* Interactive API Relationship Graph
* Potential Attacker Movement Paths
* Critical Exposure Analysis

### Attack Simulation Engine

* SQL Injection Simulation
* Token Hijacking Simulation
* Brute Force Attack Simulation
* Lateral Movement Analysis

### Honeypot Defense System

* Zombie API Conversion
* Attacker Profiling
* Threat Intelligence Collection
* Decoy Endpoint Monitoring

### Automated Response Engine

* API Quarantine Recommendations
* Kill Switch Activation
* Security Alert Generation
* Mitigation Suggestions

### SOC Dashboard

* API Inventory Overview
* Zombie API Statistics
* Threat Monitoring
* Risk Analysis Dashboard
* Attack Path Visualization
* Honeypot Intelligence Feed
* Incident Reporting

---

## Architecture Overview

```text
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
```

---

## Known Limitations

* Uses synthetic banking API inventory data.
* Discovery operates on structured datasets rather than live infrastructure.
* Attack simulations are generated scenarios and not real attacks.
* Threat analytics currently uses heuristic-based prediction.
* No direct integration with API gateways, SIEM platforms, or production banking systems.
* Automated responses are simulated and do not execute real containment actions.
* Designed as a hackathon proof-of-concept rather than a production deployment.

---

## Future Enhancements

* Real-Time API Discovery
* API Gateway Integration (Kong / Apigee)
* Live Traffic Monitoring
* Machine Learning-Based Zombie API Prediction
* SIEM & SOC Integration
* Automated Threat Response Orchestration
* Multi-Bank Threat Intelligence Sharing
* Enterprise RBAC & Audit Logging
* Compliance & Regulatory Reporting

---

## Team

### Team Name

**Shadow Legion**

### Team Members

* Utkarsh Dodmise — ML Lead
* Mayuresh Jha — Backend Developer
* Jagriti Prasad — Frontend Developer
* Ishwari Chaudhari — Domain Research

---

## Hackathon Details

**Project:** NECROS X — Intelligent Zombie API Security Platform

**Problem Statement:** PS9 — Zombie API Discovery

**Hackathon:** PSBs Hackathon Series 2026 (iDEA 2.0)

---

## License

This project was developed for educational and hackathon purposes. All datasets used are synthetic and created solely for demonstration.
