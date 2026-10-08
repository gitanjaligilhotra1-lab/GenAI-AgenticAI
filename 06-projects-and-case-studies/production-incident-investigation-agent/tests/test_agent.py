import unittest
from agent import IncidentInvestigationAgent
from rag import search_runbook
from tools import get_incident,get_logs,get_metrics
class IncidentAgentTests(unittest.TestCase):
    def setUp(self): self.agent=IncidentInvestigationAgent()
    def test_lookup(self): self.assertEqual(get_incident("INC-1001")["service"],"checkout-api")
    def test_metrics(self): self.assertGreater(get_metrics("checkout-api")["error_rate"],10)
    def test_logs(self): self.assertTrue(any("pool exhausted" in x["message"] for x in get_logs("checkout-api")))
    def test_runbook(self): self.assertEqual(search_runbook("checkout errors deployment")["source"],"checkout.md")
    def test_deployment_correlation(self):
        result=self.agent.chat("Investigate INC-1001"); self.assertIn("8 minutes before",result); self.assertIn("Confidence: HIGH",result); self.assertIn("request on-call approval",result); self.assertIn("does not execute",result)
    def test_dependency_does_not_blame_old_deploy(self):
        result=self.agent.chat("Investigate INC-1002"); self.assertIn("Dependency timeout",result); self.assertIn("Confidence: MEDIUM",result); self.assertIn("dependency-timeout.md",result)
if __name__=="__main__": unittest.main()
