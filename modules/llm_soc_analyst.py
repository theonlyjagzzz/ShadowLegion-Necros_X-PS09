"""
NECROS X - LLM SOC Analyst Module
Generates structured SOC analysis summaries from attack telemetry.
Preserved from original + enhanced with structured threat intelligence sections.
"""
from datetime import datetime


def generate_soc_summary(attack_history):
    if len(attack_history) == 0:
        return """SOC ANALYST REPORT
══════════════════════════════

Status: STABLE — No active threats

No attacks detected in current session.
System monitoring is active.
All honeypots are listening.
API kill switch is on standby.
"""

    total_attacks = len(attack_history)

    critical_count = len([a for a in attack_history if a["severity"] == "Critical"])
    high_count = len([a for a in attack_history if a["severity"] == "High"])
    medium_count = len([a for a in attack_history if a["severity"] == "Medium"])
    low_count = len([a for a in attack_history if a["severity"] == "Low"])

    targeted_apis = list(set(a["api_target"] for a in attack_history))
    source_ips = list(set(a["source_ip"] for a in attack_history))
    attack_types = list(set(a["attack_type"] for a in attack_history))

    # Most targeted API
    api_counts = {}
    for a in attack_history:
        api_counts[a["api_target"]] = api_counts.get(a["api_target"], 0) + 1
    top_api = max(api_counts, key=api_counts.get)
    top_api_count = api_counts[top_api]

    # Most active source IP
    ip_counts = {}
    for a in attack_history:
        ip_counts[a["source_ip"]] = ip_counts.get(a["source_ip"], 0) + 1
    top_ip = max(ip_counts, key=ip_counts.get)
    top_ip_count = ip_counts[top_ip]

    # Status classification
    if critical_count > 0:
        overall_status = "🔴 CRITICAL — Active Breach Indicators"
    elif high_count > 0:
        overall_status = "🟠 HIGH — Elevated Threat Activity"
    elif medium_count > 0:
        overall_status = "🟡 MEDIUM — Suspicious Activity Detected"
    else:
        overall_status = "🟢 LOW — Normal Baseline Activity"

    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    summary = f"""SOC ANALYST REPORT
Generated: {report_time}
══════════════════════════════════════════

OVERALL STATUS: {overall_status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATTACK TELEMETRY SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Events Detected : {total_attacks}
  Critical            : {critical_count}
  High                : {high_count}
  Medium              : {medium_count}
  Low                 : {low_count}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TARGET ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
APIs Under Attack     : {len(targeted_apis)}
Most Targeted API     : {top_api} ({top_api_count} hits)
All Targeted APIs     : {', '.join(targeted_apis)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THREAT ACTOR PROFILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Unique Source IPs     : {len(source_ips)}
Most Active IP        : {top_ip} ({top_ip_count} events)
Attack Techniques     : {', '.join(attack_types)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANALYST ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Attackers are actively probing the API infrastructure.
Patterns indicate {"coordinated multi-vector intrusion" if len(source_ips) > 2 else "targeted intrusion attempts"}.
{"Legacy/zombie APIs are primary attack vectors." if any("legacy" in a or "old" in a or "debug" in a for a in targeted_apis) else "Modern API endpoints are being targeted."}
{"Financial APIs are under direct attack — elevated fraud risk." if any("payment" in a or "transfer" in a for a in targeted_apis) else ""}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDED SOC ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Enable stricter API authentication on all zombie endpoints
2. Monitor honeypot activity for attacker intelligence
3. Activate automated response escalation for Critical events
4. Review attack path graph for lateral movement indicators
5. Generate formal incident report for compliance record
"""

    return summary
