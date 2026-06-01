"""
NECROS X - Attack Simulator Module
Generates simulated attack events for testing and demonstration.
Preserved from original + enhanced with payload and breach probability.
"""
import random
from datetime import datetime


ATTACK_TYPES = [
    "SQL Injection",
    "Brute Force",
    "Credential Stuffing",
    "API Abuse",
    "Privilege Escalation",
    "Rate Limit Bypass",
    "Token Hijacking",
    "BOLA / IDOR",
    "Mass Assignment",
    "Server-Side Request Forgery",
]

TARGETED_APIS = [
    "login_api",
    "legacy_transfer_api",
    "old_payment_gateway",
    "admin_api",
    "internal_audit_api",
    "payment_api",
    "upi_transfer_api",
    "debug_api",
    "test_admin_api",
    "sandbox_api",
]

IP_ADDRESSES = [
    "192.168.1.25",
    "45.67.89.10",
    "203.54.1.90",
    "177.23.44.8",
    "99.23.11.45",
    "112.44.77.33",
    "61.19.200.5",
    "87.65.43.21",
]

SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]

PAYLOADS = {
    "SQL Injection": ["' OR 1=1 --", "'; DROP TABLE users;--", "1 UNION SELECT * FROM accounts"],
    "Brute Force": ["admin:admin", "root:password", "user:123456"],
    "Token Hijacking": ["Bearer eyJhbGc...(truncated)", "Authorization: stolen_token_xyz"],
    "API Abuse": ["/api/v1/users?limit=99999", "GET /internal/debug?verbose=true"],
    "Privilege Escalation": ["role=admin&bypass=true", "X-Admin-Override: 1"],
    "BOLA / IDOR": ["/api/users/1337/account", "/api/transactions/all"],
    "Mass Assignment": ['{"role":"admin","verified":true}', '{"_isAdmin":true}'],
    "Credential Stuffing": ["leaked_db_combo_1042", "breach_list_entry_7734"],
    "Rate Limit Bypass": ["X-Forwarded-For: 1.2.3.4", "X-Real-IP spoofed header"],
    "Server-Side Request Forgery": ["url=http://169.254.169.254/metadata", "fetch=file:///etc/passwd"],
}

BREACH_PROBABILITY_MAP = {
    ("SQL Injection", "Critical"): 88,
    ("SQL Injection", "High"): 72,
    ("Brute Force", "Critical"): 65,
    ("Credential Stuffing", "Critical"): 80,
    ("Token Hijacking", "Critical"): 91,
    ("Privilege Escalation", "Critical"): 85,
    ("BOLA / IDOR", "High"): 70,
    ("API Abuse", "Medium"): 40,
}


def generate_attack():
    attack_type = random.choice(ATTACK_TYPES)
    severity = random.choice(SEVERITY_LEVELS)
    api_target = random.choice(TARGETED_APIS)

    payload_list = PAYLOADS.get(attack_type, ["<unknown_payload>"])
    payload = random.choice(payload_list)

    breach_prob = BREACH_PROBABILITY_MAP.get(
        (attack_type, severity),
        random.randint(15, 60)
    )

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "api_target": api_target,
        "attack_type": attack_type,
        "source_ip": random.choice(IP_ADDRESSES),
        "severity": severity,
        "payload": payload,
        "breach_probability": breach_prob,
        "status": random.choice(["Detected", "Blocked", "Investigating"]),
    }


def generate_multiple_attacks(number_of_attacks=5):
    return [generate_attack() for _ in range(number_of_attacks)]
