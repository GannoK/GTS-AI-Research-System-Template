from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("run_methodology_evals", ROOT / "tools" / "run_methodology_evals.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class MethodologyEvalHarnessTests(unittest.TestCase):
    def test_all_cases_materialized(self):
        cases=MODULE.load_cases()
        self.assertEqual([c["eval_id"] for c in cases], [f"AR-{n:03d}" for n in range(1,15)])

    def test_self_test_deterministic_assertions(self):
        for case in MODULE.load_cases():
            self.assertEqual(MODULE.evaluate(case, case["self_test_result"]), [])

    def test_failure_is_detected(self):
        case=MODULE.load_cases()[3]
        bad=dict(case["self_test_result"])
        bad["source_status"]="ACTIVE"
        self.assertTrue(MODULE.evaluate(case,bad))


if __name__ == "__main__":
    unittest.main()
