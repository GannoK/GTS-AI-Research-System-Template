from __future__ import annotations

import importlib.util
import copy
import hashlib
import json
import tempfile
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

    def test_missing_or_empty_assertions_never_pass(self):
        original = MODULE.load_cases()[6]
        for checks in [None, []]:
            with self.subTest(checks=checks):
                case = copy.deepcopy(original)
                if checks is None:
                    del case["deterministic_checks"]
                else:
                    case["deterministic_checks"] = checks
                with self.assertRaises(ValueError):
                    MODULE.evaluate(case, {"conflict_recorded": False, "both_evidence_paths_preserved": False})

    def test_malformed_assertions_and_review_flags_are_rejected(self):
        original = MODULE.load_cases()[6]
        variants = []
        for key, value in [("op", "silently_ignore"), ("path", "")]:
            case = copy.deepcopy(original)
            case["deterministic_checks"][0][key] = value
            variants.append(case)
        case = copy.deepcopy(original)
        del case["deterministic_checks"][0]["value"]
        variants.append(case)
        case = copy.deepcopy(original)
        case["semantic_review_required"] = "false"
        variants.append(case)
        for case in variants:
            with self.subTest(case=case), self.assertRaises(ValueError):
                MODULE.evaluate(case, original["self_test_result"])

    def test_numeric_values_cannot_impersonate_boolean_results(self):
        case = MODULE.load_cases()[6]
        self.assertTrue(MODULE.evaluate(case, {"conflict_recorded": 1, "both_evidence_paths_preserved": 1}))

    def test_malformed_fixture_fails_loading(self):
        suite = json.loads(MODULE.CASES.read_text())
        del suite["cases"][6]["deterministic_checks"]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "CASES.json"
            path.write_text(json.dumps(suite))
            with self.assertRaises(ValueError):
                MODULE.load_cases(path)

    def test_missing_results_are_unknown_without_becoming_failures(self):
        payload = MODULE.run_evaluations(MODULE.load_cases())
        self.assertEqual(payload["evaluation_kind"], "RESEARCH_SYSTEM_RESULTS")
        self.assertEqual({item["status"] for item in payload["results"]}, {"UNKNOWN"})

    def test_actual_results_need_retained_matching_evidence(self):
        case = MODULE.load_cases()[3]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            trace = root / "trace.txt"
            trace.write_text("Retraction response trace retained for this test.\n")
            record = {
                "eval_id": case["eval_id"], "system_id": "test-system", "run_id": "test-run",
                "result": case["self_test_result"],
                "evidence": [{"path": "trace.txt", "sha256": hashlib.sha256(trace.read_bytes()).hexdigest()}],
            }
            path = root / "AR-004.json"
            path.write_text(json.dumps(record))
            self.assertEqual(MODULE.run_evaluations([case], results_dir=root)["results"][0]["status"], "PASS")
            trace.write_text("different content")
            failed = MODULE.run_evaluations([case], results_dir=root)["results"][0]
            self.assertEqual(failed["status"], "FAIL")
            self.assertIn("checksum mismatch", failed["notes"][0])
            trace.unlink()
            self.assertEqual(MODULE.run_evaluations([case], results_dir=root)["results"][0]["status"], "FAIL")

    def test_bare_assertions_and_outside_evidence_are_rejected(self):
        case = MODULE.load_cases()[3]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "AR-004.json"
            path.write_text(json.dumps(case["self_test_result"]))
            self.assertEqual(MODULE.run_evaluations([case], results_dir=root)["results"][0]["status"], "FAIL")
            path.write_text(json.dumps({
                "eval_id": "AR-004", "system_id": "test", "run_id": "test",
                "result": case["self_test_result"],
                "evidence": [{"path": "../outside.txt", "sha256": "a" * 64}],
            }))
            failed = MODULE.run_evaluations([case], results_dir=root)["results"][0]
            self.assertEqual(failed["status"], "FAIL")
            self.assertIn("inside the results directory", failed["notes"][0])

    def test_hybrid_results_keep_manual_review_after_assertions_pass(self):
        payload = MODULE.run_evaluations(MODULE.load_cases(), self_test=True)
        self.assertEqual(payload["evaluation_kind"], "HARNESS_SELF_TEST")
        self.assertEqual(payload["results"][0]["status"], "MANUAL")


if __name__ == "__main__":
    unittest.main()
