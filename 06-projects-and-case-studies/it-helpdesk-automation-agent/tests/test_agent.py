import unittest
from agent import HelpdeskAgent
from rag import search_kb

class HelpdeskTests(unittest.TestCase):
    def test_vpn_escalation(self):
        agent = HelpdeskAgent()
        self.assertIn("expired", agent.chat("VPN will not connect on LAPTOP-42"))
        self.assertIn("IT-", agent.chat("yes"))
    def test_cancel(self):
        agent = HelpdeskAgent()
        agent.chat("VPN will not connect on LAPTOP-42")
        self.assertIn("No ticket", agent.chat("no"))
    def test_privileged_access(self):
        self.assertIn("will not grant", HelpdeskAgent().chat("give me admin access"))
    def test_privileged_request_clears_pending_ticket(self):
        agent = HelpdeskAgent()
        agent.chat("VPN will not connect on LAPTOP-42")
        agent.chat("give me admin access")
        self.assertNotIn("IT-", agent.chat("yes"))
    def test_device_id_required(self):
        self.assertIn("provide your managed device ID", HelpdeskAgent().chat("VPN will not connect"))
    def test_unknown_device(self):
        self.assertIn("Device record unavailable", HelpdeskAgent().chat("VPN will not connect on LAPTOP-999"))
    def test_unknown_knowledge(self):
        self.assertIsNone(search_kb("quantum zebra"))
if __name__ == "__main__":
    unittest.main()
