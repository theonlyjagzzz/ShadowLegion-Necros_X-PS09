"""
NECROS X - Predictive Threat Engine Module
AI prediction of future attack targets based on historical patterns.
Preserved from original + enhanced with confidence scoring and root cause analysis.
"""
import pandas as pd


def predict_future_targets(attack_history):
    if len(attack_history) == 0:
        return pd.DataFrame()

    attack_df = pd.DataFrame(attack_history)

    # Count attacks per API
    api_counts = (
        attack_df["api_target"]
        .value_counts()
        .reset_index()
    )
    api_counts.columns = ["api_name", "attack_count"]

    max_attacks = api_counts["attack_count"].max()

    api_counts["prediction_score"] = (
        api_counts["attack_count"] / max_attacks
    ) * 100

    # Confidence: more data = higher confidence
    total_events = len(attack_history)
    base_confidence = min(55 + (total_events * 1.5), 95)

    api_counts["confidence"] = api_counts["prediction_score"].apply(
        lambda s: round(min(base_confidence * (s / 100) + 30, 97), 1)
    )

    def classify_prediction(score):
        if score >= 80:
            return "Critical"
        elif score >= 60:
            return "High"
        elif score >= 40:
            return "Medium"
        else:
            return "Low"

    api_counts["future_risk"] = api_counts["prediction_score"].apply(classify_prediction)

    def root_cause(row):
        api = row["api_name"]
        if "legacy" in api or "old" in api:
            return "Legacy endpoint — unpatched, no auth enforcement"
        elif "admin" in api:
            return "Privileged endpoint — high-value target for privilege escalation"
        elif "payment" in api or "transfer" in api:
            return "Financial endpoint — prime target for fraud attacks"
        elif "debug" in api or "test" in api or "sandbox" in api:
            return "Dev/test endpoint exposed to production traffic"
        elif "login" in api:
            return "Auth endpoint — credential stuffing / brute force target"
        else:
            return "Repeated pattern detected — attacker probing attack surface"

    api_counts["root_cause"] = api_counts.apply(root_cause, axis=1)

    return api_counts
