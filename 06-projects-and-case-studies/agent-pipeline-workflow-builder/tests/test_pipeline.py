import unittest
from unittest.mock import patch
from pipeline import Pipeline

class PipelineTests(unittest.TestCase):
    def test_three_options(self):
        result = Pipeline().run("compare postgres mongodb dynamodb")
        self.assertIn("PostgreSQL", result)
        self.assertIn("MongoDB", result)
        self.assertIn("Critic:", result)
    def test_default_plan(self):
        result = Pipeline().run("compare databases")
        self.assertIn("Plan: postgres, mongodb", result)
    def test_partial_research_failure(self):
        def lookup_with_failure(subject):
            if subject == "mongodb":
                raise KeyError("missing sample")
            return {"name": "PostgreSQL", "strength": "transactions", "tradeoff": "operations"}
        with patch("agents.lookup", side_effect=lookup_with_failure):
            result = Pipeline().run("compare postgres mongodb")
        self.assertIn("Evidence gaps:", result)
        self.assertIn("PostgreSQL", result)
        self.assertNotIn("- MongoDB:", result)
    def test_no_evidence(self):
        with patch("agents.lookup", side_effect=KeyError("unavailable")):
            result = Pipeline().run("compare postgres mongodb")
        self.assertIn("Comparison unavailable", result)
        self.assertIn("insufficient evidence", result)
if __name__ == "__main__":
    unittest.main()
