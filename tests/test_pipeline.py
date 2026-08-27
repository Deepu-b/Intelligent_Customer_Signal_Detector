"""
End-to-end integration test for Intelligent Customer Signal Detector pipeline.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import CustomerDataLoader
from src.llm_reasoning import GeminiSignalDetector, build_microbatch_prompt, build_single_analysis_prompt


class TestCustomerSignalDetector(unittest.TestCase):
    def setUp(self):
        self.loader = CustomerDataLoader()
        self.detector = GeminiSignalDetector()

    def test_data_loading(self):
        records = self.loader.get_all_records()
        self.assertEqual(len(records), 75)
        self.assertTrue(all(r.customer_id.startswith("CUST-") for r in records))

    def test_stage1_funnel(self):
        candidates = self.loader.get_candidates_for_llm()
        healthy = self.loader.get_healthy_cohort()
        self.assertEqual(len(candidates) + len(healthy), 75)
        self.assertGreater(len(candidates), 0)

    def test_batch_prompt_generation(self):
        candidates = self.loader.get_candidates_for_llm()
        baseline = {"avg_latency_ms": 480.0, "avg_outflow_inr": 1500000.0, "avg_volume_change_pct": -45.0}
        prompt = build_microbatch_prompt([c.to_dict() for c in candidates[:15]], baseline)
        self.assertIn("CUST-1001", prompt)
        self.assertIn("GLOBAL COHORT BASELINE", prompt)
        self.assertIn("480.0 ms", prompt)
        self.assertIn("JSON array", prompt)


if __name__ == "__main__":
    unittest.main()
