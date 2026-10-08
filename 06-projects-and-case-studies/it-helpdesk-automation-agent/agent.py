import re
from rag import search_kb
from tools import device_status, create_ticket

class HelpdeskAgent:
    def __init__(self):
        self.pending = None

    def chat(self, message):
        text = message.lower().strip()
        if self.pending and text in {"yes", "confirm", "create ticket"}:
            summary = self.pending
            self.pending = None
            return "Escalation created: " + create_ticket(summary)
        if self.pending and text in {"no", "cancel", "no thanks"}:
            self.pending = None
            return "Okay. No ticket was created."
        if "admin" in text or "access" in text:
            self.pending = None
            return "Privileged access requires identity verification and manager approval; I will not grant it automatically."
        if "vpn" in text:
            match = re.search(r"LAPTOP-[0-9]+", message.upper())
            if not match:
                return "Please provide your managed device ID, for example LAPTOP-42."
            device_id = match.group(0)
            device = device_status(device_id)
            if not device:
                return "Device record unavailable. Please contact IT support."
            article = search_kb("vpn cannot connect certificate")
            if device["certificate_days"] <= 0:
                self.pending = "VPN certificate expired on " + device_id
                return "I found an expired VPN certificate. " + article["step"] + " If that fails, should I create an IT ticket?"
            return article["step"] if article else "Knowledge article unavailable. Please contact IT support."
        if "password" in text:
            article = search_kb("password reset")
            return article["step"] if article else "Please contact the IT service desk."
        return "I can troubleshoot VPN and password issues, or explain the privileged-access path."
