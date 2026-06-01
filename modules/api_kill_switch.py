"""
NECROS X - API Kill Switch Module
Activates emergency containment actions for compromised APIs.
Preserved from original + enhanced with action logging and traffic isolation.
"""
import random
from datetime import datetime


CONTAINMENT_ACTIONS = [
    "API Endpoint Isolated — Traffic Blocked",
    "Traffic Redirected to Honeypot",
    "Emergency Firewall Rule Applied",
    "Temporary API Shutdown Initiated",
    "Zero Trust Lockdown Activated",
    "Rate Limiting Override Applied",
    "WAF Block Rule Deployed",
]

ISOLATION_METHODS = [
    "IP Blacklist Rule",
    "API Gateway Policy Block",
    "Reverse Proxy Drop Rule",
    "Load Balancer Drain",
    "DNS Sinkholes",
]


def activate_kill_switch(attacks):
    """
    Activates kill switch containment for Critical-severity attacks.
    Returns list of containment action records.
    """
    responses = []

    for attack in attacks:
        if attack["severity"] == "Critical":
            responses.append({
                "target_api": attack["api_target"],
                "source_ip": attack.get("source_ip", "Unknown"),
                "action": random.choice(CONTAINMENT_ACTIONS),
                "isolation_method": random.choice(ISOLATION_METHODS),
                "status": "Containment Successful",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "severity": "Critical",
            })

    return responses


def manual_isolate_api(api_name):
    """
    Manual operator-triggered API isolation.
    """
    return {
        "target_api": api_name,
        "action": "MANUAL ISOLATION — Operator Initiated",
        "isolation_method": random.choice(ISOLATION_METHODS),
        "status": "Isolated",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "triggered_by": "SOC Operator",
    }


def deploy_honeypot_redirect(api_name):
    """
    Redirect a zombie/deprecated API to honeypot for attacker intelligence.
    """
    return {
        "target_api": api_name,
        "action": "HONEYPOT REDIRECT — Attacker Intelligence Mode",
        "isolation_method": "Traffic Mirroring to Honeypot",
        "status": "Honeypot Active",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "triggered_by": "Automated Response System",
    }
