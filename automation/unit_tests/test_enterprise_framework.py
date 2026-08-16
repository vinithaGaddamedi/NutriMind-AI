import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from automation.config.config import FrameworkConfig
from agents.self_healing.healer import SelfHealingHealer
from automation.utils.data_loader import DataLoader
from agents.intelligence.quality_gates import evaluate_quality_gate

class TestEnterpriseFramework(unittest.TestCase):

    def test_framework_config(self):
        self.assertEqual(FrameworkConfig.get_base_url(), "http://localhost:5173")
        self.assertEqual(FrameworkConfig.get_api_url(), "http://localhost:8000")
        self.assertEqual(FrameworkConfig.get_gemini_model(), "gemini-2.5-flash")
        self.assertTrue(FrameworkConfig.get_timeout() > 0)

    def test_self_healing_healer_fallback(self):
        with patch.dict(os.environ, {}, clear=True):
            healer = SelfHealingHealer()
            selector = healer.heal_selector("button#submit_btn", "<div><button>Submit</button></div>")
            self.assertEqual(selector, "button")

    def test_data_loader_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "..", "ui_tests", "data", "test_data.csv")
        if os.path.exists(csv_path):
            rows = DataLoader.load_csv(csv_path)
            self.assertTrue(len(rows) >= 1)
            self.assertIn("username", rows[0])

    def test_quality_gate_evaluation(self):
        result = evaluate_quality_gate(pass_rate_threshold=80.0, report_dir="reports/empty_reports")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
