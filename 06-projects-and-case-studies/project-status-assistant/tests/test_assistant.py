import unittest
from unittest.mock import patch
from assistant import ProjectStatusAssistant

class ProjectStatusTests(unittest.TestCase):
    def setUp(self):
        self.assistant = ProjectStatusAssistant()
    def test_status(self):
        result = self.assistant.answer("status")
        self.assertIn("AT RISK", result)
        self.assertIn("Assessment basis:", result)
        self.assertIn("local project.json", result)
    def test_blocker(self):
        self.assertIn("credentials", self.assistant.answer("blockers"))
    def test_changes(self):
        self.assertIn("70%", self.assistant.answer("what changed"))
    def test_unsupported_question(self):
        self.assertIn("Try:", self.assistant.answer("hello"))
    def test_healthy_snapshot(self):
        sample = {"project": "Sample", "tasks": [{"name": "Done", "status": "done"}], "p95_ms": 900, "target_p95_ms": 1000, "milestone": "Review", "changes": []}
        with patch("assistant.project_data", return_value=sample):
            self.assertIn("ON TRACK", self.assistant.answer("status"))
            self.assertIn("No recent changes", self.assistant.answer("what changed"))
            self.assertIn("No blocked tasks", self.assistant.answer("blockers"))
    def test_missing_metrics_is_unknown(self):
        sample = {"project": "Sample", "tasks": [{"name": "Done", "status": "done"}], "milestone": "Review", "changes": []}
        with patch("assistant.project_data", return_value=sample):
            result = self.assistant.answer("status")
        self.assertIn("UNKNOWN / NEEDS REVIEW", result)
        self.assertIn("required latency evidence missing", result)
    def test_empty_tasks_is_unknown(self):
        sample = {"project": "Sample", "tasks": [], "p95_ms": 100, "target_p95_ms": 200, "milestone": "Review", "changes": []}
        with patch("assistant.project_data", return_value=sample):
            self.assertIn("UNKNOWN / NEEDS REVIEW", self.assistant.answer("status"))
if __name__ == "__main__":
    unittest.main()
