"""
NECROS X - Attack Pattern Analysis Module
Analyzes sequences of attacks to identify lateral movement, escalation patterns.
Preserved from original + enhanced with MITRE ATT&CK mapping and timeline analysis.
"""
import pandas as pd


MITRE_MAPPING = {
    "Privilege Escalation Attempt": "TA0004 - Privilege Escalation",
    "Lateral Movement Across Legacy Systems": "TA0008 - Lateral Movement",
    "Financial Infrastructure Targeting": "TA0040 - Impact / Financial Fraud",
    "Credential Harvesting": "TA0006 - Credential Access",
    "Reconnaissance": "TA0043 - Reconnaissance",
    "General Reconnaissance": "TA0043 - Reconnaissance",
    "API Enumeration": "T1595.002 - Active Scanning",
    "Session Hijacking": "T1563 - Remote Session Hijacking",
}


def analyze_attack_patterns(attack_history):
    if len(attack_history) < 3:
        return []

    attack_df = pd.DataFrame(attack_history)
    detected_patterns = []

    api_sequence = attack_df["api_target"].tolist()
    attack_type_seq = attack_df["attack_type"].tolist()

    for i in range(len(api_sequence) - 2):
        pattern = (
            f"{api_sequence[i]}"
            f" → "
            f"{api_sequence[i+1]}"
            f" → "
            f"{api_sequence[i+2]}"
        )

        risk = "Low"
        behavior = "General Reconnaissance"
        mitre = MITRE_MAPPING.get("General Reconnaissance", "TA0043")
        description = "Attacker is probing the API surface systematically."

        # Privilege escalation detection
        if "login" in pattern and "admin" in pattern:
            risk = "Critical"
            behavior = "Privilege Escalation Attempt"
            description = "Login → Admin path detected. Attacker likely attempting privilege escalation after credential theft."

        # Lateral movement
        elif "legacy" in pattern or "internal" in pattern:
            risk = "High"
            behavior = "Lateral Movement Across Legacy Systems"
            description = "Movement through legacy/internal APIs. Attacker exploiting unguarded legacy surface."

        # Financial targeting
        elif "payment" in pattern or "transfer" in pattern:
            risk = "High"
            behavior = "Financial Infrastructure Targeting"
            description = "Payment/transfer endpoints being chained. Financial fraud pattern detected."

        # Token/session abuse
        elif "Token Hijacking" in attack_type_seq[i:i+3]:
            risk = "High"
            behavior = "Session Hijacking"
            description = "Token hijacking in attack chain. Session replay attack in progress."

        # Recon pattern
        elif "debug" in pattern or "sandbox" in pattern or "test" in pattern:
            risk = "Medium"
            behavior = "API Enumeration"
            description = "Debug/test endpoints being probed. Attacker mapping internal API surface."

        mitre = MITRE_MAPPING.get(behavior, "TA0043 - Reconnaissance")

        detected_patterns.append({
            "attack_pattern": pattern,
            "behavior_type": behavior,
            "risk_level": risk,
            "description": description,
            "mitre_technique": mitre,
        })

    # Deduplicate by pattern string
    seen = set()
    unique_patterns = []
    for p in detected_patterns:
        if p["attack_pattern"] not in seen:
            seen.add(p["attack_pattern"])
            unique_patterns.append(p)

    return unique_patterns
