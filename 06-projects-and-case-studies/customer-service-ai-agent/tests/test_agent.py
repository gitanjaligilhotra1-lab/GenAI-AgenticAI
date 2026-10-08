import unittest
from agent import CustomerSupportAgent
from guardrails import can_auto_refund
from rag import search_policy
from tools import get_order

class CustomerSupportTests(unittest.TestCase):
    def test_order_lookup(self): self.assertEqual(get_order("ORD-1001")["item"], "Wireless Headphones")
    def test_policy_retrieval(self): self.assertIn("Damaged", search_policy("damaged replacement")["text"])
    def test_refund_guardrail(self):
        self.assertTrue(can_auto_refund(79.99)); self.assertFalse(can_auto_refund(150)); self.assertFalse(can_auto_refund(0))
    def test_replacement_requires_confirmation(self):
        agent=CustomerSupportAgent(); first=agent.chat("My order ORD-1001 arrived damaged. Replace it.")
        self.assertIn("Would you like", first); self.assertIn("Replacement ID:", agent.chat("yes"))
    def test_replacement_can_be_cancelled(self):
        agent=CustomerSupportAgent(); agent.chat("ORD-1001 is damaged"); self.assertIn("did not create",agent.chat("no"))
    def test_undelivered_order(self): self.assertIn("not been delivered",CustomerSupportAgent().chat("ORD-1003 is damaged"))
    def test_refund_above_price(self): self.assertIn("cannot refund more",CustomerSupportAgent().chat("Refund $500 for ORD-1001"))
    def test_high_value_refund_not_executed(self): self.assertIn("No refund was executed",CustomerSupportAgent().chat("Refund $150 for ORD-1002"))
    def test_refund_requires_confirmation(self):
        agent = CustomerSupportAgent()
        first = agent.chat("Refund $20 for ORD-1001")
        self.assertIn("Please confirm", first)
        self.assertNotIn("Refund ID:", first)
        self.assertIn("Refund ID:", agent.chat("yes"))
    def test_refund_cancellation(self):
        agent = CustomerSupportAgent()
        agent.chat("Refund $20 for ORD-1001")
        self.assertIn("did not create", agent.chat("no"))
        self.assertNotIn("Refund ID:", agent.chat("yes"))
    def test_zero_refund_is_rejected(self):
        self.assertIn("greater than zero", CustomerSupportAgent().chat("Refund $0 for ORD-1001"))
    def test_negative_refund_is_rejected(self):
        self.assertIn("valid positive", CustomerSupportAgent().chat("Refund $-5 for ORD-1001"))
    def test_refund_without_amount_requires_confirmation(self):
        self.assertIn("$79.99", CustomerSupportAgent().chat("Refund ORD-1001"))
    def test_new_request_clears_pending_action(self):
        agent = CustomerSupportAgent()
        agent.chat("Refund $20 for ORD-1001")
        agent.chat("What is your return policy?")
        self.assertNotIn("Refund ID:", agent.chat("yes"))
if __name__=="__main__": unittest.main()
