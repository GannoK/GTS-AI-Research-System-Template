from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import generate_qualification_bundle as BUNDLE
import run_methodology_evals as EVALS


def bundle_inputs():
    # Pure synthetic command results: bundle tests never execute the unit suite.
    cases = EVALS.load_cases()
    validator_ids = ["RI-IDENTITY", "RI-SCHEMAS", "RI-HISTORICAL-NO-TOUCH", "RI-SECRET-EXPOSURE", "DQ-INVARIANTS", "DQ-COMPONENT-REGISTRY"]
    validator = {"results": [{"control_id": cid, "status": "PASS", "evidence": ["test fixture"]} for cid in validator_ids]}
    commands = [{"control_id": cid, "status": "PASS", "command": ["fixture-only"], "returncode": 0,
                 "stdout": "test fixture", "stderr": ""}
                for cid in ["RI-REPOSITORY", "RI-AIRST-VALIDATION", "MV-EVAL-HARNESS", "RI-UNIT-TESTS"]]
    commands[1]["stdout"] = json.dumps(validator)
    commands[2]["stdout"] = json.dumps(EVALS.run_evaluations(cases, self_test=True))
    return {
        "commands": commands, "methodology": EVALS.run_evaluations(cases),
        "assurance": EVALS.read_json(ROOT / "ASSURANCE.json"),
        "control_map": EVALS.read_json(ROOT / "evals/methodology/CONTROL_MAP.json"),
        "acceptance": EVALS.read_json(ROOT / "HARDENING/AIRST-HARDENING-001-ACCEPTANCE.json"),
        "metadata": EVALS.read_json(ROOT / "AIRST_METADATA.json"),
        "implementation_commit": "a" * 40,
        "repository_state": {"dirty": False, "manifest_sha256": "b" * 64},
    }


def sample_bundle():
    return BUNDLE.build_bundle(**bundle_inputs())


