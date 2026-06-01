"""
NECROS X - Automated Response System Module
Generates automated defensive actions based on attack severity.
Preserved from original + enhanced with workflow steps, timeline, and defense playbooks.
"""
import pandas as pd
from datetime import datetime


RESPONSE_PLAYBOOKS = {
    "Critical": {
        "action": "BLOCK IP + QUARANTINE API + ENABLE FORENSIC LOGGING",
        "steps": [
            "Immediately block source IP at firewall layer",
            "Quarantine API — redirect traffic to honeypot",
            "Enable full packet capture and forensic logging",
            "Alert SOC team via PagerDuty / Slack",
            "Preserve evidence chain for incident report",
            "Initiate zero-trust lockdown on affected service",
        ],
        "estimated_time": "< 2 minutes (automated)",
        "escalation": "CISO + Legal",
    },
    "High": {
        "action": "RATE LIMIT SOURCE IP + ENABLE TRAFFIC MONITORING",
        "steps": [
            "Apply rate limiting: max 10 req/min from source IP",
            "Enable enhanced traffic monitoring on target API",
            "Flag session for manual SOC review",
            "Notify on-call security engineer",
        ],
        "estimated_time": "< 5 minutes (automated)",
        "escalation": "Security Engineer",
    },
    "Medium": {
        "action": "MONITOR SESSION + INCREASE LOGGING",
        "steps": [
            "Increase logging verbosity on target endpoint",
            "Monitor session for further escalation",
            "Add IP to watchlist for 24h observation",
        ],
        "estimated_time": "< 10 minutes (automated)",
        "escalation": "L1 Analyst",
    },
    "Low": {
        "action": "CONTINUE PASSIVE MONITORING",
        "steps": [
            "Log event for baseline analysis",
            "Continue passive monitoring",
        ],
        "estimated_time": "Passive",
        "escalation": "None",
    },
}


def automated_threat_response(attack_history):
    if len(attack_history) == 0:
        return []

    attack_df = pd.DataFrame(attack_history)
    response_actions = []

    for _, attack in attack_df.iterrows():
        source_ip = attack["source_ip"]
        api = attack["api_target"]
        severity = attack["severity"]
        attack_type = attack["attack_type"]

        playbook = RESPONSE_PLAYBOOKS.get(severity, RESPONSE_PLAYBOOKS["Low"])

        response_actions.append({
            "source_ip": source_ip,
            "target_api": api,
            "attack_type": attack_type,
            "severity": severity,
            "automated_action": playbook["action"],
            "response_steps": playbook["steps"],
            "estimated_time": playbook["estimated_time"],
            "escalation_path": playbook["escalation"],
            "timestamp": attack.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "status": "Executed",
        })

    return response_actions
