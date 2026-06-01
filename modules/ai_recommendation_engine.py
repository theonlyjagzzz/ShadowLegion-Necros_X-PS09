"""
NECROS X - AI Recommendation Engine Module
Generates security recommendations based on API risk profiles.
Preserved from original + enhanced with confidence scoring, actionable links, and root cause cards.
"""
import pandas as pd


RECOMMENDATION_ACTIONS = {
    "Critical": [
        {"action": "Activate Kill Switch", "module": "Autonomous Response", "icon": "🔴"},
        {"action": "Deploy Honeypot",      "module": "Honeypot Intelligence", "icon": "🍯"},
        {"action": "View Attack Path",     "module": "Attack Visualization",  "icon": "🕸️"},
        {"action": "Generate Report",      "module": "Incident Reports",      "icon": "📄"},
    ],
    "High": [
        {"action": "Enable Rate Limiting", "module": "Autonomous Response",  "icon": "⚡"},
        {"action": "Monitor Traffic",      "module": "Threat Monitoring",     "icon": "📡"},
        {"action": "View AI Predictions",  "module": "AI Intelligence",       "icon": "🤖"},
    ],
    "Medium": [
        {"action": "Review Access Logs",   "module": "SOC Analyst",           "icon": "🔍"},
        {"action": "Strengthen Auth",      "module": "AI Intelligence",       "icon": "🔐"},
    ],
    "Low": [
        {"action": "Schedule Audit",       "module": "Incident Reports",      "icon": "📋"},
    ],
}

CONFIDENCE_SCORES = {
    "Critical": 94,
    "High":     87,
    "Medium":   71,
    "Low":      58,
}


def generate_security_recommendations(api_data):
    recommendations = []

    for _, row in api_data.iterrows():
        api_name  = row["api_name"]
        risk      = row["threat_level"]
        auth      = row["authentication"]
        status    = row["status"]
        sensitive = row["sensitive_data"]
        last_used = row.get("last_used_days", 0)

        # Build context-aware findings
        findings = []
        if status == "Zombie":
            findings.append("Zombie API — no active owner, unmonitored traffic")
        if status == "Deprecated":
            findings.append("API is Deprecated — scheduled for removal but still reachable")
        if auth == "No_Auth":
            findings.append("No authentication layer — unauthenticated access possible")
        if sensitive == "Yes":
            findings.append("Handles sensitive data — PII/financial exposure risk")
        if last_used > 300:
            findings.append(f"Last used {last_used} days ago — potential zombie vector")

        if risk == "Critical":
            recommendation = (
                "🔴 CRITICAL: Immediate action required.\n"
                "• Disable unused endpoint access immediately\n"
                "• Enable multi-factor authentication\n"
                "• Place API behind secure API gateway\n"
                "• Enable continuous traffic monitoring\n"
                "• Restrict access using IP whitelisting\n"
                "• Rotate all API keys and tokens"
            )
        elif risk == "High":
            recommendation = (
                "🟠 HIGH: Urgent remediation recommended.\n"
                "• Enable OAuth2 / JWT authentication\n"
                "• Monitor for abnormal request patterns\n"
                "• Add rate limiting and throttling\n"
                "• Encrypt sensitive transactions in transit"
            )
        elif risk == "Medium":
            recommendation = (
                "🟡 MEDIUM: Schedule remediation within 30 days.\n"
                "• Review and audit API access logs\n"
                "• Strengthen authentication policy\n"
                "• Monitor failed login / auth attempts\n"
                "• Consider API versioning and deprecation policy"
            )
        else:
            recommendation = (
                "🟢 LOW: Routine maintenance recommended.\n"
                "• Continue periodic security monitoring\n"
                "• Maintain regular security audits\n"
                "• Ensure documentation is current"
            )

        recommendations.append({
            "api_name":      api_name,
            "threat_level":  risk,
            "recommendation": recommendation,
            "findings":      findings,
            "actions":       RECOMMENDATION_ACTIONS.get(risk, []),
            "confidence":    CONFIDENCE_SCORES.get(risk, 60),
        })

    return recommendations


def get_api_intelligence(api_row, attack_history=None):
    """
    Generate a full API Intelligence Panel data dict for a single API.
    api_row may or may not already contain risk_score / threat_level.
    """
    from modules.risk_analyzer import (
        calculate_risk_score,
        classify_threat_level,
        calculate_zombie_probability,
    )

    # Work on a copy so we never mutate the caller's dict
    row = dict(api_row)

    # Ensure computed fields exist
    if "risk_score" not in row:
        row["risk_score"] = calculate_risk_score(row)
    if "threat_level" not in row:
        row["threat_level"] = classify_threat_level(row["risk_score"])

    api_name     = row["api_name"]
    threat_level = row["threat_level"]
    risk_score   = row["risk_score"]
    zombie_prob  = calculate_zombie_probability(row)
    auth         = row.get("authentication", "Unknown")

    # Traffic analysis from attack history
    traffic_events = []
    if attack_history:
        traffic_events = [a for a in attack_history if a.get("api_target") == api_name]

    attack_types_seen = list(set(a.get("attack_type", "") for a in traffic_events))
    source_ips        = list(set(a.get("source_ip", "") for a in traffic_events))
    breach_probs      = [a.get("breach_probability", 0) for a in traffic_events]
    avg_breach        = round(sum(breach_probs) / len(breach_probs), 1) if breach_probs else 0

    # Auth analysis
    auth_analysis = {
        "No_Auth":    "❌ No authentication — completely open endpoint",
        "Basic_Auth": "⚠️ Basic Auth — credentials in plain headers",
        "API_Key":    "🟡 API Key — static key, no token rotation",
        "OAuth":      "✅ OAuth — token-based authentication in place",
    }.get(auth, f"Unknown auth method: {auth}")

    # Findings
    findings = []
    if row.get("status") == "Zombie":
        findings.append("Zombie API — no active ownership or maintenance")
    if row.get("status") == "Deprecated":
        findings.append("Deprecated — still accessible after end-of-life")
    if auth == "No_Auth":
        findings.append("Unauthenticated endpoint — critical exposure")
    if row.get("sensitive_data") == "Yes":
        findings.append("Handles sensitive/financial data")
    if row.get("last_used_days", 0) > 300:
        findings.append(f"Dormant for {row.get('last_used_days')} days")
    if traffic_events:
        findings.append(f"{len(traffic_events)} attack events detected against this endpoint")

    # Recommendations (pass fully-enriched row)
    enriched_df = pd.DataFrame([row])
    recs = generate_security_recommendations(enriched_df)
    rec  = recs[0] if recs else {}

    return {
        "api_name":             api_name,
        "zombie_probability":   zombie_prob,
        "risk_score":           risk_score,
        "threat_level":         threat_level,
        "findings":             findings,
        "traffic_events":       len(traffic_events),
        "attack_types":         attack_types_seen,
        "source_ips":           source_ips,
        "avg_breach_probability": avg_breach,
        "breach_probability":   avg_breach,   # alias for test assertions
        "auth_analysis":        auth_analysis,
        "recommendation":       rec.get("recommendation", ""),
        "actions":              rec.get("actions", []),
        "confidence":           rec.get("confidence", 60),
        "status":               row.get("status", "Unknown"),
        "authentication":       auth,
        "sensitive_data":       row.get("sensitive_data", "No"),
        "last_used_days":       row.get("last_used_days", 0),
        "traffic":              row.get("traffic", "Unknown"),
    }
