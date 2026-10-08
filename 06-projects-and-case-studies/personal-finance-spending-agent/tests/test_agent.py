import unittest
from agent import FinanceAgent

class FinanceAgentTests(unittest.TestCase):
    def setUp(self):
        self.agent = FinanceAgent()
    def test_summary(self):
        result = self.agent.chat("summary")
        self.assertIn("Recorded spending:", result)
        self.assertIn("Illustrative remainder:", result)
    def test_recurring(self):
        result = self.agent.chat("subscriptions")
        self.assertIn("Netflix", result)
        self.assertIn("Total marked recurring:", result)
    def test_large_purchase_is_threshold_based(self):
        result = self.agent.chat("anything unusual")
        self.assertIn("Amazon", result)
        self.assertIn("not statistical anomaly detection", result)
    def test_scenario_disclaimer(self):
        result = self.agent.chat("can I afford 1500")
        self.assertIn("After a $1,500.00 purchase:", result)
        self.assertIn("not a reliable affordability determination", result)
    def test_missing_amount(self):
        self.assertIn("provide a purchase amount", self.agent.chat("can I afford this"))
    def test_zero_amount(self):
        self.assertIn("positive purchase amount", self.agent.chat("can I afford 0"))
    def test_unknown_intent(self):
        self.assertIn("Try:", self.agent.chat("hello"))
if __name__ == "__main__":
    unittest.main()
