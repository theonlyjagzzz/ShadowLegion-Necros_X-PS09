"""
NECROS X - Honeypot Engine Module
Detects and profiles attackers who probe honeypot APIs.
Preserved from original + enhanced with threat intelligence scoring and payload capture.
"""
import pandas as pd
import random

# Zombie APIs converted into honeypots
HONEYPOT_APIS = [
    "legacy_transfer_api",
    "old_payment_gateway",
    "internal_audit_api",
    "debug_api",
    "test_admin_api",
]

ATTACK_CATEGORIES = {
    "SQL Injection": "Data Exfiltration",
    "Brute Force": "Credential Harvesting",
    "Token Hijacking": "Session Takeover",
    "Privilege Escalation": "Unauthorized Access",
    "API Abuse": "Reconnaissance",
    "Credential Stuffing": "Account Takeover",
    "BOLA / IDOR": "Horizontal Privilege Escalation",
    "Mass Assignment": "Parameter Tampering",
    "Rate Limit Bypass": "DDoS / Flood",
    "Server-Side Request Forgery": "Internal Network Pivot",
}

THREAT_SCORES = {
    "Critical": 95,
    "High": 72,
    "Medium": 45,
    "Low": 18,
}

INTELLIGENCE_REPORTS = [
    "IP matches known botnet C2 range. Likely automated scanner.",
    "Geolocation: Eastern Europe. Matches APT-41 TTP profile.",
    "Traffic pattern consistent with credential stuffing toolkit.",
    "Multiple honeypot interactions detected — persistent threat actor.",
    "First seen 48 hrs ago. Rapid escalation pattern.",
    "Payload signatures match open-source exploitation framework.",
]


def analyze_honeypot_activity(attack_logs):
    honeypot_hits = []
    for attack in attack_logs:
        if attack.get("api_target") in HONEYPOT_APIS:
            enriched = dict(attack)
            enriched["honeypot_triggered"] = "YES"
            enriched["attack_category"] = ATTACK_CATEGORIES.get(
                attack.get("attack_type", ""), "Unknown"
            )
            enriched["threat_score"] = THREAT_SCORES.get(
                attack.get("severity", "Low"), 18
            )
            enriched["intelligence_report"] = random.choice(INTELLIGENCE_REPORTS)
            honeypot_hits.append(enriched)
    return pd.DataFrame(honeypot_hits)


def generate_attacker_profile(honeypot_logs):
    if honeypot_logs.empty:
        return pd.DataFrame()

    attacker_profiles = (
        honeypot_logs.groupby("source_ip")
        .agg(
            honeypot_hits=("source_ip", "count"),
            avg_threat_score=("threat_score", "mean") if "threat_score" in honeypot_logs.columns else ("source_ip", "count"),
            last_seen=("timestamp", "max") if "timestamp" in honeypot_logs.columns else ("source_ip", "first"),
        )
        .reset_index()
    )

    def classify_attacker(hits):
        if hits >= 5:
            return "Critical"
        elif hits >= 3:
            return "High"
        elif hits >= 2:
            return "Medium"
        else:
            return "Low"

    attacker_profiles["threat_level"] = attacker_profiles["honeypot_hits"].apply(classify_attacker)
    attacker_profiles["intel_summary"] = attacker_profiles["source_ip"].apply(
        lambda _: random.choice(INTELLIGENCE_REPORTS)
    )

    return attacker_profiles


def get_honeypot_apis():
    return HONEYPOT_APIS
