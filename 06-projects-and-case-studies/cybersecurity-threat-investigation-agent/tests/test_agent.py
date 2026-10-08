import unittest
from unittest.mock import patch
from agent import ThreatAgent
from tools import get_auth_events

class ThreatInvestigationTests(unittest.TestCase):
    def test_high_risk(self):
        result = ThreatAgent().investigate("ALERT-9001")
        self.assertIn("Risk: HIGH", result)
        self.assertIn("Unknown device", result)
        self.assertIn("SOC analyst approval", result)
        self.assertIn("Illustrative risk score: 100/100", result)
    def test_repeated_events_do_not_inflate_score(self):
        result = ThreatAgent().investigate("ALERT-9001")
        self.assertEqual(result.count("High-risk IP:"), 1)
        self.assertEqual(result.count("Unknown device:"), 1)
    def test_missing_alert(self):
        self.assertEqual(ThreatAgent().investigate("ALERT-9999"), "Alert not found.")
    def test_events_outside_window_do_not_influence_score(self):
        events = [{"user": "alex@example.test", "time": "01:00", "ip": "203.0.113.77", "device": "UNKNOWN-9", "mfa": "failed"}]
        with patch("agent.get_auth_events", return_value=events):
            result = ThreatAgent().investigate("ALERT-9001")
        self.assertNotIn("High-risk IP:", result)
        self.assertNotIn("Unknown device:", result)
    def test_missing_window_requires_review(self):
        with patch("agent.get_alert", return_value={"user": "alex@example.test"}):
            self.assertIn("window unavailable", ThreatAgent().investigate("ALERT-X"))
    def test_event_count(self):
        self.assertEqual(len(get_auth_events("alex@example.test")), 3)
if __name__ == "__main__":
    unittest.main()
