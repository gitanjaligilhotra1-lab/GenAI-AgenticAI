import unittest
from agent import VoiceRetailAgent
class VoiceRetailTests(unittest.TestCase):
    def test_stateful_confirmation(self):
        a=VoiceRetailAgent(); r=a.handle_turn("ORD-2002 arrived damaged")
        self.assertIn("Would you like",r); self.assertIn("Replacement created",a.handle_turn("yes"))
    def test_decline_clears_action(self):
        a=VoiceRetailAgent(); a.handle_turn("ORD-2002 arrived damaged"); self.assertIn("will not create",a.handle_turn("no"))
    def test_order_status(self): self.assertIn("out for delivery",VoiceRetailAgent().handle_turn("Where is ORD-2001?"))
    def test_undelivered_cannot_replace(self): self.assertIn("not been delivered",VoiceRetailAgent().handle_turn("ORD-2001 is damaged"))
    def test_unknown_order(self): self.assertIn("could not find",VoiceRetailAgent().handle_turn("ORD-9999 is damaged"))
    def test_switching_orders_cancels_pending_action(self):
        agent = VoiceRetailAgent()
        agent.handle_turn("ORD-2002 arrived damaged")
        agent.handle_turn("Where is ORD-2001?")
        self.assertNotIn("Replacement created", agent.handle_turn("yes"))
    def test_unrelated_turn_cancels_pending_action(self):
        agent = VoiceRetailAgent()
        agent.handle_turn("ORD-2002 arrived damaged")
        agent.handle_turn("What is the return policy?")
        self.assertNotIn("Replacement created", agent.handle_turn("yes"))
if __name__=="__main__": unittest.main()
