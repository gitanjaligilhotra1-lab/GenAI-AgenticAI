from datetime import datetime
from tools import get_alert, get_auth_events, get_device
from threat_intel import lookup_ip

class ThreatAgent:
    def investigate(self, alert_id):
        alert = get_alert(alert_id)
        if not alert:
            return "Alert not found."
        start, end = alert.get("window_start"), alert.get("window_end")
        if not start or not end or start > end:
            return "Alert investigation window unavailable; analyst review required."
        events = sorted((e for e in get_auth_events(alert["user"]) if start <= e["time"] <= end), key=lambda e: e["time"])
        score = 0
        evidence = []
        suspicious_ips = {e["ip"] for e in events if lookup_ip(e["ip"])["risk"] == "high"}
        unknown_devices = {e["device"] for e in events if not get_device(e["device"])}
        if suspicious_ips:
            score += 35
            evidence.append("High-risk IP: " + ", ".join(sorted(suspicious_ips)))
        if unknown_devices:
            score += 25
            evidence.append("Unknown device: " + ", ".join(sorted(unknown_devices)))
        if any(e["mfa"] == "failed" for e in events):
            score += 15
            evidence.append("Failed MFA observed before or near suspicious access")
        if alert["privileged_access"]:
            score += 25
            evidence.append("Alert indicates privileged resource access")
        if alert["type"] == "impossible_travel" and len(events) >= 2:
            evidence.append("Impossible-travel alert requires geographic and timing validation; sample events do not include geolocation")
        level = "HIGH" if score >= 60 else "MEDIUM" if score >= 30 else "LOW"
        return "\n".join([
            "Alert: " + alert_id,
            "User: " + alert["user"],
            "Sample investigation window: " + start + "–" + end + " (time-of-day only)",
            "Risk: " + level,
            "Illustrative risk score: " + str(score) + "/100",
            "", "Evidence:",
            *["- " + item for item in evidence],
            "", "Assessment: Suspicious activity warrants analyst review; this score is not a probability of compromise.",
            "Recommended: validate session and device evidence, then consider session revocation and credential reset only after SOC analyst approval.",
            "Safety: Read-only investigation. No response-execution credentials or containment actions are available."
        ])