class QualificationBundleTests(unittest.TestCase):
    def test_all_required_manual_and_acceptance_controls_are_accounted_for(self):
        inputs = bundle_inputs()
        bundle = BUNDLE.build_bundle(**inputs)
        rows = {r["control_id"]: r for r in bundle["controls"]}
        self.assertTrue(set(inputs["assurance"]["required_checks"]) <= rows.keys())
        for manual in inputs["assurance"]["manual_controls"]:
            self.assertEqual(rows[manual["control_id"]]["status"], "MANUAL")
        self.assertEqual({r["control_id"] for r in bundle["acceptance_controls"]}, {f"AC-{n:02d}" for n in range(1, 16)})
        self.assertEqual(rows["MV-EVAL-HARNESS"]["status"], "PASS")
        self.assertEqual(rows["MV-CONTRADICTION"]["status"], "UNKNOWN")
        self.assertEqual(bundle["parent_qualification_state"], "QUALIFICATION_CANDIDATE_EVIDENCE_INCOMPLETE")
        self.assertEqual(bundle["release_readiness_state"], "BLOCKED_MISSING_EVIDENCE")

    def test_unmapped_new_required_control_is_unknown(self):
        inputs = bundle_inputs()
        inputs["assurance"]["required_checks"].append("MV-NEW-REQUIRED-CHECK")
        bundle = BUNDLE.build_bundle(**inputs)
        found = next(r for r in bundle["controls"] if r["control_id"] == "MV-NEW-REQUIRED-CHECK")
        self.assertEqual(found["status"], "UNKNOWN")
        self.assertFalse(found["evidence"])

    def test_self_test_payload_cannot_be_used_as_real_system_evidence(self):
        inputs = bundle_inputs()
        inputs["methodology"] = EVALS.run_evaluations(EVALS.load_cases(), self_test=True)
        with self.assertRaises(ValueError):
            BUNDLE.build_bundle(**inputs)

    def test_actual_failure_propagates_to_mapped_control_and_readiness(self):
        inputs = bundle_inputs()
        inputs["methodology"]["results"][6]["status"] = "FAIL"
        inputs["methodology"]["results"][6]["notes"] = ["contradiction was discarded"]
        bundle = BUNDLE.build_bundle(**inputs)
        rows = {r["control_id"]: r for r in bundle["controls"]}
        self.assertEqual(rows["MV-CONTRADICTION"]["status"], "FAIL")
        self.assertEqual(bundle["parent_qualification_state"], "FAILED")
        self.assertEqual(bundle["release_readiness_state"], "BLOCKED_FAILED_CONTROLS")

    def test_real_deterministic_results_do_not_erase_six_manual_judgments(self):
        inputs = bundle_inputs()
        for item in inputs["methodology"]["results"]:
            item.update(status="PASS", evidence=["synthetic test-only retained evidence"])
        bundle = BUNDLE.build_bundle(**inputs)
        self.assertEqual(bundle["parent_qualification_state"], "QUALIFICATION_CANDIDATE_MANUAL_REVIEW")
        self.assertEqual(sum(r["status"] == "MANUAL" for r in bundle["controls"]), 6)
        self.assertTrue(all(r["status"] == "MANUAL" for r in bundle["acceptance_controls"]))

    def test_current_release_narrative_comes_from_metadata(self):
        inputs = bundle_inputs()
        inputs["metadata"]["release_state"].update(last_declared_version="0.2.1", next_planned_version="0.3.0", development_state="UNRELEASED_POST_V0_2_1_HARDENING", new_release_declared=False)
        bundle = BUNDLE.build_bundle(**inputs)
        self.assertEqual(bundle["release_state"], inputs["metadata"]["release_state"])
        self.assertIn("0.2.1", bundle["compatibility_findings"][0])
        self.assertNotIn("post-v0.2.0", " ".join(bundle["compatibility_findings"]))

    def test_missing_control_unknown_status_and_inconsistent_readiness_are_rejected(self):
        original = sample_bundle()
        broken = copy.deepcopy(original)
        broken["controls"] = [r for r in broken["controls"] if r["control_id"] != "MV-PROVENANCE"]
        with self.assertRaises(ValueError):
            BUNDLE.validate_bundle(broken)
        for bad_status in [None, "FIAL"]:
            broken = copy.deepcopy(original)
            if bad_status is None:
                del broken["controls"][0]["status"]
            else:
                broken["controls"][0]["status"] = bad_status
            with self.assertRaises(ValueError):
                BUNDLE.validate_bundle(broken)
        broken = copy.deepcopy(original)
        broken["parent_qualification_state"] = "QUALIFICATION_CANDIDATE_AUTOMATED_PASS"
        with self.assertRaises(ValueError):
            BUNDLE.validate_bundle(broken)

    def test_missing_acceptance_and_duplicate_control_are_rejected(self):
        original = sample_bundle()
        broken = copy.deepcopy(original)
        broken["acceptance_controls"].pop()
        with self.assertRaises(ValueError):
            BUNDLE.validate_bundle(broken)
        broken = copy.deepcopy(original)
        broken["controls"].append(copy.deepcopy(broken["controls"][0]))
        with self.assertRaises(ValueError):
            BUNDLE.validate_bundle(broken)

    def test_stale_mapped_status_cannot_hide_a_failed_methodology_result(self):
        broken = sample_bundle()
        leaf = next(r for r in broken["methodology_results"]["results"] if r["eval_id"] == "AR-007")
        leaf.update(status="FAIL", notes=["Contradictory evidence was discarded."])
        with self.assertRaisesRegex(ValueError, "mapped methodology results"):
            BUNDLE.validate_bundle(broken)

    def test_stale_command_status_and_returncode_cannot_hide_failures(self):
        broken = sample_bundle()
        command = next(r for r in broken["command_results"] if r["control_id"] == "RI-UNIT-TESTS")
        command.update(status="FAIL", returncode=1)
        with self.assertRaisesRegex(ValueError, "retained command result"):
            BUNDLE.validate_bundle(broken)
        command["status"] = "PASS"
        with self.assertRaises(ValueError):
            BUNDLE.validate_bundle(broken)

    def test_successful_validator_command_cannot_hide_a_failed_child(self):
        broken = sample_bundle()
        command = next(r for r in broken["command_results"] if r["control_id"] == "RI-AIRST-VALIDATION")
        output = json.loads(command["stdout"])
        output["results"][0]["status"] = "FAIL"
        command["stdout"] = json.dumps(output)
        with self.assertRaisesRegex(ValueError, "contains failed result"):
            BUNDLE.validate_bundle(broken)


if __name__ == "__main__":
    unittest.main()
