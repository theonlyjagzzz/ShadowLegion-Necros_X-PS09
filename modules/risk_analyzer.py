"""
NECROS X - Risk Analyzer Module
Calculates API risk scores and threat levels.
Preserved from original + enhanced with zombie probability scoring.
"""


def calculate_risk_score(api):
    risk_score = 0

    # Zombie APIs are dangerous
    if api["status"] == "Zombie":
        risk_score += 40

    # Deprecated APIs are risky
    if api["status"] == "Deprecated":
        risk_score += 25

    # No authentication is highly dangerous
    if api["authentication"] == "No_Auth":
        risk_score += 30

    # Sensitive financial data increases risk
    if api["sensitive_data"] == "Yes":
        risk_score += 20

    # Very old APIs are suspicious
    if api["last_used_days"] > 300:
        risk_score += 20
    elif api["last_used_days"] > 100:
        risk_score += 10

    return min(risk_score, 100)


def classify_threat_level(risk_score):
    if risk_score >= 81:
        return "Critical"
    elif risk_score >= 61:
        return "High"
    elif risk_score >= 31:
        return "Medium"
    else:
        return "Low"


def calculate_zombie_probability(api):
    """Calculate probability that an API is a zombie (0-100%)"""
    score = 0

    if api["status"] == "Zombie":
        score += 50
    elif api["status"] == "Deprecated":
        score += 25

    if api["last_used_days"] > 500:
        score += 30
    elif api["last_used_days"] > 300:
        score += 20
    elif api["last_used_days"] > 100:
        score += 10

    traffic = str(api.get("traffic", "")).lower()
    if traffic in ["no_auth", "very low", "none"]:
        score += 15
    elif traffic == "low":
        score += 8

    if api["authentication"] == "No_Auth":
        score += 10

    return min(score, 100)


def get_severity_color(threat_level):
    """Return CSS color class for a threat level."""
    colors = {
        "Critical": "#ff4b4b",
        "High": "#ff9f43",
        "Medium": "#f9ca24",
        "Low": "#6ab04c",
    }
    return colors.get(threat_level, "#6ab04c")


def get_led_status(api_row):
    """Return LED status for an API: green/amber/red/flashing_red"""
    status = api_row.get("status", "")
    threat = api_row.get("threat_level", "Low")
    if status == "Zombie" and threat == "Critical":
        return "flashing_red"
    elif status == "Zombie":
        return "red"
    elif status == "Deprecated":
        return "amber"
    else:
        return "green"
